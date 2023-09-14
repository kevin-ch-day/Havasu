# static.py

import os
import datetime
import zipfile

# main
def main():
    while True:
        staticMenu()
        menuChoice = input("\nSelect choice: ")
        menuChoice = int(menuChoice)
        
        # Exit application
        if menuChoice == 0:
            print("Exiting.")
            exit(0)
        
        # Display available apks
        elif menuChoice == 1:
            displayAvailableApks()

        # Decompile APK
        elif menuChoice == 2:
            decompileApk()
        
        # Convert APK to JAR
        elif menuChoice == 3:
            apkToJar()

        # Scan decompiled APK
        elif menuChoice == 4:
            scanApk()
        
        # Return to main menu
        elif menuChoice == 9:
            break
        
        # Invalid user selection
        else:
            print("Invalid Selected\n")
        # if
    # menu

# Static analysis menu
def staticMenu():
    print("\nStatic Analysis")
    print(" 1 - Display Available APK files")
    print(" 2 - Decompile APK")
    print(" 3 - APK to JAR") 
    print(" 4 - Scan Decompiled APK") 
    print(" 9 - Return to main")
    print(" 0 - Exit app")

# Display available APKS
def displayAvailableApks():
    files = os.listdir("Input/APK")
    apks = list()
    
    for index in files:
        if ".apk" in index:
            apks.append(index)
    
    if not apks:
        print("No apks found")
    else:
        print("\nAvaiable APKs")
        cnt = 1
        for index in apks:
            print(" [" + str(cnt) + "] " + index)
            cnt = cnt + 1

# Decompile APK
def decompileApk():
    displayAvailableApks()
    
    print("Decompile APK file\n")
    APK_FILE = input("Enter APK to decompile: ")
    if APK_FILE == "-1" or None: # exit case
        return
    # if
    APK_PATH = "Input/APK/" + APK_FILE
    os_apktool(APK_FILE, APK_PATH)

# Apktool
def os_apktool(APK_FILE, APK_PATH):
    if not ".apk" in APK_FILE:
        print("Error: Invaild file suppiled")

    else:
        index = APK_FILE.index(".apk")
        OUTPUT_FILE_NAME = APK_FILE[:index]
        decompiledDir = os.listdir("Output/Decompiled")

        if not OUTPUT_FILE_NAME in decompiledDir:
            os.system("apktool d " + APK_PATH + " --output Output/Decompiled/" + OUTPUT_FILE_NAME)
        else:
            print("Error: APK already decompiled")
        # if
    # if

# Convert APK to JAR
def apkToJar():
    pass

# Sign APK
def signApk():
    pass

# Dex2jar
def os_dex2jar(APK_FILE, APK_PATH):
    if not ".apk" in APK_FILE:
        print("Error: Invaild file suppiled")

    else:
        index = APK_FILE.index(".apk")
        OUTPUT_JAR_NAME = APK_FILE[:index]
        generatedJars = os.listdir("Output/JAR")

        if not OUTPUT_JAR_NAME in generatedJars:
            os.system("d2j-dex2jar " + APK_PATH + " --output Output/JAR/" + OUTPUT_JAR_NAME)
        else:
            print("Error: APK already decompiled")
        # if
    # if

# Scan decompile APK
def scanApk():
    files = os.listdir("Output/Decompiled")
    cnt = 1
    print("Avaiable Decompiled APKs:")
    avaibleApks = list()
    for index in files:
        print(" [" + str(cnt) + "] " + index)
        avaibleApks.append(index)
        cnt = cnt + 1
    # for

    apkChoice = input("\nEnter selection: ")
    if apkChoice == "-1": # exit case
        return
    # if

    APK_MANIFEST_PATH = "Output/Decompiled/" + apkChoice + "/AndroidManifest.xml"
    ANALYSIS_DIR_PATH = "Output/Analysis/" + apkChoice
    print(APK_MANIFEST_PATH)

