"""
Main Web Testing Framework for AdGem offerwall through freecash.com
"""
import sys
sys.path.append('./Functions')

import adgem_info
import pandas as pd
import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.mark.usefixtures("setup_raw_adgem_page")
class TestBaselineAdgem:
    """
    Baseline Adgem Offerwall test suite
    """
    def test_access_adgem_offerwall(self,setup_raw_adgem_page):
        """
        Tests if able to successfully open Adgem Offerwall
        """
        assert setup_raw_adgem_page.current_url == os.environ['MASTER_ADGEM']

    def test_parsed_offer_info_is_dict(self,setup_raw_adgem_page):
        """
        Tests if output of function is an expected dictionary.
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_raw_adgem_page)
        assert isinstance(offer_dict, dict)


    def test_parsed_offer_info_is_equal(self,setup_raw_adgem_page):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_raw_adgem_page)
        key_list = list(offer_dict.keys())
        assert len(offer_dict.get(key_list[0])) ==  \
            len(offer_dict.get(key_list[1])) ==     \
            len(offer_dict.get(key_list[2])) ==     \
            len(offer_dict.get(key_list[3])) ==     \
            len(offer_dict.get(key_list[4]))


    def test_parsed_offer_info_dict_size(self,setup_raw_adgem_page,size=5):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of (5) [keys].
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_raw_adgem_page)
        assert len(offer_dict) == size


    def test_parsed_dataframe_is_dataframe(self, setup_raw_adgem_page):
        """
        Tests if resultant dataframe is type dataframe.
        """
        offer_dict = adgem_info.parse_available_offer_information(setup_raw_adgem_page)
        offer_dataframe = adgem_info.create_available_offer_dataframe(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)


    # def test_values_in_multiple_rewards(self):
    #     """
    #     Tests if all values in multiple_rewards column are either 1 or 0
    #     """
    #     full_adgem_page = self.adgem_base_page
    #     offer_dict = adgem_info.parse_available_offer_information(full_adgem_page)
    #     offer_dataframe = adgem_info.create_available_offer_dataframe(offer_dict)
    #     indicator_values = offer_dataframe['multiple_rewards'].unique()
    #     assert [0 and 1] in indicator_values


    # def test_values_in_devices(self):
    #     """
    #     Tests if all values in offer_device column are either:
    #     android
    #     iphone
    #     desktop
    #     """
    #     full_adgem_page = self.adgem_base_page
    #     offer_dict = adgem_info.parse_available_offer_information(full_adgem_page)
    #     offer_dataframe = adgem_info.create_available_offer_dataframe(offer_dict)
    #     offer_device_vals = offer_dataframe['offer_device'].unique()
    #     assert ['apple' and 'android' and 'desktop'] in offer_device_vals


# @pytest.mark.usefixtures("setup_main_user_adgem_page")
# class TestMainUserAdgem:
  # """
  #  Main User Adgem Offerwall test suite
  #  """
  #  def test_access_adgem_offerwall_main(self,setup_main_user_adgem_page):
  #      """
  #      Tests if able to successfully open Adgem Offerwall
  #      """
  #      assert setup_main_user_adgem_page.current_url == os.environ['ADGEM']

  #  def test_adgem_device_list(self,setup_main_user_adgem_page):
  #      """
  #      Tests if device list has expected values on Adgem Main Page
  #      """
  #      device_list = setup_main_user_adgem_page.find_elements(By.XPATH,"//div[@class = 'col-sm-4 text-center ']/div")
  #      text_check = [device_names.text for device_names in device_list]
  #      assert ('Android' and 'iPhone' and 'iPad') in text_check

    # def test_parsed_completed_offer_info_is_dict(self):
    #     """
    #     Tests if output of function is an expected dictionary.
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     completed_offer_dict = adgem_info.parse_completed_offer_info(full_adgem_page)
    #     assert isinstance(completed_offer_dict, dict)


    # def test_parsed_completed_offer_info_dict_size(self,size=3):
    #     """
    #     Tests if resulting completed offer dictionary is the correct size.
    #     Should have length of (3) [keys].
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     completed_offer_dict = adgem_info.parse_completed_offer_info(full_adgem_page)
    #     assert len(completed_offer_dict) == size


    # def test_parsed_completed_offer_info_is_equal(self):
    #     """
    #     Tests if length of key:value pairs in comnpleted offer dict are
    #     the same size across all key:value lists.
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     completed_offer_dict = adgem_info.parse_completed_offer_info(full_adgem_page)
    #     key_list = list(completed_offer_dict.keys())
    #     assert len(completed_offer_dict.get(key_list[0])) == \
    #             len(completed_offer_dict.get(key_list[1])) == \
    #             len(completed_offer_dict.get(key_list[2]))


    # def test_completed_dataframe_is_dataframe(self):
    #     """
    #     Tests if resultant dataframe is type dataframe.
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     completed_offer_dict = adgem_info.parse_completed_offer_info(full_adgem_page)
    #     completed_offer_dataframe = adgem_info.create_completed_offer_dataframe(completed_offer_dict)
    #     assert isinstance(completed_offer_dataframe, pd.DataFrame)


    # def test_parsed_pending_offer_info_is_dict(self):
    #     """
    #     Tests if output of function is an expected dictionary.
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     pending_offer_dict = adgem_info.parse_pending_offer_info(full_adgem_page)
    #     assert isinstance(pending_offer_dict, dict)


    # def test_parsed_pending_offer_info_dict_size(self,size=3):
    #     """
    #     Tests if resulting pending offer dictionary is the correct size.
    #     Should have length of (3) [keys].
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     pending_offer_dict = adgem_info.parse_pending_offer_info(full_adgem_page)
    #     assert len(pending_offer_dict) == size


    # def test_parsed_pending_offer_info_is_equal(self):
    #     """
    #     Tests if length of key:value pairs in pending offer dict are
    #     the same size across all key:value lists.
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     pending_offer_dict = adgem_info.parse_pending_offer_info(full_adgem_page)
    #     key_list = list(pending_offer_dict.keys())
    #     assert len(pending_offer_dict.get(key_list[0])) == \
    #             len(pending_offer_dict.get(key_list[1])) == \
    #             len(pending_offer_dict.get(key_list[2]))


    # def test_pending_dataframe_is_dataframe(self):
    #     """
    #     Tests if resultant dataframe is type dataframe.
    #     """
    #     full_adgem_page = self.adgem_main_page
    #     pending_offer_dict = adgem_info.parse_pending_offer_info(full_adgem_page)
    #     pending_offer_dataframe = adgem_info.create_pending_offer_dataframe(pending_offer_dict)
    #     assert isinstance(pending_offer_dataframe, pd.DataFrame)
