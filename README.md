# Google Pro Helper

This repository contains two independent versions: the Browser Extension version and the Batch Console version, each maintaining their own directory structure and original codebase.

| Version | Directory | Description |
| --- | --- | --- |
| Browser Extension | [extension](./extension/) | Browser extension project including manifest, popup interface, scripts, and icons. |
| Batch Console | [batch](./batch/) | Local console project for batch account task management, including web UI, backend, startup scripts, and tests. |

## Directory Structure

```text
google-pro-helper/
├── extension/   # Browser extension version
├── batch/       # Batch console version
├── .gitignore
└── README.md
```

## Browser Extension Version

Original discussion:

[https://linux.do/t/topic/3123997](https://linux.do/t/topic/3123997)

(Free activation of Google AI Pro 12 / 24 months | offer token injection)

> **Notice: Do not use primary accounts!**

### **1. In Chrome browser, open Developer Mode and click "Load unpacked extension"**

![image](https://i0.hdslb.com/bfs/new_dyn/f6ecc1314583543aedb82bf0d950213e3747579686817540.png@1192w.webp)

### **2. Open one.google.com/plans, follow the steps in the extension, first activate the 12-month tier. Note the green banner at top and bottom-right badge.**

![image](https://i0.hdslb.com/bfs/new_dyn/5de4698ae0cd2a371a1ecb3e6727a8823747579686817540.png@1130w_1760h.webp)

![image](https://i0.hdslb.com/bfs/new_dyn/33147e398928380c614b5ae85bd50a903747579686817540.png@1192w.webp)

![image](https://i0.hdslb.com/bfs/new_dyn/2544ad49e1db82fb90999fe3355e6fbd3747579686817540.png@92h.webp)

### **3. Select the Pro plan, bind payment card (card requires at least $1 for verification, most cards work). Always verify before payment: first month must be $0.00.**

> Note: If a discount has already been applied, checkout might require paying for the first month of YouTube Premium. Be careful; normal orders only charge starting next month.

![image](https://i0.hdslb.com/bfs/new_dyn/b24d7dc8773238dce8883de6ac8fb5a13747579686817540.png@1192w.webp)

![image](https://i0.hdslb.com/bfs/new_dyn/9b5d510ce927dc364d468eb82cc7182e3747579686817540.png@1046w_1590h.webp)

### **4. If the subscription page no longer appears, switch the extension to 6 months, reload the page, and switch to annual billing.**

The subscription page will appear again showing a deferred payment date (e.g. 2028-05-05). It remains free until that date. Repeat the procedure for the next 6-month tier to achieve 2 years of Pro membership.

![image](https://i0.hdslb.com/bfs/new_dyn/59a750f80e575523398a3cee77f0ae343747579686817540.png@1192w.webp)

> Note:
>
> Remember to cancel auto-renewal afterwards to avoid monthly charges for attached YouTube add-ons.

![image](https://i0.hdslb.com/bfs/new_dyn/c65340f450d8c110abd88de7f0faa99c3747579686817540.png@1192w.webp)

**Community Notes:**

> Fy6666:
>
> If you see "YouTube Premium Individual Add On cannot be used. You can subscribe to other products in this bundle separately": YouTube add-on is only supported in US, Canada, Brazil, France, Germany, Japan.

> aikavvak12una:
>
> If account region is not US, you can directly add a US payment method before subscribing. Changing Google Play payment method region works regardless of Google account registration region.


## Batch Console Version

**Google AI Pro (5 TB) Zero Cost 2-Year (US$0.00 -> 24 Months) Automated Console**

> The "Zero Cost 2-Year" refers to the project target and does not constitute a guaranteed subscription outcome. Actual costs and benefits depend on checkout and upstream responses.

### 1. Runtime Environment Requirements
1. Windows 10 / 11 System
2. Google Chrome installed (default path is fine)
3. Python 3.10 or higher installed (check "Add Python to PATH")
4. Network environment: US proxy enabled locally, or configure proxy template in console

### 2. Quick Start Steps
1. First-time use: double-click [1_initial_setup_and_start.bat]
2. Daily use: double-click [2_start_console.bat]
3. Browser opens automatically at: http://127.0.0.1:8765

### 3. Payment Card Setup & Account Execution Guide
#### 1. Fill in Payment Card (Required):
   - In "Global Configuration" on the left, enter your Visa or Mastercard card details:
     * Card Number (16 digits)
     * Expiration Date (MM / YY, e.g., 08 / 29)
     * Security Code (3-digit CVC)
     * Cardholder Name (English)
     * Tax-free ZIP code preset to 97201 (Oregon tax-free state)
   - Click [Save Configuration].
   - Note: The script features strict zero-cost protection, only subscribing when checkout confirms US$0.00.

#### 2. Batch Import Google Accounts:
   - Paste accounts in "Import Accounts" on the right (one per line). Supported formats:
     * email----password----recovery_email
     * email----password----recovery_email----2fa_secret
     * email----password----2fa_secret
   - Click [Import Account List].

#### 3. Start Automated Execution:
   - Click [Start] next to an account or [Run Batch] at top.
   - The script automates:
     - Step 1: Log in to Google and pass Recovery Email / 2FA verification
     - Step 2: Inline tax-free card binding + Layer 1 12-month free package (US$0.00)
     - Step 3: Stack Layer 2 6-month free package (US$0.00 -> 18 months)
     - Step 4: Stack Layer 3 6-month free package (US$0.00 -> 24 months cap)
     - Step 5: Navigate to Google Play to cancel auto-renewal, lock 2-year benefits, and capture verification screenshot

### 4. Isolation & Sensitive Data

- Browser extension resides in `extension/`, batch console resides in `batch/`.
- The batch console uses dedicated browser profiles per account.
- Passwords, 2FA secrets, payment card details, and browser session data are sensitive; local configuration, profiles, screenshots, logs, and cache should not be committed to repositories.


## Usage Entrypoints

- **Browser Extension**: Open Chrome Extension Manager, enable Developer Mode, click "Load unpacked", and select the `extension` directory.
- **Batch Console**: Enter the `batch` directory on Windows, run `1_initial_setup_and_start.bat` for first use, and `2_start_console.bat` subsequently.

Both versions can be used independently. Local configurations (`config*.json`), environment files, cache, and runtime data should not be committed to the repository.
