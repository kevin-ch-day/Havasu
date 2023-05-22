# Zorivis.py
# Author: kevin.ch.day@gmail.com
# Android Permissions: https://developer.android.com/reference/android/Manifest.permission
# Date last updated: 5/20/2023

import mysql.connector
import pandas as pd
import random

def startDBConn():
    """ Connect to MySQL database """
    try:
        global db_connection
        global db_cursor

        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            #password="",
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
    sql = "select max(scan_id) from detected_standard_permissions"
    db_cursor.execute(sql)
    result = db_cursor.fetchall()
    if result[0][0] == None:
        return str(1000) # Default starting scan id
    else:
        return str(result[0][0] + 1) 
    # if
# function

# read detected permission from text file
def readDetectedPermissionInput():
    f = open("INPUT\\DATA_PERMISSION_INPUT.txt", "r")
    temp = list()
    
    for line in f:
        temp.append(line.strip())
    # for

    return temp
# function

# create scan record for trojan id
def createPermissionRecord(scanId, trojan):
    print("Scan ID:", scanId, " Trojan ID: ", trojan, "\n")

    sql = "INSERT INTO detected_standard_permissions (scan_id, trojan_id ) VALUES (%s, %s)"
    val = (scanId, trojan)
    db_cursor.execute(sql, val)
    db_connection.commit()
# function

def classifyPermissions(scan, trojan, permissions):
    standardFormatPerms = list()
    unknownPermissions = list()
    unknownPermissionsFound = False
    numUnknownPermissions = 0
    numStandardPermissions = 0

    for index in permissions:

        # check if permission matches the standard permission formatted
        if "android.permission." in index:
            standardFormatPerms.append(index)
            #print("Permission: " + index) # DEBUGGING
            numStandardPermissions = 1 + numStandardPermissions
        else:
            unknownPermissions.append(index)
            unknownPermissionsFound = True
        # if
    # for
    print("Standard Permissions found: "+ str(numStandardPermissions)) # new line

    if unknownPermissionsFound:
        numUnknownPermissions = 0
        f = open("OUTPUT\\UnknownPermissionFound.txt", "w")
        try:
           for index in unknownPermissions:
                #print(index) # debugging
                f.write(index + "\n")
                numUnknownPermissions = 1 + numUnknownPermissions
            # for
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit()
        # try
        print("Unknown Permissions found: "+ str(numUnknownPermissions))
    # if

    recordAndroidPermissions(scan, trojan, standardFormatPerms)
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
        if 'scan_id' == i[0] or 'trojan_id' == i[0]:
            pass
        else:
            permissionList.append(i[0])
    # for

    return permissionList
# function

# Record Android Permissions
def recordAndroidPermissions(scanId, trojan, permissions):
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
                sql = sql + slicedPermissions + " = 'X' WHERE scan_id = " + scanId
                db_cursor.execute(sql)
                db_connection.commit()
                updatedColumns = updatedColumns + 1
            except mysql.connector.Error as err:
                print("[!!] MySQL Error: {}".format(err))
                exit()
            # try
        # if
    # for
    print()

    print("#1 - Standard permission columns.")
    print(str(updatedColumns) + " columns updated.")

    #recordUnknownPermissions(scanId, trojan, unknownPermissions)
# function

def recordUnknownPermissions(scanId, trojan, unknownPermissions):
    tableColumns = list()
    columnsAdded = 0
    columnsUpdate = 0

    sql = "show columns from detected_other_permissions"
    db_cursor.execute(sql)
    dbResults = db_cursor.fetchall()
    if not dbResults:
        print("[!!] - No columns retrieved from: detected_other_permissions")
        exit()
    # if

    for i in dbResults:
        if 'scan_id' == i[0] or 'trojan_id' == i[0]:
            pass
        else:
            tableColumns.append(i[0])
        # if
    # for
    #print(unknownPermissions) # DEBUGGING

    # Display Non-Standard Permissions
    sql = "INSERT INTO detected_other_permissions (scan_id, trojan_id ) VALUES (%s, %s)"
    val = (scanId, trojan)
    try:
        db_cursor.execute(sql, val)
        db_connection.commit()
    except mysql.connector.Error as err:
        print("[!!] MySQL Error: {}".format(err))
    # try

    print("#2 - Non-standard permissions columns.")
    for index in unknownPermissions:
        if index not in tableColumns:

            # add new columns to table: detected_other_permissions
            print(index) # DEBUGGING
            sql = "ALTER TABLE detected_other_permissions add " + index + " VARCHAR(1) NULL DEFAULT NULL"
            try:
                db_cursor.execute(sql)
                db_connection.commit()
                columnsAdded = columnsAdded + 1

            except mysql.connector.Error as err:
                print("[!!] MySQL Error: {}".format(err))
            # try
        # if

        # update column within permission record
        sql = "update detected_other_permissions set " + index + " = 'X' where scan_id = " + scanId
        try:
            db_cursor.execute(sql)
            db_connection.commit()
            columnsUpdate = columnsUpdate + 1

        except mysql.connector.Error as err:
            print("[!!] MySQL Error: {}".format(err))
        # try
    # for

    print(str(columnsAdded) + " columns added.")
    print(str(columnsUpdate) + " columns updated.\n")
# function