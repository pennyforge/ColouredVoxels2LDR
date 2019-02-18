import glob,os,sys

def checkInput(nosOfFiles):
	userNumber = input("Choose number? (q to quit) ")
	if userNumber == "q" or userNumber == "Q" or userNumber == "Quit":
		print("Exiting...")
		print ()
		sys.exit(0)
	else:
		try:
			numberChosen = int(userNumber)
			#pass
		except:
			print ()
			print ("Opps that's not a number")
			userNumber = checkInput(nosOfFiles)
			numberChosen = userNumber
		
	while numberChosen < 1 or numberChosen > nosOfFiles:
		if nosOfFiles == 1:
			print ()
			print ("You need to choose '1'!")				
			userNumber = checkInput(nosOfFiles)
		else:	
			print ()
			print ("Opps that number is not between 1 and ", nosOfFiles)
			userNumber = checkInput(nosOfFiles)
	
		numberChosen = userNumber
		print ("Good choice...",numberChosen)
		break
	return (numberChosen)
		
def getFile():
	pathName = os.path.dirname(os.path.abspath(__file__))
	# Find all the .bmps in the script folder...
	fileList=[] 
	nosOfFiles = 0
	for file in sorted(glob.glob( os.path.join(pathName, '*.vox') )):
		fileName = os.path.basename(file)
		fileList.append(fileName)
		nosOfFiles=nosOfFiles + 1

	if nosOfFiles > 0:	
		print ("Enter the number of the file you want to make an ldr of...")
		for fileName in fileList:
			indexNumber = fileList.index(fileName)
			print (indexNumber+1, "-", fileName)
		confirmedNumber = checkInput(nosOfFiles)
		print ("Confirmed Number:",confirmedNumber)
		#input()
		nameOfFile = fileList[int(confirmedNumber)-1]
	else:
		print ("Please add some .vox images files to the script folder") 
		print ("Script will now quit...")
		print ()
		sys.exit(0)
	
	return (nameOfFile)	


print ("Looking for .vox files...")
initialFileName = getFile()
print ("You chose: ", initialFileName)