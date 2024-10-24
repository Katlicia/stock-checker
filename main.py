from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from account import * 

def check_stock_and_add_to_cart(driver, products):
    for product_name, stock_state in products.items():
        try:
            # Find products
            product_elements = driver.find_elements(By.CLASS_NAME, "product-item")
            for product in product_elements:
                name = product.find_element(By.CLASS_NAME, "product-item-name").text
                if name == product_name:
                    add_to_cart_button = product.find_element(By.CSS_SELECTOR, ".action.tocart.primary")
                    # Check stock status
                    if add_to_cart_button.is_enabled() and stock_state == 0:  # If it came in stock
                        add_to_cart_button.click()
                        print(f"{product_name} added to cart.")
                        products[product_name] = 1  # Set stock to True
                    elif not add_to_cart_button.is_enabled():
                        print(f"{product_name}: Out of stock.")
                        products[product_name] = 0  # Set stock to False
                    break
        except Exception as e:
            print(f"{product_name}: Error - {e}")

def login_and_check_wishlist():
    browser_options = Options()
    browser_options.add_argument("--headless")
    driver = webdriver.Chrome(options = browser_options,service=Service(ChromeDriverManager().install()))
    driver.get("https://www.rossmann.com.tr/customer/account/login/")
    
    # Refresh the site so it doesn't error.
    driver.refresh()

    # Login (Max timeout after 10 sec)
    wait = WebDriverWait(driver, 10)

    # Login
    username = wait.until(EC.presence_of_element_located((By.NAME, "login[username]")))
    password = wait.until(EC.presence_of_element_located((By.NAME, "login[password]")))
    
    username.send_keys(mail)
    password.send_keys(acc_password)

    # Click to login
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "action.login.primary")))
    login_button.click()

    time.sleep(5)

    # Go to wishlist
    WISHLIST_URL = 'https://www.rossmann.com.tr/wishlist?limit=1000'
    driver.get(WISHLIST_URL)
    
    # Wait 5 sec for it to load the page
    time.sleep(5)
    
    # Pull all items
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")
    
    products = {}
    for product in product_items:
        try:
            product_name = product.find_element(By.CLASS_NAME, "product-item-name").text
            add_to_cart_button = product.find_element(By.CSS_SELECTOR, ".action.tocart.primary")
            if add_to_cart_button.is_enabled():
                print(f"{product_name}: In stock")
                products[product_name] = 1
            else:
                print(f"{product_name}: Out of stock.")
                products[product_name] = 0
        except Exception as e:
            print(f"{product_name}: Error - {e}")
    # Stock control loop
    try:
        while True:
            print("Checking stock status...")
            check_stock_and_add_to_cart(driver, products)
            print(products)
            time.sleep(10)  # Wait 10 sec
    except KeyboardInterrupt:
        print("Stopped control loop.")

    # Close browser.
    driver.quit()

login_and_check_wishlist()
