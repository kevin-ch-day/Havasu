# main.py
import os

from Server import utils
from Server import database

# main
def run():
    while True:
        mainMenu()
        menuChoice = input("Enter choice: ")      
        if menuChoice == "0": # Exit application
            print("Exiting application")
            exit(0)

        elif menuChoice == "1": # chech hash
            hash = input("Enter hash: ")
            if not hash or hash == "\n":
                print("[!!] Input error")
            else:
                utils.checkHash(hash)

        elif menuChoice == "2": # View Data
            viewData()

        elif menuChoice == "3": # Record Data
            recordData()

        elif menuChoice == "4": # Generate Data
            generateData()

        elif menuChoice == "5": # Main menu
            return
        
        else:
            print("Invalid menu selection.")

# menu
def mainMenu():
    print("\n*** Data Menu ***")
    print(" 1 - Check Hash")
    print(" 2 - View Data")
    print(" 3 - Record Data")
    print(" 4 - Generate Data")
    print(" 5 - Main Menu")
    print(" 0 - Exit")

def recordData():
    while True:
        print("\n** Record Sample Data **")
        print(" 1 - Create sample record")
        print(" 2 - Record sample permissions")
        print(" 3 - Record mitre att&ck data")
        print(" 4 - Return to data menu")

        choice = input("Enter choice: ")
        if choice == "1": # create sample record
            createSampleRecord()
        
        elif choice == "2": # record permission data
            recordSamplePermissions()
        
        elif choice == "3": # record mitre att&ck data
            utils.readMitreData()

        elif choice == "4": # return to menu
            return

def viewData():
    print("*** View Data ***")

# Record Apk Permissions
def recordSamplePermissions():

	# check if permission input file exists
    if not checkPermissionInput():
        print("Error: permission input does not exists")
        return
    
    else:
        # prompt user for sample id
        sample_id = input("Enter sample id: ")

        # check if permission records exists for sample id
        if utils.checkSamplePermissionIdRecords(sample_id):
            print("\nRecord exist for sample: " + str(sample_id))
            userChoice = input("Overwrite records for sample? (y/n): ")
            
            # delete sample id permission records
            if userChoice.lower() == "y":
                deleteSampleRecords(sample_id)
                createPermissionRecord(sample_id)

            # dont delete records, exit
            elif userChoice.lower() == "n":
                return None
            
        # no record for sample id exists   
        else:
            createPermissionRecord(sample_id)

# delete sample permission records
def deleteSampleRecords(sample_id):
    sql = "DELETE FROM detected_standard_permissions WHERE id = '"+sample_id+"'"
    database.executeSQL(sql)

    sql = "DELETE FROM detected_unknown_permissions WHERE id = '"+sample_id+"'"
    database.executeSQL(sql)
    
    print("Sample ID: " + sample_id + " deleted.")

# check if sample id record exists in permission tables
def checkSampleIdRecord(sample_id):
    recordExists = False

    # check detected_standard_permissions table
    sql = "select id from malware_samples where id = '" + sample_id + "'"
    results = database.query_data(sql)
    if results[0][0]:
        recordExists = True

    return recordExists

# check if sample id record exists in permission tables
def checkSamplePermissionIdRecord(sample_id):
    recordExists = False

    # check detected_standard_permissions table
    sql = "select id from detected_standard_permissions where id = '" + sample_id + "'"
    results = database.query_data(sql)
    if results[0][0]:
        recordExists = True
    
    # check detected_unknown_permissions table
    sql = "select id from detected_unknown_permissions where id = '" + sample_id + "'"
    results = database.query_data(sql)
    if results[0][0]:
        recordExists = True
 
    return recordExists

# create sample record
def createSampleRecord():
    # prompt user
    name = input("Enter sample name: ")
    family = input("Enter sample name: ")
    md5 = input("Enter sample name: ")

    if name.isnumeric():
        print("Error: name is numeric")
        return

    if family.isnumeric():
        print("Error: family is numeric")
        return

    if md5.isnumeric():
        print("Error: md5 is numeric")
        return

    # create sql
    sql = "INSERT INTO malware_samples (Name, Family, MD5) VALUES (%s, %s, %s)"
    values = (name, family, md5)
    database.executeSQL(sql, values)

# check if permission input file exists
def checkPermissionInput():
    permissionInputPath = "Input\APK_PERMISSIONS.txt"
    result = os.path.isfile(permissionInputPath)
    return result

def createPermissionRecord(id):
    # create sample id record
    utils.createSampleIdPermissionRecord(id)

    # get detected apk permissions
    permissions = utils.readDetectedPermissionsInput()
    permissions.sort()
    
    # record sample permissions
    utils.writeSamplePermissionData(id, permissions)

# Data generation menu
def generateData():
    while True:
        print("\n*** Generate Data ***")
        print(" 1 - Sample/family data")
        print(" 2 - Permission data")
        print(" 3 - Mitre Att&ck data")
        print(" 4 - Menu return")

        choice = input("Enter choice: ")
        if choice == "1": # sample/family data
            sampleData()

        elif choice == "2": # permission data
            permissionData()
        
        elif choice == "3": # mitre att&ck data
            mitreAttackData()

        elif choice == "4": # return to menu
            return

# Sample data generation
def sampleData():
    pass

# Permission data generation menu
def permissionData():
    print("\n*** Permission Data ***")
    print("1 - Family")
    print("2 - Sample ids")
    print("0 - Return to menu")
    userChoice = input("Choice: ")

    if userChoice == "0":
        return # data menu
    
    elif userChoice == "1": # family
        familyInput = input("Enter family: ")
        family = familyInput.strip()
        sample_set = utils.getFamilySampleSet(family)

    elif userChoice == "2": # samples
        samplesInput = input("Enter samples: ")
        sample_set = tuple(samplesInput.split())

    print() # newline
    utils.outputStandardPermissions(sample_set)
    utils.outputUnknownPermissions(sample_set)

    utils.outputNormalPermissions(sample_set)
    utils.outputDangerousPermissions(sample_set)

# Mitre Attack Data
def mitreAttackData():
    utils.populateMitreMatrixTable()
