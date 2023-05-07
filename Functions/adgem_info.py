"""
This module will contain code necessary to connect to and
scrape data from freecash.com
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
## Uncomment line below to run Chrome in 'headless' mode - ADGEM does not support headless mode.
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")


#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

def start_driver_and_open_adgem(offerwall_version):
    """
    Downloads and installs the latest version of Google chromedriver and
    opens the Adgem offerwall within a WebDriver

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

    #Set Adgem URL
    adgem = os.environ[offerwall_version]
    #Open webpage
    driver.get(adgem)
    return driver

def parse_offer_information(driver):
    """
    This function parses through the Adgem offerwall text and extracts:
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
        adgem_dict: `dict`
            A Python dictionary containing the offer information
    """
    #Create dictionary to hold offer information
    adgem_dict = {'offer_title':[],'offer_description':[],'offer_amount':[],'offer_device':[]}

    #Wait for page to load
    try:
        #Wait for list of offers to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,\
            "//span[@class = 'tw-text-sm satoshi-700 tw-text-[#2D2D2D] tw-leading-5 tw-break-words tw-w-full']")))
        #Explicit Wait
        time.sleep(1)
        #Get sorting buttons on page
        buttons = driver.find_elements(By.XPATH,"//div[@class = 'tw-relative tw-inline-block text-left tw-px-2 tw-w-full']")
        #Click this button to open device type menu
        buttons[-1].click()
        #Get device sorting options on page
        options = driver.find_elements(By.XPATH,"//a[@class = 'tw-block tw-px-4 tw-py-2 tw-text-lg tw-text-gray-700 hover:tw-bg-gray-100 hover:tw-text-gray-900 tw-cursor-pointer']")
        #Select the option that shows all offers for all devices
        for opts in options:
            if opts.get_attribute('innerText') == 'All':
                opts.click()
                break
            else:
                continue
    #Wait for list of offers to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,\
            "//span[@class = 'tw-text-sm satoshi-700 tw-text-[#2D2D2D] tw-leading-5 tw-break-words tw-w-full']")))
        #Explicit wait
        time.sleep(1)
    except Exception as err:
        print(f"'Waiting for hamburger button Error: {err}'")
        sys.exit(0)

    try:
        #Focus on offerwall information
        offers = driver.find_elements(By.XPATH,"//span[@class = 'tw-text-sm satoshi-700 tw-text-[#2D2D2D] tw-leading-5 tw-break-words tw-w-full']")
        descriptions = driver.find_elements(By.XPATH,"//span[@class = 'tw-flex tw-mt-1 tw-text-sm tw-text-[#969696] satoshi-400 tw-break-words tw-w-full']")
        amounts = driver.find_elements(By.XPATH,"//div[@class = 'tw-flex tw-items-center tw-justify-center tw-mb-1']")
        devices = driver.find_elements(By.XPATH,"//span[@class = 'tw-hidden md:tw-flex md:tw-items-center md:tw-justify-center']")
        for (o,d,a,dev) in zip(offers,descriptions,amounts,devices):
            try:
                #Grab the name of the offer
                name = o.get_attribute('innerText')
                #Grab the description of the offer
                description = d.get_attribute('innerText')
                #Grab the amount of the offer
                amount = a.get_attribute('innerText')
                #Grab the device name
                device = d.get_attribute('innerHTML')
                if 'Android' in device:
                    device = 'Android'
                elif 'Apple' in device:
                    device = 'Apple'
                else:
                    device = 'Desktop'
                #Add information to dictionary
                adgem_dict['offer_title'].append(name)
                adgem_dict['offer_description'].append(description)
                adgem_dict['offer_amount'].append(amount)
                adgem_dict['offer_device'].append(device)

            except Exception as err:
                print(f"'Parsing offer information error: {err}'")
                sys.exit(0)
    except Exception as err:
        print(f"'Finding page elements error: {err}'")
        sys.exit(0)
    return adgem_dict

def create_offer_dataframe(adgem_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.

    Parameters
    ----------
        adgem_dict: `dict`
            A Python dictionary containing the offer information.

    Returns
    -------
        offer_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the offer information.
    """
    offer_dataframe = pd.DataFrame.from_dict(adgem_dict)
    return offer_dataframe

