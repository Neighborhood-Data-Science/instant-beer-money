"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import freecash_info
import pytest
import os
from dotenv import load_dotenv
#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.fixture(scope="class",autouse=True)
def setup_ayet_page(request):
    """
    Set Ayet page as fixture
    """
    ayet_page = freecash_info.start_driver_and_open_ayet()
    request.cls.ayet_page = ayet_page
    yield ayet_page
    ayet_page.close()

@pytest.mark.usefixtures("setup_ayet_page")
class TestAYET:
    """
    Full Ayet test suite
    """
    def test_access_ayet_offerwall(self):
        """
        Tests if able to successfully open Ayet Offerwall
        """
        full_ayet_page = self.ayet_page
        assert full_ayet_page.current_url == os.environ['AYET']

    def test_parsed_offer_info_is_dict(self):
        """
        Tests if output of function is an expected dictionary.
        """
        full_ayet_page = self.ayet_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        assert isinstance(offer_dict, dict)

    def test_parsed_offer_info_is_equal(self):
        """
        Tests if length of key:value pairs in offer dict are
        the same size across all key:value lists.
        """
        full_ayet_page = self.ayet_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        key_list = list(offer_dict.keys())
        assert len(offer_dict.get(key_list[0])) == \
            len(offer_dict.get(key_list[1])) == len(offer_dict.get(key_list[2]))

    def test_parsed_offer_info_dict_size(self,size=4):
        """
        Tests if resulting offer dictionary is the correct size.
        Should have length of (4) [keys].
        """
        full_ayet_page = self.ayet_page
        offer_dict = freecash_info.parse_offer_information(full_ayet_page)
        assert len(offer_dict) == size

    def test_values_in_multiple_rewards(self):
        """
        Tests if all values in multiple_rewards column are either 1 or 0
        """

