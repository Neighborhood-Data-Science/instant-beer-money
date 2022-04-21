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

@pytest.mark.usefixtures("setup_raw_revu_page")
class TestBaselineREVU:
    """
    Baseline RevU Offerwall test suite
    """
    def test_access_revu_offerwall(self,setup_raw_revu_page):
        """
        Tests if able to successfully open RevU Offerwall
        """
        assert setup_raw_revu_page.current_url == os.environ['MASTER_REVU']


    def test_parsed_offer_info_is_dict(self,setup_raw_revu_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = revu_info.parse_available_offer_information(setup_raw_revu_page)
        assert isinstance(offer_dict, dict)


    def test_parsed_offer_info_is_equal(self,setup_raw_revu_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = revu_info.parse_available_offer_information(setup_raw_revu_page)
        key_list = list(offer_dict.keys())
        assert len(offer_dict.get(key_list[0])) ==  \
            len(offer_dict.get(key_list[1])) ==     \
            len(offer_dict.get(key_list[2])) ==     \
            len(offer_dict.get(key_list[3]))


    def test_parsed_offer_info_dict_size(self,setup_raw_revu_page,size=4):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of (4) [keys].
        """
        offer_dict = revu_info.parse_available_offer_information(setup_raw_revu_page)
        assert len(offer_dict) == size


    def test_parsed_dataframe_is_dataframe(self,setup_raw_revu_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = revu_info.parse_available_offer_information(setup_raw_revu_page)
        offer_dataframe = revu_info.create_available_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)

@pytest.mark.usefixtures("setup_main_user_revu_page")
class TestMainUserREVU:
    """
    Main User RevU Offerwall test suite
    """
    def test_access_offerwall_main_user(self,setup_main_user_revu_page):
        """
        Tests if able to successfully open RevU Offerwall
        """
        assert setup_main_user_revu_page.current_url == os.environ['REVU']

    # def test_parsed_completed_offer_info_is_dict(self,setup_main_user_revu_page):
    #     """
    #     Tests if output of function is an expected dictionary.
    #     """
    #     completed_offer_dict = revu_info.parse_completed_offer_info(setup_main_user_revu_page)
    #     assert isinstance(completed_offer_dict, dict)


    # def test_parsed_completed_offer_info_dict_size(self, setup_main_user_revu_page, size=4):
    #     """
    #     Tests if resulting completed offer dictionary is the correct size.
    #     Should have length of (4) [keys].
    #     """
    #     completed_offer_dict = revu_info.parse_completed_offer_info(setup_main_user_revu_page)
    #     assert len(completed_offer_dict) == size


    # def test_parsed_completed_offer_info_is_equal(self, setup_main_user_revu_page):
    #     """
    #     Tests if length of key:value pairs in comnpleted offer dict are
    #     the same size across all key:value lists.
    #     """
    #     completed_offer_dict = revu_info.parse_completed_offer_info(setup_main_user_revu_page)
    #     key_list = list(completed_offer_dict.keys())
    #     assert len(completed_offer_dict.get(key_list[0])) == \
    #             len(completed_offer_dict.get(key_list[1])) == \
    #             len(completed_offer_dict.get(key_list[2])) == \
    #             len(completed_offer_dict.get(key_list[3]))


    # def test_completed_dataframe_is_dataframe(self, setup_main_user_revu_page):
    #     """
    #     Tests if resultant dataframe is type dataframe.
    #     """
    #     completed_offer_dict = revu_info.parse_completed_offer_info(setup_main_user_revu_page)
    #     completed_offer_dataframe = revu_info.create_completed_offer_dataframe(completed_offer_dict)
    #     assert isinstance(completed_offer_dataframe, pd.DataFrame)
