# main.py
from .utils import *
import os

# main
def run():
    while True:
        mainMenu()
        menuChoice = input("\nEnter choice: ")      
        if menuChoice == "0": # Exit application
            print("Exiting application")
            exit(0)

        elif menuChoice == "1": # chech hash
            hash = input("Enter hash: ")
            checkHash(hash)

        elif menuChoice == "2": # Record Data
            recordData()

        elif menuChoice == "3": # Generate Data
            generateData()

        elif menuChoice == "4": # Permission Data
            permissionData()

        elif menuChoice == "5": # Mitre Attack Data
            mitreAttackData()

        elif menuChoice == "6": # Main menu
            return
        
        else:
            print("Invalid menu selection.")

# menu
def mainMenu():
    print("\nData Menu")
    print("----------------------------")
    print(" 1 - Check Hash")
    print(" 2 - Record Sample Data")
    print(" 3 - Generate Sample Data")
    print(" 4 - Permission Data")
    print(" 5 - Mitre Att&ck Data")
    print(" 6 - Main Menu")
    print(" 0 - Exit")

def recordData():
    while True:
        print("\nRecord Sample Data")
        print("----------------------------")
        print(" 1 - Create sample record")
        print(" 2 - Record permission data")
        print(" 3 - Record mitre att&ck data")
        print(" 4 - Return to data menu")

        choice = input("\nEnter choice: ")
        if choice == "1": # create sample record
            createSampleRecord()
        
        elif choice == "2": # record permission data
            recordSamplePermissions()
        
        elif choice == "3": # record mitre att&ck data
            readMitreData()

        elif choice == "4": # return to menu
            return

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
        if checkSamplePermissionIdRecords(sample_id):
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

def deleteSampleRecords(sample_id):
    sql = "DELETE FROM detected_standard_permissions WHERE id = '"+sample_id+"'"
    executeSQL(sql)

    sql = "DELETE FROM detected_unknown_permissions WHERE id = '"+sample_id+"'"
    executeSQL(sql)
    
    print("Sample ID: " + sample_id + " deleted.")

# check if sample id record exists in permission tables
def checkSampleIdRecord(sample_id):
    recordExists = False

    # check detected_standard_permissions table
    sql = "select id from malware_samples where id = '" + sample_id + "'"
    results = query_data(sql)
    if results[0][0]:
        recordExists = True

    return recordExists

# check if sample id record exists in permission tables
def checkSamplePermissionIdRecord(sample_id):
    recordExists = False

    # check detected_standard_permissions table
    sql = "select id from detected_standard_permissions where id = '" + sample_id + "'"
    results = query_data(sql)
    if results[0][0]:
        recordExists = True
    
    # check detected_unknown_permissions table
    sql = "select id from detected_unknown_permissions where id = '" + sample_id + "'"
    results = query_data(sql)
    if results[0][0]:
        recordExists = True

    return recordExists
    
def createSampleRecord():
    pass

# check if permission input file exists
def checkPermissionInput():
    permissionInputPath = "Input\APK_PERMISSIONS.txt"
    result = os.path.isfile(permissionInputPath)
    return result

def createPermissionRecord(id):
    # create sample id record
    createSampleIdPermissionRecord(id)

    # get detected apk permissions
    permissions = readDetectedPermissionsInput()
    permissions.sort()
    
    # record sample permissions
    recordSamplePermissions(id, permissions)

def generateData():
    while True:
        print("\nGenerate Data")
        print("----------------------------")
        print(" 1 - Sample/family data")
        print(" 2 - Permission data")
        print(" 3 - Mitre Att&ck data")
        print(" 4 - Menu return")

        choice = input("\nEnter choice: ")
        if choice == "1": # sample/family data
            sampleData()

        elif choice == "2": # permission data
            permissionData()
        
        elif choice == "3": # mitre att&ck data
            mitreAttackData()

        elif choice == "4": # return to menu
            return

def sampleData():
    pass

def permissionData():
    pass

def mitreAttackData():
    populateMitreMatrixTable()