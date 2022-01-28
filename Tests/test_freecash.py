"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import freecash_info
import pandas as pd
import pytest
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.fixture(scope="class",autouse=True)
def setup_raw_ayet_page(request):
    """
    Set Ayet page as fixture using baseline ayet offerwall
    """
    offerwall_version = 'MASTER_AYET'
    ayet_base_page = freecash_info.start_driver_and_open_ayet(offerwall_version)
    request.cls.ayet_base_page = ayet_base_page
    yield ayet_base_page
    ayet_base_page.quit()

@pytest.fixture(scope="class",autouse=True)
def setup_main_user_ayet_page(request):
    """
    Set Ayet page as fixture using main user ayet offerwall
    """
    offerwall_version = 'AYET'
    ayet_main_page = freecash_info.start_driver_and_open_ayet(offerwall_version)
    request.cls.ayet_main_page = ayet_main_page
    yield ayet_main_page
    ayet_main_page.quit()

@pytest.mark.usefixtures("setup_raw_ayet_page")
class TestBaselineAYET:
    """
    Baseline Ayet Offerwall test suite
    """
    def test_access_ayet_offerwall(self):
        """
        Tests if able to successfully open Ayet Offerwall
        """
        full_ayet_page = self.ayet_base_page
        assert full_ayet_page.current_url == os.environ['MASTER_AYET']

    def test_parsed_offer_info_is_dict(self):
        """
        Tests if output of function is an expected dictionary.
        """
        full_ayet_page = self.ayet_base_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        assert isinstance(offer_dict, dict)

    def test_parsed_offer_info_is_equal(self):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        full_ayet_page = self.ayet_base_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        key_list = list(offer_dict.keys())
        assert len(offer_dict.get(key_list[0])) == \
            len(offer_dict.get(key_list[1])) == len(offer_dict.get(key_list[2]))

    def test_parsed_offer_info_dict_size(self,size=4):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of (4) [keys].
        """
        full_ayet_page = self.ayet_base_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        assert len(offer_dict) == size

    def test_dataframe_is_dataframe(self):
        """
        Tests if resultant dataframe is type dataframe.
        """
        full_ayet_page = self.ayet_base_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        offer_dataframe = pd.DataFrame(offer_dict)
        assert isinstance(offer_dataframe, pd.DataFrame)

    def test_values_in_multiple_rewards(self):
        """
        Tests if all values in multiple_rewards column are either 1 or 0
        """
        full_ayet_page = self.ayet_base_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        offer_dataframe = pd.DataFrame(offer_dict)
        indicator_values = offer_dataframe['multiple_rewards'].unique()
        assert len(indicator_values) == 2
        assert [0 and 1] in indicator_values

@pytest.mark.usefixtures("setup_main_user_ayet_page")
class TestMainUserAYET:
    """
    Main User Ayet Offerwall test suite
    """
    def test_parsed_completed_offer_info_is_dict(self):
        """
        Tests if output of function is an expected dictionary.
        """
        full_ayet_page = self.ayet_main_page
        completed_offer_dict = freecash_info.parse_completed_offer_info(full_ayet_page)
        assert isinstance(completed_offer_dict, dict)

    def test_parsed_completed_offer_info_dict_size(self,size=3):
        """
        Tests if resulting completed offer dictionary is the correct size.
        Should have length of (3) [keys].
        """
        full_ayet_page = self.ayet_main_page
        completed_offer_dict = freecash_info.parse_completed_offer_info(full_ayet_page)
        assert len(completed_offer_dict) == size

    def test_parsed_completed_offer_info_is_equal(self):
        """
        Tests if length of key:value pairs in comnpleted offer dict are
        the same size across all key:value lists.
        """
        full_ayet_page = self.ayet_main_page
        completed_offer_dict = freecash_info.parse_completed_offer_info(full_ayet_page)
        key_list = list(completed_offer_dict.keys())
        assert len(completed_offer_dict.get(key_list[0])) == \
                len(completed_offer_dict.get(key_list[1])) == \
                len(completed_offer_dict.get(key_list[2]))

    def test_completed_dataframe_is_dataframe(self):
        """
        Tests if resultant dataframe is type dataframe.
        """
        full_ayet_page = self.ayet_main_page
        completed_offer_dict = freecash_info.parse_completed_offer_info(full_ayet_page)
        completed_offer_dataframe = pd.DataFrame(completed_offer_dict)
        assert isinstance(completed_offer_dataframe, pd.DataFrame)

    def test_parsed_pending_offer_info_is_dict(self):
        """
        Tests if output of function is an expected dictionary.
        """
        full_ayet_page = self.ayet_main_page
        pending_offer_dict = freecash_info.parse_pending_offer_info(full_ayet_page)
        assert isinstance(pending_offer_dict, dict)

    def test_parsed_pending_offer_info_dict_size(self,size=3):
        """
        Tests if resulting pending offer dictionary is the correct size.
        Should have length of (3) [keys].
        """
        full_ayet_page = self.ayet_main_page
        pending_offer_dict = freecash_info.parse_pending_offer_info(full_ayet_page)
        assert len(pending_offer_dict) == size

    def test_parsed_pending_offer_info_is_equal(self):
        """
        Tests if length of key:value pairs in comnpleted offer dict are
        the same size across all key:value lists.
        """
        full_ayet_page = self.ayet_main_page
        pending_offer_dict = freecash_info.parse_pending_offer_info(full_ayet_page)
        key_list = list(pending_offer_dict.keys())
        assert len(pending_offer_dict.get(key_list[0])) == \
                len(pending_offer_dict.get(key_list[1])) == \
                len(pending_offer_dict.get(key_list[2]))

    def test_pending_dataframe_is_dataframe(self):
        """
        Tests if resultant dataframe is type dataframe.
        """
        full_ayet_page = self.ayet_main_page
        pending_offer_dict = freecash_info.parse_pending_offer_info(full_ayet_page)
        pending_offer_dataframe = pd.DataFrame(pending_offer_dict)
        assert isinstance(pending_offer_dataframe, pd.DataFrame)
