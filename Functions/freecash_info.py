"""
This module will contain code necessary to connect to and
scrape data from freecash.com
"""
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

from webdriver_manager.chrome import ChromeDriverManager

#Set options to run Chrome in 'Headless' mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

def start_driver_and_open_ayet():
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

    #Set Ayet URL
    ayet = os.environ['AYET']
    #Open webpage
    driver.get(ayet)
    return driver

def parse_offer_information(driver):
    """
    This function parses through the Ayet offerwall text and extracts:
    1. Offer Titles
    2. Offer Description
    3. Offer Amount
    Also determines if Multiple Reward or not.
    """
    #Create dictionary to hold offer information
    offer_dict = {'total_coins_earnable':[],'offer_title':[],'offer_description':[],'multiple_rewards':[]}
    #Focus on offerwall information
    offer_info = driver.find_elements(By.XPATH, "//div[@class='row offer-row-basic offer-row-basic-cl ']")
    ############# LOGIC BLOCK ##############
    #Cycle through each offer
    for offers in offer_info:
        offer_text = offers.get_attribute('innerText')
        #Split the text
        split_offer_info = offer_text.split('\n')
        #Insert values to dictionary
        if len(split_offer_info) == 7:
            offer_dict['total_coins_earnable'].append(split_offer_info[2])
            offer_dict['offer_title'].append(split_offer_info[3])
            offer_dict['offer_description'].append(split_offer_info[5])
            offer_dict['multiple_rewards'].append(1)
        elif len(split_offer_info) == 6:
            offer_dict['total_coins_earnable'].append(split_offer_info[2])
            offer_dict['offer_title'].append(split_offer_info[3])
            offer_dict['offer_description'].append(split_offer_info[4])
            offer_dict['multiple_rewards'].append(0)
        elif len(split_offer_info) == 5:
            offer_dict['total_coins_earnable'].append(split_offer_info[1])
            offer_dict['offer_title'].append(split_offer_info[2])
            offer_dict['offer_description'].append(split_offer_info[3])
            offer_dict['multiple_rewards'].append(0)
        elif len(split_offer_info) == 1:
            continue
        else:
            raise Exception ('Unexpected offer split size')
    ############# LOGIC BLOCK ##############
    return offer_dict

def create_offer_dataframe(offer_dict):
    """
    This function returns the offer dict as a pandas DataFrame.
    """
    offer_dataframe = pd.DataFrame.from_dict(offer_dict)
    return offer_dataframe
