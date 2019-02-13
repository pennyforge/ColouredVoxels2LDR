import os.path
import math

#Read LDConfig File
def checkAndReadLDConfig():
	which_Ldraw = "C:\\ldraw\\LDConfig.ldr"
	if os.path.isfile(which_Ldraw):
		print ("Found LDConfig")
		with open(which_Ldraw) as f:
			lines = f.readlines()
	else:
		print ("Unable to find LDConfig file")
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
			#print (line[:-1])
			first = "VALUE "
			last = "   EDGE"
			hexColour = find_between( line, first, last )
			print (hexColour)
			rgbValues = hex2rgb(hexColour)
			print ("RGB:",rgbValues)
			first = "CODE"
			last = "VALUE"
			try:
				legoColourCode =  int(find_between( line, first, last ))
			except:
				print ("invalid value - skipping...")
			#legoColourCode = int(legoColourCode.strip())
			print ("CODE:",legoColourCode)
			#aDict[key] = value
			legoRGBCodeDictionary[legoColourCode] = rgbValues
			print("============================================")

	print (legoRGBCodeDictionary)
	return legoRGBCodeDictionary

def findClosestLegoColurCode(rgb,legoRGBCodeDictionary):
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
			#print ("Key:", key, "Value:",value)
			closestLegoCode = key
		#print ("==================================")
		#input()
	return closestLegoCode

rgb = (78,200,100)

legoRGBCodeDictionary = createCodeDictionary()
closestLegoCode = findClosestLegoColurCode(rgb,legoRGBCodeDictionary)

print ()
print ()
print ("The closest Lego colour code to your colour", rgb," is:",closestLegoCode)

