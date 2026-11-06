# adminAutomation
scripts to automate some day-to-day tasks
# CRM Routing Automation Script (Playwright Async Edition)

Высокоэффективный асинхронный скрипт на **Python** для автоматизации массового изменения конфигураций маршрутизации (рероутинга) мерчантов в панели управления. 

Проект полностью переписан с **Selenium** на **Playwright (Async API)** для обеспечения максимальной стабильности, снижения потребления оперативной памяти и обхода проблем с динамическим рендерингом элементов (Stale Elements).

## 🚀 Ключевые особенности и оптимизации

- **CDP Connection (`connect_over_cdp`):** Скрипт подключается к уже запущенной сессии Chrome. Это экономит до 100% дополнительной оперативной памяти, что критически важно для систем с ограниченными ресурсами (тестировалось на ПК с 4 ГБ ОЗУ).
- **Auto-waiting & Global Slow-mo:** Использование встроенных механизмов ожидания видимости элементов в Playwright и аккуратного режима замедления шагов (`slow_mo`) предотвращает "захлебывание" интерфейса при тяжелом рендеринге страниц (React/Vue).
- **Human-like Cadence:** Имитация физического ввода данных пользователем (`Type Delay`) для защиты от срабатывания систем безопасности.
- **Fail-safe Loop Architecture:** Изолированная обработка каждой строки данных. Если одна запись не найдена, скрипт безопасно сбрасывает интерфейс и переходит к следующей без падения всего цикла.
- **Graceful Shutdown:** Безопасная экстренная остановка по `Ctrl + C` без потери сохраненных данных и без системного мусора в консоли.

## 🛠 Установка и запуск

1. Клонируйте репозиторий и активируйте виртуальное окружение.
2. Установите зависимости проекта:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. Запустите ваш браузер Chrome с флагом удаленной отладки:
   ```bash
   chrome.exe --remote-debugging-port=9222
   ```
4. Подготовьте файл `data.txt` в формате: `Имя_Сайта, Номер_Канала`.
5. Запустите автоматизацию:
   ```bash
   python rerouteSite_playwright.py
   ```
   
## 📈 Результаты миграции с Selenium
- Потребление ОЗУ снижено практически в **2 раза**.
- Скорость прохождения UI-шагов увеличилась благодаря встроенной асинхронности.
- Исчезли случайные падения скрипта из-за неполной загрузки элементов DOM-дерева.

# rerouteSite Bot(Selenium)

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
2. In the CLI run:
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

In the CLI run:
   ```bash
   .venv\Scripts\activate
   pip install requests
   python broadcast_alert.py
   ```
   
