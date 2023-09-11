# __main__.py

import pandas as pd
import openpyxl as xl
import database as db

# Check supplied hash against database records 
def checkHash(hash):
    hashFound = False
    
    sql = "select * from malware_samples where md5 = '" + hash + "'"
    results = db.queryData(sql)
    if results:
        hashFound = True
        print("MD5 hash match found")
        #self.displayMalwareRecord(results[0])
        return
    # if

    sql = "select * from malware_samples where sha1 = '" + hash + "'"
    results = db.queryData(sql)
    if results:
        hashFound = True
        print("SHA1 hash match found")
        displayMalwareRecord(results)
        return
    # if

    sql = "select * from malware_samples where sha256 = '" + hash + "'"
    results = db.queryData(sql)
    if results:
        hashFound = True
        print("SHA256 hash match found")
        displayMalwareRecord(results)
        return
    # if

    if not hashFound:
        print("No hash record found.")
    # if

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
    results = db.runQuery(sql)
    if not results:
        return None
    # if

# create scan record for trojan id
def createPermissionRecord(trojan_id):
    sql = "INSERT INTO detected_standard_permissions (id) VALUES (%s)"
    val = (trojan_id, )
    db.executeSQL(sql, val)
    print("Permission record created for " + trojan_id)

# Read Mitre data
def readMitreData():
    FILE_PATH = "Input\\MITRE-INPUT.xlsx"
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

            db.executeSQL(sql, values)
            #print(cursor.rowcount, "record inserted.")
        # for
        print() # newline
    # for

# read detected permission from text file
def readDetectedPermissions():
    fPERMISSION_INPUT = open("Input\\APK_PERMISSIONS.txt", "r")
    buff = list()
    for p in fPERMISSION_INPUT:
        buff.append(p.strip())
    # for
    return buff

# Standard Android Permissions
def getStandardAndroidPermissionList():
    permissions = list()

    results = db.runQuery("show columns from detected_standard_permissions")
    if not results:
        print("[!!] - No permission columns retrieved from database.")
        exit()
    # if
    
    for i in results:
        if 'ID' == i[0]:
            pass
        else:
            permissions.append(i[0])
    # for
    return permissions

# Record Android permissions
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
            sql = "UPDATE detected_standard_permissions SET "
            sql = sql + slicedPermissions + " = 'X' WHERE id = " + str(trojan)
            db.executeSQL(sql)
            updatedColumns = updatedColumns + 1
        # if
    # for

    print("\n** Standard permission columns **")
    print(str(updatedColumns) + " columns updated.")
    recordNonStandardPermissions(trojan, unknownPermissions)


# Load Mitre data
def loadMitreData():
    print("loadMitreData()") # DEBUGGING
    
    columns = set() # empty set

    sql = "select distinct description, attack_id"
    sql = sql + " from mitre_detection"
    sql = sql + " order by description, attack_id"

    df = db.pandasDataFrame(sql)

    for index, row in df.iterrows():
        col = row[0] + " " + row[1]
        columns.add(col)
    # for

    return sorted(columns)

# Mitre data dictionary
def getMitreDict():
    print("getMitreDict()") # DEBUGGING

    dict = dict()  
    for i in loadMitreData():
        dict[i] = list()
    # for

    print("\nLoading Mitre Data") # newline
    print("---------------") # newline
    for k in dict:
        print(k)
    # for
    print() # newline

    sql = "select description, ATTACK_ID, trojan_id"
    sql = sql + " from mitre_detection"
    sql = sql + " order by trojan_id, description, ATTACK_ID"

    df = db.pandasDataFrame(sql)

    for index, row in df.iterrows():
        key = row[0] + " " + row[1]
        #print(key)
        items = dict[key]
        items.append(row[2])
        items.sort()
        dict[key] = items
    # for

    return dict

# Get mitre matrix columns
def getMitreMatrixColumns():
    print("getMitreMatrixColumns()") # DEBUGGING

    sql = "SHOW COLUMNS FROM mitre_matrix"
    df = db.pandasDataFrame(sql)
    
    cols = df.loc[:, 'Field']  
    cols = cols.drop(cols.index[0])

    return cols.tolist()

