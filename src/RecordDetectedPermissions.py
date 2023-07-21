import Zorivis

Zorivis.startDBConn() # start database connection

TROJAN = 110
permissions = Zorivis.readDetectedPermissions()
permissions.sort()

# create trojan record for permissions
Zorivis.createPermissionRecord(TROJAN)

# update record for permissions with detected permissions
Zorivis.classifyPermissions(TROJAN, permissions)

# end database connection
Zorivis.endDBConn()