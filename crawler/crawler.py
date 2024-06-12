from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from params import CHROMEPATH

import re
import time

def set_up_driver(url):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("--window-size=1920x1080")
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option('useAutomationExtension', False)

    service = Service(executable_path=CHROMEPATH)
    driver = webdriver.Chrome(service=service, options=chromeOptions)
    driver.get(url)

    return driver

def crawl(url, plz):
    driver = set_up_driver(url)

    try:
        parent_div = WebDriverWait(driver, 20000).until(EC.presence_of_element_located((By.ID, "usercentrics-root")))
        shadowRoot = driver.execute_script("return arguments[0].shadowRoot", parent_div)
        print("shadowroot found")

        button = WebDriverWait(shadowRoot, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".uc-deny-all")))
        button.click()
        print("cookies clicked")

        button_to_open_popup = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Verfügbarkeit in einem dm-Markt prüfen']"))
        )
        print("Verfügbarkeit button found")
        button_to_open_popup.click()
        print("Verfügbarkeit button clicked")
        print(driver.page_source)

        input_field = WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Suche nach PLZ, Straße oder Ort']"))
        )
        print("plz search bar found")
        input_field.send_keys(plz)

        search_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Suche absenden']"))
        )
        driver.execute_script("arguments[0].click();", search_button)

        print("plz sent")
        print("search_button:")
        print(search_button)


        time.sleep(7)
        source = driver.page_source
        print("source:")
        print(source)
        driver.quit()
        return source
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

def get_shops(url, plz):
    source = crawl(url, plz)
    if source is None:
        print("Failed to retrieve the page source.")
        return {}

    soup = BeautifulSoup(source, 'html.parser')
    store_teasers = soup.find_all(attrs={"data-dmid": "store-teaser"})

    shop_dict = {}
    for teaser in store_teasers:
        verf = teaser.find('span', {'data-dmid': 'availability-hint-text-container'}).text.strip()
        if "Momentan verfügbar" in verf:
            address = teaser.find('div', {'data-dmid': 'store-teaser-street'}).text.strip()
            stueck = re.search(r'\((\d+ Stück)\)', verf).group(1)
            shop_dict[address] = stueck

    return shop_dict
