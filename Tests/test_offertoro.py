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

@pytest.mark.usefixtures("setup_raw_toro_page")
class TestBaselineTORO:
    """
    Baseline OfferToro Offerwall test suite
    """
    def test_access_toro_offerwall(self,setup_raw_toro_page):
        """
        Tests if able to successfully open OfferToro Offerwall
        """
        assert setup_raw_toro_page.current_url == os.environ['MASTER_TORO']


    # def test_parsed_offer_info_is_dict(self,setup_raw_toro_page):
    #     """
    #     Tests if output of function is an expected dictionary.
    #     """
    #     offer_dict = toro_info.parse_available_offer_information(setup_raw_toro_page)
    #     assert isinstance(offer_dict, dict)


    # def test_parsed_offer_info_is_equal(self,setup_raw_toro_page):
    #     """
    #     Tests if length of key:value pairs in offer dict are
    #     the same size across all key:value lists.
    #     """
    #     offer_dict = toro_info.parse_available_offer_information(setup_raw_toro_page)
    #     key_list = list(offer_dict.keys())
    #     assert len(offer_dict.get(key_list[0])) ==  \
    #         len(offer_dict.get(key_list[2])) ==     \
    #         len(offer_dict.get(key_list[3])) ==     \
    #         len(offer_dict.get(key_list[4]))


    # def test_parsed_offer_info_dict_size(self,setup_raw_toro_page,size=5):
    #     """
    #     Tests if resulting offer dictionary is the correct size.
    #     Should have length of (5) [keys].
    #     """
    #     offer_dict = toro_info.parse_available_offer_information(setup_raw_toro_page)
    #     assert len(offer_dict) == size


    # def test_parsed_dataframe_is_dataframe(self,setup_raw_toro_page):
    #     """
    #     Tests if resultant dataframe is type dataframe.
    #     """
    #     offer_dict = toro_info.parse_available_offer_information(setup_raw_toro_page)
    #     offer_dataframe = toro_info.create_available_offer_dataframe(offer_dict)
    #     assert isinstance(offer_dataframe, pd.DataFrame)


    # def test_values_in_multiple_rewards(self,setup_raw_toro_page):
    #     """
    #     Tests if all values in multiple_rewards column are either 1 or 0
    #     """
    #     offer_dict = toro_info.parse_available_offer_information(setup_raw_toro_page)
    #     offer_dataframe = toro_info.create_available_offer_dataframe(offer_dict)
    #     indicator_values = offer_dataframe['multiple_rewards'].unique()
    #     assert [0 and 1] in indicator_values


    # def test_values_in_devices(self,setup_raw_toro_page):
    #     """
    #     Tests if all values in offer_device column are either:
    #     android
    #     iphone
    #     desktop
    #     """
    #     offer_dict = toro_info.parse_available_offer_information(setup_raw_toro_page)
    #     offer_dataframe = toro_info.create_available_offer_dataframe(offer_dict)
    #     offer_device_vals = offer_dataframe['offer_device'].unique()
    #     assert ['apple' and 'android' and 'desktop'] in offer_device_vals


@pytest.mark.usefixtures("setup_main_user_toro_page")
class TestMainUserTORO:
    """
    Main User OfferToro Offerwall test suite
    """
    def test_access_offerwall_main_user(self,setup_main_user_toro_page):
        """
        Tests if able to successfully open OfferToro Offerwall
        """
        assert setup_main_user_toro_page.current_url == os.environ['TORO']


    # def test_parsed_completed_offer_info_is_dict(self,setup_main_user_toro_page):
    #     """
    #     Tests if output of function is an expected dictionary.
    #     """
    #     completed_offer_dict = toro_info.parse_completed_offer_info(setup_main_user_toro_page)
    #     assert isinstance(completed_offer_dict, dict)


    # def test_parsed_completed_offer_info_dict_size(self, setup_main_user_toro_page, size=3):
    #     """
    #     Tests if resulting completed offer dictionary is the correct size.
    #     Should have length of (3) [keys].
    #     """
    #     completed_offer_dict = toro_info.parse_completed_offer_info(setup_main_user_toro_page)
    #     assert len(completed_offer_dict) == size


    # def test_parsed_completed_offer_info_is_equal(self, setup_main_user_toro_page):
    #     """
    #     Tests if length of key:value pairs in comnpleted offer dict are
    #     the same size across all key:value lists.
    #     """
    #     completed_offer_dict = toro_info.parse_completed_offer_info(setup_main_user_toro_page)
    #     key_list = list(completed_offer_dict.keys())
    #     assert len(completed_offer_dict.get(key_list[0])) == \
    #             len(completed_offer_dict.get(key_list[1])) == \
    #             len(completed_offer_dict.get(key_list[2]))


    # def test_completed_dataframe_is_dataframe(self, setup_main_user_toro_page):
    #     """
    #     Tests if resultant dataframe is type dataframe.
    #     """
    #     completed_offer_dict = toro_info.parse_completed_offer_info(setup_main_user_toro_page)
    #     completed_offer_dataframe = toro_info.create_completed_offer_dataframe(completed_offer_dict)
    #     assert isinstance(completed_offer_dataframe, pd.DataFrame)


    # def test_parsed_pending_offer_info_is_dict(self, setup_main_user_toro_page):
    #     """
    #     Tests if output of function is an expected dictionary.
    #     """
    #     pending_offer_dict = toro_info.parse_pending_offer_info(setup_main_user_toro_page)
    #     assert isinstance(pending_offer_dict, dict)


    # def test_parsed_pending_offer_info_dict_size(self, setup_main_user_toro_page, size=3):
    #     """
    #     Tests if resulting pending offer dictionary is the correct size.
    #     Should have length of (3) [keys].
    #     """
    #     pending_offer_dict = toro_info.parse_pending_offer_info(setup_main_user_toro_page)
    #     assert len(pending_offer_dict) == size


    # def test_parsed_pending_offer_info_is_equal(self, setup_main_user_toro_page):
    #     """
    #     Tests if length of key:value pairs in pending offer dict are
    #     the same size across all key:value lists.
    #     """
    #     pending_offer_dict = toro_info.parse_pending_offer_info(setup_main_user_toro_page)
    #     key_list = list(pending_offer_dict.keys())
    #     assert len(pending_offer_dict.get(key_list[0])) == \
    #             len(pending_offer_dict.get(key_list[1])) == \
    #             len(pending_offer_dict.get(key_list[2]))


    # def test_pending_dataframe_is_dataframe(self, setup_main_user_toro_page):
    #     """
    #     Tests if resultant dataframe is type dataframe.
    #     """
    #     pending_offer_dict = toro_info.parse_pending_offer_info(setup_main_user_toro_page)
    #     pending_offer_dataframe = toro_info.create_pending_offer_dataframe(pending_offer_dict)
    #     assert isinstance(pending_offer_dataframe, pd.DataFrame)
