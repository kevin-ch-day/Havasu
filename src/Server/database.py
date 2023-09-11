# database.py

import mysql.connector
import pandas as pd

connection = None
cursor = None

def createConnection():
    """ Connect to MySQL database """
    global connection
    global cursor

    SERVER = "localhost"
    USERNAME = "root"
    DATABASE = "capstone_dev"
    PASSWORD = ""
    PORT = 3306

    try:
        connection = mysql.connector.connect(
            host = SERVER,
            user = USERNAME,
            password = PASSWORD,
            database = DATABASE,
            port = PORT)

        if not connection.is_connected():
            print("Error: cannot connected to database.\n")
            exit()
        # if

        cursor = connection.cursor()

    except Exception as exp:
        print("[!!]- Error creating database connection")
        print(str(exp))
    # try
# function

def closeConnection():
    """ Disconnect from MySQL database """
    global connection

    try:
        connection.close()
    except Exception as exp:
        print("[!!] - Error ending database connection")
        print(str(exp))
    # try
# function

def queryData(sql):
    global cursor

    try:
        createConnection()
        cursor.execute(sql)
        results = cursor.fetchall()
        if not results:
            return None
        else:
            return results
    
    except mysql.connector.Error as err:
        print(err)
        return None
    
    finally:
        closeConnection()
    # try
# function

def executeSQL(sql, values = None):
    global cursor
    global connection

    try:
        createConnection()
        if not values:
            cursor.execute(sql)
        else:
            cursor.execute(sql, values)
        # if
    except mysql.connector.Error as err:
        print("[!!] MySQL Error: {}".format(err))
        return None
    
    finally:
        connection.commit()
        closeConnection()
    # try
# function

def pandasDataFrame(sql):
    global cursor
    global connection

    try:
        createConnection()

        results = pd.read_sql_query(sql, connection)
        records = pd.DataFrame(results)

        if not records:
            return None
        else:
            return records
    
    except mysql.connector.Error as err:
        print(err)
        return None
    
    finally:
        closeConnection()
    # try
# function
    