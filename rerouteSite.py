import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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

def sequential_back_navigation(driver):
    """Executes two separate single clicks to step back exactly two pages safely."""
    back_button_xpath = "//button[text()='Go back'] | //span[text()='Go back'] | //*[contains(text(), 'Go back')]"
    
    back_button_1 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, back_button_xpath))
    )
    ActionChains(driver).move_to_element(back_button_1).click().perform()
    
    time.sleep(1.5)
    
    back_button_2 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, back_button_xpath))
    )
    ActionChains(driver).move_to_element(back_button_2).click().perform()


# =====================================================================
# ВЫДЕЛЕННЫЙ МОДУЛЬ ОБРАБОТКИ ЗАПИСИ (Isolated Processing Block)
# =====================================================================

def process_merchant_record(driver, site_name, channel_number):
    """Handles the inner routing configuration flow for a single merchant."""
    # 1. Clear main panel box and execute query string input
    search_field = driver.find_element(By.XPATH, "//input[@placeholder='Site name, ID or URL']")
    search_field.clear()
    search_field.send_keys(site_name)
    time.sleep(1.5)
    
    # 2. Match record target and click table row (Where a missing element error usually happens)
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
    
    # 9. Rapid reset to dashboard via explicit sequential navigation
    time.sleep(1.5)
    sequential_back_navigation(driver)


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
            print(f"❌ Structural format error at line {index}. Skipping line.")
            continue

        print(f"\n--- [{index}/{len(lines)}] Running Action: {site_name} ➡️ Channel: {channel_number} ---")
        
        try:
            # Let the layout visually stabilize before kicking off the selector loop
            time.sleep(2.0) 
            
            # Fire the isolated step execution
            process_merchant_record(driver, site_name, channel_number)
            print("-> Dynamic navigation cycle cleared. Moving to next item...")
            
        except (NoSuchElementException, TimeoutException) as element_error:
            # Catch specifically when the search result doesn't show up or an element is missing
            print(f"⚠️ Notice: Record '{site_name}' not found or unreachable. Cleaning up field to skip...")
            
            try:
                # Recover safely: locate search field, clear it so it's clean for the next record
                search_field = driver.find_element(By.XPATH, "//input[@placeholder='Site name, ID or URL']")
                search_field.clear()
                # Optional: Send a backspace or click away if the UI requires a trigger to refresh the table
                search_field.send_keys(Keys.ESCAPE) 
                time.sleep(1.0)
            except Exception as recovery_error:
                print(f"❌ Critical error during UI skip recovery: {recovery_error}")
                print("🛑 Halting loop to prevent destructive out-of-sync actions.")
                return
                
            continue # Cleanly proceed to the next item in 'lines' without crashing
            
        except Exception as critical_error:
            # Catch unexpected system/browser crashes that shouldn't be ignored
            print(f"\n❌ HALTING EXECUTION: Unexpected systemic loop anomaly: {critical_error}")
            print("🛑 Browser left resting on current frame path for error review.")
            return

    print("\n🎉 Automation cycle completely cleared without further exceptions!")

if __name__ == "__main__":
    run_automation()
