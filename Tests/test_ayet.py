"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import ayet_info 
import pandas as pd
import pytest
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.mark.usefixtures("setup_ayet_page")
class TestAYET:
    """
    Test suite for the Ayet offerwall.

    This test suite is designed to test the functionality of `ayet_info.py` to ensure 
    it operates as expected.
    """
    def test_access_ayet_offerwall(self,setup_ayet_page):
        """
        Tests if able to successfully open Ayet Offerwall
        """
        assert setup_ayet_page.current_url == os.environ['AYET']


    def test_parsed_offer_info_is_dict(self,setup_ayet_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = ayet_info.parse_available_offer_information(setup_ayet_page)
        assert isinstance(offer_dict, dict)


    def test_parsed_offer_info_is_equal(self,setup_ayet_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = ayet_info.parse_available_offer_information(setup_ayet_page)
        key_list = list(offer_dict.keys())
        assert len(offer_dict.get(key_list[0])) ==  \
            len(offer_dict.get(key_list[2])) ==     \
            len(offer_dict.get(key_list[3])) ==     \
            len(offer_dict.get(key_list[4]))


    def test_parsed_offer_info_dict_size(self,setup_ayet_page,size=5):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of (5) [keys].
        """
        offer_dict = ayet_info.parse_available_offer_information(setup_ayet_page)
        assert len(offer_dict) == size


    def test_parsed_dataframe_is_dataframe(self,setup_ayet_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = ayet_info.parse_available_offer_information(setup_ayet_page)
        offer_dataframe = ayet_info.create_available_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)


    def test_values_in_multiple_rewards(self,setup_ayet_page):
        """
        Tests if all values in multiple_rewards column are either 1 or 0
        """
        offer_dict = ayet_info.parse_available_offer_information(setup_ayet_page)
        offer_dataframe = ayet_info.create_available_offer_dataframe(offer_dict)
        indicator_values = offer_dataframe['multiple_rewards'].unique()
        assert [0 and 1] in indicator_values


    def test_values_in_devices(self,setup_ayet_page):
        """
        Tests if all values in offer_device column are either:
        android
        iphone
        desktop
        """
        offer_dict = ayet_info.parse_available_offer_information(setup_ayet_page)
        offer_dataframe = ayet_info.create_available_offer_dataframe(offer_dict)
        offer_device_vals = offer_dataframe['offer_device'].unique()
        assert ['apple' and 'android' and 'desktop'] in offer_device_vals
