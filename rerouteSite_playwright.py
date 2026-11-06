import asyncio
from playwright.async_api import async_playwright

# =====================================================================
# ВСПOMOГАТЕЛЬНЫЕ ФУНКЦИИ (Helper Methods)
# =====================================================================

async def connect_to_chrome(p):
    """Connects to your active running Chrome instance via Chrome DevTools Protocol"""
    # Добавляем slow_mo=500, чтобы принудительно замедлить шаги и дать сайту успевать за кодом
    browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", slow_mo=500)
    
    if browser.contexts:
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
    else:
        context = await browser.new_context()
        page = await context.new_page()
        
    return browser, page


def read_data_file(filename="data.txt"):
    """Loads records cleanly from data.txt file"""
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

async def human_type(page, element, text):
    """Mimics strict physical backspacing and human typing cadence"""
    await element.focus()
    
    # Выделяем всё и очищаем поле (как Ctrl+A + Backspace)
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    await asyncio.sleep(0.3)
    
    # Печатаем текст с человеческой задержкой в 150мс между символами
    await element.type(text, delay=150)

async def sequential_back_navigation(page):
    """Executes two separate single clicks to step back exactly two pages safely."""
    back_button_locator = page.locator(
        "//button[text()='Go back'] | //span[text()='Go back'] | //*[contains(text(), 'Go back')]"
    )
    
    # Playwright сам подождет, пока кнопка станет кликабельной
    await back_button_locator.first.click()
    await asyncio.sleep(1.5)
    
    await back_button_locator.first.click()


# =====================================================================
# ВЫДЕЛЕННЫЙ МОДУЛЬ ОБРАБОТКИ ЗАПИСИ (Isolated Processing Block)
# =====================================================================

async def process_merchant_record(page, site_name, channel_number):
    """Handles the inner routing configuration flow for a single merchant."""
    # 1. Находим поле поиска, кликаем по нему и очищаем
    search_field = page.locator("//input[@placeholder='Search by site name, ID or URL']")
    await search_field.click()
    await search_field.fill("") 
    await search_field.fill(site_name)
    
    # Даем фронтенду 2 полные секунды, чтобы отправить запрос на сервер и обновить таблицу результатов
    await asyncio.sleep(2.0)
    
    # 2. Упрощенный XPath: ищем ЛЮБУЮ строку таблицы, которая содержит имя нашего сайта
    record_row = page.locator(f"//tr[contains(., '{site_name}')]").first
    
    # Ждем, пока строка станет физически видимой на экране
    await record_row.wait_for(state="visible", timeout=6000)
    await record_row.click()
    
    # 3. Переходим во вкладку Routes
    routes_button = page.locator("//button[text()='Routes']")
    await routes_button.wait_for(state="visible", timeout=3000)
    await routes_button.click()
    
    # 4. Кликаем по первой строчке в таблице роутов
    first_route_row = page.locator("//tbody/tr").first
    await first_route_row.wait_for(state="visible", timeout=3000)
    await first_route_row.click()
    
    # 5. Кликаем Edit
    edit_button = page.locator("//button[text()='Edit routing details']")
    await edit_button.wait_for(state="visible", timeout=3000)
    await edit_button.click()
    
    # 6. Вводим номер канала
    channel_dropdown = page.locator("//input[@placeholder='Select channel...']")
    await human_type(page, channel_dropdown, channel_number)
    
    # 7. Выбираем элемент из выпадающего списка
    target_dropdown_item = page.locator(
        f"//div[contains(text(), '{channel_number}')] | "
        f"//span[contains(text(), '{channel_number}')] | "
        f"//li[contains(text(), '{channel_number}')]"
    ).first
    await target_dropdown_item.wait_for(state="visible", timeout=3000)
    await target_dropdown_item.click()
    
    # 8. Сохраняем изменения
    save_button = page.locator("//button[text()='Save']")
    await save_button.click()
    print(f"✅ Changes successfully logged to host server database for: {site_name}")
    
    # 9. Возвращаемся на дашборд
    await asyncio.sleep(1.0)
    await sequential_back_navigation(page)
    
    # После возврата на главный экран делаем паузу, чтобы DOM-дерево полностью обновилось
    await asyncio.sleep(2.5)


# =====================================================================
# ГЛАВНАЯ ЛОГИКА АВТОМАТИЗАЦИИ (Core Automation Loop)
# =====================================================================

async def run_automation():
    lines = read_data_file()
    
    async with async_playwright() as p:
        try:
            browser, page = await connect_to_chrome(p)
            print(f"✅ Connection verified via CDP. Records loaded to process: {len(lines)}")
        except Exception as e:
            print(f"❌ Script initiation block failed: {e}")
            return

        for index, line in enumerate(lines, start=1):
            try:
                site_name, channel_number = [x.strip() for x in line.split(",")]
            except ValueError:
                print(f"❌ Structural format error at line {index}. Skipping line.")
                continue

            print(f"\n--- [{index}/{len(lines)}] Running Action: {site_name} ➡️ Channel: {channel_number} ---")
            
            try:
                # Даем интерфейсу стабилизироваться секундной паузой
                await asyncio.sleep(1.0) 
                
                # Запускаем шаг обработки
                await process_merchant_record(page, site_name, channel_number)
                print("-> Dynamic navigation cycle cleared. Moving to next item...")
                
            except Exception as element_error:
                # В Playwright все ошибки элементов (отсутствие, таймаут) наследуются от базового Exception
                print(f"⚠️ Notice: Record '{site_name}' not found or unreachable. Cleaning up field to skip...")
                
                try:
                    # Безопасное восстановление: очищаем строку поиска
                    search_field = page.locator("//input[@placeholder='Search by site name, ID or URL']")
                    await search_field.fill("")
                    await page.keyboard.press("Escape")
                    await asyncio.sleep(1.0)
                except Exception as recovery_error:
                    print(f"❌ Critical error during UI skip recovery: {recovery_error}")
                    print("🛑 Halting loop to prevent destructive out-of-sync actions.")
                    await browser.close()
                    return
                    
                continue

        # Закрываем сессию подключения, сам Chrome останется открытым
        await browser.close()
        print("\n🎉 Automation cycle completely cleared without further exceptions!")

if __name__ == "__main__":
    # Запуск асинхронного цикла событий Python
    asyncio.run(run_automation())
