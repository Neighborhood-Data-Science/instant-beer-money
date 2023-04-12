"""
This module will contain code necessary to connect to and
scrape data from freecash.com
"""
import os
import time
import pandas as pd
import utils
import sys

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Set options to run Chrome in 'Headless' mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

def start_driver_and_open_ayet(offerwall_version):
    """
    Downloads and installs the latest version of Google chromedriver and
    opens the Ayet offerwall within a WebDriver

    Parameters
    ----------
        offerwall_version: `str`
            The version of the offerwall to open. Set up in the .env file.

    Returns
    -------
        driver: `WebDriver`
            WebDriver object that can be used to interact with the given `offerwall_version`.
    """
    #This installs the latest version of the official Google chromedriver
    #Accesses cached version if present.

    #Initialize variable
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
                options=chrome_options)
    except Exception as err:
        print(f"'Setting Driver Error: {err}'")
        sys.exit(0)

    #Set Ayet URL
    ayet = os.environ[offerwall_version]
    #Open webpage
    driver.get(ayet)
    return driver

def parse_offer_information(driver):
    """
    This function parses through the ayet offerwall text and extracts:
    1. Offer Titles
    2. Offer Descriptions
    3. Offer Amount
    4. Offer Device

    Parameters
    ----------
        driver: `WebDriver`
            WebDriver with URL of the offerwall

    Returns
    -------
        ayet_dict: `dict`
            A Python dictionary containing the offer information
    """
    # Create dictionary to hold offer information
    ayet_dict = {'offerLow':[],'offerHigh':[],
                 'Name':[],'Description':[],
                 'Additional':[],'Difficulty':[],
                 'Ignore3':[]}
    # Wait for Hamburger button to appear
    try:
        # Wait for hamburger button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hamburger-button")))
        # Explicit Wait
        time.sleep(1)
    except Exception as err:
        print(f"'Waiting for hamburger button Error: {err}'")
        sys.exit(0)

    # Grab offer information
    offer_info = driver.find_elements(By.XPATH,"//div[@class = 'row offer-row-basic offer-row-basic-cl ']")

    ############# LOGIC BLOCK ##############
    for o in offer_info:
        # Grab raw text. On Ayet offerwall, there are no seperate classes for the elements on the page.
        # Therefore, we have to extract all text within an offerwall object.
        offer_text = o.get_attribute('innerText')
        list_offer_text = offer_text.split('\n')
        #For each element of the offer text:
            # Append the element to the ayet_dictionary IN ORDER OF KEYS (set by ayet_dict)
            # An index error indicates that an element is not present for a particular key
            # in the dictionary. If we receive this error, impute the value for that key as `None`

        # Set iterator to 0
        i = 0
        for key in ayet_dict:
            try:
                ayet_dict[key].append(list_offer_text[i])
                i += 1
                continue
            except IndexError:
                ayet_dict[key].append(None)
                i += 1
                continue
    ############# LOGIC BLOCK ##############
    return ayet_dict

def create_offer_dataframe(ayet_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.
    """
    offer_dataframe = pd.DataFrame.from_dict(ayet_dict)
    return offer_dataframe

