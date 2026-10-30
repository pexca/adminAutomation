import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# =====================================================================
# ВСПOMOГАТЕЛЬНЫЕ ФУНКЦИИ (Helper Methods)
# =====================================================================

def connect_to_chrome():
    """Connects to your active running Chrome instance"""
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    return webdriver.Chrome(options=chrome_options)

def read_data_file(filename="data.txt"):
    """Loads records cleanly from data.txt file"""
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

def human_type(driver, element, text):
    """Mimics strict physical backspacing and human typing cadence"""
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
    time.sleep(0.5)
    
    actions.send_keys(Keys.CONTROL + "a").perform()
    actions.send_keys(Keys.BACKSPACE).perform()
    time.sleep(0.5)
    
    for character in text:
        actions.send_keys(character).perform()
        time.sleep(0.15)

def native_click(driver, element):
    """Executes a true coordinates-based cursor mouse down action"""
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()

def double_click_back(driver):
    """Executes a native double-click sequence on the target back tracker"""
    back_button = driver.find_element(By.XPATH, "//button[text()='Go back'] | //span[text()='Go back'] | //*[contains(text(), 'Go back')]")
    actions = ActionChains(driver)
    actions.move_to_element(back_button).double_click().perform()


# =====================================================================
# ГЛАВНАЯ ЛОГИКА АВТОМАТИЗАЦИИ (Core Automation Loop)
# =====================================================================

def run_automation():
    try:
        driver = connect_to_chrome()
        lines = read_data_file()
        print(f"✅ Connection verified. Records loaded to process: {len(lines)}")
    except Exception as e:
        print(f"❌ Script initiation block failed: {e}")
        return

    for index, line in enumerate(lines, start=1):
        try:
            site_name, channel_number = [x.strip() for x in line.split(",")]
        except ValueError:
            print(f"❌ Structural format error at line {index}. Exiting.")
            return

        print(f"\n--- [{index}/{len(lines)}] Running Action: {site_name} ➡️ Channel: {channel_number} ---")
        
        try:
            # Let the layout visually stabilize before kicking off the selectors loop
            time.sleep(2.0) 
            
            # 1. Clear main panel box and execute query string input
            search_field = driver.find_element(By.XPATH, "//input[@placeholder='Site name, ID or URL']")
            search_field.clear()
            search_field.send_keys(site_name)
            time.sleep(1.5)
            
            # 2. Match record target and click table row
            record_row = driver.find_element(By.XPATH, f"//tr[td[contains(text(), '{site_name}')]]")
            record_row.click()
            time.sleep(2.5)
            
            # 3. Enter Routes tab configuration layer
            routes_button = driver.find_element(By.XPATH, "//button[text()='Routes']")
            routes_button.click()
            time.sleep(1.5)
            
            # 4. Target and click top row in the routes metrics table
            first_route_row = driver.find_element(By.XPATH, "//tbody/tr")
            first_route_row.click()
            time.sleep(1.5)
            
            # 5. Open editing form view panel
            edit_button = driver.find_element(By.XPATH, "//button[text()='Edit routing details']")
            edit_button.click()
            time.sleep(1.5)
            
            # 6. Type the new target channel code input string natively
            channel_dropdown = driver.find_element(By.XPATH, "//input[@placeholder='Select channel...']")
            human_type(driver, channel_dropdown, channel_number)
            time.sleep(2.0)
            
            # 7. Match specific dropdown overlay cell list option and click
            target_dropdown_item = driver.find_element(By.XPATH, f"//div[contains(text(), '{channel_number}')] | //span[contains(text(), '{channel_number}')] | //li[contains(text(), '{channel_number}')]")
            native_click(driver, target_dropdown_item)
            time.sleep(1.5)
            
            # 8. Submit updating changes via native Save validation trigger
            save_button = driver.find_element(By.XPATH, "//button[text()='Save']")
            native_click(driver, save_button)
            print(f"✅ Changes successfully logged to host server database for: {site_name}")
            
            # 9. REFACTOR STEP: Rapid reset to dashboard via double-click navigation
            time.sleep(2.0)
            double_click_back(driver)
            print("-> Dynamic back tracker executed. Awaiting next loop iteration dashboard view...")
            
        except Exception as e:
            print(f"\n❌ HALTING EXECUTION: Critical element loop anomaly on merchant record '{site_name}': {e}")
            print("🛑 Browser left resting on current frame path for error review.")
            return

    print("\n🎉 Automation cycle completely cleared without further exceptions!")

if __name__ == "__main__":
    run_automation()
