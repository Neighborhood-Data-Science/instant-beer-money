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
@pytest.mark.xfail(reason='New headless not supported on CircleCI')
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

    def test_parsed_offer_info_is_dict_adgem(self,setup_adgem_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = adgem_info.parse_offer_information(setup_adgem_page)
        assert isinstance(offer_dict, dict)


    def test_parsed_offer_info_is_equal_adgem(self,setup_adgem_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = adgem_info.parse_offer_information(setup_adgem_page)
        key_list = list(offer_dict.keys())
        first_size = len(offer_dict[key_list[0]])
        for remaining_keys in key_list[1:]:
            assert len(offer_dict[remaining_keys]) == first_size


    def test_parsed_offer_info_dict_size_adgem(self,setup_adgem_page,size=4):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of 4 keys.
        """
        offer_dict = adgem_info.parse_offer_information(setup_adgem_page)
        assert len(offer_dict) == size


    def test_parsed_dataframe_is_dataframe_adgem(self, setup_adgem_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = adgem_info.parse_offer_information(setup_adgem_page)
        offer_dataframe = adgem_info.create_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)

    def test_parsed_dataframe_not_empty_adgem(self, setup_adgem_page):
        """
        Tests if resultant dataframe is not empty.
        """
        offer_dict = adgem_info.parse_offer_information(setup_adgem_page)
        offer_dataframe = adgem_info.create_offer_dataframe(offer_dict)
        assert len(offer_dataframe) > 0
