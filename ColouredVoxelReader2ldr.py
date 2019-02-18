#ColouredVoxel2LDR Converter
#Neil Marsden Feb 2017

try: # Check for numpy
	import numpy 
	from numpy import zeros,newaxis,array
	from numpy import vstack,hstack,dstack
except:
	print ("Opps - you need 'numpy' try 'pip install numpy'")
	print ("Script will now exit")
	print
	sys.exit(0)

try: # Check for py-vox-io
	from pyvox.models import Vox
	from pyvox.writer import VoxWriter
	from pyvox.parser import VoxParser
except:
	print ("Opps - you need 'py-vox-io' get it from 'https://github.com/gromgull/py-vox-io'")
	print ("Script will now exit")
	print
	sys.exit(0)

import random
import os,datetime, time, sys,math
from copy import deepcopy
import glob

#Create a human readable timestamp`
def timeStamp ():
	ts = time.time()	
	dateTimeString = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d%H%M')
	return (dateTimeString)

#Write individual lines to an LDR file
def legoWriter(fileName,dateTimeStamp,ldrLine):
	if os.path.isfile(fileName): # If the file exists then just append 'a' the line
		LDrawFile = open(fileName, 'a')
		LDrawFile.write('\n')
	else:
		LDrawFile = open(fileName, 'w') # Otherwise create a new file 'w' and put the header info in
		LDrawFile.write('0 // Name: '+ fileName +'\n')
		LDrawFile.write('0 // Author:  Neil Marsden ' + dateTimeStamp +'\n')
		# Add a red reference stud if you want one - set the first digit to 1 to enable
		LDrawFile.write('0 4 70 -8 70 0 0 1 0 1 0 -1 0 0 6141.dat'+'\n')
		LDrawFile.write('\n')
	print ("WRITING LINE")
	LDrawFile.write(ldrLine)
	return fileName

def activeLine(active,colour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID):
	#1 69 -20 -24 -20 0 0 1 0 1 0 -1 0 0 3005.dat # EXAMPLE LINE
	active = str(active)
	colour = str(colour)	
	width = str(width)
	height = str(height)
	depth = str(depth)
	m1 = str(m1)
	m2 = str(m2)
	m3 = str(m3)
	m4 = str(m4)
	m5 = str(m5)
	m6 = str(m6)
	m7 = str(m7)
	m8 = str(m8)
	m9 = str(m9)
	ldrLine = active + " " + colour + " " + width + " " + height+ " " + depth  + " " + m1 + " " + m2 + " " + m3 + " " + m4 + " " + m5 + " " + m6 + " " + m7 + " " + m8 + " " + m9 + " " + partID
	return ldrLine

def brickMatrix(x,y,voxelColour): #Calculate the size of the brick
	studMatrix = []
	Width = x
	Depth = y
	StudCount = 0 
	print ("Brick is ",Width, "x" ,Depth)
	for i in range (0,Width):
		for j in range(0,Depth):
			studMatrix.append(voxelColour)
	brickMatrix = numpy.array(studMatrix).reshape(Depth,Width);
	return brickMatrix		


