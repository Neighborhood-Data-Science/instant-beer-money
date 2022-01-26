"""
This module will contain code necessary to connect to and
scrape data from freecash.com
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

def set_driver():
    """
    Downloads the latest version of Google chromedriver
    """
    #This installs the latest version of the official Google chromedriver
    #Accesses cached version if present.
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        return driver
    except Exception as err:
        print('Setting Driver Error: ' + err)

def open_and_scrape_ayet_offerwall(driver):
    """
    This function will open the Ayet offerwall within a webdriver
    """
    #Set Ayet URL - This should move to config file
    ayet = "https://www.ayetstudios.com/offers/web_offerwall/2693?external_identifier=fsid-2308045-607783a635"
    #Open webpage
    driver.get(ayet)
    return driver
