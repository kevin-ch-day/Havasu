# utils.py

import pandas as pd
import openpyxl as xl
import database as db
import os

# Check hash against database records 
def checkHash(hash):
    
    # MD5
    sql = "select * from malware_samples where md5 = '" + hash + "'"
    results = db.queryData(sql)
    if results:
        print("MD5 match found.")
        displayMalwareRecord(results)
        return

    # SHA1
    sql = "select * from malware_samples where sha1 = '" + hash + "'"
    results = db.queryData(sql)
    if results:
        print("SHA1 match found.")
        displayMalwareRecord(results)
        return

    # SHA256
    sql = "select * from malware_samples where sha256 = '" + hash + "'"
    results = db.queryData(sql)
    if results:
        print("SHA256 match found.")
        displayMalwareRecord(results)
        return

    print("No matching record found.")

# check if permission input txt file exists
def checkPermissionInput():
    fileExist = os.path.isfile("..\Input\APK_PERMISSIONS.txt")
    return fileExist

# check sample id
def checkSamplePermissionIdRecords(id):
    sql = "select ID from detected_standard_permissions where ID = '" + id + "'"
    results = db.queryData(sql)
    if results:
        return True
    
    sql = "select ID from detected_unknown_permissions where ID = '" + id + "'"
    results = db.queryData(sql)
    if results:
        return True
    
    return False

def deleteSampleRecords(id):
    # delete from table: detected_standard_permissions
    sql = "DELETE FROM detected_standard_permissions WHERE ID = '"  + id + "'"
    db.executeSQL(sql)
    
    # delete from table: detected_unknown_permissions
    sql = "DELETE FROM detected_unknown_permissions WHERE ID = '"  + id + "'"
    db.executeSQL(sql)

# Display malware record
def displayMalwareRecord(record):
    data = record[0]
    print("\nID: " + str(data[0]))
    print("Name: " + data[1])
    print("Family: " + data[2])
    print("Size: " + data[12])
    print("VirusTotal: " + data[4])

# check permission records
def checkPermissionRecords(id):
    sql = "SELECT * FROM detected_standard_permissions where id = '" + id + "'"
    results = db.queryData(sql)
    if not results:
        return None
    # if

# create scan record for trojan id
def createSampleIdPermissionRecord(trojan_id):
    sql = "INSERT INTO detected_standard_permissions (id) VALUES (%s)"
    val = (trojan_id, )
    db.executeSQL(sql, val)
    print("Permission record created for " + trojan_id)

# Read Mitre data
def readMitreData():
    MITRE_INPUT_FILE_PATH = "..\Input\MITRE-INPUT.xlsx"
    if not os.path.isfile(MITRE_INPUT_FILE_PATH):
        print("[!] - Mitre Att&ck excel file not found.")
        return
    
    wb = xl.load_workbook(MITRE_INPUT_FILE_PATH)
    print("\nReading Mitre Att&ck excel data.")

    for i in wb.sheetnames:
        print("Sheetname: ", i)
        df = pd.read_excel(MITRE_INPUT_FILE_PATH, sheet_name = i)

        sql = "INSERT INTO mitre_detection"
        sql = sql + " (Trojan_ID, ATTACK_ID, Tactic, Description, Malicious_Indicators, "
        sql = sql + "Suspicious_Indicators, Informative_Indicators)"
        sql = sql + " VALUES (%s, %s, %s, %s, %s, %s, %s)"

        values = list()
        for index, row in df.iterrows():
            sample_id = row[0]
            attack = row[1]
            technique = row[2]
            tactic = row[3]
            mali = row[4]
            susp = row[5]
            info = row[6]

            data = (sample_id, attack, technique, tactic, mali, susp, info)
            values.append(data)
            db.executeSQLMany(sql, values)

# read detected permission from text file
def readDetectedPermissionsInput():
    PERMISSIONS_INPUT_PATH = "..\Input\APK_PERMISSIONS.txt"
    fPermissions = open(PERMISSIONS_INPUT_PATH, "r")

    permissions = list()
    for index in fPermissions:
        permissions.append(index.strip())
    # for
    return permissions

# Standard Android Permissions
def getStandardAndroidPermissionList():
    permissions = list()

    results = db.queryData("show columns from detected_standard_permissions")
    if not results:
        print("[!!] - No permission columns retrieved from database.")
        exit()
    
    for i in results:
        if 'ID' == i[0]:
            pass
        else:
            permissions.append(i[0])

    return permissions

# Record Android permissions
def recordAndroidPermissions(trojan, permissions):
    updatedColumns = 0
    unknownPermissions = list()
    standardPermissions = getStandardAndroidPermissionList()
    FORMAT_HEADER = len("android.permission.")

    for index in permissions:
        permission = index[FORMAT_HEADER:]

        if permission not in standardPermissions:
            print("Unknown Permission: " + index)
            unknownPermissions.append(permission)
            #print(slicedPermissions) # DEBUGGING

        # if permission does not exists within table
        else:
            sql = "UPDATE detected_standard_permissions SET "
            sql = sql + permission + " = 'X' WHERE id = " + str(trojan)
            db.executeSQL(sql)
            updatedColumns = updatedColumns + 1

    print(str(updatedColumns) + " columns updated.")
    if len(unknownPermissions) != 0:
        recordNonStandardPermissions(trojan, unknownPermissions)