def optimiseSlice(baseMatrix,previousMatrix,sliceValue):
	print ("Optimising Layer...")
	print ("baseMatrix",baseMatrix)
	print ("previousMatrix",previousMatrix)
	print ("sliceValue",sliceValue)
	
	
	optimisedBrickData = []
	sliceCounter = 0
	layerBrickDiscard = 0
	#print brick
	print ()
	optimise = True
	brickCounter = 0
	dictionaryCounter = 902 # keep a track of the bricks swaps as you work through the matrix but make the number larger than 300 so that it doesn't get mixed up with 256 colour values
	x = 0
	y = 0

	while optimise:
		while x < baseMatrix.shape[0]: # Use a while loop rather than a for loop as it gives you more control moving through the loop
			while y < baseMatrix.shape[1]:
				voxelColour = int(baseMatrix[x,y])
				if voxelColour > 0 and voxelColour < 899: #Make sure we only process coloured voxels not voxels that have already been converted to bricks.
					print ("found unprocessed voxel...")
				else:
					print ("voxel already processed...moving on...")
					y = y + 1
					continue
				print (x,y,baseMatrix[x,y])
				
				if voxelColour >= 1:
					brickCounter = brickCounter + 1
					print ("Found Coloured Voxel (2)...")
					
					d = optimisationDictionary
					sortedDictionary = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
					for key, value in sortedDictionary:
						dictionaryCounter = dictionaryCounter + 1
						#check the shapes around the voxel 
						brickX,brickY = value
						brick = brickMatrix(brickX,brickY,voxelColour)
						maxValue = max(value)
						print (brick.shape)
						if sliceValue%2 == 0:
							brick = brick.reshape(brickX,brickY) # flips the array horizontal
						#Find out the distances to the edge of the matrix		

						subMatrixH = baseMatrix[x:x+brickX,y:y+brickY]
						subMatrixV = baseMatrix[x:x+brickY,y:y+brickX]

						print ()
						print (baseMatrix)
						print ()
						print (previousMatrix) 
						# Check to see if the this layer and the previous layer are the same - if so discard the largest brick (to try to solve the weak corner problem)
						if (baseMatrix==previousMatrix).all() and sliceValue%2 == 0 and brickY > 6:
							layerBrickDiscard = 1
							print ("Matching Layers")
							#print ("Discarding ", brick, " brick to fix weak corneres...")
							#Discard this brick by ignoring it and continue the loop to the next brick....
							continue
						else:
							try:
								if numpy.amax(subMatrixH) == numpy.amin(subMatrixH) and brick.shape == subMatrixH.shape:
									print ("MATCH HORIZONTAL!")
									rotate = 0
									#print (key, dictionaryCounter)
									baseMatrix[x:x+brickX,y:y+brickY] = dictionaryCounter
									#print ("baseMatrix")
									#print (baseMatrix)
									dictionaryCounter = 902
									print (x,y)
									optimisedBrickData.append([key,x,y,brickX,brickY,rotate,voxelColour])
									if layerBrickDiscard == 1:
										previousMatrix =  deepcopy(baseMatrix)
									print("jump here by...",brickY)
									# you matched a brick but now you need to jump the while loop...
									y = y + brickY
									break
								elif numpy.amax(subMatrixV) == numpy.amin(subMatrixV) and brick.shape == subMatrixV.shape:
									print ("MATCH VERTICAL!")
									rotate = 1
									#print (key, dictionaryCounter)
									#print (dictionaryCounter)
									baseMatrix[x:x+brickY,y:y+brickX] = dictionaryCounter
									#print (baseMatrix)
									dictionaryCounter = 902
									#print (x,y)
									optimisedBrickData.append([key,x,y,brickX,brickY,rotate,voxelColour])
									if layerBrickDiscard == 1:
										previousMatrix =  deepcopy(baseMatrix)
									print("jump here by...",brickX)
									y = y + brickX
									#input()
									break
								else:
									print ("Brick won't fit - trying next brick...")
									print ("======================================")
							except Exception as e:
								print ("<<<<<<<<<<<<<-", e,"->>>>>>>>>>>>>>>")
								print ("Brick won't fit on matrix anyway- trying next brick...")
								print ("======================================")								
				else:
					print ("No Voxel")
					dictionaryCounter = 902
					y = y + 1
			layerBrickDiscard = 0
			x = x + 1
			y=0
		optimise = False
		previousMatrix =  deepcopy(baseMatrix)
	return (baseMatrix,previousMatrix,optimisedBrickData)	

def getColourList(voxelColourRGB):
	voxelRGBCodeDictionary = {}
	for c in range(len(voxelColourRGB)):
		#print (".vox colour value:",c+1," - ",voxelColourRGB[c])
		colourValues = voxelColourRGB[c]
		colourValueR = getattr(colourValues, 'r')
		colourValueG = getattr(colourValues, 'g')
		colourValueB = getattr(colourValues, 'b')
		colourValueA = getattr(colourValues, 'a')
		#print (colourValueR,",",colourValueG,",",colourValueB,",",colourValueA)
		voxelRGBCodeDictionary[c+1] = (colourValueR,colourValueG,colourValueB)
	return voxelRGBCodeDictionary

