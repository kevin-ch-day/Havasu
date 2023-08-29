import Havasu

Havasu.startDBConn() # start database connection

<<<<<<< HEAD
TROJAN = 85
=======
TROJAN = 1
>>>>>>> c93f3aed4f0bb5fa9558c034334597fd9a36292b
permissions = Havasu.readDetectedPermissions()
permissions.sort()

# create trojan record for permissions
Havasu.createPermissionRecord(TROJAN)

# update record for permissions with detected permissions
Havasu.classifyPermissions(TROJAN, permissions)

# end database connection
Havasu.endDBConn()