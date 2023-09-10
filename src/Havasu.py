# havasu.py

import database
import pandas as pd
import openpyxl as xl
import mysql.connector
import os
import datetime
import zipfile

VERSION_NUMBER = "1.0.1"

# start database connection
def startDB():
    database.start()

# end database connection
def endDB():
    database.end()

# OS Tool: apktool d
# decompile APK file
def decompileAPK(apk):
    os.system("apktool d " + apk)

# OS Tool: dex2jar
# convert APK to JAR file
def generateJAR(apk):
    os.system("d2j-dex2jar " + apk)
 
# Display version number
def version():
    global VERSION_NUMBER
    return VERSION_NUMBER

# Check supplied hash against database
def checkHash(hash):
    hashFound = False
    
    sql = "select * from malware_samples where md5 = '" + hash + "'"
    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    if results:
        hashFound = True
        print("MD5 hash match found")
        #self.displayMalwareRecord(results[0])
        return
    # if

    sql = "select * from malware_samples where sha1 = '" + hash + "'"
    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    if results:
        hashFound = True
        print("SHA1 hash match found")
        displayMalwareRecord(results)
        return
    # if

    sql = "select * from malware_samples where sha256 = '" + hash + "'"
    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    if results:
        hashFound = True
        print("SHA256 hash match found")
        displayMalwareRecord(results)
        return
    # if

    if not hashFound:
        print("No hash record found.")
    # if
# checkHash()

# Display malware record
def displayMalwareRecord(record):
    print("ID:\t\t" + str(record[0]))
    print("Name:\t\t" + record[1])
    print("Family:\t\t" + record[2])
    print("Size:\t\t" + record[12])
    print("VirusTotal:\t" + record[4])

# check permission records
def checkPermissionRecords(id):
    sql = "SELECT * FROM detected_standard_permissions where id = '" + id + "'"
    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    if not results:
        return None
    # if

# create scan record for trojan id
def createPermissionRecord(trojan_id):
    sql = "INSERT INTO detected_standard_permissions (id) VALUES (%s)"
    val = (trojan_id, )
    database.cursor.execute(sql, val)
    database.connection.commit()
    print("Permission record created for " + trojan_id)

# Read mitre data
def readMitreData():
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

            database.cursor.execute(sql, data)
            #print(cursor.rowcount, "record inserted.")
        # for

        database.connection.commit()
        print() # newline
    # for

# read detected permission from text file
def readDetectedPermissions():
    fPERMISSION_INPUT = open("INPUT\\APK_PERMISSIONS.txt", "r")
    buff = list()
    for p in fPERMISSION_INPUT:
        buff.append(p.strip())
    # for

    return buff

# Standard Android Permissions
def getStandardAndroidPermissionList():
    permissionList = list()

    database.cursor.execute("show columns from detected_standard_permissions")
    results = database.cursor.fetchall()
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

# Classify detected permissions
def classifyPermissions(trojan, permissions):
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

# Record Android Permissions
def recordAndroidPermissions(trojan, permissions):
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
                database.cursor.execute(sql)
                database.connection.commit()
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

def recordNonStandardPermissions(trojan, unknownPermissions):
    dbCols = list()
    addedCols = updatedCols = 0

    sql = "show columns from detected_unknown_permissions"
    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    if not results:
        print("[!!] - No columns retrieved from: unknown_permissions")
        exit()
    # if

    for i in results:
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
        database.cursor.execute(sql, val)
        database.connection.commit()
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
                database.cursor.execute(sql)
                database.connection.commit()
                addedCols = addedCols + 1
            except mysql.connector.Error as err:
                print("[!!] MySQL Error: {}".format(err))
            # try
        # if

        # update column within permission record
        sql = "update detected_unknown_permissions set " + index + " = 'X' where id = " + str(trojan)
        try:
            database.cursor.execute(sql)
            database.connection.commit()
            updatedCols = updatedCols + 1
        except mysql.connector.Error as err:
            print("[!!] MySQL Error: {}".format(err))
        # try
    # for

    print(str(addedCols) + " columns added.")
    print(str(updatedCols) + " columns updated.\n")

# Generate mitre matrix
def generateMitreMatrix(sample_set):
    FILE_PATH = 'OUTPUT\\Mitre-Matrix.xlsx'
    
    sql = "select * from mitre_matrix "
    sql = sql + " where trojan_id in " + sample_set
    sql = sql + " order by trojan_id"

    df_raw = pd.read_sql_query(sql, database.connection)

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
    df_beta.to_excel(FILE_PATH)


# Read AndroidManifest.xml permissions
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

# Get permissions
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

# Get AndroidManifest.xml services
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

# Get APK META data
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

# Get AndroidManifest.xml features used
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