# Get permissions
def analyzeManifestPermissions(androidManifest):
    permissionDict = {}
    permissionDict['standard'] = list()
    permissionDict['unknown'] = list()
    
    USES_PERMSSION = "uses-permission"
    PERMS_ATTR_NAME_LABEL = "android:name="
    ANDROID_PERMISSION = "android.permission."

    detecedPermissions = list()
    detecedUnknownPermissions = list()
    
    for manifestIndex in androidManifest:
        manifestIndex = manifestIndex.strip()
        
        # user-permission
        if USES_PERMSSION in manifestIndex:

            # standard formatted Android permission
            if PERMS_ATTR_NAME_LABEL in manifestIndex:

                # find beginning of permission
                positionX = manifestIndex.index(PERMS_ATTR_NAME_LABEL) # starting index
                positionY = positionX + len(PERMS_ATTR_NAME_LABEL) + 1
                lineSlice = manifestIndex[positionY : ] # tail slice
            
                # find end of permission
                positionZ = lineSlice.index("\"/>") # ending index
                lineSlice = lineSlice[ : positionZ] # head slice
            
                #print(lineSlice) # Debugging: captured permission name
                detecedPermissions.append(lineSlice)
                
            # android.permission.
            elif ANDROID_PERMISSION in manifestIndex:

                unknownPermissionCnt = unknownPermissionCnt + 1
                
                #print(manifestIndex) # DEBUGGING
                positionX = manifestIndex.index(ANDROID_PERMISSION)
                permission_name = manifestIndex[positionX : ]
                
                positionY = permission_name.index("\"/>")
                permission_name = permission_name[ : positionY]
                
                detecedPermissions.append(permission_name)
                detecedUnknownPermissions.append(manifestIndex)

            else:
                print("[*] Cannot process permission: " + manifestIndex)
    
    if detecedUnknownPermissions:
        print("\n[*] Detected Unknown Permissions")
        for i in detecedUnknownPermissions:
            print(i)

    detecedPermissions = list(dict.fromkeys(detecedPermissions))
    detecedPermissions.sort()
    
    return detecedPermissions, detecedUnknownPermissions  

# Get AndroidManifest.xml services
def getManifestServices(manifest):
    services = list() # empty list
    for line in manifest:
        if "<service " in line:
            startPos = line.find("android:name=") + len("android:name=\"")
            temp = line[startPos:]
            endPos = int(temp.find("\""))
            services.append(temp[:(endPos)])
    
    services.sort() # sort services found
    return services

# get AndroidManifest Tag
def getManifestTag(manifest):
    for index in manifest:
        if "<manifest " in index:
            return index

# APK Compiled SDK Version
def getCompileSDKVersion(manifestTag):
    startIndex = manifestTag.find("compileSdkVersion=\"")
    sliced = manifestTag[startIndex:]
            
	# find end of tag
    if not sliced.find("\" ") == -1:
        endIndex = sliced.find("\" ")
    else:
        endIndex = sliced.find("\">")

    return sliced[sliced.find("\"") + 1 : endIndex]

# APK Compile SDK Version Codename
def getCompileSDKVersionCodename(manifestTag):
    startTag = manifestTag.find("compileSdkVersionCodename=\"")
    sliced = manifestTag[startTag:]
    
    # find end of tag
    if not sliced.find("\" ") == -1:
        endTag = sliced.find("\" ")
    else:
        endTag = sliced.find("\">")
    
    return sliced[sliced.find("\"") + 1 : endTag]

# APK Package name
def getPackageName(manifestTag):
    startPos = manifestTag.find("package=\"")
    sliced = manifestTag[startPos:]
            
    # find end of tag
    if not sliced.find("\" ") == -1:
        endPos = sliced.find("\" ")
    else:
        endPos = sliced.find("\">")

    return sliced[sliced.find("\"")+1:endPos]

# APK Platform Build Version Code
def getPlatformBuildVersionCode(manifestTag):
    startPos = manifestTag.find("platformBuildVersionCode=\"")
    sliced = manifestTag[startPos:]

    # find end of tag
    if not sliced.find("\" ") == -1:
        endPos = sliced.find("\" ")
    else:
        endPos = sliced.find("\">")

    return sliced[sliced.find("\"")+1:endPos]

# APK Platform Build Version Name
def getPlatformBuildVersionName(manifestTag):
    startPos = manifestTag.find("platformBuildVersionName=\"")
    sliced = manifestTag[startPos:]

    # check if at end of the tag
    if not sliced.find("\" ") == -1:
        endPos = sliced.find("\" ")
    else:
        endPos = sliced.find("\">")

    return sliced[sliced.find("\"")+1:endPos]

# Get AndroidManifest.xml features used
def getUsesFeatures(ANDROID_MANIFEST_PATH):
    usesFeatures = dict()
    unknownFeatures = list()
    unknownFeaturesFound = False
    
    androidManifest = readAndroidManifest(ANDROID_MANIFEST_PATH)

    for index in androidManifest:
        if "<uses-feature " in index:
            featureName = ""
            glEsVersion = ""

            if not index.find("android:name=\"") == -1:
                startPos = index.find("android:name=\"")
                sliced = index[startPos+len("android:name=\""):]
                endPos = sliced.find("\"")
                featureName = sliced[:endPos]
                key = featureName

            elif not index.find("android:glEsVersion=\"") == -1: 
                startPos = index.find("android:glEsVersion=\"")
                sliced = index[startPos+len("android:glEsVersion=\""):]
                endPos = sliced.find("\"")
                glEsVersion = sliced[:endPos]
                
                #print("Gles Version: "+glEsVersion)
                key = "glEsVersion=" + glEsVersion
            
            else:
                unknownFeatures.append(index.strip())
                unknownFeatures = True
                continue

            if not index.find("android:required=\"") == -1:
                startPos = index.find("android:required=\"")
                x = index[startPos+len("android:required=\""):]
                status = x[:x.find("\"")]

                if status.lower() == "true":
                    usesFeatures[key] = True
                    continue

            usesFeatures[key] = False
    
    if unknownFeatures:
        print("\nUnknown Features Found:")
        cnt = 1
        for i in unknownFeatures:
            print("["+str(cnt)+"] "+i)
            cnt = cnt + 1
        # for
    # if

    return usesFeatures

