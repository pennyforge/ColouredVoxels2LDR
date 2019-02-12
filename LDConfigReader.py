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

rgb_code_dictionary = {}
linesFromLDConfig = checkAndReadLDConfig()

for line in linesFromLDConfig:
	if str(line)[0:4] == '0 !C':
		print (line[:-1])
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
		print("============================================")