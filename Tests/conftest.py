"""
Offical PyTest Fixture .py file.
This file will hold all fixtures that are needed in
any test across the application.

"""
import pytest
import pandas as pd # type: ignore # Pylance(reportMissingImports)
import sys
sys.path.append('./Functions')
import ayet_info # type: ignore # Pylance(reportMissingImports)
import adgem_info # type: ignore # Pylance(reportMissingImports)
import offertoro_info # type: ignore # Pylance(reportMissingImports)
import revu_info # type: ignore # Pylance(reportMissingImports)
import offer_cleanup # type: ignore # Pylance(reportMissingImports)

@pytest.fixture(scope="class",autouse=False)
def setup_ayet_page(request):
    """
    Set Ayet page as fixture. 
    """
    offerwall_version = 'AYET'
    ayet_main_page = ayet_info.start_driver_and_open_ayet(offerwall_version)
    ayet_main_page.maximize_window()
    yield ayet_main_page
    ayet_main_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_adgem_page(request):
    """
    Set Adgem page as fixture. 
    """
    offerwall_version = 'ADGEM'
    adgem_main_page = adgem_info.start_driver_and_open_adgem(offerwall_version)
    adgem_main_page.maximize_window()
    yield adgem_main_page
    adgem_main_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_toro_page(request):
    """
    Set OfferToro page as fixture.
    """
    offerwall_version = 'TORO'
    toro_main_page = offertoro_info.start_driver_and_open_offertoro(offerwall_version)
    toro_main_page.maximize_window()
    yield toro_main_page
    toro_main_page.close()

@pytest.fixture(scope="class",autouse=False)
def setup_revu_page(request):
    """
    Set Revenue Univerise page as fixture.
    """
    offerwall_version = 'REVU'
    revu_main_page = revu_info.start_driver_and_open_revu(offerwall_version)
    revu_main_page.maximize_window()
    yield revu_main_page
    revu_main_page.close()

@pytest.fixture(scope="class",autouse=False)
def qa_ayet(request):
    """
    Set Ayet page as fixture. 
    """
    data = {
    'offerLow': ['10', '20', '30'],
    'offerHigh': [None, '50', '60'],
    'Name': ['Offer 1', 'Offer 2', 'Offer 3'],
    'Description': ['Multiple rewards', 'Description 2', 'Multiple rewards'],
    'Additional': ['Additional 1', None, 'Additional 2'],
    'Difficulty': ['Easy', None, 'Medium'],
    'Ignore3': [None, None, 'Value']
    }

    data_frame = pd.DataFrame(data)
    cleaned_frame = offer_cleanup.clean_ayet(data_frame)
    return cleaned_frame
