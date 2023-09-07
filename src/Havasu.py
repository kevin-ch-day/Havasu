# havasu.py

import database
import pandas as pd
import openpyxl as xl

# Havasu class definition
class Havasu:

    __version__ = "1.0.0"
    connection = None
    cursor = None

    def __init__(self):
        # start database connection
        self.cursor, self.connection = database.startConnection(self)
        #print(self.connection) # DEBUGGING
        #print(self.cursor) # DEBUGGING
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
            print("MD5 hash match found")
            self.displayMalwareRecord(results[0])
            return
        # if

        sql = "select * from malware_samples where sha1 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("SHA1 hash match found")
            self.displayMalwareRecord(results)
            return
        # if

        sql = "select * from malware_samples where sha256 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("SHA256 hash match found")
            self.displayMalwareRecord(results)
            return
        # if

        if not hashFound:
            print("No hash record found.")
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

def readMitreData(self):
    FILE_PATH = "MITRE-INPUT.xlsx"
    wb = xl.load_workbook(FILE_PATH)

    for i in wb.sheetnames:
        print("Worksheet: ", i)
        values = list()
        df = pd.read_excel(FILE_PATH, sheet_name = i)

        sql = "INSERT INTO mitre_detection"
        sql = sql + " (Trojan_ID, ATTACK_ID, Tactic, Description, Malicious_Indicators, "
        sql = sql + "Suspicious_Indicators, Informative_Indicators)"
        sql = sql + " VALUES (%s, %s, %s, %s, %s, %s, %s)"

        for index, row in df.iterrows():
            trojan_id = row[0]
            attack_id = row[1]
            technique = row[2]
            tactic = row[3]
            mali = row[4]
            susp = row[5]
            info = row[6]

            data = (trojan_id, attack_id, technique, tactic, mali, susp, info)
            print(data) # DEGUGGING
            values.append(data)

            self.cursor.execute(sql, data)

            #print(cursor.rowcount, "record inserted.")
        # for

        self.connection.commit()
        print() # newline
    # for
# function