# havasu.py

import database
import pandas as pd
import openpyxl as xl
import mysql.connector
import os
import datetime
import zipfile

# Havasu class definition
class Havasu:

    __version__ = "1.0.1" # version number
    connection = None # database connection
    cursor = None # database cursor

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

    # Classify detected permissions
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
        Havasu.recordAndroidPermissions(trojan, standardFormatPerms)
        print("\nStandard Permissions found: ", len(standardFormatPerms))
    # function

    # Record Android Permissions
    def recordAndroidPermissions(self, trojan, permissions):
        updatedColumns = 0
        unknownPermissions = list()
        standardPermissionList = Havasu.getStandardAndroidPermissionList()
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
                    self.cursor.execute(sql)
                    self.connection.commit()
                    updatedColumns = updatedColumns + 1
                except mysql.connector.Error as err:
                    print("[!!] MySQL Error: {}".format(err))
                    exit()
                # try
            # if
        # for

        print("\n** Standard permission columns **")
        print(str(updatedColumns) + " columns updated.")
        Havasu.recordNonStandardPermissions(trojan, unknownPermissions)
    # function

    def recordNonStandardPermissions(self, trojan, unknownPermissions):
        dbCols = list()
        addedCols = updatedCols = 0

        sql = "show columns from detected_unknown_permissions"
        self.cursor.execute(sql)
        dbResults = self.cursor.fetchall()
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
            self.cursor.execute(sql, val)
            self.connection.commit()
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
                    self.cursor.execute(sql)
                    self.connection.commit()
                    addedCols = addedCols + 1
                except mysql.connector.Error as err:
                    print("[!!] MySQL Error: {}".format(err))
                # try
            # if

            # update column within permission record
            sql = "update detected_unknown_permissions set " + index + " = 'X' where id = " + str(trojan)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
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

    # APK Tool
    def decompileAPK(apk_arg):
        os.system("apktool d " + apk_arg)
    # function

    # DEX2JAR Tool
    def generateJAR(apk_arg):
        os.system("d2j-dex2jar " + apk_arg)
    # function 

    def scanManifest(manifest_path):
        manifestCopy = None
        
        try:
            manifest = open(manifest_path, "r")
            manifestCopy = manifest.readlines() # copy manifest
            manifest.close()
            
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()
        # try
        
        return manifestCopy  
    # function

    def getManifestPermissions(androidManifest):
        standardPermissions = list()
        unknownPermissions = list()
        signaturePermissions = list()
        temp_string = ""

        for index in androidManifest:
            if "uses-permission" in index:
                startPos = index.find("android:name=")
                offset = len("android:name=")+1
                temp_string = index[startPos+offset:-4]

                if "permission " in temp_string:
                    temp = len("permission android.permission.")
                    temp_string = temp_string[temp:]
                    standardPermissions.append(temp_string)
                                    
                elif "com." in temp_string:
                    unknownPermissions.append(temp_string)
                                    
                else:
                    temp = len("android.permission.")
                    temp_string = temp_string[temp:]
                    standardPermissions.append(temp_string)
                # if
            # if
        # for
        
        standardPermissions.sort()
        unknownPermissions.sort()
        return standardPermissions, unknownPermissions
    # function

    def getPermissions(manifest):
        detectedPermissions = list()
        unknownPermissionFormat = False
        unknownExample = ""
        unknownCnt = 0
        
        for manifestLine in manifest:
            manifestLine = manifestLine.strip() # remove whitespace
            
            # check is user-permission is within manifest line
            if "uses-permission" in manifestLine:

                # standard formatted Android permission
                if "android:name=" in manifestLine:
                    # find beginning of permission
                    startIndex = manifestLine.index("android:name=")# starting index
                    temp = manifestLine[startIndex + len("android:name=") + 1 :] # slice
                
                    # find end of permission
                    endIndex = temp.index("\"/>") # ending index
                    temp = temp[:endIndex] # slice
                
                    #print(sPerm) # DEBUG: Captured Permission
                    detectedPermissions.append(temp)
                    
                # Non-standard formatted Android Permission
                elif "android.permission." in manifestLine:
                    #print(manifestLine) # DEBUGGING
                    temp = manifestLine[manifestLine.index("android.permission."):]
                    endIndex = temp.index("\"/>")
                    permissionSliced = temp[:endIndex]
                    detectedPermissions.append(permissionSliced)
                    unknownPermissionFormat = True
                    if unknownPermissionFormat:
                        unknownExample = manifestLine
                        unknownCnt = unknownCnt + 1
                    # if
                    
                # default
                else:
                    print("[*] Cannot process permission: " + manifestLine)
                # if
            # if
        # for
        
        if unknownPermissionFormat:
            print("\n[*] Possible permission obfuscation: " + str(unknownCnt))
            print("Example: " + unknownExample)
        # if

        detectedPermissions = list(dict.fromkeys(detectedPermissions))
        detectedPermissions.sort()
        
        return detectedPermissions
    # function

    def getManifestServices(manifest):
        services = list() # empty list
        for line in manifest:
            if "<service " in line:
                startPos = line.find("android:name=")+len("android:name=\"")
                temp = line[startPos:]
                endPos = int(temp.find("\""))
                services.append(temp[:(endPos)])
            # if
        # for
        
        services.sort() # sort services found
        return services
    # function

    # def analyzeJAR(apk):
    #     pos = apk.find(".")
    #     jar = apk[:pos] + "-dex2jar.jar"
    #     zippedFile = zipfile.ZipFile(jar, 'r')
    #     jarClasses = list()
    #     try:
    #         lst = zf.infolist()
    #         for zi in lst:
    #             fn = zi.filename
    #             if fn.endswith('.class'):
    #                 jarClasses.append(fn)
    #             # if
    #         # for
    #     except IOError:
    #         print ('unable to read file {file}'.format(file = jar))
    #         exit(1)
    #     except zipfile.BadZipfile:
    #         print ('file {file} is not a zip file'.format(file = jar))
    #         exit(1)
    #     finally:
    #         zippedFile.close()
    #     # try
    #     return jarClasses
    # # function

    def getAPKMetaData(manifest):
        for index in manifest:
            if "<manifest " in index:
                startPos = index.find("compileSdkVersion=\"")
                sliced = index[startPos:]
                
                # check if at end of the tag
                if not sliced.find("\" ") == -1:
                    endPos = sliced.find("\" ")
                else:
                    endPos = sliced.find("\">")
                # if

                compileSdkVersion = sliced[sliced.find("\"")+1:endPos]
                startPos = index.find("compileSdkVersionCodename=\"")
                sliced = index[startPos:]

                # check if at end of the tag
                if not sliced.find("\" ") == -1:
                    endPos = sliced.find("\" ")
                else:
                    endPos = sliced.find("\">")
                # if

                compileSdkVersionCodename = sliced[sliced.find("\"")+1:endPos]

                startPos = index.find("package=\"")
                sliced = index[startPos:]
                
                # check if at end of the tag
                if not sliced.find("\" ") == -1:
                    endPos = sliced.find("\" ")
                else:
                    endPos = sliced.find("\">")
                # if

                apkPackagename = sliced[sliced.find("\"")+1:endPos]
                startPos = index.find("platformBuildVersionCode=\"")
                sliced = index[startPos:]

                # check if at end of the tag
                if not sliced.find("\" ") == -1:
                    endPos = sliced.find("\" ")
                else:
                    endPos = sliced.find("\">")
                # if

                platformBuildVersionCode = sliced[sliced.find("\"")+1:endPos]
                startPos = index.find("platformBuildVersionName=\"")
                sliced = index[startPos:]

                # check if at end of the tag
                if not sliced.find("\" ") == -1:
                    endPos = sliced.find("\" ")
                else:
                    endPos = sliced.find("\">")
                # if

                platformBuildVersionName = sliced[sliced.find("\"")+1:endPos]
                return compileSdkVersion, compileSdkVersionCodename, apkPackagename, platformBuildVersionCode, platformBuildVersionName
            # if
        # for
    # function

    def getManifestFeaturesUsed(manifest):
        usesFeatures = dict()
        unknownFeatures = list()
        unknownFeaturesFound = False
        
        for index in manifest:
            if "<uses-feature " in index:
                featureName = ""
                glEsVersion = ""

                if not index.find("android:name=\"") == -1:
                    startPos = index.find("android:name=\"")
                    sliced = index[startPos+len("android:name=\""):]
                    endPos = sliced.find("\"")
                    featureName = sliced[:endPos]

                    #print("Feature: "+featureName)
                    key = featureName

                elif not index.find("android:glEsVersion=\"") == -1: 
                    startPos = index.find("android:glEsVersion=\"")
                    sliced = index[startPos+len("android:glEsVersion=\""):]
                    endPos = sliced.find("\"")
                    glEsVersion = sliced[:endPos]
                    
                    #print("Gles Version: "+glEsVersion)
                    key = "glEsVersion=" + glEsVersion
                else:
                    unknownFeatures.append(index.strip())
                    unknownFeatures = True
                    continue
                # if

                if not index.find("android:required=\"") == -1:
                    startPos = index.find("android:required=\"")
                    x = index[startPos+len("android:required=\""):]
                    status = x[:x.find("\"")]

                    if status.lower() == "true":
                        usesFeatures[key] = True
                        continue # next iteration
                    # if

                #print("Required: "+str(isRequired)+"\n")
                usesFeatures[key] = False
            # if
        # for
        
        if unknownFeatures:
            print("\nUnknown Features Found:")
            cnt = 1
            for i in unknownFeatures:
                print("["+str(cnt)+"] "+i)
                cnt = cnt + 1 # increment count
            # for
        # if

        return usesFeatures
    # function

    def manifestToTxt(apk):
        name = apk[:-4]
        manifest_path = "./" + name + "/AndroidManifest.xml"
        output_path = "OUTPUT/" + name + "_AndroidManifest.txt"
        #manifestInput = scanManifest(manifest_path)
        
        try:
            manifest = Havasu.scanManifest(manifest_path)
            fOutput = open(output_path, "w")
            
            try:
                for i in manifest:
                    fOutput.write(i)
            finally:
                fOutput.close()
            # try

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()
        # try
    # function

    # Log detected Android permissions
    def logPermissions(apk):
        APK_NAME = apk[:-4]
        PERMISSION_LOG_NAME = "OUTPUT/" + APK_NAME + "_DetectedPermissions.txt"	
        androidManifest = Havasu.scanManifest("./" + APK_NAME + "/AndroidManifest.xml")
        PERMISSION_HEAD_FORMAT = "android.permission."
        
        detectedPermissions = Havasu.etPermissions(androidManifest)
        NUM_PERMISSIONS = str(len(detectedPermissions))
        #print("Total permissions: " + NUM_DETECTED_PERMISSIONS)
        if(NUM_PERMISSIONS == 0 ):
            print("No permissions detected [!!]")
            return
        # if
        
        standardPerms = list()
        unknownPerms = list()
        
        for index in detectedPermissions:
            if PERMISSION_HEAD_FORMAT in index:
                standardPerms.append(index)
            else:
                unknownPerms.append(index)
            # if
        # for
        
        standardPerms.sort()
        unknownPerms.sort()
        
        log = open(PERMISSION_LOG_NAME, "w")
        try:
            log.write("APK NAME: " + APK_NAME +"\n")
            log.write("Total permissions: " + NUM_PERMISSIONS + "\n\n")
            
            # standard format permissions
            NUM_STANDARD_PERMISSIONS = len(standardPerms)
            print("\nStandard permissions: "+str(NUM_STANDARD_PERMISSIONS))
            log.write("Standard permissions: " + str(NUM_STANDARD_PERMISSIONS) + "\n")
            log.write("----------------------------\n")
            for index in standardPerms:
                log.write(index + "\n")
            # for
            
            # unknown permissions
            NUM_UNKNOWN_PERMISSIONS = len(unknownPerms)
            if NUM_UNKNOWN_PERMISSIONS != 0:
                print("\nUnknown permissions: " + str(NUM_UNKNOWN_PERMISSIONS))
                log.write("\nUnknown permissions: " + str(NUM_UNKNOWN_PERMISSIONS) + "\n")
                log.write("----------------------------\n")
                for index in unknownPerms:
                    log.write(index + "\n")
                # for
            # if
        except IOError:
            print("IO ERROR")
        # try
    # function

    # Analyze Android manifest
    def analyzeAndroidManifest(apk):

        APK_NAME = apk[:-4]
        F_LOG_NAME = "OUTPUT/"+APK_NAME+"_AnalysisLog.txt"
        DATE = datetime.datetime.now().strftime("%A %B %d, %Y %I:%M %p")
        manifest = Havasu.scanManifest("./" + APK_NAME + "/AndroidManifest.xml")

        compileSdkVersion, compileSdkVersionCodename, apkPackagename, platformBuildVersionCode, platformBuildVersionName = Havasu.getAPKMetaData(manifest)
        standardPermissions, customPermissions = Havasu.getManifestPermissions(manifest)
        num_permissions = str(len(standardPermissions) +  len(customPermissions))

        log = open(F_LOG_NAME, "w")
        log.write("File: "+apk+"\n")
        log.write("Date: " + DATE + "\n")
        log.write("Package: " + apkPackagename + "\n")
        log.write("Compiled SDK Version: " + compileSdkVersion + "\n")
        log.write("Compiled SDK Version Codename: " + compileSdkVersionCodename + "\n")
        log.write("Platform Build Version Code: " + platformBuildVersionCode + "\n")
        log.write("Platform Build Version Name: " + platformBuildVersionName + "\n")
        log.write("Total Permissions: " + num_permissions+"\n")
        
        # Standard Permissions
        log.write("\nStandard Permissions: " + str(len(standardPermissions)) + "\n")
        for i in standardPermissions:
            log.write(i + "\n")
        # for
        log.write("\n")
        
        # Custom Permissions
        log.write("Unknown Permissions: " + str(len(customPermissions)) + "\n")
        for i in customPermissions:
            log.write(i + "\n")
        # for
        log.write("\n")

        # Log detected uses-features
        uses_features = Havasu.getManifestFeaturesUsed(manifest)
        if uses_features:
            log.write("USES-FEATURES\n")
            for key,value in uses_features.items():
                log.write(key+" "+str(value)+"\n")
            # for
            log.write("\n")
        # if
        
        # Log detected APK services
        services = Havasu.getManifestServices(manifest)
        log.write("Services\n")
        
        for i in services:
            log.write(i + "\n")
        # for

        log.write("\n")
    # function

    # Load Mitre data
    def loadMitreData(self):
        print("loadMitreData()") # DEBUGGING
        
        columns = set() # empty set

        sql = "select distinct description, attack_id"
        sql = sql + " from mitre_detection"
        sql = sql + " order by description, attack_id"

        results = pd.read_sql_query(sql, self.connection)
        records = pd.DataFrame(results)

        for index, row in records.iterrows():
            col = row[0] + " " + row[1]
            columns.add(col)
        # for

        return sorted(columns)
    # function

    # Mitre data dictionary
    def getMitreDict(self):
        print("getMitreDict()") # DEBUGGING

        dict_mitre = dict()  
        for i in Havasu.loadMitreData():
            dict_mitre[i] = list()
        # for

        print("\nLoading Mitre Data") # newline
        print("---------------") # newline
        for k in dict_mitre:
            print(k)
        # for
        print() # newline

        sql = "select description, ATTACK_ID, trojan_id"
        sql = sql + " from mitre_detection"
        sql = sql + " order by trojan_id, description, ATTACK_ID"

        results = pd.read_sql_query(sql, self.connection)
        df_samples = pd.DataFrame(results)

        for index, row in df_samples.iterrows():
            key = row[0] + " " + row[1]
            #print(key)
            items = dict_mitre[key]
            items.append(row[2])
            items.sort()
            dict_mitre[key] = items
        # for

        return dict_mitre
    # function

    # Get mitre matrix columns
    def getMitreMatrixColumns(self):
        print("getMitreMatrixColumns()") # DEBUGGING

        sql = "SHOW COLUMNS FROM mitre_matrix"
        results = pd.read_sql_query(sql, self.connection)
        
        cols = results.loc[:, 'Field']  
        cols = cols.drop(cols.index[0])

        return cols.tolist()
    # function

    # Get sample ids
    def getSampleIds(self):
        print("getSampleIds()") # DEBUGGING

        sql = "select DISTINCT trojan_id from mitre_detection"
        results = pd.read_sql_query(sql, self.connection)
        records = pd.DataFrame(results)
        
        temp = list()
        for i in records.loc[:, 'trojan_id']:
            temp.append(i)
        # for

        temp.sort()

        return temp
    # function

    # Add ids mitra matrix
    def addIdsMitreMatrix(self):
        print("addIdsMitreMatrix()") # DEBUGGING

        samples = Havasu.getSampleIds()

        for index in samples:
            sql = "select * from mitre_matrix where trojan_id = " + str(index)
            results = pd.read_sql_query(sql, self.connection)
            
            if results.empty:
                sql = "insert into mitre_matrix (trojan_id) value (%s)"
                self.cursor.execute(sql, (str(index),))
                self.connection.commit()

                print("Added sample id: " + str(index))
            # if
        # for

        print() # newline
    # function

    # Populate mitre matrix table
    def populateMitreMatrixTable(self):
        Havasu.addIdsMitreMatrix()

        columns = Havasu.getMitreMatrixColumns()
        dict_mitreMatrix = Havasu.getMitreDict()
        
        # iterator to find any missing columns 
        for index in dict_mitreMatrix:
            
            # check if column does not exist in the table
            if index not in columns:
                print(index + " Does not exist")
                sql = "ALTER TABLE `mitre_matrix` ADD `"+ index +"` varchar(1) null"
                self.cursor.execute(sql)
                self.connection.commit()
            # if
        # for
        print() # newline

        for key in dict_mitreMatrix:
            print(key)
            values = dict_mitreMatrix[key]
            
            for i in values:
                sql = "UPDATE mitre_matrix SET `" + key + "` = 'X' WHERE trojan_id = " + str(i)
                self.cursor.execute(sql)
                self.connection.commit()
            # for
        # for
    # function

    # Generate LatTeX Charts
    def generateLaTexCharts(self, argv):

        sql = "SELECT ID, "
        sql = sql + "Kaspersky_Label Kaspersky, "
        sql = sql + "HybridAnalysis_Label HybridAnalysis, "
        sql = sql + "VirusTotal_DetectionRatio, "
        sql = sql + "HybridAnalysis_AV_Detection "
        sql = sql + "FROM malware_samples "
        sql = sql + "WHERE family = '" + argv[0] + "' order by id"

        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        Havasu.displayLaTeXCharts(results, "\nDataset Labels\n")

        sql = "SELECT y.id, y.security_score score, y.grade, "
        sql = sql + "y.trackers_detections tracker, y.high_risks, y.medium_risks "
        sql = sql + "FROM malware_samples x JOIN mobfs_analysis y ON y.id = x.id "
        sql = sql + "where x.family = '" + argv[0] + "' order by x.id"

        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        Havasu.displayLaTeXCharts(results, "\nMobSF Security Score\n")

        sql = "select x.id, "
        sql = sql + "x.size, "
        sql = sql + "x.Target_SDK, x.Minimum_SDK,"
        sql = sql + "y.activities, "
        sql = sql + "y.services, "
        sql = sql + "y.receivers, "
        sql = sql + "y.providers "
        sql = sql + "from malware_samples x "
        sql = sql + "join mobfs_analysis y "
        sql = sql + "on y.id = x.id "
        sql = sql + "where x.family = '"+argv[0]+"' "
        sql = sql + "order by x.id "

        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        Havasu.displayLaTeXCharts(results, "\nStatic Analysis\n")
    # function

    # Display LaTeX Charts
    def displayLaTeXCharts(results, chartTitle):
        print(chartTitle) # newline
        for row in results:
            buff = ""
            cnt = 0

            for element in row:
                if cnt == (len(row) - 1):
                    buff = buff + str(element) + " \\\\"
                else:
                    buff = buff + str(element) + " & "
                # if

                cnt = cnt + 1 # increment
            # for
            print(buff)
        # for
    # function
# class