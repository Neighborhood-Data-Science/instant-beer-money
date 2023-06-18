"""
Main Web Testing Framework
"""
import os
import pandas as pd
import pytest
import ayet_info
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# The environment variables should be present in your CI/CD pipeline
# and/or server side as well.


@pytest.mark.usefixtures("setup_ayet_page")
class TestAYET:
    """
    Test suite for the Ayet offerwall.

    This test suite is designed to test the functionality of `ayet_info.py` to ensure 
    it operates as expected.
    """

    def test_access_ayet_offerwall(self, setup_ayet_page):
        """
        Tests if able to successfully open Ayet Offerwall
        """
        assert setup_ayet_page.current_url == os.environ['AYET']

    def test_parsed_offer_info_is_dict_ayet(self, setup_ayet_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = ayet_info.parse_offer_information(setup_ayet_page)
        assert isinstance(offer_dict, dict)

    def test_parsed_offer_info_is_equal_ayet(self, setup_ayet_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = ayet_info.parse_offer_information(setup_ayet_page)
        key_list = list(offer_dict.keys())
        first_size = len(offer_dict[key_list[0]])
        for remaining_keys in key_list[1:]:
            assert len(offer_dict[remaining_keys]) == first_size

    def test_parsed_offer_info_dict_size_ayet(self, setup_ayet_page, size=7):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of 7 keys.
        """
        offer_dict = ayet_info.parse_offer_information(setup_ayet_page)
        assert len(offer_dict) == size

    def test_parsed_dataframe_is_dataframe_ayet(self, setup_ayet_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = ayet_info.parse_offer_information(setup_ayet_page)
        offer_dataframe = ayet_info.create_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)

    def test_parsed_dataframe_not_empty_ayet(self, setup_ayet_page):
        """
        Tests if resultant dataframe is not empty.
        """
        offer_dict = ayet_info.parse_offer_information(setup_ayet_page)
        offer_dataframe = ayet_info.create_offer_dataframe(offer_dict)
        assert len(offer_dataframe) > 0