# Load Mitre data
def loadMitreData():
    
    columns = set() # empty set

    sql = "select distinct description, attack_id"
    sql = sql + " from mitre_detection"
    sql = sql + " order by description, attack_id"

    df = db.pandasDataFrame(sql)
    for index, row in df.iterrows():
        data = row[0] + " " + row[1]
        columns.add(data)

    return sorted(columns)

# Mitre data dictionary
def getMitreDict():

    dict = dict()  
    for i in loadMitreData():
        dict[i] = list()
    # for

    print("\nLoading Mitre Data") # newline
    print("---------------") # newline
    for k in dict:
        print(k)
    print() # newline

    sql = "select description, ATTACK_ID, trojan_id"
    sql = sql + " from mitre_detection"
    sql = sql + " order by trojan_id, description, ATTACK_ID"

    df = db.pandasDataFrame(sql)

    for index, row in df.iterrows():
        key = row[0] + " " + row[1]
        items = dict[key]
        items.append(row[2])
        items.sort()
        dict[key] = items

    return dict

# Get mitre matrix columns
def getMitreMatrixColumns():

    sql = "SHOW COLUMNS FROM mitre_matrix"
    df = db.pandasDataFrame(sql)
    
    cols = df.loc[:, 'Field']  
    cols = cols.drop(cols.index[0])

    return cols.tolist()

# Get sample ids
def getMitreSampleIds():
    ids = list()

    sql = "select DISTINCT trojan_id from mitre_detection"
    df = db.pandasDataFrame(sql)
    
    for i in df.loc[:, 'trojan_id']:
        ids.append(i)

    ids.sort()
    return ids

# Add ids mitra matrix
def addIdsMitreMatrix():
    samples = getMitreSampleIds()
    for index in samples:
        sql = "select * from mitre_matrix where trojan_id = " + str(index)
        df = db.pandasDataFrame(sql)

        if df.empty:
            sql = "insert into mitre_matrix (trojan_id) value (%s)"
            db.executeSQL(sql, (str(index),))
            print("Added sample id: " + str(index))

# Populate mitre matrix table
def populateMitreMatrixTable():
    addIdsMitreMatrix()

    columns = getMitreMatrixColumns()
    dict_mitreMatrix = getMitreDict()
    
    # Iterate to find any missing columns 
    for index in dict_mitreMatrix:
        
        # check if column does not exist in the table
        if index not in columns:
            print(index + " Does not exist")
            sql = "ALTER TABLE `mitre_matrix` ADD `"+ index +"` varchar(1) null"
            db.executeSQL(sql)
    print() # newline

    for key in dict_mitreMatrix:
        print(key)
        values = dict_mitreMatrix[key]
        for index in values:
            sql = "UPDATE mitre_matrix SET `" + key + "` = 'X' WHERE trojan_id = " + str(index)
            db.executeSQL(sql)

# Generate sample data by ids to .xlsx file
def outputMalwareRecordsById(ids):
    FILE_PATH = "..\Output\Output-Excel.xlsx"

    sql = "SELECT * FROM mobfs_analysis WHERE id in " + ids
    df = db.pandasDataFrame(sql)
    df.to_excel(FILE_PATH)

# Generate sample data by family to .xlsx file
def outputMalwareRecordsByFamily(database, family):
    FILE_PATH = "..\Output\Output-Excel.xlsx"
    
    sql = "SELECT * FROM malware_samples WHERE family = '" + family + "'"        
    df = db.pandasDataFrame(sql)
    df.to_excel(FILE_PATH)

# Standard Permissions
def outputStandardPermissions(sample_set):
    EXCEL_FILE_PATH = '..\Output\Android-Permissions.xlsx'
    
    sql = "select * from detected_standard_permissions "
    sql = sql + " where id in " + str(sample_set)
    sql = sql + " order by id"

    df_alpha = db.getDataFrame(sql)
    df_beta = pd.DataFrame() # create empty data frame

    df_beta['ID'] = df_alpha['ID']
    df_alpha = df_alpha.drop(columns=['ID'])

    for column in df_alpha:
        for cell in df_alpha[column]:
            if cell is not None:
                df_beta[column] = df_alpha[column]
                break
    df_beta.to_excel(EXCEL_FILE_PATH)

# Unknown Permissions
def outputUnknownPermissions(sample_set):
    EXCEL_FILE_PATH = "..\\Output\\Unknown-Permissions.xlsx"

    sql = "select * from detected_unknown_permissions "
    sql = sql + " where id in " + sample_set
    sql = sql + " order by id"

    df_alpha = df_alpha = db.getDataFrame(sql)
    df_beta = pd.DataFrame()

    df_beta['ID'] = df_alpha['ID']
    df_alpha = df_alpha.drop(columns=['ID'])

    for column in df_alpha:
        for cell in df_alpha[column]:
            if cell is not None:
                df_beta[column] = df_alpha[column]
                break
    df_beta.to_excel(EXCEL_FILE_PATH)

