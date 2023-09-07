# database.py
import mysql.connector

# Start database connection
def startConnection(self):
    """ Connect to MySQL database """
    try:
        SERVER = "localhost"

        # Username selection
        #USER_NAME = "WebAdmin"
        USER_NAME = "root"

        # Database selection
        #DATABASE_NAME = "capstone_prod"
        DATABASE_NAME = "capstone_dev"

        # Password selection
        #PASSWORD = "Passwor01"
        PASSWORD = ""

        PORT_NUMBER = 3306

        connection = mysql.connector.connect(
            host = SERVER,
            user = USER_NAME,
            password = PASSWORD,
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

    # check for android_permissions table
    
    # check for banking_samples
    
    # check for detected_standard_permissions
    
    # check for detected_unknown_permissions
    
    # check for malware_samples
    
    # check for mitre_detection
    
    # check for mitre_matrix
    
    # check for mobfs_analysis

    pass
# function