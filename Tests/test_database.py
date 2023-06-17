"""
Main Testing Framework to confirm database connectivity and operation.
"""

import os
import pytest
import sys
sys.path.append('./Main')
import main_db_push


@pytest.mark.usefixtures("main_db_mock", "db_connection", "db_table")
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
        connection = main_db_push.establish_connection()
        assert connection.is_connected()
        connection.close()

    def test_get_offerwall_data(self):
        """
        Test that we are able to retrieve data from the offerwalls
        """
        offer_data = main_db_push.get_offerwall_data()
        assert isinstance(offer_data, list)
        assert len(offer_data) > 0

    def test_insert_data(self, main_db_mock, db_connection):
        """
        Test that we are able to insert data into the database.
        """

        # Create sample DataFrames for testing
        dataframe_list = [main_db_mock, main_db_mock]

        # Set cursor
        cursor = db_connection.cursor()

        for dataframe in dataframe_list:
            # Collect the column names from the dataframe.
            query_cols = ', '.join(dataframe.columns)
            # Calculate the proper number of %s placeholders for each column in the dataframe.
            value_len = ', '.join(['%s'] * len(dataframe.columns))
            # Query to insert the data into the database
            insert_query = f"INSERT INTO {os.environ['DB_TEST_TABLE']}\
                 ({query_cols}) VALUES ({value_len})"
            # Get the values from the DataFrame as a list of tuples
            values = [tuple(row) for row in dataframe.values]
            # Execute the INSERT statement with multiple rows
            cursor.executemany(insert_query, values)
            # Commit the changes to the database
            db_connection.commit()

        # Check validity of the database
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        assert os.environ['DB_TEST_TABLE'] in tables

        cursor.execute(f"SELECT * FROM {os.environ['DB_TEST_TABLE']}")
        rows = cursor.fetchall()
        assert len(rows) > 0
        # Close the cursor
        cursor.close()
