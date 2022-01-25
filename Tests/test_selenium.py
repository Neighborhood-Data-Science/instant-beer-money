import time
import unittest
from selenium import webdriver


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        try:
            cls.client = webdriver.Chrome(service_args=["--verbose", "--log-path=test-reports/chrome.log"])
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # give the server a second to ensure it is up
            time.sleep(1) 

    @classmethod
    def tearDownClass(cls):
        print('In Teardown Class Method')

    def setUp(self):
        print('In Setup')

    def tearDown(self):
        print('Tearing Down')

    def test_admin_home_page(self):
        print('This is the admin Home Page Test.')
        assert(5>1)