# AndroidManifest.xml to text
def manifestToTxt(apk):
    name = apk[:-4]
    ANDROID_MANIFEST_PATH = "./" + apk + "/AndroidManifest.xml"
    OUTPUT_PATH = "OUTPUT/" + name + "_AndroidManifest.txt"
    
    try:
        manifest = open(ANDROID_MANIFEST_PATH, "r")
        androidManifest = manifest.readlines() # copy manifest
        manifest.close()
        f = open(OUTPUT_PATH, "w")
        
        try:
            for i in androidManifest:
                f.write(i)
        finally:
            f.close()
        # try

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    # try

# Log detected Android permissions
def logPermissions(apk):
    APK_NAME = apk[:-4]
    ANDROID_MANIFEST_PATH = "./" + APK_NAME + "/AndroidManifest.xml"
    PERMISSION_LOG_PATH = "OUTPUT/" + APK_NAME + "_DetectedPermissions.txt"	

    # Scan AndroidManifest.xml
    try:
        manifest = open(ANDROID_MANIFEST_PATH, "r")
        androidManifest = manifest.readlines() # copy manifest
        manifest.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    finally:
        manifest.close()
    # try

    standardPerms = list()
    unknownPerms = list()
    
    detectedPermissions = getPermissions(androidManifest)
    NUM_PERMISSIONS = str(len(detectedPermissions))
    #print("Total permissions: " + NUM_DETECTED_PERMISSIONS)
    if(NUM_PERMISSIONS == 0 ):
        print("No permissions detected [!!]")
        return
    # if
    
    for index in detectedPermissions:
        if "android.permission." in index:
            standardPerms.append(index)
        else:
            unknownPerms.append(index)
        # if
    # for
    
    log = open(PERMISSION_LOG_PATH, "w")
    try:
        log.write("APK NAME: " + APK_NAME +"\n")
        log.write("Total permissions: " + NUM_PERMISSIONS + "\n\n")
        
        # standard format permissions
        standardPerms.sort()
        NUM_STANDARD_PERMISSIONS = len(standardPerms)
        print("\nStandard permissions: "+str(NUM_STANDARD_PERMISSIONS))
        log.write("Standard permissions: " + str(NUM_STANDARD_PERMISSIONS) + "\n")
        log.write("----------------------------\n")
        for index in standardPerms:
            log.write(index + "\n")
        # for
        
        # unknown permissions
        unknownPerms.sort()
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

# Analyze Android manifest
def analyzeAndroidManifest(apk):
    APK_NAME = apk[:-4]

    ANALYIS_LOG_PATH = "OUTPUT/" + APK_NAME + "_AnalysisLog.txt"
    DATE = datetime.datetime.now().strftime("%A %B %d, %Y %I:%M %p")
    ANDROID_MANIFEST_PATH = "./" + APK_NAME + "/AndroidManifest.xml"
    
    # Scan AndroidManifest.xml
    try:
        f = open(ANDROID_MANIFEST_PATH, "r")
        androidManifest = f.readlines() # copy manifest
        f.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    finally:
        f.close()
    # try

    compileSdkVersion, compileSdkVersionCodename, apkPackagename, platformBuildVersionCode, platformBuildVersionName = getAPKMetaData(androidManifest)
    standardPermissions, customPermissions = getManifestPermissions(androidManifest)
    num_permissions = str(len(standardPermissions) +  len(customPermissions))

    log = open(ANALYIS_LOG_PATH, "w")
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
    log.write("\n")

    # Log uses-features
    uses_features = getManifestFeaturesUsed(androidManifest)
    if uses_features:
        log.write("USES-FEATURES\n")
        for key,value in uses_features.items():
            log.write(key+" "+str(value)+"\n")
        log.write("\n")
    # if
    
    # Log APK services
    services = getManifestServices(androidManifest)
    log.write("Services\n")
    
    for i in services:
        log.write(i + "\n")
    log.write("\n")

# Load Mitre data
def loadMitreData():
    print("loadMitreData()") # DEBUGGING
    
    columns = set() # empty set

    sql = "select distinct description, attack_id"
    sql = sql + " from mitre_detection"
    sql = sql + " order by description, attack_id"

    results = pd.read_sql_query(sql, database.connection)
    records = pd.DataFrame(results)

    for index, row in records.iterrows():
        col = row[0] + " " + row[1]
        columns.add(col)
    # for

    return sorted(columns)

# Mitre data dictionary
def getMitreDict():
    print("getMitreDict()") # DEBUGGING

    dict_mitre = dict()  
    for i in loadMitreData():
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

    results = pd.read_sql_query(sql, database.connection)
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

# Get mitre matrix columns
def getMitreMatrixColumns():
    print("getMitreMatrixColumns()") # DEBUGGING

    sql = "SHOW COLUMNS FROM mitre_matrix"
    results = pd.read_sql_query(sql, database.connection)
    
    cols = results.loc[:, 'Field']  
    cols = cols.drop(cols.index[0])

    return cols.tolist()

