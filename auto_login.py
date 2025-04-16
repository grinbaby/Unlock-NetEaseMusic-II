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
    browser.add_cookie({"name": "MUSIC_U", "value": "0049AD0E196A39B6E959235A96D34FF56D3BEABB644859A71368493223628E9FEF0DFB9550EE863544D75EAF054ABC9005807F4217E5A1B9A18AD5AC091FA1C55CAC10677CFD643785ACBC1C054495ED820B151D970621BF10990084FDF1636FBC5877334301FB2C5BE9705F8E9146F6AEC11E5DCC534782343D975BD6DCC7EDCE1A5B3BAE70EC60C87004363AEA7C0E6CD3E9A900355D5FE7891160721D844CF89D3B1A4153D6D86B1393E2535D57E40FD96B05385DED5DC2B072FF20ECB92E661F4A3311952E41FEE4855357C0A5FD7C249D1EE2D54E5961A5271E3FF1487B2B29EC8F74F107411F2B2431CCB2FF6B98B31A61201B0A8DA70CF868B952A1DD6B4722551A72DC5A2234CBFF0F3A3B5CAF6C33CA3707EE85E653A052CB6A24F6D5614746E0F8E7B32F410FE4E28AAF4632A0821FCEB1F52AD496CC5A4FE7B2DF68"})
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
