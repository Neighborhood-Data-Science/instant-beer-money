import time
import sys
import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def parse_toro(driver):
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
    # Create dictionary to hold offer information
    toro_dict = {'offer_title': [],
                 'offer_amount': [], 'offer_device': []}

    try:
        # Wait for offers to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "offert")))
        # Explicit Wait
        time.sleep(1)
    except Exception as err:
        print(f"'Waiting for offers Error: {err}'")
        sys.exit(0)

    try:
        # Focus on offerwall information
        offer_info = driver.find_elements(By.CLASS_NAME, "offert")

        ############# LOGIC BLOCK ##############
        for offers in offer_info:
            try:
                # Set variables equal to text values of the offers
                offer_payout = offers.get_attribute('data-offer_payout')
                offer_device = offers.get_attribute('data-offer_device')
                # Split the offer text to gain information about the offer itself
                offer_text = offers.get_attribute('innerText').split('\t')[1]

                # Insert into dictionary
                toro_dict['offer_title'].append(offer_text)
                toro_dict['offer_amount'].append(offer_payout)
                toro_dict['offer_device'].append(offer_device)

            except IndexError:
                # Check if length of requested offer_text is 1. If so, skip that entry, otherwise fail
                assert len(offers.get_attribute('innerText').split('\t')) == 1

    except Exception as err:
        print(f"'Parsing offer information Error: {err}'")
        sys.exit(0)
    ############# LOGIC BLOCK ##############

    return toro_dict

def parse_revu(driver):
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
    # Create dictionary to hold offer information
    revu_dict = {'offer_title': [], 'offer_amount': []}

    try:
        # Wait for 'Most popular' Icon to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='select2-selection select2-selection--single']")))
        # Explicit Wait
        time.sleep(1)
    except Exception as err:
        print(f"'Setting Driver Error: {err}'")
        sys.exit(0)

    # Focus on offerwall information
    offer_name = driver.find_elements(
        by=By.CLASS_NAME, value='main__card-left')
    offer_amount = driver.find_elements(
        by=By.CLASS_NAME, value='main__card-right')

    ############# LOGIC BLOCK ##############
    for (offers, amount) in zip(offer_name, offer_amount):
        try:
            # Grab the name/description of the offer
            name = offers.get_attribute('innerText')
            # Grab the amount of the offer (typicall highest value is second).
            amount = amount.get_attribute('innerText').split('\n')[1]
            # Add information to dictionary
            revu_dict['offer_title'].append(name)
            revu_dict['offer_amount'].append(amount)
        except IndexError:
            # Skip the offer if there is no amount
            # type: ignore # Pylance(reportUnboundVariable)
            print(f'Skipped: {name} No amount found.')
            continue
    ############# LOGIC BLOCK ##############
    return revu_dict

