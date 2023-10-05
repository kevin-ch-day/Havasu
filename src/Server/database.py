# database.py

import mysql.connector as mysql
import pandas as pd

connection = None
cursor = None


# create database connection
def create_connection():
    """ Connect to MySQL database """
    global connection
    global cursor

    # configuration
    server = "localhost"
    uname = "root"
    database = "havasu_dev"
    passwd = ""
    port = 3306

    try:
        connection = mysql.connect(
            host=server,
            user=uname,
            password=passwd,
            database=database,
            port=port)

        if not connection.is_connected():
            print("Error: cannot connected to database.\n")
            exit()

        cursor = connection.cursor()

    except Exception as exp:
        print("[!!]- Error creating database connection")
        print(str(exp))

# close database connection
def close_connection():
    """ Disconnect from MySQL database """
    global connection

    try:
        connection.close()
    except Exception as exp:
        print("[!!] - Error ending database connection")
        print(str(exp))

# query sql statement
def query_data(sql):
    global cursor

    try:
        create_connection()
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
        close_connection()

# execute SQL statement
def executeSQL(sql, values=None):
    global cursor
    global connection

    try:
        create_connection()
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
        close_connection()

# execute SQL statement
def executeSQLMany(sql, values):
    global cursor
    global connection

    try:
        create_connection()
        cursor.executemany(sql, values)

    except mysql.Error as err:
        print("[!!] MySQL Error: {}".format(err))
        return None

    finally:
        connection.commit()
        close_connection()

def generate_dataframe(sql):
    global cursor
    global connection

    try:
        create_connection()
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
        close_connection()

# Pandas read SQL query
def pandasReadSqlQuery(sql):
    global cursor
    global connection

    try:
        create_connection()
        results = pd.read_sql_query(sql, connection)

        if not results:
            return None
        else:
            return results

    except mysql.Error as err:
        print(err)
        return None

    finally:
        close_connection()
