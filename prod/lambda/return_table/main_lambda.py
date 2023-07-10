import json
import os
import datetime
import mysql.connector
from mysql.connector import Error

# To handle datetime objects we need a Custom JSON encoder that handles datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


def establish_connection():
    """
    Function to establish a connection to the database.

    Parameters
    ----------
    None

    Returns
    -------
        database_conn: `mysql.connector.connection_cext.CMySQLConnection` 
            A connection to the database.
    """

    try:
        database_conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME']
        )
        return database_conn
    except Error as process_error:
        print(process_error)


def return_table(database):
    """
    Function to insert data into the database.

    Parameters
    ----------
        database: `mysql.connector.connection_cext.CMySQLConnection` 
            A successfully connected database.

    Returns
    -------
        table_dump: `JSON object` 
            A json object containing the data from the database.
    """

    # Create a cursor object to execute SQL queries
    cursor = database.cursor()

    # Retrieve all information from the database
    # This is to be changed in future versions
    sql = f"SELECT * FROM {os.environ['DB_MAIN_TABLE']};"

    # Execute the SQL query
    cursor.execute(sql)

    # Return the results of the query
    rows = cursor.fetchall()

    # Turn the results into a JSON object using a custom JSON encoder for datetime objects
    json_rows = json.dumps(rows, cls=DateTimeEncoder)
    
    # Close the cursor and the connection
    cursor.close()
    database.close()

    return json_rows


def lambda_handler(event=None, context=None):
    """
    The main execution step of the AWS Lambda function.
    """
    database_conn = establish_connection()
    table_dump = return_table(database_conn)
    return {
        "body": table_dump
    }