# Get sample ids
def getSampleIds():
    print("getSampleIds()") # DEBUGGING

    sql = "select DISTINCT trojan_id from mitre_detection"
    results = pd.read_sql_query(sql, database.connection)
    records = pd.DataFrame(results)
    
    temp = list()
    for i in records.loc[:, 'trojan_id']:
        temp.append(i)
    # for
    temp.sort()

    return temp

# Add ids mitra matrix
def addIdsMitreMatrix():
    print("addIdsMitreMatrix()") # DEBUGGING

    samples = getSampleIds()

    for index in samples:
        sql = "select * from mitre_matrix where trojan_id = " + str(index)
        results = pd.read_sql_query(sql, database.connection)
        
        if results.empty:
            sql = "insert into mitre_matrix (trojan_id) value (%s)"
            database.cursor.execute(sql, (str(index),))
            database.connection.commit()

            print("Added sample id: " + str(index))
        # if
    # for

    print() # newline

# Populate mitre matrix table
def populateMitreMatrixTable():
    addIdsMitreMatrix()

    columns = getMitreMatrixColumns()
    dict_mitreMatrix = getMitreDict()
    
    # iterator to find any missing columns 
    for index in dict_mitreMatrix:
        
        # check if column does not exist in the table
        if index not in columns:
            print(index + " Does not exist")
            sql = "ALTER TABLE `mitre_matrix` ADD `"+ index +"` varchar(1) null"
            database.cursor.execute(sql)
            database.connection.commit()
        # if
    # for
    print() # newline

    for key in dict_mitreMatrix:
        print(key)
        values = dict_mitreMatrix[key]
        
        for i in values:
            sql = "UPDATE mitre_matrix SET `" + key + "` = 'X' WHERE trojan_id = " + str(i)
            database.cursor.execute(sql)
            database.connection.commit()
        # for
    # for

# Generate LatTeX Charts
def generateLaTexCharts(family):
    sql = "SELECT ID, "
    sql = sql + "Kaspersky_Label Kaspersky, "
    sql = sql + "HybridAnalysis_Label HybridAnalysis, "
    sql = sql + "VirusTotal_DetectionRatio, "
    sql = sql + "HybridAnalysis_AV_Detection "
    sql = sql + "FROM malware_samples "
    sql = sql + "WHERE family = '" + family + "' order by id"

    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    displayLaTeXCharts(results, "\nDataset Labels\n")

    sql = "SELECT y.id, y.security_score score, y.grade, "
    sql = sql + "y.trackers_detections tracker, y.high_risks, y.medium_risks "
    sql = sql + "FROM malware_samples x JOIN mobfs_analysis y ON y.id = x.id "
    sql = sql + "where x.family = '" + family + "' order by x.id"

    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    displayLaTeXCharts(results, "\nMobSF Security Score\n")

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
    sql = sql + "where x.family = '" + family + "' "
    sql = sql + "order by x.id "

    database.cursor.execute(sql)
    results = database.cursor.fetchall()
    displayLaTeXCharts(results, "\nStatic Analysis\n")

# Display LaTeX Charts
def displayLaTeXCharts(results, chartTitle):
    print(chartTitle)
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

# Generate sample data by ids to .xlsx file
def outputMalwareRecordsById(ids):
    FILE_PATH = "OUTPUT\\Output-Excel.xlsx"
    sql = "SELECT * FROM mobfs_analysis WHERE id in " + ids
    df = pd.read_sql_query(sql, database.cursor)
    df.to_excel(FILE_PATH)

# Generate sample data by family to .xlsx file
def outputMalwareRecordsByFamily(database, family):
    FILE_PATH = "OUTPUT\\Output-Excel.xlsx"
    sql = "SELECT * FROM malware_samples WHERE family = '" + family + "'"        
    df = pd.read_sql_query(sql, database.cursor)
    df.to_excel(FILE_PATH)

# Standard Permissions
def outputStandardPermissions(sample_set):
    EXCEL_FILE = 'OUTPUT\\Android-Permissions.xlsx'
    
    sql = "select * from detected_standard_permissions "
    sql = sql + " where id in " + str(sample_set)
    sql = sql + " order by id"

    sql_query = pd.read_sql_query(sql, database.connection)
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

# Unknown Permissions
def outputUnknownPermissions(sample_set):
    FILE_PATH = 'OUTPUT\\Unknown-Permissions.xlsx'

    sql = "select * from detected_unknown_permissions "
    sql = sql + " where id in " + sample_set
    sql = sql + " order by id"

    sql_query = pd.read_sql_query(sql, database.connection)
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

# Normal Permissions
def outputNormalPermissions(sample_set):
    EXCEL_FILE = 'OUTPUT\\Normal-Permissions.xlsx'

    sql = "select name from android_permissions where Protection_level = 'Normal' order by name"
    database.cursor.execute(sql)
    results = database.cursor.fetchall()
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
    database.cursor.execute(sql)
    results = database.cursor.fetchall()
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

    sql_query = pd.read_sql_query(sql, database.connection)
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