#Read LDConfig File
def checkAndReadLDConfig():
	which_Ldraw = "C:\\ldraw\\LDConfig.ldr"
	if os.path.isfile(which_Ldraw):
		print ("Found LDConfig")
		with open(which_Ldraw) as f:
			lines = f.readlines()
	else:
		print ("Unable to find LDConfig file")
		sys.exit(0)
	return lines

def hex2rgb(hexColour): # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
	h = hexColour.lstrip('#')
	#print('RGB =', tuple(int(h[i:i+2], 16) for i in (0, 2 ,4)))
	rgbValues = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
	return rgbValues

def find_between( s, first, last ): # https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

#From http://stackoverflow.com/questions/34366981/python-pil-finding-nearest-color-rounding-colors
def distance(c1, c2): # Work out the nearest colour 
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

def createCodeDictionary():
	legoRGBCodeDictionary = {}
	linesFromLDConfig = checkAndReadLDConfig()
	for line in linesFromLDConfig:
		if str(line)[0:4] == '0 !C' and ("ALPHA" or "RUBBER" or "MATERIAL" or "METAL" or "CHROME" or "PEARLESCENT") not in str(line):
			first = "VALUE "
			last = "   EDGE"
			hexColour = find_between( line, first, last )
			#print (hexColour)
			rgbValues = hex2rgb(hexColour)
			#print ("RGB:",rgbValues)
			first = "CODE"
			last = "VALUE"
			try:
				legoColourCode =  int(find_between( line, first, last ))
			except:
				print ("invalid value - skipping...")
			#print ("CODE:",legoColourCode)
			legoRGBCodeDictionary[legoColourCode] = rgbValues
			#print("============================================")
	#print("Lego Colours From LDConfig.ldr")
	#print (legoRGBCodeDictionary)
	return legoRGBCodeDictionary

def findClosestLegoColourCode(rgb,legoRGBCodeDictionary):
	comparisionDictionary = {}
	legoRGBCodeDictionaryKeys = list(legoRGBCodeDictionary.keys()) #Get all the keys from the TLG Colour Dictionary (as the numbers don't run consequetively)
	#print (legoRGBCodeDictionaryKeys)
	print ("Running compare...please wait...")
	for legoColourCode in legoRGBCodeDictionaryKeys: # For each key do...
		#print ("Lego Colour Code:",legoColourCode) # Get the TLG colour
		dictRGB = legoRGBCodeDictionary.get(legoColourCode) # Get the dictionary RGB value
		#print ("Dictionary RGB Value:",dictRGB)
		colourDistance = distance(rgb,dictRGB) #now compare the two rgb values
		#print ("Colour Distance:",colourDistance)
		comparisionDictionary[legoColourCode] = colourDistance	#Put the TLG colour code in a dictionary with the distance value
		d = comparisionDictionary
		sortedDictionary = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)] # Reverse - Make sure the last value it spits out is the closest...
		for key, value in sortedDictionary:
			closestLegoCode = key
	return closestLegoCode

def checkInput(nosOfFiles):
	userNumber = input("Choose number? (q to quit) ")
	if userNumber == "q" or userNumber == "Q" or userNumber == "Quit":
		print("Exiting...")
		print ()
		sys.exit(0)
	else:
		try:
			numberChosen = int(userNumber)
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
	# Find all the .vox files in the script folder...
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


##################### MAIN CODE #####################
#Set up the colour dictionary...
legoRGBCodeDictionary = createCodeDictionary()
layerStop = 10000
#Read the .vox voxel file...
print ("Looking for .vox files...")
initialFileName = getFile()
print ("You chose: ", initialFileName)
try:
	voxelMatrix = VoxParser(initialFileName).parse()
except:
	print("There is a problem reading this .vox file - Try exporting the file from Goxel as a .vox file")
	print ()
	print ("Script will now exit")
	print
	sys.exit(0)
