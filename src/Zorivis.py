# Zorivis.py
# Author: kevin.ch.day@gmail.com
# Date last updated: 8/10/2023
#
# Android Permissions Source: https://developer.android.com/reference/android/Manifest.permission

import mysql.connector
import pandas as pd

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

# read detected permission from text file
def readDetectedPermissions():
    fPERMISSION_INPUT = open("INPUT\\DATA_PERMISSION_INPUT.txt", "r")
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
        fUnknownPermissions = open("OUTPUT\\"+trojan+"-UnknownPerms.txt", "w")
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

    recordUnknownPermissions(trojan, unknownPermissions)
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
    dbColumns = list()
    newColumns = updatedColumns = 0

    sql = "show columns from detected_other_permissions"
    db_cursor.execute(sql)
    dbResults = db_cursor.fetchall()
    if not dbResults:
        print("[!!] - No columns retrieved from: detected_other_permissions")
        exit()
    # if

    for i in dbResults:
        if 'id' == i[0]:
            pass
        else:
            dbColumns.append(i[0])
        # if
    # for
    #print(unknownPermissions) # DEBUGGING

    # Display Non-Standard Permissions
    sql = "INSERT INTO detected_other_permissions (id) VALUES (%s)"
    val = (trojan, )
    try:
        db_cursor.execute(sql, val)
        db_connection.commit()
    except mysql.connector.Error as err:
        print("[!!] MySQL Error: {}".format(err))
    # try

    print("\n** Non-standard permissions columns **")
    for index in unknownPermissions:
        if index not in dbColumns:
            # add new columns to table: detected_other_permissions
            print(index) # DEBUGGING
            sql = "ALTER TABLE detected_other_permissions add " + index + " VARCHAR(1) NULL DEFAULT NULL"
            try:
                db_cursor.execute(sql)
                db_connection.commit()
                newColumns = newColumns + 1

            except mysql.connector.Error as err:
                print("[!!] MySQL Error: {}".format(err))
            # try
        # if

        # update column within permission record
        sql = "update detected_other_permissions set " + index + " = 'X' where id = " + str(trojan)
        try:
            db_cursor.execute(sql)
            db_connection.commit()
            updatedColumns = updatedColumns + 1

        except mysql.connector.Error as err:
            print("[!!] MySQL Error: {}".format(err))
        # try
    # for

    print(str(updatedColumns) + " columns added.")
    print(str(updatedColumns) + " columns updated.\n")
# function

def recordUnknownPermissions(trojan, unknownPermissions):
    print("\n** Recording unknown Android permissions **")
    sql = "INSERT INTO detected_unknown_permissions (id, permission_name) VALUES (%s, %s)"
    for i in unknownPermissions:
        val = (trojan, i)
        db_cursor.execute(sql, val)
    # for
# function