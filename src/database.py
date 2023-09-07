import mysql.connector

def startConnection(self):
    """ Connect to MySQL database """
    try:
        SERVER = "localhost"
        USER_NAME = "root"
        DATABASE_NAME = "cyberops_capstone_android"
        PORT_NUMBER = 3306

        connection = mysql.connector.connect(
            host = SERVER,
            user = USER_NAME,
            #password="",
            database = DATABASE_NAME,
            port = PORT_NUMBER)

        if not connection.is_connected():
            print("Cannot connected to data.\n")
            exit()
        # if

        cursor = connection.cursor()
        return cursor, connection

    except Exception as e:
        print("[!!]- Error start database connection.\n")
        print(str(e))
    # try
# function

def endConnection(self):
    """ disconnect to MySQL database """
    try:
        self.connection.close()
    except Exception as e:
        print("[!!] - Error ending database connection.\n")
        print(str(e))
    # try
# function