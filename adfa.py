from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from account import *  # mail ve acc_password tanımlı olmalı

def gratis_check_stock_and_add_to_cart(driver, products):
    product_items = driver.find_elements(By.CLASS_NAME, "col-xs-6.col-md-4.ng-star-inserted")
    for product in product_items:
        try:
            product_name = product.find_element(By.CLASS_NAME, "cx-product-name").text
            print(f"Ürün adı: {product_name}")  # Hata ayıklama için eklendi

            try:
                add_to_cart_button = product.find_element(By.CLASS_NAME, "add-to-basket.add-to-cart-for-product-grid-item")
                if add_to_cart_button.is_enabled():
                    print(f"{product_name}: Stokta var")
                    products[product_name] = 1
            except Exception as e:
                print(f"{product_name}: Sepete ekleme butonu bulunamadı veya tıklanamadı: {e}")

            try:
                unavailable_stock = product.find_element(By.CLASS_NAME, "add-to-basket.productNo.ng-star-inserted")
                if unavailable_stock.is_enabled():
                    print(f"{product_name}: Stokta yok")
                    products[product_name] = 0
            except Exception as e:
                print(f"{product_name}: Stokta olmadığını belirten element bulunamadı: {e}")
                
        except Exception as e:
            print(f"Ürün işlenirken hata oluştu: {e}")

def gratis_login_and_check_wishlist():
    browser_options = Options()
    browser_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browser_options)
    driver.get("https://www.gratis.com/login")
    
    driver.refresh()

    wait = WebDriverWait(driver, 10)
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="userId"]')))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="password"]')))
    username.send_keys(mail)
    password.send_keys(acc_password)

    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "round-btns")))
    login_button.click()

    time.sleep(5)

    WISHLIST_URL = 'https://www.gratis.com/my-account/wishlist'
    driver.get(WISHLIST_URL)
    time.sleep(5)
    
    product_items = driver.find_elements(By.CLASS_NAME, "col-xs-6.col-md-4.ng-star-inserted")
    
    products = {}
    for product in product_items:
        try:
            product_name = product.find_element(By.CLASS_NAME, "cx-product-name").text
            try:
                add_to_cart_button = product.find_element(By.CLASS_NAME, "add-to-basket.add-to-cart-for-product-grid-item")
                if add_to_cart_button.is_enabled():
                    print(f"{product_name}: Stokta var")
                    products[product_name] = 1
            except Exception as e:
                print(f"{product_name}: Sepete ekleme butonu bulunamadı: {e}")
                products[product_name] = 0
        except Exception as e:
            print(f"Ürün adı alınamadı: {e}")

    print("\nStok durumunu simüle ediyoruz...")
    test_product_name = "Test Ürünü"
    products[test_product_name] = 0

    try:
        while True:
            print("Stok durumu kontrol ediliyor...")
            gratis_check_stock_and_add_to_cart(driver, products)
            print(products)
            time.sleep(10)
    except KeyboardInterrupt:
        print("Kontrol döngüsü durduruldu.")

    driver.quit()

gratis_login_and_check_wishlist()