#print (voxelMatrix) #view the whole voxel matrix for checking
#input()

#Get the dimensions of the vox file
z = voxelMatrix.models[0][0][0]
y = voxelMatrix.models[0][0][1]
x = voxelMatrix.models[0][0][2]
print ()
print ("Matrix Dimensions: X",x,"*Y",y,"*Z",z,"(1)")
nosOfVoxels = x*y*z
print (nosOfVoxels)
print ("Will continue in a second...")
time.sleep(2) # So you can see the total number of voxels...

#Create a lookup table for the colours
voxelColourRGB = voxelMatrix._palette
voxelRGBCodeDictionary = getColourList(voxelColourRGB)
print ("Original Voxel Colour Palette")
print (voxelRGBCodeDictionary)
voxelRGBList = []
#Zero out the numpy array used to store the primary Lego matrix
numpyArrayForLego = numpy.zeros([x, y, z],dtype=int)
for i in range(0,nosOfVoxels):
	try:
		#Pull out the relevant numbers from the .vox file 
		colour = getattr(voxelMatrix.models[0][1][i], 'c')
		voxelX = getattr(voxelMatrix.models[0][1][i], 'z') # VoxelX = z - Weird I know but it's to do with the orienation of the model!	
		voxelY = getattr(voxelMatrix.models[0][1][i], 'y') 
		voxelZ = getattr(voxelMatrix.models[0][1][i], 'x') # voxelZ = x - Weird I know but it's to do with the orienation of the model!

		print (colour, voxelX,voxelY,voxelZ)
		
		print ("===========Start Colour Conversion============")
		print ("Voxel Colour Value",colour)
		voxelPointColour = voxelRGBCodeDictionary.get(int(colour))
		print ("ORIGINAL VOXEL PALETTE COLOUR RGB",voxelPointColour)
		if voxelPointColour not in voxelRGBList:
			voxelRGBList.append(voxelPointColour)
		closestLegoCode = findClosestLegoColourCode(voxelPointColour,legoRGBCodeDictionary)

		colour = closestLegoCode
		print ("Closest Lego Code Colour:",closestLegoCode)
		#Update the array with the colour values
		numpyArrayForLego[int(voxelX),int(voxelY),int(voxelZ)] = colour
	except Exception as e: 
		#print(e)
		#input()
		print ("Assuming no voxel - skipping")
#Print the primary numpy array
print ("===========================================")
print ("original",numpyArrayForLego)
print ("===========================================")
print ("Matrix Dimensions: X",x,"*Y",y,"*Z",z,"(2)")
#Create another viariable to store x,y,z
heightOfMatrix = x
widthOfMatrix = y
depthOfMatrix = z
#print ()
#THIS IS THE FIRST SLICE OF THE ARRAY
#print (numpyArrayForLego[0])

dateTimeStamp = timeStamp() #Get timeStamp for fileName
		
#Set Up the Brick Dictionary
optimisationDictionary = {}
optimisationDictionary["3006.DAT"]=[2,10]	#3 903
optimisationDictionary["3007.DAT"]=[2,8]	#4 904
optimisationDictionary["2456.DAT"]=[2,6]	#5 905
optimisationDictionary["3001.DAT"]=[2,4]	#6 906
optimisationDictionary["3002.DAT"]=[2,3]	#7 907
optimisationDictionary["3003.DAT"]=[2,2]	#8 908
optimisationDictionary["3008.DAT"]=[1,8]	#9 909
optimisationDictionary["3009.DAT"]=[1,6]	#10 910
optimisationDictionary["3010.DAT"]=[1,4]	#11 911
optimisationDictionary["3622.DAT"]=[1,3]	#12 912
optimisationDictionary["3004.DAT"]=[1,2]	#13 913
optimisationDictionary["3005.DAT"]=[1,1]	#14 914
	
