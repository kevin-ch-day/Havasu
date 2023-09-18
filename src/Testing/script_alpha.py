# script_alpha.py
# Testing script

def getUsesFeatures(androidManifest):
    print("getUsesFeatures()")

    usesFeatures = dict()
    unknownFeatures = list()
    unknownFeaturesFound = False

    for index in androidManifest:
        if "<uses-feature " in index:
            print(index)
            
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

    return usesFeatures, unknownFeatures

# Read AndroidManifest.xml
def readAndroidManifest(ANDROID_MANIFEST_PATH):
    manifestData = None

    try:
        f = open(ANDROID_MANIFEST_PATH, "r")
        manifestData = f.readlines() 
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    finally:
        f.close()

    return manifestData

def main():
    ANDROID_MANIFEST_PATH = "../Output/Decompiled/b7b6ae08971e111291e2dffe48667c42/AndroidManifest.xml"
   
    androidManifest = readAndroidManifest(ANDROID_MANIFEST_PATH)
    getUsesFeatures(androidManifest)

main()
