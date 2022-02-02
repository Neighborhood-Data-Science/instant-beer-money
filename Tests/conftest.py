"""
Offical PyTest Fixture .py file.
This file will hold all fixtures that are needed in
any test across the application.

"""
import pytest
import sys
sys.path.append('./Functions')
import freecash_info

@pytest.fixture(scope="class",autouse=True)
def setup_raw_ayet_page(request):
    """
    Set Ayet page as fixture using baseline ayet offerwall
    """
    offerwall_version = 'MASTER_AYET'
    ayet_base_page = freecash_info.start_driver_and_open_ayet(offerwall_version)
    ayet_base_page.maximize_window()
    yield ayet_base_page
    ayet_base_page.close()

@pytest.fixture(scope="class",autouse=True)
def setup_main_user_ayet_page(request):
    """
    Set Ayet page as fixture using main user ayet offerwall
    """
    offerwall_version = 'AYET'
    ayet_main_page = freecash_info.start_driver_and_open_ayet(offerwall_version)
    ayet_main_page.maximize_window()
    yield ayet_main_page
    ayet_main_page.close()