#LDR Line example
#1 69 -20 -24 -20 0 0 1 0 1 0 -1 0 0 3005.dat
#Setup the basic LDR line...
active = 1
colour = 7
width = 0
height = 0
depth = 0
#Set up the basic rotation matrix for the ldr file
m1 = 0;m2 = 0;m3 = 1;m4 = 0;m5 = 1;m6 = 0;m7 = -1;m8 = 0;m9 = 0
#Set the part for each voxel - currently this only works for 1x1 bricks - now unused
partID = "3005.dat" #Use 1x1 bricks

dateTimeStamp = timeStamp() #Get timeStamp for fileName
fileName = initialFileName[:-4] +"_" + dateTimeStamp + ".ldr" #Give every ldr fileName a timestamp
fileName = initialFileName[:-4] + ".ldr" #Give every ldr file the SAME  fileName

ldrLine = activeLine(active,colour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID) #Create a raw ldr line width,height and depth will be updated as the loop below scans the .vox array

count = 0 # Used to count the total number of 1x1 bricks
studMatrix = [] #Used to view slices (for humans!)
sliceMatrix = []

optimise = True
#The following loops do the heavy lifting reading the .vox array and writing out the bricks to an ldr file...
while optimise:
	for z in range(heightOfMatrix): #Reads the size of the array from the .vox model dimensions - in z - the height
		legoWriter(fileName,dateTimeStamp,'0 STEP') # Add a step for each layer
		#Set up the variables to optimise the layer
		sliceValue = z 
		print (z)
		#input()
		#Orientate the TOP view in LDR to match the TOP view in GOXEL
		sliceMatrix = numpy.rot90(numpy.fliplr(numpyArrayForLego[z]),1)
		originalMatrix = deepcopy(numpy.rot90(numpy.fliplr(numpyArrayForLego[z]),1))
		previousMatrix = deepcopy(numpy.rot90(numpy.fliplr(numpyArrayForLego[z]),1))
		#==================================
		#Hollowing function - WORK IN PROGRESS
		'''#For Hollowing but needs adjustment to reduce the degree of hollowing before the final layer above the hollowing (otherwise bricks will simply fall in the hollow!
		if layer > minLayer and layer < maxLayer:
			baseMatrix = queryHollowing(baseMatrix)
			hollowMatrix = deepcopy(baseMatrix)
		if layer == maxLayer-1:
			baseMatrix = originalMatrix
			colour = 47
			raw_input()
		'''	
		#Optimise the layer...
		sliceMatrix,previousMatrix, optimisedBrickData = optimiseSlice(sliceMatrix,previousMatrix,z)
		print ("OPTIMISATION COMPLETE...")
		print
		print ("Original Voxel Matrix Slice")
		print (originalMatrix)
		print
		print ("Optimised Lego Matrix Slice")
		print (sliceMatrix)		
		print	
		sliceMatrix = deepcopy(originalMatrix)
		#input()
		if z >= layerStop:
			input() #USEFUL FOR CHECKING EACH LAYER
		#Now read the bricks in the optimisedBrickData array and actually write them out as an ldr file...
		countBrick = 0
		for brick in optimisedBrickData:
			countBrick = countBrick + 1
			print (brick)
			print ()
			print (brick[0],brick[1],brick[2],brick[3],brick[4],brick[5],brick[6])
			#Assign the variables for each element in optimisedBrickData  
			partID = brick[0]
			x = brick[1]
			y = brick[2]
			brickX = brick[3]
			brickY = brick[4]
			brickRotate = brick[5]
			brickColour = brick[6]

			#Convert to Lego Values
			width = x*20+10 #Convert x and y into lego dimensions
			depth = y*20+10+((brickY/2)*20) #Convert x and y into lego dimensions
			height = z*-24 #Convert z into lego dimensions

			#MAKE ADJUSTMENTS DEPENDING ON BRICK SIZE 
			correctionX = 0
			correctionY = 0
			
			if brickX%2 != 0:
				print ("EVEN")
				correctionX = 10
				if z%2 != 0:
					correctionX = 10
			if brickY%2 != 0 and brickX !=1 and brickY !=1:
				print ("ODD")
				correctionY = 10
				if z%2 != 0:
					print ("EVEN 3x2")
					correctionY = 10
					correctionX = 10
				else:
					correctionY = 0
			#MAKE ADJUSTMENTS DEPENDING ON BRICK SIZE IF THE BRICKS ARE ROTATED
			if brickX == 1 and brickY != 1 and brickRotate == 1:
				if brickY%2 == 0:
					print ("EVEN + ROTATE")
				else:
					print ("ODD + ROTATE")
					correctionY = correctionY-10	
					correctionX = correctionX+30
				print ("found complex error")
				if brickY == 3 and brickX == 1:
					print ("Found 1x3 - Correcting...")
					correctionY = correctionY+10
					correctionX = correctionX-30
				correctionY = correctionY-20
				print (correctionY)
				#raw_input()
			if brickY==4 and brickX == 2 and brickRotate ==1:
				print ("Found 4x2 - Correcting...")
				correctionY = correctionY - 30
				correctionX = correctionX + 10
				
				
			if brickY==3 and brickX == 2 and brickRotate ==1:
				print ("Found 3x2 - Correcting...")
				correctionY = correctionY - 40
				
				
			if brickY==10 and brickX == 2 and brickRotate ==1:
				print ("Found 10x2 - Correcting...")
				correctionY = correctionY - 30
				correctionX = correctionX + 10
				
			if brickY==6 and brickX == 2 and brickRotate ==1:
				print ("Found 6x2 - Correcting...")
				correctionY = correctionY - 30
				correctionX = correctionX + 10

			if brickY==8 and brickX == 2 and brickRotate ==1:
				print ("Found 8x2 - Correcting...")
				correctionY = correctionY - 30
				correctionX = correctionX + 10
				
			if brickRotate == 0:
				width = width - correctionX
				depth = depth + correctionY
				ldrLine = activeLine(active,brickColour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID) #Construct the ldr line
				print (ldrLine)
			else:
				width = x*20+((brickY/2)*20)-correctionX #Convert x and y into lego dimensions
				depth = y*20-correctionY #Convert x and y into lego dimensions
				#Change the rotation of the brick - Example below...
				#90 brickRotate 1 4 20 -104 20 -1 0 0 0 1 0 0 0 -1 3001.dat	
				m1 = -1;m2 = 0;m3 = 0;m4 = 0;m5 = 1;m6 = 0;m7 = 0;m8 = 0;m9 = -1
				#Create the ldrLine
				ldrLine = activeLine(active,brickColour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID) #Construct the ldr line
				print (ldrLine)
			#initialise the ldr file on the first pass
			if z == 0 and countBrick == 1:
				LDrawFile = open(fileName, 'w')
				LDrawFile.close()
			#Write the LDR name to file...	
			legoWriter(fileName,dateTimeStamp,ldrLine) #Write the line to a ldr file
			print ("countBrick:",countBrick)
			if z >= layerStop:
				input() # USEFUL FOR CHECKING EACH BRICK ADDITION
			legoWriter(fileName,dateTimeStamp,'0 STEP')
		z = z + 1
		#count = count + 1
		optimisedBrickData = []
		brickRotate = 0
		previousMatrix =  deepcopy(sliceMatrix)
		sliceMatrix = deepcopy(originalMatrix)
		#Reset the rotation values - this is important otherwise the rotation "sticks" on the next layer!
		m1 = 0;m2 = 0;m3 = 1;m4 = 0;m5 = 1;m6 = 0;m7 = -1;m8 = 0;m9 = 0
		print ("Layer: ",heightOfMatrix)			
		#==================================
		count = 0
		studMatrix = []
		#if z == heightOfMatrix:
		#	optimise = False # Quit when the top layer is reached
		
	optimise = False # Quit when the top layer is reached
	#input("YOU ARE AT THE END...Z:",z,"heighOfMatrix:",heightOfMatrix)
print ("MODEL CONVERSION COMPLETE - Your .ldr file is:", fileName)
print ("Colour Palette as RGB")
#print (voxelColourRGB)
print ()
print (voxelRGBList)
