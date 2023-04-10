"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import revu_info
import pandas as pd
import pytest
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.mark.usefixtures("setup_revu_page")
class TestREVU:
    """
    Test suite for the Revenue Universe offerwall.

    This test suite is designed to test the functionality of `revu_info.py` to ensure it operates as expected.
    """
    def test_access_revu_offerwall(self,setup_revu_page):
        """
        Tests if able to successfully open RevU offerwall
        """
        assert setup_revu_page.current_url == os.environ['REVU']


    def test_parsed_offer_info_is_dict(self,setup_revu_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = revu_info.parse_offer_information(setup_revu_page)
        assert isinstance(offer_dict, dict)


    def test_parsed_offer_info_is_equal(self,setup_revu_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = revu_info.parse_offer_information(setup_revu_page)
        key_list = list(offer_dict.keys())
        assert len(offer_dict.get(key_list[0])) == len(offer_dict.get(key_list[1]))


    def test_parsed_offer_info_dict_size(self,setup_revu_page,size=2):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of 2 keys.
        """
        offer_dict = revu_info.parse_offer_information(setup_revu_page)
        assert len(offer_dict) == size


    def test_parsed_dataframe_is_dataframe(self,setup_revu_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = revu_info.parse_offer_information(setup_revu_page)
        offer_dataframe = revu_info.create_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)