def create_offer_dataframe(offerwall_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.

    Parameters
    ----------
        offerwall_dict: `dict`
            A Python dictionary containing the offer information

    Returns
    -------
        offer_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the offer information.
    """
    offer_dataframe = pd.DataFrame.from_dict(offerwall_dict)
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

def clean_offertoro(toro_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Offertoro offerwall.

    Parameters
    ----------
        toro_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Offertoro offerwall.

    Returns
    -------
        clean_toro_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Offertoro offerwall.
    """

    # Define replacement dictionary
    replace_dict = {'android phone': 'Android',
                    'iphone/ipad': 'iOS', 'device': 'Desktop'}

    # Remove and replace the values ' phone' and 'device' from the offer_device column
    toro_dataframe.loc[:, 'offer_device'] = toro_dataframe['offer_device'].replace(
        replace_dict)

    # Declare the refined title list
    refined_title = []

    for vals in toro_dataframe['offer_title']:
        # Returning first element of the split
        splits_ = vals.strip().split('\n')[0]
        # Check if there is a '-' and keep all text up to the '-' marker
        index = splits_.find('-')
        title_split = splits_[:index]
        # Additional strip of text to remove whitespaces
        title_split = title_split.rstrip()
        # Append the title split to the refined title list
        refined_title.append(title_split)

    # Replace the offer_title column with the refined title list
    toro_dataframe.loc[:, 'offer_title'] = refined_title

    # Add a new column to the dataframe containing the name of the offerwall.
    toro_dataframe['offerwall_name'] = 'Offertoro'

    return toro_dataframe

def clean_revu(revu_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Revenue Universe offerwall.

    Parameters
    ----------
        revu_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Revenue Universe offerwall.

    Returns
    -------
        clean_revu_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Revenue Universe offerwall.
    """

    # Remove commas from values in offer_amount column
    revu_dataframe.loc[:, 'offer_amount'] = [str(x).replace(',', '') for x in revu_dataframe.loc[:,'offer_amount']]

    # Add a new column to the dataframe containing the name of the offerwall.
    revu_dataframe['offerwall_name'] = 'RevU'

    return revu_dataframe

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
        driver = start_driver_and_open_url(os.environ.get('AYET'))
        offer_info = parse_ayet(driver)
        ayet_dataframe = create_offer_dataframe(offer_info)
        clean_ayet_dataframe = clean_ayet(ayet_dataframe)
    except Error as process_error:
        print(process_error)

    # try:
    #     # Read and parse the data from Adgem offerwall
    #     driver = start_driver_and_open_adgem('ADGEM')
    #     offer_info = parse_ayet(driver)
    #     adgem_dataframe = create_offer_dataframe(offer_info)
    #     clean_adgem_dataframe = clean_adgem(adgem_dataframe)
    # except Error as process_error:
    #     print(process_error)

    try:
        # Read and parse the data from Offertoro offerwall
        driver = start_driver_and_open_url(os.environ.get('TORO'))
        offer_info = parse_toro(driver)
        offertoro_dataframe = create_offer_dataframe(offer_info)
        clean_offertoro_dataframe = clean_offertoro(
            offertoro_dataframe)
    except Error as process_error:
        print(process_error)

    try:
        # Read and parse the data from Revu offerwall
        driver = start_driver_and_open_url(os.environ.get('REVU'))
        offer_info = parse_revu(driver)
        revu_dataframe = create_offer_dataframe(offer_info)
        clean_revu_dataframe = clean_revu(revu_dataframe)
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

def establish_connection():
    """
    Function to establish a connection to the database.

    Parameters
    ----------
    None

    Returns
    -------
        database_conn: `mysql.connector.connection_cext.CMySQLConnection` 
            A connection to the database.
    """

    try:
        database_conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME']
        )
        return database_conn
    except Error as process_error:
        print(process_error)

def insert_offer_data(dataframe_list, database):
    """
    Function to insert data into the database.

    Parameters
    ----------
        dataframe_list: `list`  
            A list containing each offerwall dataframe that was successfully scraped and parsed.
        database: `mysql.connector.connection_cext.CMySQLConnection` 
            A successfully connected database.

    Returns
    -------
        None
    """

    # Create a cursor object to execute SQL queries
    cursor = database.cursor()

    # Loop through each dataframe in the list and add it to the database
    for dataframe in dataframe_list:
        # Collect the column names from the dataframe.
        query_cols = ', '.join(dataframe.columns)
        # Calculate the proper number of %s placeholders for each column in the dataframe.
        value_len = ', '.join(['%s'] * len(dataframe.columns))
        # Query to insert the data into the database
        insert_query = f"INSERT INTO {os.environ['DB_MAIN_TABLE']} ({query_cols}) VALUES ({value_len})"
        # Get the values from the DataFrame as a list of tuples
        values = [tuple(row) for row in dataframe.values]
        # Execute the INSERT statement with multiple rows
        cursor.executemany(insert_query, values)
        # Commit the changes to the database
        database.commit()

    # Close the cursor and the connection
    cursor.close()
    database.close()

    return 'SUCCESS'

def lambda_handler(event=None, context=None):
    """
    The main execution step of the AWS Lambda function.
    """
    # dataframe_list = get_offerwall_data()
    # database_conn = establish_connection()
    # table_submission = insert_offer_data(dataframe_list, database_conn)
    time.sleep(5)
    text = 'This is a test message.'
    return {
        "body": text
    }
