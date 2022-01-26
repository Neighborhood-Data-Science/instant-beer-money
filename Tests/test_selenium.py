"""
Main Web Testing Framework
"""
import sys
sys.path.append('./Functions')

import freecash_info

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


@pytest.fixture(scope="class")
def webdriver_values():
    """
    Test Doc Info
    """
    ayet = "https://www.ayetstudios.com/offers/web_offerwall/2693?external_identifier=fsid-2308045-607783a635"
    yield ayet

@pytest.fixture(scope="class")
def setup_driver():
    """
    Test Doc Info
    """
    _driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    yield _driver
    _driver.close()

def test_driver_setting():
    """
    Test whether driver set up was successful
    """
    test_driver = freecash_info.set_driver()
    assert isinstance(test_driver,webdriver.chrome.webdriver.WebDriver)

def test_access_ayet_offerwall(setup_driver,webdriver_values):
    """
    Tests if able to successfully open Ayet Offerwall
    """
    setup_driver.get(webdriver_values)
    html= setup_driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    assert len(soup.getText())>1
