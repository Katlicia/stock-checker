from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
from account import * 

def rossmann_check_stock_and_add_to_cart(driver, products):
    # Check Stock
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")
    for product in product_items:
        # If add to cart exists the item is in stock.
        try:
            product_brand = product.find_element(By.CLASS_NAME, "product-item-name").text
            product_link = product.find_element(By.CLASS_NAME, "product-item-link").text
            product_name = product_brand + " " + product_link
            try:
                add_to_cart_button = product.find_element(By.CSS_SELECTOR, ".action.tocart.primary")
                if add_to_cart_button.is_enabled():
                    print(f"{product_name}: In stock")
                    products[product_name] = 1
            except:
                unavailable_stock = product.find_element(By.CLASS_NAME, "unavailable.stock")
                if unavailable_stock:
                    print(f"{product_name}: Out of stock")
                    products[product_name] = 0
        except Exception:
            pass

    # Add to card
    for product_name, stock_state in products.items():
        try:
            # Find products
            for product in product_items:
                brand = product.find_element(By.CLASS_NAME, "product-item-name").text
                link = product.find_element(By.CLASS_NAME, "product-item-link").text
                name = brand + " " +link
                if product_name == name:
                    add_to_cart_button = product.find_element(By.CSS_SELECTOR, ".action.tocart.primary")
                    # Check stock status
                    if add_to_cart_button.is_enabled() and stock_state == 0:  # If it came in stock
                        add_to_cart_button.click()
                        print(f"{product_name} added to cart.")
                        products[product_name] = 1
                    break
        except:
            pass
    
    driver.refresh()
    print("Refreshing Website")

def rossmann_login_and_check_wishlist():
    browser_options = Options()
    browser_options.add_argument("--headless")
    driver = webdriver.Chrome(options= browser_options, service=Service(ChromeDriverManager().install()))
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

    print("Logged into ROSSMANN")

    # Go to wishlist
    WISHLIST_URL = 'https://www.rossmann.com.tr/wishlist?limit=1000'
    print("In ROSSMANN wishlist")
    driver.get(WISHLIST_URL)
    
    # Wait 5 sec for it to load the page
    time.sleep(5)
    
    products = {}

    # Stock control loop
    try:
        while True:
            print("Checking stock status...")
            rossmann_check_stock_and_add_to_cart(driver, products)
            print(products)
            time.sleep(10)  # Wait 10 sec
    except KeyboardInterrupt:
        print("Stopped control loop.")

    # Close browser.
    driver.quit()

def gratis_check_stock_and_add_to_cart(driver, products):
    # Check Stock
    product_items = driver.find_elements(By.CLASS_NAME, "col-xs-6.col-md-4.ng-star-inserted")
    for product in product_items:
        try:
            # If add to cart exists the item is in stock.
            product_name = product.find_element(By.CLASS_NAME, "cx-product-name").text
            try:
                add_to_cart_button = product.find_element(By.CLASS_NAME, "add-to-basket.add-to-cart-for-product-grid-item")
                if add_to_cart_button.is_enabled():
                    print(f"{product_name}: In stock")
                    products[product_name] = 1
            except:
                pass
            try:
                unavailable_stock = product.find_element(By.CLASS_NAME, "add-to-basket.productNo.ng-star-inserted")
                if unavailable_stock.is_enabled():
                    print(f"{product_name}: Out of stock")
                    products[product_name] = 0
            except:
                pass
        except:
            pass

    # Add to card
    for product_name, stock_state in products.items():
        try:
            # Find products
            for product in product_items:
                ActionChains(driver).move_to_element(product).perform()
                name = product.find_element(By.CLASS_NAME, "cx-product-name").text
                if product_name == name:
                    add_to_cart_button = product.find_element(By.CLASS_NAME, "add-to-basket.add-to-cart-for-product-grid-item")
                    # Check stock status
                    if add_to_cart_button.is_enabled() and stock_state == 0:  # If it came in stock
                        add_to_cart_button.click()
                        print(f"{product_name} added to cart.")
                        products[product_name] = 1
                    unavailable_stock = product.find_element(By.CLASS_NAME, "add-to-basket.productNo.ng-star-inserted")
                    if unavailable_stock.is_enabled():
                        print(f"{product_name}: Out of stock")
                        products[product_name] = 0
                    break
        except:
            pass
    


def gratis_login_and_check_wishlist():
    browser_options = Options()
    browser_options.add_argument("--headless")
    #driver = webdriver.Chrome(options= browser_options, service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.gratis.com/login")
    
    # Refresh the site so it doesn't error.
    driver.refresh()

    # Login (Max timeout after 10 sec)
    wait = WebDriverWait(driver, 10)

    # Login
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="userId"]')))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="password"]')))
    
    username.send_keys(mail)
    password.send_keys(acc_password)

    time.sleep(3)

    # Click to login
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "round-btns")))
    login_button.click()

    time.sleep(5)

    print("Logged into GRATIS")
    
    try:
        popup_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "popup_close")))
        popup_button.click()
    except:
        pass

    # Go to wishlist
    WISHLIST_URL = 'https://www.gratis.com/my-account/wishlist'
    driver.get(WISHLIST_URL)
    
    # Wait 5 sec for it to load the page
    time.sleep(5)
    
    print("In GRATIS wishlist")

    products = {}

    # Stock control loop
    try:
        while True:
            print("Checking stock status...")
            gratis_check_stock_and_add_to_cart(driver, products)
            print(products)
            driver.refresh()
            print("Refreshing Website")
            time.sleep(10)  # Wait 10 sec
    except KeyboardInterrupt:
        print("Stopped control loop.")

    # Close browser.
    driver.quit()

def run_parallel_checks():
    rossmann_thread = threading.Thread(target=rossmann_login_and_check_wishlist)
    gratis_thread = threading.Thread(target=gratis_login_and_check_wishlist)

    rossmann_thread.start()
    gratis_thread.start()

    rossmann_thread.join()
    gratis_thread.join()

run_parallel_checks()
