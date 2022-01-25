import pytest
from selenium import webdriver
from bs4 import BeautifulSoup
import timeit

@pytest.fixture(scope="class")
def webdriver_values():
    ayet = "https://www.ayetstudios.com/offers/web_offerwall/2693?external_identifier=fsid-2308045-607783a635"
    yield ayet

@pytest.fixture(scope="class")
def setup_driver():
    _driver = webdriver.Chrome()
    yield _driver
    _driver.close()

def test_webdriver_circle(setup_driver,webdriver_values):
    _driver.get(webdriver_values)
    html=_driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    assert (len(soup.getText())>1)
