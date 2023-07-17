import os
import json
import mysql.connector
from mysql.connector import Error


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


def update_table(rowId, database):
    """
    Function to update the 'hidden' value for a particular row in the database.

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
    sql = f"""
    UPDATE {os.environ['DB_MAIN_TABLE']}
    SET hidden = 1
    WHERE ID = {rowId};
    """

    # Execute the SQL query
    cursor.execute(sql)

    # Save changes to the database
    database.commit()
    # Close the cursor and the connection
    cursor.close()
    database.close()

    return 'SUCCESS'


def lambda_handler(event, context):
    """
    The main execution step of the AWS Lambda function.
    """
    # Access the rowId from the event object
    if 'body' in event:
        body = event['body']
        if isinstance(body, str):
            body = json.loads(body)
        rowId = body.get('rowId')
    else:
        rowId = None  # Set a default value or handle the case when rowId is not present

    # Rest of your code
    database_conn = establish_connection()
    table_action = update_table(rowId, database_conn)
    return table_action

