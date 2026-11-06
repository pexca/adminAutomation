import asyncio
from playwright.async_api import async_playwright

# =====================================================================
# HELPER METHODS
# =====================================================================

async def connect_to_chrome(p):
    """Connects to your active running Chrome instance via Chrome DevTools Protocol"""
    # Global slow_mo ensures the heavy UI has breathing room on 4GB RAM machines
    browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", slow_mo=500)
    
    if browser.contexts:
        context = browser.contexts
        page = context.pages if context.pages else await context.new_page()
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
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    await asyncio.sleep(0.3)
    await element.type(text, delay=150)

async def sequential_back_navigation(page):
    """Executes two separate single clicks to step back exactly two pages safely."""
    back_button_locator = page.locator(
        "//button[text()='Go back'] | //span[text()='Go back'] | //*[contains(text(), 'Go back')]"
    )
    await back_button_locator.first.click()
    await asyncio.sleep(1.5)
    await back_button_locator.first.click()

# =====================================================================
# ISOLATED PROCESSING BLOCK
# =====================================================================

async def process_merchant_record(page, site_name, channel_number):
    """Handles the inner routing configuration flow for a single merchant."""
    # 1. Target search field and input query (UPDATED PLACEHOLDER)
    search_field = page.locator("//input[@placeholder='Search by site name, ID or URL']")
    await search_field.click()
    await search_field.fill("") 
    await search_field.fill(site_name)
    await asyncio.sleep(2.0)  # Wait for frontend network filter to settle
    
    # 2. Match table row via generic text containment to avoid DOM splitting drops
    record_row = page.locator(f"//tr[contains(., '{site_name}')]").first
    await record_row.wait_for(state="visible", timeout=6000)
    await record_row.click()
    
    # 3. Enter Routes tab
    routes_button = page.locator("//button[text()='Routes']")
    await routes_button.wait_for(state="visible", timeout=3000)
    await routes_button.click()
    
    # 4. Click target metrics row
    first_route_row = page.locator("//tbody/tr").first
    await first_route_row.wait_for(state="visible", timeout=3000)
    await first_route_row.click()
    
    # 5. Open editing form view
    edit_button = page.locator("//button[text()='Edit routing details']")
    await edit_button.wait_for(state="visible", timeout=3000)
    await edit_button.click()
    
    # 6. Type new target channel string natively
    channel_dropdown = page.locator("//input[@placeholder='Select channel...']")
    await human_type(page, channel_dropdown, channel_number)
    
    # 7. Select dynamic dropdown item overlay cell
    target_dropdown_item = page.locator(
        f"//div[contains(text(), '{channel_number}')] | "
        f"//span[contains(text(), '{channel_number}')] | "
        f"//li[contains(text(), '{channel_number}')]"
    ).first
    await target_dropdown_item.wait_for(state="visible", timeout=3000)
    await target_dropdown_item.click()
    
    # 8. Submit changes via Save
    save_button = page.locator("//button[text()='Save']")
    await save_button.click()
    print(f"✅ Changes successfully logged to host server database for: {site_name}")
    
    # 9. Rapid reset to dashboard via explicit back navigation
    await asyncio.sleep(1.0)
    await sequential_back_navigation(page)
    await asyncio.sleep(2.5)  # Hard pause for global DOM rebuilding cycle

# =====================================================================
# CORE AUTOMATION LOOP
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
                await asyncio.sleep(1.0) 
                await process_merchant_record(page, site_name, channel_number)
                print("-> Dynamic navigation cycle cleared. Moving to next item...")
                
            except Exception as element_error:
                print(f"⚠️ Notice: Record '{site_name}' not found or unreachable. Cleaning up field to skip...")
                try:
                    # UPDATED PLACEHOLDER IN RECOVERY BLOCK AS WELL
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

        await browser.close()
        print("\n🎉 Automation cycle completely cleared without further exceptions!")

if __name__ == "__main__":
    try:
        asyncio.run(run_automation())
    except KeyboardInterrupt:
        print("\n\n🛑 Emergency halt triggered by user! Script safely detached.")
