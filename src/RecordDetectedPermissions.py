import Zorivis

Zorivis.startDBConn() # start database connection

TROJAN = 100
SCAN_ID = Zorivis.getNewScanId() # create scan id #

permissions = Zorivis.readDetectedPermissions()
permissions.sort()

# create trojan record for permissions
Zorivis.createPermissionRecord(SCAN_ID, TROJAN)

# update record for permissions with detected permissions
Zorivis.classifyPermissions(SCAN_ID, TROJAN, permissions)

# end database connection
Zorivis.endDBConn()