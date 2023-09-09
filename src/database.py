# database.py
import mysql.connector

connection = None
cursor = None

def start():
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
            print("Cannot connected to data.\n")
            exit()
        # if

        cursor = connection.cursor()

    except Exception as exp:
        print("[!!]- Error start database connection")
        print(str(exp))
    # try
# function

def close():
    """ disconnect to MySQL database """
    global connection

    try:
        connection.close()
    except Exception as exp:
        print("[!!] - Error ending database connection")
        print(str(exp))
    # try
# function