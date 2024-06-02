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
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-setuid-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("start-minimized")
    chromeOptions.add_argument("disable-infobars")
    chromeOptions.add_argument("--remote-debugging-port=9222")

    service = Service(executable_path=CHROMEPATH)
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    return driver

def crawl(url, plz):
    driver = set_up_driver(url)

    try:
        button_to_open_popup = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Verfügbarkeit in einem dm-Markt prüfen']"))
        )
        button_to_open_popup.click()

        # Wait for the input field to be visible in the popup
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Suche nach PLZ, Straße oder Ort']"))
        )
        # Enter the zip code
        input_field.send_keys(plz)  # Replace '12345' with the desired zip code

        # Wait for the search button to be clickable and then click it
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Suche absenden']"))
        )
        driver.execute_script("arguments[0].click();", search_button)

        # Get the page source after the results are loaded
        time.sleep(7)
        source = driver.page_source
        driver.quit()
        return source
    except Exception as e:
        print(f"An error occurred: {e}")

def get_shops(url, plz):

    source = crawl(url, plz)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(source, 'html.parser')

    # Find all elements with data-dmid="store-teaser"
    store_teasers = soup.find_all(attrs={"data-dmid": "store-teaser"})

    shop_dict = {}

    # Print the found elements
    for teaser in store_teasers:
        verf = teaser.find('span', {'data-dmid': 'availability-hint-text-container'}).text.strip()
        if "Momentan verfügbar" in verf:
            address = teaser.find('div', {'data-dmid': 'store-teaser-street'}).text.strip()
            stueck =  re.search(r'\((\d+ Stück)\)', verf).group(1)
            shop_dict[address] = stueck

    return shop_dict
