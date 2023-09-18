# main.py

import utils

# main
def main():
    while True:
        menu()
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

        elif menuChoice == 6: # MobSF Data
            mobSFData()

        elif menuChoice == 7: # Main menu
            return
        
        else:
            print("Invalid menu selection.")

# menu
def menu():
    print("1 - Check Hash")
    print("2 - Record Sample Data")
    print("3 - Generate Sample Data")
    print("4 - Permission Data")
    print("5 - Mitre Att&ck Data")
    print("6 - MobSF Data")
    print("7 - Main Menu")
    print("0 - Exit")

# Record Apk Permissions
def recordSamplePermissions():

	# check if permission input file exists
    if not utils.permissionInput():
        print("Error: permission input does not exists")
    
    else:
    
        sample_id = input("Enter sample id: ")

        # check if records exists for sample id
        if utils.checkSamplePermissionRecord(sample_id):
            print("Record exist for sample: " + str(sample_id))
            userChoice = input("Overwrite records for sample? (y/n) ")
            
            if userChoice.lower() == "y":
                # delete sample id permission records
                utils.deleteSampleRecords(sample_id)
                
            elif userChoice.lower() == "n":
                return None
                
            else:
                print("Invalid choice.")
                return None
        else:
        
            # create sample id record
            utils.createSampleIdPermissionRecord(sample_id)
            sample_permissions = utils.readDetectedPermissionsInput()
            sample_permissions.sort()
            utils.recordSampleIdPermissions(sample_id, sample_permissions)


def recordSampleData():
    # record sample data
    # record sample permissions
    # record sample mitre data
    # record sample mobSF data
    pass

def generateSampleData():
    # generate sample data
    # generate sample permission mitre
    # generate sample mitre data
    # generate sample mobSF data
    pass

def permissionData():
    pass

def mitreAttackData():
    pass

def mobSFData():
    pass

main()