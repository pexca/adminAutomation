# adminAutomation
scripts to automate some day-to-day tasks
# rerouteSite Bot

## 🚀 The Problem & The Solution
*   **The Problem:** we need to reroute multiple merchant sites manually.
*   **The Solution:** The bot uses Selenium to emulate user behaviour (`ActionChains`), including the navigation back to the initial site search page(the list of merchant sites section).

## 🛠️ Tech Stack & Constraints
*   **Language:** Python 3.13+
*   **Automation Engine:** Selenium WebDriver
*   **Design Pattern:** Modular Functional Architecture (Page Object variant)
*   **Hardware Constraint Optimization:** Tailored specifically to run flawlessly on low-spec hardware (4GB RAM) by leveraging native session hooks instead of spawning heavy detached browser processes.

## 📋 Features
- **Dynamic File Reading:** Processes bulk inputs sequentially from a structured flat data file (`data.txt`).
- **SPA State-Synchronization:** Utilizes low-level hardware input emulation to trigger framework internal listeners (`onChange`/`onSelect`) where native Selenium inputs failed.
- **Fail-Fast Error Handling:** Halts execution instantly upon encountering anomalous UI states to prevent cascading database write errors.
- **Zero-Process Overhead:** Reuses the current browser profile workspace to minimize memory utilization.

## 🔧 Setup & Execution

1. Launch Chrome via terminal in debugging mode:
   ```bash
   chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_dev_profile"
   ```
2. Activate your isolated virtual environment and run:
   ```bash
   .venv\Scripts\activate
   pip install selenium
   python rerouteSite.py
   ```
   # broadcast_alert Bot
   
## 🚀 The Problem & The Solution
*   **The Problem:** we need to notify multiple groups of tg users about maintenance/recovery of our services.
*   **The Solution:** The bot uses python "requests" library and the list of chat ids to post notifications.
  
## 🔧 Setup & Execution

CLI:
   .venv\Scripts\activate
   pip install requests
   python broadcast_alert.py
   
