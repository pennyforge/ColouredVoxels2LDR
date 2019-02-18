def checkInput(nosOfFiles):
	userNumber = raw_input("Choose number? (q to quit) ")


	if userNumber == "q" or userNumber == "Q" or userNumber == "Quit":
		sys.exit()
	
	try:
		numberChosen = int(userNumber)

		if numberChosen < 1 or numberChosen > nosOfFiles:
			if nosOfFiles == 1:
				print
				print "You need to choose '1'!"				
				userNumber = checkInput(nosOfFiles)
				numberChosen = int(userNumber)
				return numberChosen
			else:	
				print
				print "Opps that number is not between 1 and ", nosOfFiles
				userNumber = checkInput(nosOfFiles)	
		else:
			print "Good choice...",numberChosen	
			return numberChosen
	except:
		print
		print "Opps that's not a number"
		userNumber = checkInput(nosOfFiles)
		numberChosen = int(userNumber)
		return numberChosen


		
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
		print ("Enter the number of the file you want to convert to .ldr...")
		for fileName in fileList:
			indexNumber = fileList.index(fileName)
			print indexNumber+1, "-", fileName
		confirmedNumber = checkInput(nosOfFiles)
		nameOfFile = fileList[int(confirmedNumber)-1]
	else:
		print ("Please add some .vox files to the script folder") 
		print ("Script will now quit...")
		print
		sys.exit()
	
	return (nameOfFile)	