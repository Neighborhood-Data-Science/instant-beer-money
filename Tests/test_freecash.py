"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import freecash_info
import pytest
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
#Load environment variables
#load_dotenv()
#The above line should remain commented out unless 
#conducting LOCAL TESTING

@pytest.fixture(scope="class",autouse=True)
def setup_ayet_page(request):
    """
    Set Ayet page as fixture
    """
    ayet_page = freecash_info.set_driver_and_scrape_ayet()
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

    def test_get_offerwall_content(self):
        """
        Tests if able to successfully get content from the Ayet Offerwall
        """
        full_ayet_page = self.ayet_page
        get_offers = freecash_info.get_current_ayet_offers(full_ayet_page)
        assert len(get_offers.text) > 100

    def test_parse_offer_titles(self):
        """
        Tests if able to successfully parse titles from the offerwall text
        """
        full_ayet_page = self.ayet_page
        get_offers = freecash_info.get_current_ayet_offers(full_ayet_page)
        offer_titles = freecash_info.parse_offer_titles(get_offers)
        assert len(offer_titles) > 0
