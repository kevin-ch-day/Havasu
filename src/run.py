# run.py
# Driver for Havasu

import havasu
import sys

# Application version number
def version():
    print("Havasu version " + havasu.version())
# function

# Record sample permissions
def recordSamplePermissions():

    # prompt to enter sample id
    input_sample_id = input("Enter sample id: ")
    
    try:
        testInput = int(input_sample_id) # convert to integer
        if testInput <= 0:
            print("ID cannot be zero or lower")
        # if
    except ValueError as err:
        print("[!!] Error: sample id input not an interger")
        exit(-1)
    # try
    
    # If no permission records exist
    if not havasu.checkPermissionRecords(input_sample_id):

        print("** Reading Permission Data")
        permissions = havasu.readDetectedPermissions()
        permissions.sort()
        print(permissions)

        print("** Creating permission records")
        havasu.createPermissionRecord(input_sample_id)
        havasu.classifyPermissions(input_sample_id, permissions)

    # If permissions records exist
    else:
        print("Premission records exist for " + input_sample_id)

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

    havasu.readMitreData()
    havasu.populateMitreMatrixTable()
# function

# Generate mitre matrix
def generateMitreMatrix():
    print("** Generating Mitre Matrix")
# function

# Checking hash
def checkHash(hash):
    print("** Cheching hash")
    print("Hash: " + hash + "\n")
    havasu.checkHash(hash)
# function

def decompileAPK(apk):
    print("** Decompiling APK file")

    #Havasu.decompileAPK(apk)
    #Havasu.logPermissions(apk)
    #Havasu.analyzeAndroidManifest(apk)
    #Havasu.manifestToTxt(apk)
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
        print("-h, --help Show help commands and usage")
        print("--hash Check hash against database\n")
        print("-i, --input Read data from INPUT directory")
        print("-------------------------------------------")
        print("\t-p, --permissions Read permission data")
        print("\t-m, --mitre Read mitre .xlsx data\n")
        print("-o, --output Write data to OUTPUT directory")
        print("-------------------------------------------")
        print("\t-p, --permissions Permission matrix")
        print("\t-m, --mitre Mitre matrix\n")
        print("-v --version Show version number")

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