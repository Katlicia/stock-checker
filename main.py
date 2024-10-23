from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from account import *

def login_and_check_wishlist():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.rossmann.com.tr/customer/account/login/")

    driver.refresh()

    # Giriş formunun görünmesini bekliyoruz (max 10 saniye)
    wait = WebDriverWait(driver, 10)

    # Giriş formunu dolduruyoruz
    username = wait.until(EC.presence_of_element_located((By.NAME, "login[username]")))
    password = wait.until(EC.presence_of_element_located((By.NAME, "login[password]")))
    
    username.send_keys(mail)
    password.send_keys(acc_password)

    # Giriş yap butonuna tıklıyoruz
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "action.login.primary")))
    login_button.click()

    time.sleep(5)

    # Giriş yaptıktan sonra istek listesi sayfasına gidiyoruz
    WISHLIST_URL = 'https://www.rossmann.com.tr/wishlist?limit=1000'
    driver.get(WISHLIST_URL)
    
    # Sayfanın yüklenmesi için birkaç saniye bekliyoruz
    time.sleep(5)
    
    # page_source = driver.page_source
    # soup = BeautifulSoup(page_source, 'html.parser')

    # product_items = soup.find_all("li", {"class": "product-item"})

    # Tüm ürünleri çekiyoruz
    product_items = driver.find_elements(By.CLASS_NAME, "product-item")
    
    for product in product_items:
        try:
            # Her ürün için "Sepete Ekle" butonunu bulmaya çalışıyoruz
            add_to_cart_button = product.find_element(By.CSS_SELECTOR, ".action.tocart.primary")
            if add_to_cart_button.is_enabled():
                product_name = product.find_element(By.CLASS_NAME, "product-item-name").text
                print(f"{product_name}: Stokta mevcut")
            else:
                product_name = product.find_element(By.CLASS_NAME, "product-item-name").text
                print(f"{product_name}: Stokta yok")
        except:
            product_name = product.find_element(By.CLASS_NAME, "product-item-name").text
            print(f"{product_name}: Sepete eklenemiyor, stok durumu bilinmiyor")
    
    # Tarayıcıyı en son kapatıyoruz
    driver.quit()

login_and_check_wishlist()
