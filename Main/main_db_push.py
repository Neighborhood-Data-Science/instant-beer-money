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


try:
    connection = mysql.connector.connect(host=os.environ['DB_HOST'],
                                        user=os.environ['DB_USER'],
                                        password=os.environ['DB_PASSWORD'])
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
