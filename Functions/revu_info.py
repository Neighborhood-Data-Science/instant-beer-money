"""
This module will contain code necessary to connect to and
scrape data from the Revenue Universe offerwall through
the GPT site: freecash.com
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

def start_driver_and_open_revu(offerwall_version):
    """
    Downloads the latest version of Google chromedriver and
    Opens the OfferToro offerwall within a webdriver

    str: offerwall

    offerwall examples:
    - 'BASELINE_REVU'
    - 'USER_REVU'
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
    revu = os.environ[offerwall_version]
    #Open webpage
    driver.get(revu)
    return driver

def parse_available_offer_information(driver):
    """
    This function parses through the Revenue Universe available offerwall (DESKTOP ONLY) text and extracts:
    1. Offer Titles
    2. Offer Description
    3. Offer Amount
    4. Device type

    Sets device type and
    determines if offer has multiple rewards (multi-tiered)
    """
    #Create dictionary to hold offer information
    available_offer_dict = {'total_coins_earnable':[],'offer_title':[],\
                  'offer_description':[],'offer_device':[]}

    try:
        #Wait for 'Most popular' Icon to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='select2-selection select2-selection--single']")))
        #Explicit Wait
        time.sleep(1)
    except Exception as err:
        print(f"'Error: {err}'")
        sys.exit(0)

    #Focus on offerwall information
    #Wait for menu to be visible button to appear
    available_offer_info = driver.find_elements(by=By.CLASS_NAME,value='main__card')
    ############# LOGIC BLOCK ##############
    for offers in available_offer_info:
        #Split the offer text to gain information about the offer itself
        split_available_offer_info = offers.get_attribute('innerText').split('\n')

        #Insert available offer text into dictionary based on size
        #Sizes were pre-determined from trial and error.

        if len(split_available_offer_info) == 4:
            available_offer_dict['total_coins_earnable'].append(split_available_offer_info[3])
            available_offer_dict['offer_device'].append('Desktop')
            available_offer_dict['offer_title'].append(split_available_offer_info[0])
            available_offer_dict['offer_description'].append(split_available_offer_info[0])

        elif len(split_available_offer_info) == 3:
            ##Ignore these
            continue

        else:
            print(len(split_available_offer_info))
            print(split_available_offer_info)
            raise Exception ('Unexpected offer split size')
    ############# LOGIC BLOCK ##############
    return available_offer_dict


def create_available_offer_dataframe(available_offer_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.
    """
    available_offer_dataframe = pd.DataFrame.from_dict(available_offer_dict)
    return available_offer_dataframe

def parse_completed_offer_info(driver):
    """
    This function parses through the OfferToro offerwall text and extracts:
    1. Completed Offer Titles
    2. Completed Offer Date
    3. Completed Offer Amount
    4. Offer Status (Complete, Review, Clicked)
    ### Need Device ###
    """
    #Create dictionary to hold offer information
    completed_offer_dict = {'offer_title':[],'coins_earned':[],'date_completed':[],'status':[]}

    #Navigate to reward status page
    try:
        #Wait for Cash Icon button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//i[@class='far fa-money-bill-alt']")))
        #Explicit Wait
        time.sleep(1)
        #Click button
        driver.find_element(by=By.XPATH,value="//i[@class='far fa-money-bill-alt']").click()
        #Explicit wait
        time.sleep(1)
    except Exception as err:
        print(f"'Error: {err}'")

    #Attempt to scrape completed offer information from webpage
    try:
        #Wait for Cash Icon button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//i[@class='far fa-money-bill-alt']")))
        #Explicit Wait
        time.sleep(1)
        #Extract raw completed offer info
        completed_offer_info = driver.find_element(by=By.ID,value="earnings_table").get_attribute('innerText')

        ############# LOGIC BLOCK ##############
        #Split the text
        split_completed_offer_info = completed_offer_info.split('\n')
        for lines in split_completed_offer_info:
            line_split = lines.split('\t')
            #Chunk the text for insert into dictionary
            chunked_completed_list = utils.chunked_iterable(line_split, 4)
        #Insert values to dictionary
            for chunks in chunked_completed_list:
                completed_offer_dict['date_completed'].append(chunks[0])
                completed_offer_dict['offer_title'].append(chunks[1])
                completed_offer_dict['coins_earned'].append(chunks[2])
                completed_offer_dict['status'].append(chunks[3])
            ############# LOGIC BLOCK ##############

        return completed_offer_dict
    except Exception as err:
        print(f"'Unhandled Error: %{err}'")

def create_completed_offer_dataframe(completed_offer_dict):
    """
    This function returns the completed offer dict as a pandas DataFrame.
    """
    completed_offer_dataframe = pd.DataFrame.from_dict(completed_offer_dict).drop(index=0)
    return completed_offer_dataframe

# def parse_pending_offer_info(driver):
#     """
#     Offertoro does not have a "pending" section. However, it may be possible to discern
#     this information given the 'Status' of the offer.
#     """

# def create_pending_offer_dataframe(pending_offer_dict):
#     """
#     Offertoro does not have a "pending" section. However, it may be possible to discern
#     this information given the 'Status' of the offer.
#     """
