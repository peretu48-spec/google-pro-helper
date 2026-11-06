/* popup.js */
const LABELS = { off: "Disabled", "12m": "12 Months", "6m_ss": "6 Months (SS)", "6m": "6 Months", "6m_2": "6 Months (Alt)" };
const stateEl = document.getElementById("state");

function paintState(st) {
  const layer = (st && st.layer) || "off";
  const mounted = !!(st && st.mounted) && layer !== "off";
  stateEl.className = mounted ? "ok" : "warn";
  stateEl.textContent = mounted
    ? "Mounted: " + (LABELS[layer] || layer) + " — Ready to click Get discount"
    : "Injection not detected on current page (make sure you are on one.google.com/plans and refresh)";
}

function queryTab() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const t = tabs && tabs[0];
    if (!t) return paintState(null);
    chrome.tabs.sendMessage(t.id, { type: "getState" }, (resp) => {
      if (chrome.runtime.lastError || !resp) return paintState(null);
      paintState(resp);
    });
  });
}

chrome.storage.local.get(["gapt_layer"], (r) => {
  const layer = (r && r.gapt_layer) || "off";
  document.querySelectorAll('input[name="layer"]').forEach((el) => {
    el.checked = el.value === layer;
    el.addEventListener("change", () => {
      if (!el.checked) return;
      chrome.storage.local.set({ gapt_layer: el.value }, () => {
        // Hot reload to current tab
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const t = tabs && tabs[0];
          if (!t) return queryTab();
          chrome.tabs.sendMessage(t.id, { type: "setLayer", layer: el.value }, () => {
            void chrome.runtime.lastError;
            setTimeout(queryTab, 350);
          });
        });
      });
    });
  });
  queryTab();
  setTimeout(queryTab, 800);
});

setInterval(queryTab, 1500);
