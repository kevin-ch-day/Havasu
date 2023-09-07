from havasu import *
import sys

def recordSamplePermissions():
    TROJAN_ID = None

    # check if permissions records already exist

    permissions = Havasu.readDetectedPermissions()
    permissions.sort()
    Havasu.createPermissionRecord(TROJAN_ID)
    Havasu.classifyPermissions(TROJAN_ID, permissions)
# function

def generatePermissionAnalysis():
    SAMPLE_SET = None
    TROJAN_FAMILY = None

    Havasu.outputStandardPermissions(SAMPLE_SET)
    Havasu.outputUnknownPermissions(SAMPLE_SET)
    Havasu.outputNormalPermissions(SAMPLE_SET)
# function

def generateMitreMatrix(sample_set):
    pass
# function

def main(argv):
    #print("# command line args: " + str(len(argv))) # DEBUGGING

    # Check number of terminal arguments
    if len(argv) == 0:
        exit()

    # Show help and useage command
    elif argv[0] == '-h' or argv[0] == "--help":
        print("usage: havasu")
        print("-d, --decompile Decompile APK")
        print("-h, --help Show help commands and usage")
        print("-i, --input Read data from INPUT directory")
        print("\t-p, --permissions Read permission data")
        print("\t-m, --mitre Read mitre .xlsx data")
        print("-o, --output Write data to OUTPUT directory")
        print("\t-p, --permissions Permission matrix")
        print("--hash Check hash against database")

    # Decompile command
    elif argv[0] == '-d' or argv[0] == '--decompile':
        print(argv[1])

    # Data input command
    elif argv[0] == '-i' or argv[0] == '--input':

        # permission data
        if argv[1] == '-p' or argv[1] == '--permisions':
            print("Reading Permission Data")
            #recordSamplePermissions()

        # mitre data
        if argv[1] == '-m' or argv[1] == '--mitre':
            print("Read Mitre Data")
        # if

    # Data output command
    elif argv[0] == '-o' or argv[0] == '--output':

        # permission data
        if argv[1] == '-p' or argv[1] == '--permisions':
            print("Generating Permission Matrix")
            #generatePermissionAnalysis()

        # mitre data
        if argv[1] == '-m' or argv[1] == '--mitre':
            print("Generating Mitre Matrix")
        # if

    # Version number
    elif argv[0] == '-v' or argv[0] == '--version':
        h = Havasu()
        print("Havasu version " + h.versionNumber())

    # Check hash against database
    elif argv[0] == '--hash':
        h = Havasu()
        h.checkHash(argv[1])
    
    # Unknown command
    else:
        print("Error: unknown command\n")
    # if

    ANUBIS = "(55, 80, 81, 83, 103, 104, 105)"
    FLUBOT = "(8, 9, 10, 11, 21, 22, 29, 30, 31, 32, 33, 34, 35, 36, 37)"
    SOVA = "(44, 45, 114, 115)"
    BRATA = "(6, 7, 18, 19, 20, 117, 118)"
    VULTAUR = "(1, )"

    trojan_sample_id = 80
    sample_set = ANUBIS

    #generatePermissionAnalysis(sample_set)
# main

if __name__ == "__main__":
   main(sys.argv[1:])
# if