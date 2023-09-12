# __main__.py

import os
import datetime
import zipfile

def main():
    menu()
    while True:
        menu()
        menuChoice = input("Select choice: ")
        menuChoice = int(menuChoice)
        if menuChoice == 0:
            print("Exiting.")
            exit(0)
        
        elif menuChoice == 1:
            displayAvailableApks()

        elif menuChoice == 2:
            decompileApk()
        
        elif menuChoice == 3:
            exploreApk()
        
        elif menuChoice == 9:
            break
        
        else:
            print("Invalid Selected\n")
        # if
    # menu

def menu():
    print("Static Analysis\n")
    print(" 1 - Display Available APKs")
    print(" 2 - Decompile APK") 
    print(" 3 - Explore APK") 
    print(" 9 - Return to main")
    print(" 0 - Exit app")

def exploreApk():
    print("Explore APK")

def decompileApk():
    print("Decompile APK file")

def displayAvailableApks():
    files = os.listdir("Input")
    apks = list()
    
    for index in files:
        if ".apk" in index:
            apks.append(index)
        # if
    # for
    
    if not apks:
        print("No apks found")
    
    else:
        print("Select an APK to analysis")
        cnt = 1
        for index in apks:
            print(" [" + str(cnt) + "] " + index)
            cnt = cnt + 1
        # for
    # if


# Apktool
def apkTool(APK_PATH):
    os.system("apktool d " + APK_PATH)

# Dex2jar
def os_dex2jar(APK_PATH):
    os.system("d2j-dex2jar " + APK_PATH)

# Read AndroidManifest.xml permissions
def getManifestPermissions(androidManifest):
    standardPermissions = list()
    unknownPermissions = list()
    signaturePermissions = list()
    buffer = ""

    for index in androidManifest:
        if "uses-permission" in index:
            startingPos = index.find("android:name=")
            offset = len("android:name=")+1
            buffer = index[startingPos + offset : -4]

            if "permission " in buffer:
                startingPos = len("permission android.permission.")
                buffer = buffer[startingPos:]
                standardPermissions.append(buffer)
                                
            elif "com." in buffer:
                unknownPermissions.append(buffer)
                                
            else:
                startingPos = len("android.permission.")
                buffer = buffer[startingPos:]
                standardPermissions.append(buffer)
            # if
        # if
    # for
    
    standardPermissions.sort()
    unknownPermissions.sort()
    return standardPermissions, unknownPermissions

# Get permissions
def getPermissions(manifest):
    detectedPermissions = list()
    unknownPermissionFormat = False
    unknownExample = ""
    unknownCnt = 0
    
    for manifestLine in manifest:
        manifestLine = manifestLine.strip() # remove whitespace
        
        # check is user-permission is within manifest line
        if "uses-permission" in manifestLine:

            # standard formatted Android permission
            if "android:name=" in manifestLine:
                # find beginning of permission
                startIndex = manifestLine.index("android:name=")# starting index
                temp = manifestLine[startIndex + len("android:name=") + 1 :] # slice
            
                # find end of permission
                endIndex = temp.index("\"/>") # ending index
                temp = temp[:endIndex] # slice
            
                #print(sPerm) # DEBUG: Captured Permission
                detectedPermissions.append(temp)
                
            # Non-standard formatted Android Permission
            elif "android.permission." in manifestLine:
                #print(manifestLine) # DEBUGGING
                temp = manifestLine[manifestLine.index("android.permission."):]
                endIndex = temp.index("\"/>")
                permissionSliced = temp[:endIndex]
                detectedPermissions.append(permissionSliced)
                unknownPermissionFormat = True
                if unknownPermissionFormat:
                    unknownExample = manifestLine
                    unknownCnt = unknownCnt + 1
                # if
                
            # default
            else:
                print("[*] Cannot process permission: " + manifestLine)
            # if
        # if
    # for
    
    if unknownPermissionFormat:
        print("\n[*] Possible permission obfuscation: " + str(unknownCnt))
        print("Example: " + unknownExample)
    # if

    detectedPermissions = list(dict.fromkeys(detectedPermissions))
    detectedPermissions.sort()
    
    return detectedPermissions