# AndroidManifest.xml to text
def copyManifestAsTxt(APK_NAME, ANDROID_MANIFEST_PATH):
    name = APK_NAME[:-4]
    OUTPUT_PATH = "Output/" + name + "_AndroidManifest.txt"
    
    try:
        manifest = open(ANDROID_MANIFEST_PATH, "r")
        androidManifest = manifest.readlines() # copy manifest
        manifest.close()
        txt = open(OUTPUT_PATH, "w")
        
        try:
            for line in androidManifest:
                txt.write(line)
        finally:
            txt.close()

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()

# Log detected Android permissions
def logPermissions(APK_NAME, ANDROID_MANIFEST_PATH):
    PERMISSION_LOG_PATH = "Output/" + APK_NAME + "_DetectedPermissions.txt"	

    androidManifest = readAndroidManifest(ANDROID_MANIFEST_PATH)

    standard = list()
    unknown = list()
    
    permissions = analyzeManifestPermissions(androidManifest)
    if(len(permissions) == 0 ):
        print("No permissions detected.")
        return
    
    for index in permissions:
        if "android.permission." in index:
            standard.append(index)
        else:
            unknown.append(index)
    
    try:
        log = open(PERMISSION_LOG_PATH, "w")
        log.write("APK name: " + APK_NAME +"\n")
        log.write("Total permissions: " + str(len(permissions)) + "\n\n")
        
        # standard format permissions
        print("\nStandard permissions: "+str(len(standard)))
        #log.write("Standard permissions: " + str(len(standard)) + "\n")
        #log.write("----------------------------\n")
        standard.sort()
        for index in standard:
            log.write(index + "\n")
        # for
        
        # unknown permissions
        if len(unknown) != 0:
            log.write("\n")
            print("\nUnknown permissions: " + str(len(unknown)))
            #log.write("\nUnknown permissions: " + str(len(unknown)) + "\n")
            #log.write("----------------------------\n")
            unknown.sort()
            for index in unknown:
                log.write(index + "\n")
    
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()

# Analyze Android manifest
def analyzeAndroidManifest(APK_NAME, ANDROID_MANIFEST_PATH):

    ANALYIS_LOG_PATH = "Output/" + APK_NAME + "_AnalysisLog.txt"
    date = datetime.datetime.now().strftime("%A %B %d, %Y %I:%M %p")
    
    androidManifest = readAndroidManifest(ANDROID_MANIFEST_PATH)

    # APK Meta Data
    manifestTag = getManifestTag(androidManifest)
    compile_sdk_version = getCompileSDKVersion(manifestTag)
    compile_sdk_version_codename = getCompileSDKVersionCodename(manifestTag)
    package_name = getPackageName(manifestTag)
    platform_build_version_code = getPlatformBuildVersionCode(manifestTag)
    platform_build_version_name = getPlatformBuildVersionName(manifestTag)

    # Permissions
    standardPermissions, customPermissions = analyzeManifestPermissions(androidManifest)
    num_permissions = str(len(standardPermissions) +  len(customPermissions))

    # Write log
    log = open(ANALYIS_LOG_PATH, "w")
    log.write("File: " + APK_NAME + "\n")
    log.write("Date: " + date + "\n")
    log.write("Package: " + package_name + "\n")
    log.write("Compiled SDK Version: " + compile_sdk_version + "\n")
    log.write("Compiled SDK Version Codename: " + compile_sdk_version_codename + "\n")
    log.write("Platform Build Version Code: " + platform_build_version_code + "\n")
    log.write("Platform Build Version Name: " + platform_build_version_name + "\n")
    log.write("Total Permissions: " + num_permissions+"\n")
    
    # Standard Permissions
    log.write("\nStandard Permissions: " + str(len(standardPermissions)) + "\n")
    for i in standardPermissions:
        log.write(i + "\n")
    
    # Custom Permissions
    log.write("\nUnknown Permissions: " + str(len(customPermissions)) + "\n")
    for i in customPermissions:
        log.write(i + "\n")

    # Log APK uses-features
    uses_features = getUsesFeatures(androidManifest)
    if uses_features:
        log.write("\nUSES-FEATURES\n")
        for key,value in uses_features.items():
            log.write(key+" "+str(value)+"\n")
        log.write("\n")
    
    # Log APK services
    services = getManifestServices(androidManifest)
    log.write("\nServices\n")
    for i in services:
        log.write(i + "\n")

def readAndroidManifest(ANDROID_MANIFEST_PATH):
    try:
        f = open(ANDROID_MANIFEST_PATH, "r")
        return f.readlines() 
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    finally:
        f.close()