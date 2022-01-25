import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import timeit

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

@pytest.fixture(scope="class")
def webdriver_values():
    ayet = "https://www.ayetstudios.com/offers/web_offerwall/2693?external_identifier=fsid-2308045-607783a635"
    yield ayet

@pytest.fixture(scope="class")
def setup_driver():
    _driver = webdriver.Chrome(options=chrome_options,service_args=["--verbose", "--log-path=test-reports/chrome.log"])
    yield _driver
    _driver.close()

def test_webdriver_circle(setup_driver,webdriver_values):
    _driver.get(webdriver_values)
    html=_driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    assert (len(soup.getText())>1)
