import Havasu
import sys, getopt

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
    inputfile = ''
    outputfile = ''
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

    for opt, arg in opts:
        
        if opt == '-h': # Help
           print ('test.py -i <inputfile> -o <outputfile>')
           sys.exit()

        elif opt in ("-i", "--ifile"): # Input
            inputfile = arg

        elif opt in ("-o", "--ofile"): # Output
            outputfile = arg
        # if
    # for
    
    print ('Input file is ', inputfile)
    print ('Output file is ', outputfile)

    ANUBIS = "(55, 80, 81, 83, 103, 104, 105)"
    FLUBOT = "(8, 9, 10, 11, 21, 22, 29, 30, 31, 32, 33, 34, 35, 36, 37)"
    SOVA = "(44, 45, 114, 115)"
    BRATA = "(6, 7, 18, 19, 20, 117, 118)"
    VULTAUR = "(1, )"

    trojan_sample_id = 80
    sample_set = ANUBIS

    generatePermissionAnalysis(sample_set)
# main

if __name__ == "__main__":
   main(sys.argv[1:])
# if