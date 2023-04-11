"""
Main Web Testing Framework for AdGem offerwall through freecash.com
"""
import sys
sys.path.append('./Functions')

import adgem_info # type: ignore # Pylance(reportMissingImports)
import pandas as pd
import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.mark.usefixtures("setup_adgem_page")
class TestADGEM:
    """
    Test suite for the Adgem offerwall.

    This test suite is designed to test the functionality of `adgem_info.py` to ensure 
    it operates as expected.
    """
    def test_access_adgem_offerwall(self,setup_adgem_page):
        """
        Tests if able to successfully open Adgem Offerwall
        """
        assert setup_adgem_page.current_url == os.environ['ADGEM']

    def test_parsed_offer_info_is_dict(self,setup_adgem_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_adgem_page)
        assert isinstance(offer_dict, dict)


    def test_parsed_offer_info_is_equal(self,setup_adgem_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_adgem_page)
        key_list = list(offer_dict.keys())
        assert len(offer_dict.get(key_list[0])) ==  \
            len(offer_dict.get(key_list[1])) ==     \
            len(offer_dict.get(key_list[2])) ==     \
            len(offer_dict.get(key_list[3])) ==     \
            len(offer_dict.get(key_list[4]))


    def test_parsed_offer_info_dict_size(self,setup_adgem_page,size=5):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of (5) [keys].
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_adgem_page)
        assert len(offer_dict) == size


    def test_parsed_dataframe_is_dataframe(self, setup_adgem_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_adgem_page)
        offer_dataframe = adgem_info.create_available_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)
