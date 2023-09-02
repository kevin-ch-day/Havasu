columnToAdd = "COM.HTC.LAUNCHER.PERMISSION.READ_SETTINGS"	
testColumn = "ACCESS_COARSE_LOCATION"

if(columnToAdd < testColumn):
  print("< BEFORE")
elif(columnToAdd > testColumn):
  print("> AFTER")
# if