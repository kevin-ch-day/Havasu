# database.py

import mysql.connector as mysql
import pandas as pd

# GLOBALS
connection = None
cursor = None

# create database connection
def createConnection():
    """ Connect to MySQL database """
    global connection
    global cursor

    # configuration
    SERVER = "localhost"
    USERNAME = "root"
    DATABASE = "havasu_dev"
    PASSWORD = ""
    PORT = 3306

    try:
        connection = mysql.connect(
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

# close database connection
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

# query sql statement
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
    
    except mysql.Error as err:
        print(err)
        return None
    
    finally:
        closeConnection()
    # try
# function

# execute SQL statement
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
    except mysql.Error as err:
        print("[!!] MySQL Error: {}".format(err))
        return None
    
    finally:
        connection.commit()
        closeConnection()
    # try
# function

# execute SQL statement
def executeSQLMany(sql, values):
    global cursor
    global connection

    try:
        createConnection()
        cursor.executemany(sql, values)
        
    except mysql.Error as err:
        print("[!!] MySQL Error: {}".format(err))
        return None
    
    finally:
        connection.commit()
        closeConnection()
    # try
# function

def getDataFrame(sql):
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
    
    except mysql.Error as err:
        print(err)
        return None
    
    finally:
        closeConnection()
    # try
# function

# Pandas read SQL query
def pandasReadSQL(sql):
    global cursor
    global connection

    try:
        createConnection()
        results = pd.read_sql_query(sql, connection)

        if not results:
            return None
        else:
            return results
    
    except mysql.Error as err:
        print(err)
        return None
    
    finally:
        closeConnection()
    # try
# function