"""
This module will contain code necessary to connect to and
scrape data from freecash.com
"""
import os
import time
import pandas as pd
import utils

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
chrome_options.add_argument("--window-size=1920x1080")

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

def start_driver_and_open_ayet(offerwall_version):
    """
    Downloads the latest version of Google chromedriver and
    Opens the Ayet offerwall within a webdriver

    str: offerwall

    offerwall examples:
    - 'BASELINE_AYET'
    - 'USER_AYET'
    """
    #This installs the latest version of the official Google chromedriver
    #Accesses cached version if present.
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
                options=chrome_options)
    except Exception as err:
        print('Setting Driver Error: ' + err)

    #Set Ayet URL
    ayet = os.environ[offerwall_version]
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
    offer_dict = {'total_coins_earnable':[],'offer_title':[],\
                  'offer_description':[],'multiple_rewards':[]}
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

def parse_completed_offer_info(driver):
    """
    This function parses through the Ayet offerwall text and extracts:
    1. Completed Offer Titles
    2. Completed Offer Date
    3. Completed Offer Amount
    ### Need Device ###
    """
    #Create dictionary to hold offer information
    completed_offer_dict = {'offer_title':[],'coins_earned':[],'date_completed':[]}

    #Navigate to reward status page
    try:
        #Wait for hamburger button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hamburger-button")))
        #Explicit Wait
        time.sleep(1)
        #Click button
        driver.find_element(by=By.ID,value='hamburger-button').click()

        #Wait for reward status button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sidebar-status")))
        #Explicit wait
        time.sleep(1)
        #Click button
        driver.find_element(by=By.ID,value='sidebar-status').click()
    except Exception as err:
        print('Error: %s' % (err))

    #Attempt to scrape - Fails if offers are not marked as 'Complete' yet
    try:
        #Wait for completed page to render
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-status")))
        #Explicit wait
        time.sleep(1)
        #Extract completed offer info
        completed_offer_info = driver.find_elements(By.XPATH, "//div[@id='user-status']")[0]

        ############# LOGIC BLOCK ##############
        #Get actual text from webpage
        completed_offer_text = completed_offer_info.text
        #Split the text
        split_completed_offer_info = completed_offer_text.split('\n')
        #Chunk the text for insert into dictionary
        chunked_completed_list = utils.chunked_iterable(split_completed_offer_info, 4)
        #Insert values to dictionary
        for chunks in chunked_completed_list:
            completed_offer_dict['offer_title'].append(chunks[1])
            completed_offer_dict['coins_earned'].append(chunks[2])
            completed_offer_dict['date_completed'].append(chunks[3])
        ############# LOGIC BLOCK ##############

        return completed_offer_dict
    except Exception as err:
        print('Unhandled Error: %s' % (err))
