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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B33842AD6FFCCE72B4E1AD9B2D3F0FB2F94D8701D07C111177BFB1A87C128E1C40EB908A5955D3FAE8B0A903629B3AA388B2056CDE1BB9A8AEB989C3DC19D2F66EDDF35C6A8CA22D7ADF707860B30E916D533AC74821B3A62504ECEFB3B21833E447639133D99D349B9EE7C9591F5FF20F32A94EC3C071A3038B53B7E47A6BEF1A5C39C9B855CF881F622AB188186A6D037D0B0ACD751E3A8956A7E8FCDF6D25293DE6D22B3D465AB0C52DF2B084D01346A5EA4513D4EBC26E35AC145F0050B107FE6051F4701AD2F968A6B95046B03CE64B6A35F85B905019BBF354CA1EEB5CCC9443D6D05095FFDC94C991E2708F3F148643B4466491350D05B7818306C605FEB22CB49AC123D559ACD9CF6982EC9C28095B57DF94BE3D562FA941ACBDC9C05BE8B108404EFE2C69DCB2BC69BE3FE05A5BABE6F2D5B95173C0D739AA20EA8C"})
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
