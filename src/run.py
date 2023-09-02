import Havasu

def recordSamplePermissions(trojan_id):
    Havasu.startDBConn() 

    permissions = Havasu.readDetectedPermissions()
    permissions.sort()

    Havasu.createPermissionRecord(trojan_id)
    Havasu.classifyPermissions(trojan_id, permissions)

    Havasu.endDBConn()
# function

def generatePermissionAnalysis(sample_set):
    Havasu.startDBConn()
    Havasu.outputStandardPermissions(sample_set)
    Havasu.outputUnknownPermissions(sample_set)
    Havasu.outputNormalPermissions(sample_set)
    Havasu.endDBConn()
# function

def generateMitreMatrix(sample_set):
    pass
# function

def main():
    ANUBIS = "(55, 80, 81, 83, 103, 104, 105)"
    FLUBOT = "(8, 9, 10, 11, 21, 22, 29, 30, 31, 32, 33, 34, 35, 36, 37)"
    SOVA = "(44, 45, 114, 115)"
    BRATA = "(6, 7, 18, 19, 20, 117, 118)"
    VULTAUR = "(1, )"

    trojan_sample_id = 80
    sample_set = ANUBIS

    generatePermissionAnalysis(sample_set)
# main

main()