import os.path

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
	rgb_code_dictionary = {}
	linesFromLDConfig = checkAndReadLDConfig()
	for line in linesFromLDConfig:
		if str(line)[0:4] == '0 !C':
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
			rgb_code_dictionary[legoColourCode] = rgbValues
			print("============================================")

	print (rgb_code_dictionary)
	return rgb_code_dictionary

createCodeDictionary()

#col = rgbPixels[j,i]
		
##Check the pixel colour with the Lego dictionary colours
#point = col
#colors = list(rgb_code_dictionary.keys())
#closest_colors = sorted(colors, key=lambda color: distance(color, point))
#closest_color = closest_colors[0]
#code = rgb_code_dictionary[closest_color]


##set the Lego colour to the colour code
#col = int(code)
