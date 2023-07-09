import time
import sys
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = os.environ.get('AYET')

def start_driver_and_open_url(offerwall_version):
    """
    Open the given offerwall version within a WebDriver.

    Parameters
    ----------
        offerwall_version: `str`
            The version of the offerwall to open. Set up in the .env file.

    Returns
    -------
        offerwall_version: `WebDriver`
            WebDriver object that can be used to interact with the given `offerwall_version`.
    """

    # Initialize variable
    driver = None

    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--single-process")
    options.add_argument("--no-zygote")
    try:
        driver = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    except Exception as err:
        print(f"'Setting Driver Error: {err}'")
        sys.exit(0)

    # Open webpage
    driver.get(offerwall_version)
    return driver

def parse_ayet(driver):
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
    ayet_dict = {'offerLow': [], 'offer_amount': [],
                 'offer_title': [], 'offer_description': [],
                 'Additional': [], 'Difficulty': [],
                 'Ignore3': []}
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
    offer_info = driver.find_elements(
        By.XPATH, "//div[@class = 'row offer-row-basic offer-row-basic-cl ']")

    ############# LOGIC BLOCK ##############
    for offers in offer_info:
        # Grab raw text. On Ayet offerwall, there are no seperate classes for the elements on the page.
        # Therefore, we have to extract all text within an offerwall object.
        offer_text = offers.get_attribute('innerText')
        list_offer_text = offer_text.split('\n')
        # For each element of the offer text:
        # Append the element to the ayet_dictionary IN ORDER OF KEYS (set by ayet_dict)
        # An index error indicates that an element is not present for a particular key
        # in the dictionary. If we receive this error, impute the value for that key as `None`

        # Set iterator to 0
        i = 0
        for key,vals in ayet_dict.items():
            try:
                vals.append(list_offer_text[i])
                i += 1
                continue
            except IndexError:
                vals.append(None)
                i += 1
                continue
    ############# LOGIC BLOCK ##############
    return ayet_dict

def create_offer_dataframe(ayet_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.

    Parameters
    ----------
        ayet_dict: `dict`
            A Python dictionary containing the offer information

    Returns
    -------
        offer_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the offer information.
    """
    offer_dataframe = pd.DataFrame.from_dict(ayet_dict)
    return offer_dataframe

def clean_ayet(ayet_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Ayet offerwall.

    Parameters
    ----------
        ayet_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Ayet offerwall.

    Returns
    -------
        clean_ayet_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Ayet offerwall.
    """

    keyword_list = ['Multiple rewards']
    # Add proper description from the 'Additonal' column instead of
    # a generic 'Mulitple rewards' description.
    for index, row in ayet_dataframe.iterrows():
        if row['offer_description'] in keyword_list:
            row['offer_description'] = row['Additional']

    # Drop unneeded columns from the dataframe.
    ayet_dataframe = ayet_dataframe.drop(
        ['offerLow', 'Additional', 'Difficulty', 'Ignore3'], axis=1)

    # Drop rows containing 'None' values as these rows represent
    # duplicate data.
    ayet_dataframe = ayet_dataframe.dropna()

    # Add a new column to the dataframe containing the name of the offerwall.
    ayet_dataframe['offerwall_name'] = 'Ayet'

    return ayet_dataframe

def get_offerwall_data():
    """
    Function to pull data from the offerwalls

    Parameters
    ----------
        user_id: `str`
            The users FSID - Used to generate correct offers for a particular user.

    Returns
    -------
        dataframe_list: `list`  
            A list containing each offerwall dataframe that was successfully scraped and parsed.
    """

    try:
        # Read and parse the data from Ayet offerwall
        driver = ayet_info.start_driver_and_open_ayet('AYET')
        offer_info = ayet_info.parse_ayet(driver)
        ayet_dataframe = ayet_info.create_offer_dataframe(offer_info)
        clean_ayet_dataframe = offer_cleanup.clean_ayet(ayet_dataframe)
    except Error as process_error:
        print(process_error)

    try:
        # Read and parse the data from Adgem offerwall
        driver = adgem_info.start_driver_and_open_adgem('ADGEM')
        offer_info = adgem_info.parse_ayet(driver)
        adgem_dataframe = adgem_info.create_offer_dataframe(offer_info)
        clean_adgem_dataframe = offer_cleanup.clean_adgem(adgem_dataframe)
    except Error as process_error:
        print(process_error)

    try:
        # Read and parse the data from Offertoro offerwall
        driver = offertoro_info.start_driver_and_open_offertoro('TORO')
        offer_info = offertoro_info.parse_ayet(driver)
        offertoro_dataframe = offertoro_info.create_offer_dataframe(offer_info)
        clean_offertoro_dataframe = offer_cleanup.clean_offertoro(
            offertoro_dataframe)
    except Error as process_error:
        print(process_error)

    try:
        # Read and parse the data from Revu offerwall
        driver = revu_info.start_driver_and_open_revu('REVU')
        offer_info = revu_info.parse_ayet(driver)
        revu_dataframe = revu_info.create_offer_dataframe(offer_info)
        clean_revu_dataframe = offer_cleanup.clean_revu(revu_dataframe)
    except Error as process_error:
        print(process_error)

    # Check which dataframes were created and return those dataframes
    dataframe_list = []
    if 'clean_ayet_dataframe' in locals():
        dataframe_list.append(clean_ayet_dataframe)
    if 'clean_adgem_dataframe' in locals():
        dataframe_list.append(clean_adgem_dataframe)
    if 'clean_offertoro_dataframe' in locals():
        dataframe_list.append(clean_offertoro_dataframe)
    if 'clean_revu_dataframe' in locals():
        dataframe_list.append(clean_revu_dataframe)

    return dataframe_list

def lambda_handler(event=None, context=None):
    """
    The main execution step of the AWS Lambda function.
    """
    driver = start_driver_and_open_ayet(url)
    ayet_dict = parse_ayet(driver)
    ayet_df = create_offer_dataframe(ayet_dict)
    clean_ayet_df = clean_ayet(ayet_df)
    return {
        "body": clean_ayet_df.to_json(orient='records')
    }
