# run.py
# Driver for Havasu

from havasu import *
import sys

# Application version number
def version():
    h = Havasu()
    print("Havasu version " + h.versionNumber())
# function

# Record sample permissions
def recordSamplePermissions():

    # prompt to enter sample id
    userSampleIdInput = input("Enter sample id: ")

    if not isinstance(userSampleIdInput, int):
        print("[!!] Error: sample id input not an interger")
        exit(-1)
    # if

    TROJAN_ID = int(userSampleIdInput) # convert to integer
    
    # If no permissions records exist
    if not Havasu.checkPermissionRecords(TROJAN_ID):

        print("** Reading Permission Data")
        permissions = Havasu.readDetectedPermissions()
        permissions.sort()

        print("** Creating permission records")
        Havasu.createPermissionRecord(TROJAN_ID)
        Havasu.classifyPermissions(TROJAN_ID, permissions)

    # If permissions records exist
    else:
        print("Premission records exist for " + str(TROJAN_ID))

        # promot user if the want to delete permission record
        userDeletionInput = input("Do you want to delete permission records? (yes/no): ")
        if userDeletionInput.upper() == "Y" or userDeletionInput.upper() == "YES":
            # delete permissions record for given trojan id
            pass
        # if
    # if
# function

# Generate permission analysis matrix
def generatePermissionAnalysis():
    SAMPLE_SET = None
    TROJAN_FAMILY = None

    print("** Generating Permission Matrix")
    #Havasu.outputStandardPermissions(SAMPLE_SET)
    #Havasu.outputUnknownPermissions(SAMPLE_SET)
    #Havasu.outputNormalPermissions(SAMPLE_SET)
# function

# Reading mitre data
def readMitreData():
    print("** Reading Mitre Data")
    h = Havasu()
    h.readMitreData()
# function

# Generate mitre matrix
def generateMitreMatrix():
    print("** Generating Mitre Matrix")
# function

# Checking hash
def checkHash(hash):
    print("** Cheching hash")
    print("Hash: " + hash + "\n")
    h = Havasu()
    h.checkHash(hash)
# function

def decompileAPK():
    print("** Decompiling APK file")
# function

# main()
def main(argv):
    #print("# command line args: " + str(len(argv))) # DEBUGGING

    # Check if no argument were supplied
    if len(argv) == 0:
        exit()

    # Show help and useage command
    elif argv[0] == '-h' or argv[0] == "--help":
        print("usage: havasu")
        print("-d, --decompile Decompile APK")
        print("-h, --help Show help commands and usage\n")
        print("-i, --input Read data from INPUT directory")
        print("-------------------------------------------")
        print("\t-p, --permissions Read permission data")
        print("\t-m, --mitre Read mitre .xlsx data\n")
        print("-o, --output Write data to OUTPUT directory")
        print("-------------------------------------------")
        print("\t-p, --permissions Permission matrix\n")
        print("--hash Check hash against database")

    # Decompile APK command
    elif argv[0] == '-d' or argv[0] == '--decompile':
        decompileAPK()

    # Data input command
    elif argv[0] == '-i' or argv[0] == '--input':

        # permission data
        if argv[1] == '-p' or argv[1] == '--permisions':
            recordSamplePermissions()

        # mitre data
        if argv[1] == '-m' or argv[1] == '--mitre':
            readMitreData()
        # if

    # Data output command
    elif argv[0] == '-o' or argv[0] == '--output':

        # permission data
        if argv[1] == '-p' or argv[1] == '--permisions':
            generatePermissionAnalysis()

        # mitre data
        if argv[1] == '-m' or argv[1] == '--mitre':
            generateMitreMatrix()
        # if

    # Display version number
    elif argv[0] == '-v' or argv[0] == '--version':
        version()

    # Check hash against database
    elif argv[0] == '--hash':
        checkHash(argv[1])
    
    # Unknown command
    else:
        print("Error: unknown command\n")
    # if
# main

if __name__ == "__main__":
   main(sys.argv[1:]) # run app
# if