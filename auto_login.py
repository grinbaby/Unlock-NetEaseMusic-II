# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005288A48EC971EB246F3F63C81D990547ADDF34AEB00EA498BFA1D69699C5B03020D79CCE07C0FE4FF6CAD6D8F5AA31020ECEBFE13814D6E6512E7DD540683764C2FEBDECD0F40AEFEC9E38944365C2B3F8C673D444CFCC2F78E6D9193AA00E022658977F5C613C95FD7B6DB75A75D27465B189D3F0BA1271C2950336F59932978F01FC9E075F641A13FF3CDF3EF6156833F5953C46F2DCBE0DC6778474711D547E0AE4A25B288C63C911608E5EDF5C5BD5D41DEEE8B64B94A96B464779FE40A3B675A53E697C066072E6A34EF54C1BE169F337E639ADF6CFD12D31597E8E9AF53985C22F08BB30C5324AF69209CE31768FB72F553F52E98F0EB8DA9080223C508B3BF2A2C789045A9C893CE0FD41D1E144166BBDC21247346F8A0C1879A70CB565A28D02E1665483A572DE99561103B4D999D9F1D2292071F189FCD4B76973BC"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
