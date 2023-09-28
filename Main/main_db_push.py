"""
Main Framework for pulling data from Freecash offerwalls and pushing it to the database
"""
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
import revu_info
import offertoro_info
import ayet_info

# Load environment variables
load_dotenv()
# The environment variables should be present in your CI/CD pipeline
# and/or server side as well.

# This needs to take the userID as input --
# This will be executed when the user submits their FSID

def build_urls(fsid):
    """
    Builds a dictionary of URLs for the given FSID.

    Parameters
    ----------
        fsid: `str`
            The FSID to build URLs for. Provided by the user. 

    Returns
    -------
        urls: `list`
            List of URLs for the given FSID.
    """

    # Build URLs
    url_dict = {
        'AYET':f'https://www.ayetstudios.com/offers/web_offerwall/2693?external_identifier=fsid-{fsid}-607783a635',
        'TORO':f'https://www.offertoro.com/ifr/show/23580/fsid-{fsid}-607783a635/9746/0/0/137855987',
        'REVU':f'https://publishers.revenueuniverse.com/wall/343/offers?uid=fsid-{fsid}-607783a635&sid3=~~137857294'
    }

    return url_dict

def get_offerwall_data(url_dict):
    """
    Function to pull data from the offerwalls

    Parameters
    ----------
        url_dict: `dict`
            Dictionary containing the pre-built URLs to scrape the data from.

    Returns
    -------
        dataframe_list: `list`  
            A list containing each offerwall dataframe that was successfully scraped and parsed.
    """

    try:
        # Read and parse the data from Ayet offerwall
        driver = ayet_info.start_driver_and_open_url(url_dict.get('AYET'))
        offer_info = ayet_info.parse_ayet(driver)
        ayet_dataframe = ayet_info.create_offer_dataframe(offer_info)
        clean_ayet_dataframe = ayet_info.clean_ayet(ayet_dataframe)
    except Error as process_error:
        print(process_error)

    try:
        # Read and parse the data from Offertoro offerwall
        driver = offertoro_info.start_driver_and_open_url(url_dict.get('TORO'))
        offer_info = offertoro_info.parse_toro(driver)
        offertoro_dataframe = offertoro_info.create_offer_dataframe(offer_info)
        clean_offertoro_dataframe = offertoro_info.clean_offertoro(
            offertoro_dataframe)
    except Error as process_error:
        print(process_error)

    try:
        # Read and parse the data from Revu offerwall
        driver = revu_info.start_driver_and_open_url(url_dict.get('REVU'))
        offer_info = revu_info.parse_revu(driver)
        revu_dataframe = revu_info.create_offer_dataframe(offer_info)
        clean_revu_dataframe = revu_info.clean_revu(revu_dataframe)
    except Error as process_error:
        print(process_error)

    # Check which dataframes were created and return those dataframes
    dataframe_list = []
    if 'clean_ayet_dataframe' in locals():
        dataframe_list.append(clean_ayet_dataframe)
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

    return print('SUCCESS')
