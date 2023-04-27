"""
This module will contain code necessary to connect to and
scrape data from the Revenue Universe offerwall through
the GPT site: freecash.com
"""
import os
import time
import pandas as pd
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

def start_driver_and_open_revu(offerwall_version):
    """
    Downloads and installs the latest version of Google chromedriver and
    opens the Revenue Universe offerwall within a WebDriver

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

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
                options=chrome_options)
    except Exception as err:
        print(f"'Setting Driver Error: {err}'")
        sys.exit(0)

    #Set Revenue Universe URL
    revu = os.environ[offerwall_version]
    #Open webpage
    driver.get(revu)
    return driver

def parse_offer_information(driver):
    """
    This function parses through the Revenue Universe available offerwall text and extracts:
    1. Offer Titles
    2. Offer Amount

    Parameters
    ----------
        driver: `WebDriver`
            WebDriver with URL of the offerwall

    Returns
    -------
        revu_dict: `dict`
            A Python dictionary containing the offer information
    """
    #Create dictionary to hold offer information
    revu_dict = {'offer_title':[],'offer_amount':[]}

    try:
        #Wait for 'Most popular' Icon to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='select2-selection select2-selection--single']")))
        #Explicit Wait
        time.sleep(1)
    except Exception as err:
        print(f"'Setting Driver Error: {err}'")
        sys.exit(0)

    #Focus on offerwall information
    offer_name = driver.find_elements(by=By.CLASS_NAME,value='main__card-left')
    offer_amount = driver.find_elements(by=By.CLASS_NAME,value='main__card-right')

    ############# LOGIC BLOCK ##############
    for (offers,amount) in zip(offer_name,offer_amount):
        try:
            #Grab the name/description of the offer
            name = offers.get_attribute('innerText')
            #Grab the amount of the offer (typicall highest value is second).
            amount = amount.get_attribute('innerText').split('\n')[1]
            #Add information to dictionary
            revu_dict['offer_title'].append(name)
            revu_dict['offer_amount'].append(amount)
        except IndexError:
            #Skip the offer if there is no amount
            print(f'Skipped: {name} No amount found.') # type: ignore # Pylance(reportUnboundVariable)
            continue
    ############# LOGIC BLOCK ##############
    return revu_dict

def create_offer_dataframe(revu_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.

    Parameters
    ----------
        revu_dict: `dict`
            A Python dictionary containing the offer information.

    Returns
    -------
        offer_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the offer information.
    """
    offer_dataframe = pd.DataFrame.from_dict(revu_dict)
    return offer_dataframe
