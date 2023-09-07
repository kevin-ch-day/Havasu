from havasu import *
import sys

def recordSamplePermissions(trojan_id):
    permissions = Havasu.readDetectedPermissions()
    permissions.sort()
    Havasu.createPermissionRecord(trojan_id)
    Havasu.classifyPermissions(trojan_id, permissions)
# function

def generatePermissionAnalysis(sample_set):
    Havasu.outputStandardPermissions(sample_set)
    Havasu.outputUnknownPermissions(sample_set)
    Havasu.outputNormalPermissions(sample_set)
# function

def generateMitreMatrix(sample_set):
    pass
# function

def main(argv):
    #print("# command line args: " + str(len(argv))) # DEBUGGING

    # Check number of terminal arguments
    if len(argv) == 0:
        exit()

    # Show help and usgae command
    elif argv[0] == '-h' or argv[0] == "--help":
        print("usage: havasu")
        print("-d, --decompile\tDecompile APK")
        print("-h, --help\tShow help commands and usage")
        print("--hash\t\tCheck hash against database")

    # Decompile command
    elif argv[0] == '-d' or argv[0] == '--decompile':
        print(argv[1])

    # Data input command
    elif argv[0] == '-i' or argv[0] == '--input':
        print(argv[1])

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