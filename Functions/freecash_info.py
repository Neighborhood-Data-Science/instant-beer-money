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
        print(f"'Setting Driver Error: {err}'")

    #Set Ayet URL
    ayet = os.environ[offerwall_version]
    #Open webpage
    driver.get(ayet)
    return driver

def parse_available_offer_information(driver):
    """
    This function parses through the Ayet available offerwall text and extracts:
    1. Offer Titles
    2. Offer Description
    3. Offer Amount

    Sets device type and
    determines if offer has multiple rewards (multi-tiered)
    """
    #Create dictionary to hold offer information
    available_offer_dict = {'total_coins_earnable':[],'offer_title':[],\
                  'offer_description':[],'multiple_rewards':[],
                  'offer_device':[]}
    #Create list of devices to search through (offerwalls)
    offerwall_devices = ['desktop','android','ios']
    #Navigate to available offers page
    for offerwalls in offerwall_devices:
        try:
            #Wait for Pending button to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tabs-menu")))
            #Explicit wait
            time.sleep(1)
            #Click button
            driver.find_elements(By.XPATH, f"//li[@href='#tab_{offerwalls}']")[0].click()
            time.sleep(1)
        except Exception as err:
            print(f"'Error: {err}'")

        #Focus on offerwall information
        #Wait for menu to be visible button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//li[@href='#tab_{offerwalls}']")))
        time.sleep(1)
        available_offer_info = driver.find_elements(By.XPATH,"//div[@class = 'tab-pane active']/div")
        ############# LOGIC BLOCK ##############
        for offers in available_offer_info:
            #Set variables equal to text values of the offers
            available_offer_text = offers.get_attribute('innerText')
            #Split the offer text
            split_available_offer_info = available_offer_text.split('\n')
            #Insert available offer text into dictionary based on size
            #Sizes were pre-determined from trial and error.
            if len(split_available_offer_info) == 7:
                available_offer_dict['total_coins_earnable'].append(split_available_offer_info[2])
                available_offer_dict['offer_title'].append(split_available_offer_info[3])
                available_offer_dict['offer_description'].append(split_available_offer_info[5])
                available_offer_dict['multiple_rewards'].append(1)

            elif len(split_available_offer_info) == 6:
                available_offer_dict['total_coins_earnable'].append(split_available_offer_info[2])
                available_offer_dict['offer_title'].append(split_available_offer_info[3])
                available_offer_dict['offer_description'].append(split_available_offer_info[4])
                available_offer_dict['multiple_rewards'].append(0)

            elif len(split_available_offer_info) == 5:
                available_offer_dict['total_coins_earnable'].append(split_available_offer_info[2])
                available_offer_dict['offer_title'].append(split_available_offer_info[3])
                available_offer_dict['offer_description'].append(split_available_offer_info[4])
                available_offer_dict['multiple_rewards'].append(0)

            elif len(split_available_offer_info) == 226:
                continue
            else:
                raise Exception ('Unexpected offer split size')
            #Add offer_device value to dictionary
            available_offer_dict['offer_device'].append(offerwalls)
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
        print(f"'Error: {err}'")

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
        print(f"'Unhandled Error: %{err}'")

def create_completed_offer_dataframe(completed_offer_dict):
    """
    This function returns the completed offer dict as a pandas DataFrame.
    """
    completed_offer_dataframe = pd.DataFrame.from_dict(completed_offer_dict)
    return completed_offer_dataframe

def parse_pending_offer_info(driver):
    """
    This function parses through the Ayet offerwall text and extracts:
    1. Pending Offer Titles
    2. Pending Offer Description
    3. Pending Start Date/Time
    """
    #Create dictionary to hold offer information
    pending_offer_dict = {'pending_offer_title':[],'offer_description':[],'date_completed':[]}

    #Navigate to pending status page
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

        #Wait for Pending button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tabs-menu")))
        #Explicit wait
        time.sleep(1)
        #Click button
        driver.find_elements(By.XPATH, "//li[@href='#pending']")[0].click()
    except Exception as err:
        print(f"'Error: {err}'")

    #Attempt to scrape pending offers
    try:
        #Wait for pending page to render
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-status")))
        #Explicit wait
        time.sleep(1)
        #Extract pending offer info
        pending_offer_info = driver.find_elements(By.XPATH, "//div[@id='user-status']")[0]

        ############# LOGIC BLOCK ##############
        #Get actual text from webpage
        pending_offer_text = pending_offer_info.text
        #Split the text
        split_pending_offer_info = pending_offer_text.split('\n')
        #Chunk the text for insert into dictionary
        chunked_pending_list = utils.chunked_iterable(split_pending_offer_info, 4)
        #Insert values to dictionary
        for chunks in chunked_pending_list:
            pending_offer_dict['pending_offer_title'].append(chunks[1])
            pending_offer_dict['offer_description'].append(chunks[2])
            pending_offer_dict['date_completed'].append(chunks[3])
        ############# LOGIC BLOCK ##############

        return pending_offer_dict
    except Exception as err:
        print(f"'Unhandled Error: %{err}'")

def create_pending_offer_dataframe(pending_offer_dict):
    """
    This function returns the pending offer dict as a pandas DataFrame.
    """
    pending_offer_dataframe = pd.DataFrame.from_dict(pending_offer_dict)
    return pending_offer_dataframe

# def combine_desktop_and_other_offers(desktop_offer_dataframe,offer_dataframe):
#     """
#     This function will combine the two offer frames to ensure we have
#     the full offerwall list.
#     """
