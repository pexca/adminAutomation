# adminPanelAutomation
scripts to automate some day-to-day tasks
# Fintech Routing Workflow Automation Bot

A memory-efficient, production-grade Python script designed to automate high-volume merchant routing updates within a modern Single-Page Application (SPA) admin panel.

## 🚀 The Problem & The Solution
*   **The Problem:** An operations team had to manually update routing channels for over 100+ sites daily. This required navigating complex tables, handling dynamic drop-downs, and executing repetitive data entry, costing hours of manual labor.
*   **The Solution:** This bot automates the entire end-to-end user flow. It safely bridges into an active authenticated Chrome session via a remote debugging port, uses native hardware event simulation (`ActionChains`) to bypass heavy SPA state guards (React/Tailwind), and applies lightweight double-click browser history navigation to preserve system RAM.

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
