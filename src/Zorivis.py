# Zorivis.py
# Author: kevin.ch.day@gmail.com
# Android Permissions: https://developer.android.com/reference/android/Manifest.permission
# Date last updated: 5/20/2023

import mysql.connector
import pandas as pd
import random

def startApp():
    print("** Zorivis App Started **")
# function

def startDBConn():
    """ Connect to MySQL database """
    try:
        global db_connection
        global db_cursor

        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            #password="Kombucha23",
            database = "cyberops_capstone_android",
            port = 3306)

        if not db_connection.is_connected():
            print("Cannot connected to data.\n")
            exit()
        # if

        db_cursor = db_connection.cursor()

    except Exception as e:
        print("[!]- Error start database connection.\n")
        print(str(e))
    # try
# function

def endDBConn():
    """ disconnect to MySQL database """
    try:
        db_connection.close()
    except Exception as e:
        print("[!]- Error ending database connection.\n")
        print(str(e))
    # try
# function

def getTrojanMetaData(id):
  sql = "select family, AhnLab_V3_Label"
  sql = sql + " from trojan_analysis_main"
  sql = sql + " where trojan_id = " + str(id)
  db_cursor.execute(sql)
  result = db_cursor.fetchall()
  return result[0]
# function

def getNewScanId():
    db_cursor.execute("select max(scan_id) from detected_standard_permissions")
    result = db_cursor.fetchall()
    if result[0][0] == None:
        return str(1000)
    else:
        return str(result[0][0] + 1) 
    # if
# function

def readDetectedPermissions():
    f = open("INPUT\\DATA_PERMISSION_INPUT.txt", "r")
    temp = list()
    for line in f:
        temp.append(line.strip())
    # for
    return temp
# function

def createPermissionRecord(scanId, trojan):
    print("Create new trojan permission record")
    print("Scan: ", scanId, " Trojan: ", trojan, "\n")

    sql = "INSERT INTO detected_standard_permissions (scan_id, trojan_id ) VALUES (%s, %s)"
    val = (scanId, trojan)
    db_cursor.execute(sql, val)
    db_connection.commit()
# function

def classifyPermissions(scan, trojan, permissions):
    print("Classifying detected trojan permissions")

    standardFormatPerms = list()
    # signatue = list() # signature permissions
    unknown = list()
    unknownFound = False

    for index in permissions:

        # check if permission matches the standard permission formatted
        if "android.permission." in index:
            standardFormatPerms.append(index)
        else:
            unknown.append(index)
            unknownFound = True
        # if
    # for

    if unknownFound:
        f = open("OUTPUT\\UnknownPermissionFound.txt", "w")
        try:
           for i in unknown:
                #print(i) # debugging
                f.write(i + "\n")
            # for
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()
        # try
    # if

    recordAndroidPermissions(scan, trojan, standardFormatPerms)
    #displayUnknownPermissions(scan, trojan, unknown)
# function

# Standard Android Permissions
# # Android Permissions: https://developer.android.com/reference/android/Manifest.permission
def getStandardAndroidPermissionList():
    db_cursor.execute("show columns from detected_standard_permissions")
    results = db_cursor.fetchall()
    if not results:
        print("[!!] - No permission columns retrieved from database.")
    else:
        return results
    # if
# function

# Record Android Permissions
def recordAndroidPermissions(scanId, trojan, permissions):
    print("Record detected premissions for Trojan ID: " + str(trojan))
    cnt = 0
    unknownPermissions = list()
    standardPermissionList = getStandardAndroidPermissionList()
    FORMAT_HEADER = len("android.permission.")

    for index in permissions:
        # if detectect permission is not a  standard Android permission
        if index not in standardPermissionList:
            unknownPermissions.append(index[FORMAT_HEADER:])

        # if no record exists within table
        else:
            sql = "UPDATE detected_standard_permissions SET " + index[FORMAT_HEADER:] + " = 'X' WHERE scan_id = " + scanId
            executeQuery(sql)
            cnt = cnt + 1
        # if
    # for

    print(str(cnt) + " permission columns updated.\n")
    recordUnknownPermissions(scanId, trojan, unknownPermissions)
# function

def recordUnknownPermissions(scanId, trojan, unknownPermissions):
    db_cursor.execute("show columns from detected_other_permissions")
    results = db_cursor.fetchall()
    if not results:
        print("[!!] - No columns retrieved from: detected_other_permissions")
        exit()
    # if

    unknownPermissions = list()
    for i in results:
        if 'scan_id' == i[0] or 'trojan_id' == i[0]:
            pass
        else:
            unknownPermissions.append(i[0])
        # if
    # for
      
    print(unknownPermissions) # DEBUGGING

    # Display Non-Standard Permissions
    sql = "INSERT INTO detected_other_permissions (scan_id, trojan_id ) VALUES (%s, %s)"
    val = (scanId, trojan)
    executeQuery(sql, val)
    db_connection.commit()

    cnt = 0
    for index in unknownPermissions:
        if index not in unknownPermissions:
            print(index)
            # add new columns to table: detected_other_permissions
            sql = "ALTER TABLE detected_other_permissions add " + index + " VARCHAR(1) NULL DEFAULT NULL"
            db_cursor.execute(sql)
            executeQuery(sql, None)
            db_connection.commit()
            print("New column added: " + index + ".\n")
            exit()
        # if

        # update column within permission record
        sql = "update detected_other_permissions set " + index + " = 'X' where scan_id = " + scanId
        executeQuery(sql, None)
        cnt = cnt + 1
    # for

    print(str(cnt) + " non-standard permissions recorded.\n")
# function

# function

# execute sql query
def executeQuery(sql, val):
    results = None
    try:
        if not val:
            results = db_cursor.execute(sql)
        else:     
            results = db_cursor.execute(sql, val)
        # if
        db_connection.commit()
    except mysql.connector.Error as err:
        print("[!!] MySQL Error: {}".format(err))
        exit()
    finally:
        return results
    # try
# function