"""
Main Framework for pulling data from Freecash offerwalls and pushing it to the database
"""

import pandas as pd
import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
import sys
sys.path.append('./Functions')
import adgem_info
import ayet_info
import offertoro_info
import revu_info

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.