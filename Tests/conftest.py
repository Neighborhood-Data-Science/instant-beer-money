"""
Offical PyTest Fixture .py file.
This file will hold all fixtures that are needed in
any test across the application.

"""
import os
import pytest
import pandas as pd
import mysql.connector
import ayet_info
import adgem_info
import offertoro_info
import revu_info


@pytest.fixture(scope="class", autouse=False)
def setup_ayet_page(request):
    """
    Set Ayet page as fixture. 
    """
    offerwall_version = 'AYET'
    ayet_main_page = ayet_info.start_driver_and_open_ayet(offerwall_version)
    ayet_main_page.maximize_window()
    yield ayet_main_page
    ayet_main_page.close()


@pytest.fixture(scope="class", autouse=False)
def setup_adgem_page(request):
    """
    Set Adgem page as fixture. 
    """
    offerwall_version = 'ADGEM'
    adgem_main_page = adgem_info.start_driver_and_open_adgem(offerwall_version)
    adgem_main_page.maximize_window()
    yield adgem_main_page
    adgem_main_page.close()


@pytest.fixture(scope="class", autouse=False)
def setup_toro_page(request):
    """
    Set OfferToro page as fixture.
    """
    offerwall_version = 'TORO'
    toro_main_page = offertoro_info.start_driver_and_open_offertoro(
        offerwall_version)
    toro_main_page.maximize_window()
    yield toro_main_page
    toro_main_page.close()


@pytest.fixture(scope="class", autouse=False)
def setup_revu_page(request):
    """
    Set Revenue Univerise page as fixture.
    """
    offerwall_version = 'REVU'
    revu_main_page = revu_info.start_driver_and_open_revu(offerwall_version)
    revu_main_page.maximize_window()
    yield revu_main_page
    revu_main_page.close()


@pytest.fixture(scope="function", autouse=False)
def qa_ayet(request):
    """
    Set mock Ayet data as fixture. 
    """
    data = {
        'offerLow': ['10', '20', '30'],
        'offerHigh': [None, '50', '60'],
        'offer_name': ['Offer 1', 'Offer 2', 'Offer 3'],
        'offer_description': ['Multiple rewards', 'Description 2', 'Multiple rewards'],
        'Additional': ['Additional 1', None, 'Additional 2'],
        'Difficulty': ['Easy', None, 'Medium'],
        'Ignore3': [None, None, 'Value']
    }

    ayet_frame = pd.DataFrame(data)
    return ayet_frame


@pytest.fixture(scope="function", autouse=False)
def qa_adgem(request):
    """
    Set mock Adgem data as fixture. 
    """
    data = {
        'offer_title': ['Hidden Objects', 'Video Poker Classic', 'Smash Party'],
        'offer_description': ['Complete Level 31 to Earn!', 'Complete Multiple Goals to Earn!',
                              'Complete Multiple Goals to Earn!'],
        'offer_amount': ['683', 'Up To\n11,250', 'Up To\n13,247'],
        'offer_device': ['Apple', 'Android', 'Android']
    }

    adgem_frame = pd.DataFrame(data)
    return adgem_frame


@pytest.fixture(scope="function", autouse=False)
def qa_revu(request):
    """
    Set mock Revenue Universe data as fixture. 
    """
    data = {
        'offer_title': ['Title 1', 'Title 2', 'Title 3'],
        'offer_amount': ['255', '8,250', '165']
    }

    revu_frame = pd.DataFrame(data)
    return revu_frame


@pytest.fixture(scope="function", autouse=False)
def qa_toro(request):
    """
    Set mock Offertoro data as fixture. 
    """
    data = {
        'offer_title': ['\nTitle 1 - Source\nDescription 1', '\nTitle 2 - Source\nDescription 2'],
        'offer_device': ['android phone', 'iphone/ipad']
    }

    toro_frame = pd.DataFrame(data)
    return toro_frame


@pytest.fixture(scope="function", autouse=False)
def main_db_mock(request):
    """
    Set mock dataframe data for testing main_db_push
    """
    data = {
        'offer_title': ['Title 1', 'Title 2', 'Title 3'],
        'offer_device': ['Device 1', 'Device 2', 'Device 3']
    }

    mock_frame = pd.DataFrame(data)
    return mock_frame


@pytest.fixture(scope="module", autouse=False)
def db_connection():
    """
    Set connection to database for testing purposes
    """
    database_conn = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )
    yield database_conn
    # Close connection after the test
    database_conn.close()


@pytest.fixture(scope="module", autouse=False)
def db_table(db_connection):  # pylint: disable=W0621
    """
    Set up table for testing purposes
    """
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TEST_TABLE (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL DEFAULT 'MASTER',
            offer_title TEXT NOT NULL,
            offer_device CHAR(25) DEFAULT 'MASTER'
            )
    """)
    cursor.close()
    yield
    # Drop table after the test
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS TEST_TABLE")
    cursor.close()
