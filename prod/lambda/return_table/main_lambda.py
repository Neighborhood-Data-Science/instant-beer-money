"""
AWS Lambda Function for Retrieving Data from a MySQL Database

This Python module defines an AWS Lambda function designed to retrieve data from a MySQL database. 
The function is intended to be triggered via an HTTP request and returns a JSON object containing 
the data from the specified database table. 
It utilizes the 'mysql.connector' library to establish a connection to the database and execute SQL queries.

Functions:
    - establish_connection: Establishes a connection to the MySQL database using environment variables for credentials and configuration.
    - return_table: Queries the database for data based on the provided File System ID (FSID) and returns the results as a JSON object.
    - lambda_handler: The main entry point for the Lambda function, triggered by an HTTP request. It extracts the FSID from the request, connects to the database, retrieves the data, and returns it as a JSON response.

Dependencies:
    - Python 3.x
    - mysql.connector library
    - json library

Environment Variables (Required):
    - DB_HOST: Hostname or IP address of the MySQL database server.
    - DB_USER: MySQL database username for authentication.
    - DB_PASSWORD: Password for the MySQL database user.
    - DB_NAME: Name of the MySQL database.
    - DB_MAIN_TABLE: Name of the main database table used for data retrieval.

Note: This module should be configured as an AWS Lambda function, and the necessary environment variables must be set in the AWS Lambda console.
"""

import json
import os
import datetime
import sys
import mysql.connector
from mysql.connector import Error

# To handle datetime objects we need a Custom JSON encoder that handles datetime objects


class DateTimeEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder for Datetime Objects

    This class extends the 'json.JSONEncoder' class to provide custom serialization of Python
    'datetime.datetime' objects to ISO 8601 format when converting to JSON. It is intended to be
    used in conjunction with the 'json.dumps()' method to ensure datetime objects are serialized
    correctly in JSON format.

    Parameters
    ----------
    json.JSONEncoder : class
        The base JSON encoder class that DateTimeEncoder extends.

    Attributes
    ----------
    None

    Methods
    -------
    default(o)
        Overrides the 'default' method of the base class to provide custom serialization for
        datetime objects. If the provided object 'o' is a 'datetime.datetime' instance, it will
        be converted to ISO 8601 format. Otherwise, the base class's 'default' method is called.

    Example
    -------
    import json
    import datetime

    # Create an instance of DateTimeEncoder
    encoder = DateTimeEncoder()

    # Serialize a datetime object to JSON
    data = {'timestamp': datetime.datetime.now()}
    json_data = json.dumps(data, cls=encoder)

    See Also
    --------
    json.JSONEncoder : The base JSON encoder class that DateTimeEncoder extends.

    """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)


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


def return_table(fsid, database):
    """
    Function to insert data into the database.

    Parameters
    ----------
        database: `mysql.connector.connection_cext.CMySQLConnection` 
            A successfully connected database.

    Returns
    -------
        json_rows: `JSON object` 
            A json object containing the data from the database.
    """

    # Create a cursor object to execute SQL queries
    cursor = database.cursor()

    # Retrieve all information from the database
    # This is to be changed in future versions
    sql = f"""
    SELECT * 
    FROM {os.environ['DB_MAIN_TABLE']}
    WHERE hidden <> 1
    AND user_id = {fsid};
    """

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

    Parameters:
        event (dict): The event data passed to the Lambda function.
        context: (object): The runtime context object.

    Returns:
        dict: Dictionary containing the table from our database.
    """

    # Access the FSID from the event object
    if 'body' in event:
        body = event['body']
        if isinstance(body, str):
            body = json.loads(body)
        fsid = body.get('fsid')
    else:
        sys.exit()  # End the process if no fsid is provided.

    # Connect to the database
    database_conn = establish_connection()
    table_dump = return_table(fsid, database_conn)
    return {
        "body": table_dump
    }
