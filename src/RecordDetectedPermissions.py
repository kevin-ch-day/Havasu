import Zorivis

Zorivis.startDBConn() # start database connection

TROJAN = 60
SCAN_ID = Zorivis.getNewScanId() # create scan id #

permissions = Zorivis.readDetectedPermissionInput()
permissions.sort()

# create trojan record for permissions
Zorivis.createPermissionRecord(SCAN_ID, TROJAN)

# update record for permissions with detected permissions
Zorivis.classifyPermissions(SCAN_ID, TROJAN, permissions)

# end database connection
Zorivis.endDBConn()