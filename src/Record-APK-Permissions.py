import Havasu

Havasu.startDBConn() # start database connection

TROJAN = 11
permissions = Havasu.readDetectedPermissions()
permissions.sort()

# create trojan record for permissions
Havasu.createPermissionRecord(TROJAN)

# update record for permissions with detected permissions
Havasu.classifyPermissions(TROJAN, permissions)

# end database connection
Havasu.endDBConn()