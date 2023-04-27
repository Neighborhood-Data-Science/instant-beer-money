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
from selenium.webdriver.support.ui import WebDriverWait
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

def start_driver_and_open_offertoro(offerwall_version):
    """
    Downloads and installs the latest version of Google chromedriver and
    opens the Offertoro offerwall within a WebDriver

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

    #Set OfferToro URL
    offertoro = os.environ[offerwall_version]
    #Open webpage
    driver.get(offertoro)
    return driver

def parse_offer_information(driver):
    """
    This function parses through the OfferToro available offerwall text and extracts:
    1. Offer Title and Description
    2. Offer Amount
    3. Device type

    Parameters
    ----------
        driver: `WebDriver`
            WebDriver with URL of the offerwall

    Returns
    -------
        toro_dict: `dict`
            A Python dictionary containing the offer information

    """
    #Create dictionary to hold offer information
    toro_dict = {'offer_title_desc':[],\
                  'offer_amount':[],'offer_device':[]}

    try:
        #Wait for offers to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "offert")))
        #Explicit Wait
        time.sleep(1)
    except Exception as err:
        print(f"'Waiting for offers Error: {err}'")
        sys.exit(0)

    try:
        #Focus on offerwall information
        offer_info = driver.find_elements(By.CLASS_NAME,"offert")

        ############# LOGIC BLOCK ##############
        for offers in offer_info:
            try:
                #Set variables equal to text values of the offers
                offer_payout = offers.get_attribute('data-offer_payout')
                offer_device = offers.get_attribute('data-offer_device')
                #Split the offer text to gain information about the offer itself
                offer_text = offers.get_attribute('innerText').split('\t')[1]

                #Insert into dictionary
                toro_dict['offer_title_desc'].append(offer_text)
                toro_dict['offer_amount'].append(offer_payout)
                toro_dict['offer_device'].append(offer_device)
    
            except IndexError:
                ## Check if length of requested offer_text is 1. If so, skip that entry, otherwise fail
                assert len(offers.get_attribute('innerText').split('\t')) == 1
                pass
                
    except Exception as err:
        print(f"'Parsing offer information Error: {err}'")
        sys.exit(0)
    ############# LOGIC BLOCK ##############

    return toro_dict

def create_offer_dataframe(toro_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.

    Parameters
    ----------
        toro_dict: `dict`
            A Python dictionary containing the offer information.

    Returns
    -------
        offer_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the offer information.
    """
    offer_dataframe = pd.DataFrame.from_dict(toro_dict)
    return offer_dataframe

