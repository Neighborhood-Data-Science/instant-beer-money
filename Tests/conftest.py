"""
Offical PyTest Fixture .py file.
This file will hold all fixtures that are needed in
any test across the application.

"""
import pytest
import sys
sys.path.append('./Functions')
import ayet_info
import adgem_info
import offertoro_info
import revu_info

@pytest.fixture(scope="class",autouse=False)
def setup_raw_ayet_page(request):
    """
    Set Ayet page as fixture using baseline ayet offerwall
    """
    offerwall_version = 'MASTER_AYET'
    ayet_base_page = ayet_info.start_driver_and_open_ayet(offerwall_version)
    ayet_base_page.maximize_window()
    yield ayet_base_page
    ayet_base_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_main_user_ayet_page(request):
    """
    Set Ayet page as fixture using main user adgem offerwall
    """
    offerwall_version = 'AYET'
    ayet_main_page = ayet_info.start_driver_and_open_ayet(offerwall_version)
    ayet_main_page.maximize_window()
    yield ayet_main_page
    ayet_main_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_raw_adgem_page(request):
    """
    Set Adgem page as fixture using baseline adgem offerwall
    """
    offerwall_version = 'MASTER_ADGEM'
    adgem_base_page = adgem_info.start_driver_and_open_adgem(offerwall_version)
    adgem_base_page.maximize_window()
    yield adgem_base_page
    adgem_base_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_main_user_adgem_page(request):
    """
    Set Adgem page as fixture using main user adgem offerwall
    """
    offerwall_version = 'ADGEM'
    adgem_main_page = adgem_info.start_driver_and_open_adgem(offerwall_version)
    adgem_main_page.maximize_window()
    yield adgem_main_page
    adgem_main_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_raw_toro_page(request):
    """
    Set OfferToro page as fixture using baseline Offertoro offerwall
    """
    offerwall_version = 'MASTER_TORO'
    toro_base_page = offertoro_info.start_driver_and_open_offertoro(offerwall_version)
    toro_base_page.maximize_window()
    yield toro_base_page
    toro_base_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_main_user_toro_page(request):
    """
    Set OfferToro page as fixture using main user OfferToro offerwall
    """
    offerwall_version = 'TORO'
    toro_main_page = offertoro_info.start_driver_and_open_offertoro(offerwall_version)
    toro_main_page.maximize_window()
    yield toro_main_page
    toro_main_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_raw_revu_page(request):
    """
    Set OfferToro page as fixture using baseline Offerrevu offerwall
    """
    offerwall_version = 'MASTER_REVU'
    revu_base_page = revu_info.start_driver_and_open_revu(offerwall_version)
    revu_base_page.maximize_window()
    yield revu_base_page
    revu_base_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_main_user_revu_page(request):
    """
    Set OfferToro page as fixture using main user OfferToro offerwall
    """
    offerwall_version = 'REVU'
    revu_main_page = revu_info.start_driver_and_open_revu(offerwall_version)
    revu_main_page.maximize_window()
    yield revu_main_page
    revu_main_page.close()