import ast
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


APP_PATH = Path(os.environ.get("CONFIG_STORAGE_APP", Path(__file__).resolve().parents[1] / "app.py"))


def load_storage_functions():
    # Exercise the real storage functions without importing the browser engine.
    source = ast.parse(APP_PATH.read_text(encoding="utf-8"), filename=str(APP_PATH))
    nodes = []
    for node in source.body:
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            nodes.append(node)
        elif isinstance(node, ast.Import) and all(alias.name in {"json", "os", "tempfile"} for alias in node.names):
            nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in {"load_config", "save_config"}:
            nodes.append(node)
    namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(APP_PATH), "exec"), namespace)
    return namespace


class ConfigStorageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "config.json"
        self.storage = load_storage_functions()
        self.storage["CONFIG_PATH"] = str(self.path)
        self.previous = {"accounts": [{"id": "existing", "email": "test@example.invalid"}], "unknown_field": "preserved"}
        self.path.write_text(json.dumps(self.previous, ensure_ascii=False, indent=2), encoding="utf-8")
        self.previous_bytes = self.path.read_bytes()

    def assert_untouched(self):
        self.assertEqual(self.path.read_bytes(), self.previous_bytes)
        self.assertEqual(list(self.path.parent.glob(".config-*.tmp")), [])

    def test_round_trip_and_json_format_unchanged(self):
        config = {"accounts": [{"id": "new_account", "status": "pending"}], "auto_cancel": False, "card": {}, "unknown_field": [1, "preserved"]}
        self.assertIsNone(self.storage["save_config"](config))
        self.assertEqual(self.storage["load_config"](), config)
        with self.path.open("r", encoding="utf-8") as stream:
            self.assertEqual(stream.read(), json.dumps(config, ensure_ascii=False, indent=2))
        self.assertEqual(list(self.path.parent.glob(".config-*.tmp")), [])

    def test_serialization_failure_preserves_original(self):
        with self.assertRaises(TypeError):
            self.storage["save_config"]({"accounts": [], "invalid": object()})
        self.assert_untouched()

    def test_replace_failure_preserves_original(self):
        with mock.patch.object(os, "replace", side_effect=PermissionError("replacement blocked")):
            with self.assertRaisesRegex(PermissionError, "replacement blocked"):
                self.storage["save_config"]({"accounts": []})
        self.assert_untouched()

    def test_flush_failure_preserves_original(self):
        with mock.patch.object(os, "fsync", side_effect=OSError("disk flush failed")):
            with self.assertRaisesRegex(OSError, "disk flush failed"):
                self.storage["save_config"]({"accounts": []})
        self.assert_untouched()

    def test_temp_creation_failure_preserves_original(self):
        with mock.patch.object(tempfile, "NamedTemporaryFile", side_effect=PermissionError("creation blocked")):
            with self.assertRaisesRegex(PermissionError, "creation blocked"):
                self.storage["save_config"]({"accounts": []})
        self.assert_untouched()

    def test_replacement_receives_a_complete_closed_file_in_same_directory(self):
        config = {"accounts": [{"id": "next"}], "unknown_field": "preserved"}
        replace = os.replace

        def checked_replace(source, destination):
            self.assertEqual(Path(source).parent, self.path.parent)
            self.assertEqual(Path(destination), self.path)
            self.assertEqual(json.loads(Path(source).read_text(encoding="utf-8")), config)
            self.assertEqual(self.path.read_bytes(), self.previous_bytes)
            replace(source, destination)

        with mock.patch.object(os, "replace", side_effect=checked_replace) as replacement:
            self.storage["save_config"](config)
        replacement.assert_called_once()
        self.assertEqual(self.storage["load_config"](), config)

    def test_missing_config_keeps_defaults_and_can_be_created(self):
        self.path.unlink()
        self.assertEqual(self.storage["load_config"](), {
            "target_region": "US", "target_plan": "pro_2year_zero", "auto_cancel": True,
            "card": {}, "accounts": [],
        })
        self.storage["save_config"](self.previous)
        self.assertEqual(self.storage["load_config"](), self.previous)

    def test_invalid_existing_json_still_raises(self):
        self.path.write_text("{invalid", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            self.storage["load_config"]()

    def test_repeated_saves_leave_no_temporary_files(self):
        for number in range(25):
            self.storage["save_config"]({"accounts": [], "revision": number})
            self.assertEqual(self.storage["load_config"]()["revision"], number)
        self.assertEqual(sorted(path.name for path in self.path.parent.iterdir()), ["config.json"])


if __name__ == "__main__":
    unittest.main()