# Get AndroidManifest.xml services
def getManifestServices(manifest):
    services = list() # empty list
    for line in manifest:
        if "<service " in line:
            startPos = line.find("android:name=")+len("android:name=\"")
            temp = line[startPos:]
            endPos = int(temp.find("\""))
            services.append(temp[:(endPos)])
        # if
    # for
    
    services.sort() # sort services found
    return services

# Get APK META data
def getAPKMetaData(manifest):
    for index in manifest:
        if "<manifest " in index:
            startPos = index.find("compileSdkVersion=\"")
            sliced = index[startPos:]
            
            # check if at end of the tag
            if not sliced.find("\" ") == -1:
                endPos = sliced.find("\" ")
            else:
                endPos = sliced.find("\">")
            # if

            compileSdkVersion = sliced[sliced.find("\"")+1:endPos]
            startPos = index.find("compileSdkVersionCodename=\"")
            sliced = index[startPos:]

            # check if at end of the tag
            if not sliced.find("\" ") == -1:
                endPos = sliced.find("\" ")
            else:
                endPos = sliced.find("\">")
            # if

            compileSdkVersionCodename = sliced[sliced.find("\"")+1:endPos]

            startPos = index.find("package=\"")
            sliced = index[startPos:]
            
            # check if at end of the tag
            if not sliced.find("\" ") == -1:
                endPos = sliced.find("\" ")
            else:
                endPos = sliced.find("\">")
            # if

            apkPackagename = sliced[sliced.find("\"")+1:endPos]
            startPos = index.find("platformBuildVersionCode=\"")
            sliced = index[startPos:]

            # check if at end of the tag
            if not sliced.find("\" ") == -1:
                endPos = sliced.find("\" ")
            else:
                endPos = sliced.find("\">")
            # if

            platformBuildVersionCode = sliced[sliced.find("\"")+1:endPos]
            startPos = index.find("platformBuildVersionName=\"")
            sliced = index[startPos:]

            # check if at end of the tag
            if not sliced.find("\" ") == -1:
                endPos = sliced.find("\" ")
            else:
                endPos = sliced.find("\">")
            # if

            platformBuildVersionName = sliced[sliced.find("\"")+1:endPos]
            return compileSdkVersion, compileSdkVersionCodename, apkPackagename, platformBuildVersionCode, platformBuildVersionName
        # if
    # for

# Get AndroidManifest.xml features used
def getManifestFeaturesUsed(manifest):
    usesFeatures = dict()
    unknownFeatures = list()
    unknownFeaturesFound = False
    
    for index in manifest:
        if "<uses-feature " in index:
            featureName = ""
            glEsVersion = ""

            if not index.find("android:name=\"") == -1:
                startPos = index.find("android:name=\"")
                sliced = index[startPos+len("android:name=\""):]
                endPos = sliced.find("\"")
                featureName = sliced[:endPos]

                #print("Feature: "+featureName)
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
            # if

            if not index.find("android:required=\"") == -1:
                startPos = index.find("android:required=\"")
                x = index[startPos+len("android:required=\""):]
                status = x[:x.find("\"")]

                if status.lower() == "true":
                    usesFeatures[key] = True
                    continue # next iteration
                # if

            #print("Required: "+str(isRequired)+"\n")
            usesFeatures[key] = False
        # if
    # for
    
    if unknownFeatures:
        print("\nUnknown Features Found:")
        cnt = 1
        for i in unknownFeatures:
            print("["+str(cnt)+"] "+i)
            cnt = cnt + 1 # increment count
        # for
    # if

    return usesFeatures

