import database
import pandas as pd

class Havasu:

    __version__ = "1.0.0"
    connection = None
    cursor = None

    def __init__(self):
        # start database connection
        self.cursor, self.connection = database.startConnection(self)
        #print(self.connection)
        #print(self.cursor)
    # construction

    def __del__(self):
        # end database connection
        database.endConnection(self)
    # destructor
    
    # Display application version number
    def versionNumber(self):
        return self.__version__
    # function

    # check database
    def checkDatabaseConfig(self):
        if not database.checkDatabaseConfig(self):
            print("Error - Database is not configured")
            exit(-1)
        # if
    # function

    # Check hash
    def checkHash(self, hash):
        hashFound = False
        
        sql = "select * from malware_samples where md5 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("MD5 match found")
            self.displayMalwareRecord(results[0])
            return
        # if

        sql = "select * from malware_samples where sha1 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("SHA1 match found")
            self.displayMalwareRecord(results)
            return
        # if

        sql = "select * from malware_samples where sha256 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("SHA256 match found")
            self.displayMalwareRecord(results)
            return
        # if

        if not hashFound:
            print("No record found.")
        # if
    # checkHash()

    # Display malware record
    def displayMalwareRecord(self, record):
        print("ID:\t\t" + str(record[0]))
        print("Name:\t\t" + record[1])
        print("Family:\t\t" + record[2])
        print("Size:\t\t" + record[12])
        print("VirusTotal:\t" + record[4])
    # function

    # Generate sample data by ids to .xlsx file
    def outputMalwareRecordsById(self, ids):
        FILE_PATH = "OUTPUT\\Output-Excel.xlsx"
        sql = "SELECT * FROM mobfs_analysis WHERE id in " + ids
        df = pd.read_sql_query(sql, self.cursor)
        df.to_excel(FILE_PATH)
    # function

    # Generate sample data by family to .xlsx file
    def outputMalwareRecordsByFamily(self, family):
        FILE_PATH = "OUTPUT\\Output-Excel.xlsx"
        sql = "SELECT * FROM malware_samples WHERE family = '" + family + "'"        
        df = pd.read_sql_query(sql, self.cursor)
        df.to_excel(FILE_PATH)
    # function
# class