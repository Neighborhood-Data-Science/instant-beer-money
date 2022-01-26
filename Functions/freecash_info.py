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

def set_driver_and_scrape_ayet():
    """
    Downloads the latest version of Google chromedriver and
    Opens the Ayet offerwall within a webdriver
    """
    #This installs the latest version of the official Google chromedriver
    #Accesses cached version if present.
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    except Exception as err:
        print('Setting Driver Error: ' + err)

    #Set Ayet URL - This should move to config file
    ayet = "https://www.ayetstudios.com/offers/web_offerwall/2693?external_identifier=fsid-2308045-607783a635"
    #Open webpage
    driver.get(ayet)
    return driver

def get_current_ayet_offers(offerwall_webpage):
    """
    This function scrapes the text from the Ayet offerwall
    """
    raw_text = offerwall_webpage.page_source
    offerwall_text = BeautifulSoup(raw_text,'html.parser')
    return offerwall_text

def parse_offer_titles(offerwall_text):
    """
    This function parses through the Ayet offerwall and extracts offer titles.
    """
    #Set empty list
    offer_titles = []
    #Parse offer section of document
    parsed_offer_titles = offerwall_text.find_all("div",{"class":"offer-desc-wrap flex-desc one-line-wrap one-line-cpe-height"})
    #Parse titles from each offer section
    for titles in parsed_offer_titles:
        offer_titles.append(titles.find(class_='odw-span-title').text)
    return offer_titles

def parse_offer_description(offerwall_text):
    """
    This function parses through the Ayet offerwall and extracts offer descriptions.
    """
    return 1