# AndroidManifest.xml to text
def manifestToTxt(apk):
    name = apk[:-4]
    ANDROID_MANIFEST_PATH = "./" + apk + "/AndroidManifest.xml"
    OUTPUT_PATH = "Output/" + name + "_AndroidManifest.txt"
    
    try:
        manifest = open(ANDROID_MANIFEST_PATH, "r")
        androidManifest = manifest.readlines() # copy manifest
        manifest.close()
        f = open(OUTPUT_PATH, "w")
        
        try:
            for i in androidManifest:
                f.write(i)
        finally:
            f.close()
        # try

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    # try

# Log detected Android permissions
def logPermissions(apk):
    APK_FILE_NAME = apk[:-4]
    ANDROID_MANIFEST_PATH = "./" + APK_FILE_NAME + "/AndroidManifest.xml"
    PERMISSION_LOG_PATH = "Output/" + APK_FILE_NAME + "_DetectedPermissions.txt"	

    # Scan AndroidManifest.xml
    try:
        f = open(ANDROID_MANIFEST_PATH, "r")
        androidManifest = f.readlines() # copy AndroidManifest.xml
        f.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    finally:
        f.close()
    # try

    standard = list()
    unknown = list()
    
    permissions = getPermissions(androidManifest)
    #print("Total permissions: " + len(detectedPermissions))
    if(len(permissions) == 0 ):
        print("No permissions detected.")
        return
    # if
    
    for index in permissions:
        if "android.permission." in index:
            standard.append(index)
        else:
            unknown.append(index)
        # if
    # for
    
    log = open(PERMISSION_LOG_PATH, "w")
    try:
        log.write("APK name: " + APK_FILE_NAME +"\n")
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
            # for
        # if
    except IOError:
        print("IO ERROR")
    # try

# Analyze Android manifest
def analyzeAndroidManifest(apk):
    APK_NAME = apk[:-4]

    ANALYIS_LOG_PATH = "Output/" + APK_NAME + "_AnalysisLog.txt"
    DATE = datetime.datetime.now().strftime("%A %B %d, %Y %I:%M %p")
    ANDROID_MANIFEST_PATH = "./" + APK_NAME + "/AndroidManifest.xml"
    
    # Scan AndroidManifest.xml
    try:
        f = open(ANDROID_MANIFEST_PATH, "r")
        androidManifest = f.readlines() # copy manifest
        f.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    finally:
        f.close()
    # try

    compileSdkVersion, compileSdkVersionCodename, apkPackagename, platformBuildVersionCode, platformBuildVersionName = getAPKMetaData(androidManifest)
    standardPermissions, customPermissions = getManifestPermissions(androidManifest)
    num_permissions = str(len(standardPermissions) +  len(customPermissions))

    log = open(ANALYIS_LOG_PATH, "w")
    log.write("File: "+apk+"\n")
    log.write("Date: " + DATE + "\n")
    log.write("Package: " + apkPackagename + "\n")
    log.write("Compiled SDK Version: " + compileSdkVersion + "\n")
    log.write("Compiled SDK Version Codename: " + compileSdkVersionCodename + "\n")
    log.write("Platform Build Version Code: " + platformBuildVersionCode + "\n")
    log.write("Platform Build Version Name: " + platformBuildVersionName + "\n")
    log.write("Total Permissions: " + num_permissions+"\n")
    
    # Standard Permissions
    log.write("\nStandard Permissions: " + str(len(standardPermissions)) + "\n")
    for i in standardPermissions:
        log.write(i + "\n")
    # for
    log.write("\n")
    
    # Custom Permissions
    log.write("Unknown Permissions: " + str(len(customPermissions)) + "\n")
    for i in customPermissions:
        log.write(i + "\n")
    log.write("\n")

    # Log uses-features
    uses_features = getManifestFeaturesUsed(androidManifest)
    if uses_features:
        log.write("USES-FEATURES\n")
        for key,value in uses_features.items():
            log.write(key+" "+str(value)+"\n")
        log.write("\n")
    # if
    
    # Log APK services
    services = getManifestServices(androidManifest)
    log.write("Services\n")
    
    for i in services:
        log.write(i + "\n")
    log.write("\n")