# Normal Permissions
def outputNormalPermissions(sample_set):
    EXCEL_FILE_PATH = "..\\Ouput\\Normal-Permissions.xlsx"

    sql = "select name from android_permissions where Protection_level = 'Normal' order by name"
    results = db.queryData(sql)
    normalPermissionsColumns = "'" # start sql columns
    buff = list()
    cnt = 0

    for x in results:    
        if(x[0] == "ID"):
            print(x[0])
        elif(cnt == (len(results)-1)):
            normalPermissionsColumns = normalPermissionsColumns + x[0] + "'" # end columns
            #print(cnt, x[0])
        else:
            normalPermissionsColumns = "'" + normalPermissionsColumns + x[0] + "', " # append column
            #print(cnt, x[0])

        buff.append(x[0])
        cnt = cnt + 1

    ## ADD COLUMN CHECKING
    sql = "SHOW COLUMNS FROM detected_standard_permissions"
    results = db.queryData(sql)
    detectedPermissions = list()
    for i in results:
        if(i[0] != "ID"):
            detectedPermissions.append(i[0])

    missingPermissions = list()
    for index in buff:
        if index not in detectedPermissions:
            missingPermissions.append(index.upper())

    if missingPermissions:
        print("Missing Permissions: ")
        for i in missingPermissions:
            print(i)
        exit()
    # if

    sql = "select ID, " + normalPermissionsColumns
    sql = sql + " from detected_standard_permissions"
    sql = sql + " where ID in " + sample_set
    sql = sql + " order by ID"

    df_alpha = db.getDataFrame(sql)
    df_beta = pd.DataFrame()

    df_beta['ID'] = df_alpha['ID']
    df_alpha = df_alpha.drop(columns=['ID'])

    for column in df_alpha:
        for cell in df_alpha[column]:
            if cell is not None:
                print(column)
                df_beta[column] = df_alpha[column]
                break
    df_beta.to_excel(EXCEL_FILE_PATH)

# Classify detected permissions
def recordSamplePermissions(sample_id, permissions):
    standardFormatPerms = list()
    unknownPermissions = list()
    unknownPermissionsFound = False

    for index in permissions:

        # check if permission matches the standard permission formatted
        if "android.permission." in index:
            standardFormatPerms.append(index)
        else:
            unknownPermissions.append(index)
            unknownPermissionsFound = True

    recordAndroidPermissions(sample_id, standardFormatPerms)
    print("\nStandard Permissions found: ", len(standardFormatPerms))

    if unknownPermissionsFound:
        RECORD_UNKNOWN_PERMS_PATH = "..\Output\\"+str(sample_id)+"-UnknownPerms.txt"
        fUnknownPermissions = open(RECORD_UNKNOWN_PERMS_PATH, "w")
        try:
            for i in unknownPermissions:
                fUnknownPermissions.write(i + "\n")

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()

    print("\nUnknown Permissions found: ", len(unknownPermissions))

# Record non-standard permissions
def recordNonStandardPermissions(trojan, unknownPermissions):
    dbCols = list()
    addedCols = updatedCols = 0

    sql = "show columns from detected_unknown_permissions"
    results = db.queryData(sql)
    if not results:
        print("[!!] - No columns retrieved from: unknown_permissions")
        exit()

    for i in results:
        if 'id' == i[0]:
            pass
        else:
            dbCols.append(i[0])
    #print(unknownPermissions) # DEBUGGING

    # Create record for APK in table
    sql = "INSERT INTO detected_unknown_permissions (id) VALUES (%s)"
    values = (trojan, )
    db.executeSQL(sql, values)

    print("\nUnknown permissions")
    for index in unknownPermissions:
        if index not in dbCols:
            print("Adding new column to database: ", index)
            sql = "ALTER TABLE detected_unknown_permissions add " + index + " VARCHAR(1) NULL DEFAULT NULL"
            db.executeSQL(sql)

        # update column with permission record
        sql = "update detected_unknown_permissions set " + index + " = 'X' where id = " + str(trojan)
        db.executeSQL(sql)

    print("Columns added: " + str(addedCols) + " updated: " + str(updatedCols))

# Generate mitre matrix
def generateMitreMatrix(sample_set):
    EXCEL_FILE_PATH = '..\Output\Mitre-Matrix.xlsx'
    
    sql = "select * from mitre_matrix "
    sql = sql + " where trojan_id in " + sample_set
    sql = sql + " order by trojan_id"

    df_raw = db.pandasReadSQL(sql)

    columns = df_raw.columns.tolist()
    columns.sort()
    columns.remove('trojan_id')

    df_beta = pd.DataFrame()
    df_beta['trojan_id'] = df_raw['trojan_id']
    df_alpha = df_raw.drop(columns=['trojan_id'])

    for index in columns:
        for cell in df_alpha[index]:
            if cell is not None:
                df_beta[index] = df_alpha[index]
                break
    
    df_beta.to_excel(EXCEL_FILE_PATH)