# main.py

import utils

# main
def main():
    while True:
        mainMenu()
        menuChoice = input("Enter choice: ")
        
        if menuChoice == 0: # Exit application
            print("Exiting application")
            exit(0)

        elif menuChoice == 1: # chech hash
            hash = input("Enter hash: ")
            utils.checkHash(hash)

        elif menuChoice == 2: # Record Sample Data
            recordSampleData()

        elif menuChoice == 3: # Generate Sample Data
            generateSampleData()

        elif menuChoice == 4: # Permission Data
            permissionData()

        elif menuChoice == 5: # Mitre Attack Data
            mitreAttackData()

        elif menuChoice == 7: # Main menu
            return
        
        else:
            print("Invalid menu selection.")

# menu
def mainMenu():
    print("1 - Check Hash")
    print("2 - Record Sample Data")
    print("3 - Generate Sample Data")
    print("4 - Permission Data")
    print("5 - Mitre Att&ck Data")
    print("6 - Main Menu")
    print("0 - Exit")

# Record Apk Permissions
def recordSamplePermissions():

	# check if permission input file exists
    if not utils.permissionInput():
        print("Error: permission input does not exists")
    
    else:
        # prompt user for sample id
        sample_id = input("Enter sample id: ")

        # check if records exists for sample id
        if utils.checkSamplePermissionIdRecords(sample_id):

            # record exists for sample id
            print("Record exist for sample: " + str(sample_id))
            userChoice = input("Overwrite records for sample? (y/n) ")
            
            if userChoice.lower() == "y":
                # delete sample id permission records
                utils.deleteSampleRecords(sample_id)
                createPermissionRecord(sample_id)

            elif userChoice.lower() == "n":
                return None
            
        else:
            # no record for sample id exists
            createPermissionRecord(sample_id)

def recordSampleData():
    print()

def createPermissionRecord(id):
    # create sample id record
    utils.createSampleIdPermissionRecord(id)

    # get detected apk permissions
    permissions = utils.readDetectedPermissionsInput()
    permissions.sort()
    
    # record sample permissions
    utils.recordSamplePermissions(id, permissions)

def permissionData():
    pass

def mitreAttackData():
    pass

def mobSFData():
    pass

main()