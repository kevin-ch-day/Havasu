import mysql.connector

# Start database connection
def startConnection(self):
    """ Connect to MySQL database """
    try:
        SERVER = "localhost"
        USER_NAME = "root"
        #DATABASE_NAME = "capstone_prod"
        DATABASE_NAME = "capstone_dev"
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

    except Exception as exp:
        print("[!!]- Error start database connection.\n")
        print(str(exp))
    # try
# function

# End database connection
def endConnection(self):
    """ disconnect to MySQL database """
    try:
        self.connection.close()
    except Exception as exp:
        print("[!!] - Error ending database connection.\n")
        print(str(exp))
    # try
# function

# Check database configuration
def checkDatabaseConfig(self):
    pass
# function