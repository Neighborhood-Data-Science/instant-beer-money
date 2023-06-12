"""
Main Framework for pulling data from Freecash offerwalls and pushing it to the database
"""

import pandas as pd
import pytest
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
import sys
sys.path.append('./Functions')
import adgem_info
import ayet_info
import offertoro_info
import revu_info
import offer_cleanup

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline 
#and/or server side as well.

### This needs to take the userID as input --
### This will be executed when the user submits their FSID
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
        offer_info = ayet_info.parse_offer_information(driver)
        ayet_dataframe = ayet_info.create_offer_dataframe(offer_info)
        clean_ayet_dataframe = offer_cleanup.clean_ayet(ayet_dataframe)
    except Error as e:
        print(e)

    try:
        # Read and parse the data from Adgem offerwall
        driver = adgem_info.start_driver_and_open_adgem('ADGEM')
        offer_info = adgem_info.parse_offer_information(driver)
        adgem_dataframe = adgem_info.create_offer_dataframe(offer_info)
        clean_adgem_dataframe = offer_cleanup.clean_adgem(adgem_dataframe)
    except Error as e:
        print(e)

    try:
        # Read and parse the data from Offertoro offerwall
        driver = offertoro_info.start_driver_and_open_offertoro('TORO')
        offer_info = offertoro_info.parse_offer_information(driver)
        offertoro_dataframe = offertoro_info.create_offer_dataframe(offer_info)
        clean_offertoro_dataframe = offer_cleanup.clean_offertoro(offertoro_dataframe)
    except Error as e:
        print(e)

    try:
        # Read and parse the data from Revu offerwall
        driver = revu_info.start_driver_and_open_revu('REVU')
        offer_info = revu_info.parse_offer_information(driver)
        revu_dataframe = revu_info.create_offer_dataframe(offer_info)
        clean_revu_dataframe = offer_cleanup.clean_revu(revu_dataframe)
    except Error as e:
        print(e)

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
        mydb: `mysql.connector.connection_cext.CMySQLConnection` 
            A connection to the database.
    """

    try:
        mydb = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME']
        )
        return mydb
    except Error as e:
        print(e)

def insert_offer_data(dataframe_list, mydb):
    """
    Function to insert data into the database.

    Parameters
    ----------
        dataframe_list: `list`  
            A list containing each offerwall dataframe that was successfully scraped and parsed.
        mydb: `mysql.connector.connection_cext.CMySQLConnection` 
            A connection to the database.

    Returns
    -------
        None
    """

    # Create a cursor object to execute SQL queries
    cursor = mydb.cursor()

    # Loop through each dataframe in the list and add it to the database
    for dataframe in dataframe_list:
        # Convert the DataFrame into a list of tuples
        query_cols = ', '.join(dataframe.columns)
        value_len = ', '.join(['%s'] * len(dataframe.columns))
        insert_query = f"INSERT INTO {os.environ['DB_MAIN_TABLE']} ({query_cols}) VALUES ({value_len})"
        # Get the values from the DataFrame as a list of tuples
        values = [tuple(row) for row in dataframe.values]
        # Execute the INSERT statement with multiple rows
        cursor.executemany(insert_query, values)
        # Commit the changes to the database
        mydb.commit()

    # Close the cursor and the connection
    cursor.close()
    mydb.close()

    return 'Table inserted successfully'

if __name__ == '__main__':
    # Retrieve the offerwall data from each offerwall
    offer_data = get_offerwall_data()
    # Establish a connection to the database
    mydb = establish_connection()
    # Insert the offerwall data into the database
    insert_offer_data(offer_data, mydb)
