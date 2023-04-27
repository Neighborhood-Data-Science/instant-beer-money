"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import offertoro_info
import pandas as pd
import pytest
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.mark.usefixtures("setup_toro_page")
class TestTORO:
    """
    Test suite for the Offertoro offerwall.

    This test suite is designed to test the functionality of `offeroffertoro_info.py` to ensure 
    it operates as expected.
    """
    def test_access_toro_offerwall(self,setup_toro_page):
        """
        Tests if able to successfully open OfferToro Offerwall
        """
        assert setup_toro_page.current_url == os.environ['TORO']

    def test_parsed_offer_info_is_dict(self,setup_toro_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = offertoro_info.parse_offer_information(setup_toro_page)
        assert isinstance(offer_dict, dict)

    def test_parsed_offer_info_is_equal(self,setup_toro_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = offertoro_info.parse_offer_information(setup_toro_page)
        key_list = list(offer_dict.keys())
        first_size = len(offer_dict[key_list[0]])
        for remaining_keys in key_list[1:]:
            assert len(offer_dict[remaining_keys]) == first_size


    def test_parsed_offer_info_dict_size(self,setup_toro_page,size=3):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of 3 keys.
        """
        offer_dict = offertoro_info.parse_offer_information(setup_toro_page)
        assert len(offer_dict) == size


    def test_parsed_dataframe_is_dataframe(self,setup_toro_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = offertoro_info.parse_offer_information(setup_toro_page)
        offer_dataframe = offertoro_info.create_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)
    
    def test_parsed_dataframe_not_empty(self, setup_toro_page):
        """
        Tests if resultant dataframe is not empty.
        """
        offer_dict = offertoro_info.parse_offer_information(setup_toro_page)
        offer_dataframe = offertoro_info.create_offer_dataframe(offer_dict)
        assert len(offer_dataframe) > 0