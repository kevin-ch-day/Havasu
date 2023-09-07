# Havasu.py

import mysql.connector
import pandas as pd

__version__ = "1.0.0"

def __init__(self):
   self.startDBConn()
# construction

def __del__(self):
    self.endDBConn()
# destructor

def startDBConn(self):
    """ Connect to MySQL database """
    try:
        global db_connection
        global db_cursor

        SERVER = "localhost"
        USER_NAME = "root"
        DATABASE_NAME = "cyberops_capstone_android"
        PORT_NUMBER = 3306

        db_connection = mysql.connector.connect(
            host=SERVER,
            user=USER_NAME,
            #password="",
            database = DATABASE_NAME,
            port = PORT_NUMBER)

        if not db_connection.is_connected():
            print("Cannot connected to data.\n")
            exit()
        # if
        db_cursor = db_connection.cursor()

    except Exception as e:
        print("[!!]- Error start database connection.\n")
        print(str(e))
    # try
# function

def endDBConn():
    """ disconnect to MySQL database """
    try:
        db_connection.close()
    except Exception as e:
        print("[!!]- Error ending database connection.\n")
        print(str(e))
    # try
# function

def versionNumber():
    return __version__
# function

# read detected permission from text file
def readDetectedPermissions():
    fPERMISSION_INPUT = open("INPUT\\APK_PERMISSIONS.txt", "r")
    buff = list()
    for p in fPERMISSION_INPUT:
        buff.append(p.strip())
    # for

    return buff
# function

# create scan record for trojan id
def createPermissionRecord(trojan):
    print("Trojan ID: ", trojan, "\n")
    sql = "INSERT INTO detected_standard_permissions (id) VALUES (%s)"
    val = (trojan, )
    db_cursor.execute(sql, val)
    db_connection.commit()
# function

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
# function

# Standard Android Permissions
# Android Permissions: https://developer.android.com/reference/android/Manifest.permission
def getStandardAndroidPermissionList():
    permissionList = list()

    db_cursor.execute("show columns from detected_standard_permissions")
    results = db_cursor.fetchall()
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

def recordNonStandardPermissions(trojan, unknownPermissions):
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

def outputStandardPermissions(sample_set):
  EXCEL_FILE = 'OUTPUT\\Android-Permissions.xlsx'
  
  sql = "select * from detected_standard_permissions "
  sql = sql + " where id in " + str(sample_set)
  sql = sql + " order by id"

  sql_query = pd.read_sql_query(sql, db_connection)
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

def outputUnknownPermissions(sample_set):
  EXCEL_FILE = 'OUTPUT\\Unknown-Permissions.xlsx'

  sql = "select * from detected_unknown_permissions "
  sql = sql + " where id in " + sample_set
  sql = sql + " order by id"

  sql_query = pd.read_sql_query(sql, db_connection)
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

## NORMAL PERMISSIONS
def outputNormalPermissions(sample_set):
  EXCEL_FILE = 'OUTPUT\\Normal-Permissions.xlsx'

  sql = "select name from android_permissions where Protection_level = 'Normal' order by name"
  db_cursor.execute(sql)
  results = db_cursor.fetchall()
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
  db_cursor.execute(sql)
  results = db_cursor.fetchall()
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

  sql_query = pd.read_sql_query(sql, db_connection)
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

def generateMitreMatrix(sample_set):
    EXCEL_FILE = 'OUTPUT\\Mitre-Matrix.xlsx'
    
    sql = "select * from mitre_matrix "
    sql = sql + " where trojan_id in " + sample_set
    sql = sql + " order by trojan_id"

    df_raw = pd.read_sql_query(sql, db_connection)

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

def addHashes():
    hashes = list()

    f = open('INPUT\\newHashes.txt')
    for i in f:
        hashes.append(i.strip())
    # for

    if checkHashes(hashes):
        print("Existing Hashes: ")
        for i in hashes:
            print(i)
        # for
        exit()
    # if

    sql = "select max(id) from malware_samples"
    db_cursor.execute(sql)
    x = db_cursor.fetchall()
    currentID = x[0][0]
    values = list()

    sql = "insert into malware_samples (id, md5) values (%s, %s)"
    for i in hashes:
        currentID = currentID + 1
        values.append((currentID, i))
    # for

    db_cursor.executemany(sql, values)
    db_connection.commit()

    if (db_cursor.rowcount) == 0:
        print("No records inserted.")
    elif(db_cursor.rowcount == 1):
        print(db_cursor.rowcount, "record inserted.")
    else:
        print(db_cursor.rowcount, "records inserted.")
    # if
# main


def checkHash(hash):
    sql = "select md5 from malware_samples where md5 = '" + hash + "'"
    db_cursor.execute(sql)
    results = db_cursor.fetchall()
    print("MD5")
    print(results)

    sql = "select sha1 from malware_samples where sha1 = '" + hash + "'"
    db_cursor.execute(sql)
    results = db_cursor.fetchall()
    print("SHA1")
    print(results)

    sql = "select sha256 from malware_samples where sha256 = '" + hash + "'"
    db_cursor.execute(sql)
    results = db_cursor.fetchall()
    print("SHA256")
    print(results)
# end

def generateMalwareSampleData(sample_set):
    EXCEL_FILE = "OUTPUT\\Output-Excel.xlsx"
    sql = "SELECT * FROM malware_samples WHERE family = 'Vultur'"
    #sql = "SELECT * FROM mobfs_analysis WHERE id in (66, 67, 68, 69)"
    df = pd.read_sql_query(sql, db_cursor)
    df.to_excel(EXCEL_FILE)
# function
