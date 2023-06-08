"""
Main Testing Framework to confirm database connectivity and operation.
"""

import os
import pytest
import mysql.connector
from dotenv import load_dotenv

class TestDB:
    """
    Test suite for our mySQL Database.

    This test suite is designed to test the connectivity, functionality, and operation
    of our mySQL database hosted on Amazon.
    """

    def test_db_connection(self):
        """
        Test that we are able to connect to the database.
        """
        connection = mysql.connector.connect(host=os.environ['DB_HOST'],
                                            user=os.environ['DB_USER'],
                                            password=os.environ['DB_PASSWORD'])
        assert connection.is_connected()
        connection.close()