# Get sample ids
def getSampleIds():
    print("getSampleIds()") # DEBUGGING

    sql = "select DISTINCT trojan_id from mitre_detection"
    df = db.pandasDataFrame(sql)
    
    temp = list()
    for i in df.loc[:, 'trojan_id']:
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
        df = db.pandasDataFrame(sql)
        
        if df.empty:
            sql = "insert into mitre_matrix (trojan_id) value (%s)"
            db.executeSQL(sql, (str(index),))
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
            db.executeSQL(sql)
        # if
    # for
    print() # newline

    for key in dict_mitreMatrix:
        print(key)
        values = dict_mitreMatrix[key]
        
        for i in values:
            sql = "UPDATE mitre_matrix SET `" + key + "` = 'X' WHERE trojan_id = " + str(i)
            db.executeSQL(sql)
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

    results = db.queryData(sql)
    displayLaTeXCharts(results, "\nDataset Labels\n")

    sql = "SELECT y.id, y.security_score score, y.grade, "
    sql = sql + "y.trackers_detections tracker, y.high_risks, y.medium_risks "
    sql = sql + "FROM malware_samples x JOIN mobfs_analysis y ON y.id = x.id "
    sql = sql + "where x.family = '" + family + "' order by x.id"

    results = db.queryData(sql)
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

    results = db.queryData(sql)
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
    FILE_PATH = "Output\\Output-Excel.xlsx"
    sql = "SELECT * FROM mobfs_analysis WHERE id in " + ids
    df = db.pandasDataFrame(sql)
    df.to_excel(FILE_PATH)

# Generate sample data by family to .xlsx file
def outputMalwareRecordsByFamily(database, family):
    FILE_PATH = "Output\\Output-Excel.xlsx"
    sql = "SELECT * FROM malware_samples WHERE family = '" + family + "'"        
    df = db.pandasDataFrame(sql)
    df.to_excel(FILE_PATH)

# Standard Permissions
def outputStandardPermissions(sample_set):
    EXCEL_FILE = 'Output\\Android-Permissions.xlsx'
    
    sql = "select * from detected_standard_permissions "
    sql = sql + " where id in " + str(sample_set)
    sql = sql + " order by id"

    sql_query = pd.read_sql_query(sql, database.connection)
    df_alpha = pd.DataFrame(sql_query)
    df_beta = pd.DataFrame() # create empty data frame

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
    FILE_PATH = 'Output\\Unknown-Permissions.xlsx'

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
    EXCEL_FILE = 'ouput\\Normal-Permissions.xlsx'

    sql = "select name from android_permissions where Protection_level = 'Normal' order by name"
    results = db.runQuery(sql)
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
    results = db.runQuery(sql)
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
        fUnknownPermissions = open("Output\\"+str(trojan)+"-UnknownPerms.txt", "w")
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


# Record non-standard permissions
def recordNonStandardPermissions(trojan, unknownPermissions):
    dbCols = list()
    addedCols = updatedCols = 0

    sql = "show columns from detected_unknown_permissions"
    results = db.runQuery(sql)
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
    values = (trojan, )
    db.executeSQL(sql, values)

    print("\n** Detected unknown permissions columns **")
    for index in unknownPermissions:
        if index not in dbCols:

            # add new columns to table
            print("Adding new column: ", index) # DEBUGGING
            sql = "ALTER TABLE detected_unknown_permissions add " + index + " VARCHAR(1) NULL DEFAULT NULL"
            db.executeSQL(sql)
        # if

        # update column within permission record
        sql = "update detected_unknown_permissions set " + index + " = 'X' where id = " + str(trojan)
        db.executeSQL(sql)
    # for

    print(str(addedCols) + " columns added.")
    print(str(updatedCols) + " columns updated.\n")

# Generate mitre matrix
def generateMitreMatrix(sample_set):
    FILE_PATH = 'Output\\Mitre-Matrix.xlsx'
    
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