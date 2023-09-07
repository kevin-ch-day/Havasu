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

    # read detected permission from text file
    def readDetectedPermissions(self):
        fPERMISSION_INPUT = open("INPUT\\APK_PERMISSIONS.txt", "r")
        buff = list()
        for p in fPERMISSION_INPUT:
            buff.append(p.strip())
        # for

        return buff
    # function

    # create scan record for trojan id
    def createPermissionRecord(self, trojan_id):
        sql = "INSERT INTO detected_standard_permissions (id) VALUES (%s)"
        val = (trojan_id, )
        self.cursor.execute(sql, val)
        self.connection.commit()
        print("Permission record created for " + trojan_id)
    # function



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

    # Read mitre data
    def readMitreData(self):
        FILE_PATH = "INPUT\\MITRE-INPUT.xlsx"
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

    def classifyPermissions(self, trojan, permissions):
        standardFormatPerms = list()
        unknownPermissions = list()
        unknownPermissionsFound = False

        for index in permissions:
            # check if permission matches the standard permission formatted
            if "android.permission." in index:
                print(index) # DEBUGGING
                standardFormatPerms.append(index)
            else:
                unknownPermissions.append(index)
                unknownPermissionsFound = True
            # if
        # for

        if unknownPermissionsFound:
            fUnknownPermissions = open("OUTPUT\\"+str(trojan)+"-UnknownPerms.txt", "w")
            try:
                for i in unknownPermissions:
                    #print(index) # DEBUGGING
                    fUnknownPermissions.write(i + "\n")
                # for
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                exit()
            # try
        # if

        print("Unknown Permissions found: ", len(unknownPermissions))

        recordAndroidPermissions(trojan, standardFormatPerms)
        print("\nStandard Permissions found: ", len(standardFormatPerms))
    # function

    # Standard Android Permissions
    def getStandardAndroidPermissionList(self):
        permissionList = list()

        self.cursor.execute("show columns from detected_standard_permissions")
        results = self.cursor.fetchall()
        if not results:
            print("[!!] - No permission columns retrieved from database.")
            exit()
        # if
        
        for i in results:
            if 'ID' == i[0]:
                pass
            else:
                permissionList.append(i[0])
        # for

        return permissionList
    # function

    # Record Android Permissions
    def recordAndroidPermissions(self, trojan, permissions):
        updatedColumns = 0
        unknownPermissions = list()
        standardPermissionList = getStandardAndroidPermissionList()
        FORMAT_HEADER = len("android.permission.")

        for index in permissions:
            slicedPermissions = index[FORMAT_HEADER:]

            if slicedPermissions not in standardPermissionList:
                print("Unknown Permission: " + index)
                unknownPermissions.append(slicedPermissions)
                #print(slicedPermissions) # DEBUGGING

            # if permission does not exists within table
            else:
                try:
                    sql = "UPDATE detected_standard_permissions SET "
                    sql = sql + slicedPermissions + " = 'X' WHERE id = " + str(trojan)
                    db_cursor.execute(sql)
                    db_connection.commit()
                    updatedColumns = updatedColumns + 1
                except mysql.connector.Error as err:
                    print("[!!] MySQL Error: {}".format(err))
                    exit()
                # try
            # if
        # for

        print("\n** Standard permission columns **")
        print(str(updatedColumns) + " columns updated.")
        recordNonStandardPermissions(trojan, unknownPermissions)
    # function

    def recordNonStandardPermissions(self, trojan, unknownPermissions):
        dbCols = list()
        addedCols = updatedCols = 0

        sql = "show columns from detected_unknown_permissions"
        db_cursor.execute(sql)
        dbResults = db_cursor.fetchall()
        if not dbResults:
            print("[!!] - No columns retrieved from: unknown_permissions")
            exit()
        # if

        for i in dbResults:
            if 'id' == i[0]:
                pass
            else:
                dbCols.append(i[0])
            # if
        # for
        #print(unknownPermissions) # DEBUGGING

        # Create record for APK in table
        sql = "INSERT INTO detected_unknown_permissions (id) VALUES (%s)"
        val = (trojan, )
        try:
            db_cursor.execute(sql, val)
            db_connection.commit()
        except mysql.connector.Error as err:
            print("[!!] MySQL Error: {}".format(err))
        # try

        print("\n** Detected unknown permissions columns **")
        for index in unknownPermissions:
            if index not in dbCols:

                # add new columns to table
                print("Adding new column: ", index) # DEBUGGING
                sql = "ALTER TABLE detected_unknown_permissions add " + index + " VARCHAR(1) NULL DEFAULT NULL"

                try:
                    db_cursor.execute(sql)
                    db_connection.commit()
                    addedCols = addedCols + 1
                except mysql.connector.Error as err:
                    print("[!!] MySQL Error: {}".format(err))
                # try
            # if

            # update column within permission record
            sql = "update detected_unknown_permissions set " + index + " = 'X' where id = " + str(trojan)
            try:
                db_cursor.execute(sql)
                db_connection.commit()
                updatedCols = updatedCols + 1
            except mysql.connector.Error as err:
                print("[!!] MySQL Error: {}".format(err))
            # try
        # for

        print(str(addedCols) + " columns added.")
        print(str(updatedCols) + " columns updated.\n")
    # function

    def outputStandardPermissions(self, sample_set):
        EXCEL_FILE = 'OUTPUT\\Android-Permissions.xlsx'
        
        sql = "select * from detected_standard_permissions "
        sql = sql + " where id in " + str(sample_set)
        sql = sql + " order by id"

        sql_query = pd.read_sql_query(sql, self.connection)
        df_alpha = pd.DataFrame(sql_query)
        df_beta = pd.DataFrame()

        df_beta['ID'] = df_alpha['ID']
        df_alpha = df_alpha.drop(columns=['ID'])

        for column in df_alpha:
            for cell in df_alpha[column]:
                if cell is not None:
                    df_beta[column] = df_alpha[column]
                    break
                # if
            # for
        # for

        df_beta.to_excel(EXCEL_FILE)
    # function

    def outputUnknownPermissions(self, sample_set):
        FILE_PATH = 'OUTPUT\\Unknown-Permissions.xlsx'

        sql = "select * from detected_unknown_permissions "
        sql = sql + " where id in " + sample_set
        sql = sql + " order by id"

        sql_query = pd.read_sql_query(sql, self.connection)
        df_alpha = pd.DataFrame(sql_query)
        df_beta = pd.DataFrame()

        df_beta['ID'] = df_alpha['ID']
        df_alpha = df_alpha.drop(columns=['ID'])

        for column in df_alpha:
            for cell in df_alpha[column]:
                if cell is not None:
                    df_beta[column] = df_alpha[column]
                    break
                # if
            # for
        # for

        df_beta.to_excel(FILE_PATH)
    # function

    ## NORMAL PERMISSIONS
    def outputNormalPermissions(self, sample_set):
        EXCEL_FILE = 'OUTPUT\\Normal-Permissions.xlsx'

        sql = "select name from android_permissions where Protection_level = 'Normal' order by name"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        normalPermissionsColumns = "'"
        buff = list()
        cnt = 0

        for x in results:    
            if(x[0] == "ID"):
                print(x[0])
            elif(cnt == (len(results)-1)):
                normalPermissionsColumns = normalPermissionsColumns + x[0] + "'"
                #print(cnt, x[0])
            else:
                normalPermissionsColumns = "'" + normalPermissionsColumns + x[0] + "', "
                #print(cnt, x[0])
            # if

            buff.append(x[0])
            cnt = cnt + 1
        # for

        ## ADD COLUMN CHECKING
        sql = "SHOW COLUMNS FROM detected_standard_permissions"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        detectedPermissions = list()
        for i in results:
            if(i[0] != "ID"):
                detectedPermissions.append(i[0])
            # if
        # for

        missingPermissions = list()
        for index in buff:
            if index not in detectedPermissions:
                missingPermissions.append(index.upper())
                #for p in detectedPermissions:
                    #if(index.upper() < p):
                    #target_index = (detectedPermissions.index(p) - 1)
                    #afterColumn = detectedPermissions[target_index]
                    #sql = "ALTER TABLE detected_standard_permissions ADD "
                    #sql = sql + index.upper() + " VARCHAR(1) NULL AFTER " + afterColumn
                    #print("\n" + sql + "\n")
                    #db_cursor.execute(sql)
                # for
            # if
        # for

        if missingPermissions:
            print("Missing Permissions: ")
            for i in missingPermissions:
                print(i)
            # for
            exit()
        # if

        sql = "select ID, " + normalPermissionsColumns
        sql = sql + " from detected_standard_permissions"
        sql = sql + " where ID in " + sample_set
        sql = sql + " order by ID"

        sql_query = pd.read_sql_query(sql, self.connection)
        df_alpha = pd.DataFrame(sql_query)
        df_beta = pd.DataFrame()

        df_beta['ID'] = df_alpha['ID']
        df_alpha = df_alpha.drop(columns=['ID'])

        for column in df_alpha:
            for cell in df_alpha[column]:
                if cell is not None:
                    print(column)
                    df_beta[column] = df_alpha[column]
                    break
                # if
            # for
        # for

        df_beta.to_excel(EXCEL_FILE)
    # function

    def generateMitreMatrix(self, sample_set):
        EXCEL_FILE = 'OUTPUT\\Mitre-Matrix.xlsx'
        
        sql = "select * from mitre_matrix "
        sql = sql + " where trojan_id in " + sample_set
        sql = sql + " order by trojan_id"

        df_raw = pd.read_sql_query(sql, self.connection)

        cols = df_raw.columns.tolist()
        cols.sort()
        cols.remove('trojan_id')

        df_beta = pd.DataFrame()
        df_beta['trojan_id'] = df_raw['trojan_id']
        df_alpha = df_raw.drop(columns=['trojan_id'])

        for column in cols:
            for cell in df_alpha[column]:
                if cell is not None:
                    df_beta[column] = df_alpha[column]
                break
                # if
            # for
        # for
        df_beta.to_excel(EXCEL_FILE)
    # function
# class