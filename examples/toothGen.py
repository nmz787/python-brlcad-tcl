#Imports
import os

import python_brlcad_tcl.brlcad_tcl as brl

#Some constants
endl = '\n'
spc = ' '

#The path to output to, based on the location of the current file
scriptPath = os.path.dirname(__file__)
outFilePath = scriptPath + r'/output/toothGen.tcl'

#Some variables for creating the gear teeth
_defaultGearName = 'allTeeth'
_defaultToothName = 'tooth'
_toothHalfWidth = 0.27
_toothDepth = 0.54
_toothHeight = 0.25 - 0.0625

def createGears(gearName = _defaultGearName, toFile = False, toothHalfWidth = _toothHalfWidth, toothDepth = _toothDepth, toothHeight = _toothHeight, toothBaseName = _defaultToothName):

    make1 = "in tooth0 arb6 " + str(-toothHalfWidth) + " 0 0 " \
    						+ str(toothHalfWidth) 	+ " 0 0 " \
    						+ str(toothHalfWidth) 	+ " 0 " + str(toothHeight) + " " \
    						+ str(-toothHalfWidth) + " 0 " + str(toothHeight) + " " \
    						+ "0 " + str(toothDepth) + " 0 " \
    						+ "0 " + str(toothDepth) + " " + str(toothHeight)

    union = 'r ' + str(gearName) + ' u ' + str(toothBaseName) +'0 u '

    numTeethAdditional = 24.0
    degPerTooth = 360/ (numTeethAdditional + 1)


    lines = []

    lines.append(make1)
    lines.append(endl)

    for tooth in range(int(numTeethAdditional)):
    	tName = str(toothBaseName) + str(tooth + 1)
    	if tooth == 0:
    		prevTooth = str(toothBaseName) + '0'
    	else:
    		prevTooth = toothBaseName + str(tooth)
    		union += 'u '

    	lines.append('cp ' + str(prevTooth) + spc + str(tName))
    	lines.append('e ' + str(tName))
    	lines.append('sed ' + str(tName))
    	lines.append('keypoint 0 0 0')
    	lines.append('rot 0 0 ' + str(degPerTooth))
    	lines.append('accept')
    	lines.append(endl)

    	union += tName + spc

    lines.append(union)

    #global outFilePath
    if toFile:
        with open(outFilePath, 'w+') as outFile:
    	   outFile.write(endl.join(lines))

    #Give the lines
    return lines, gearName

if __name__ == '__main__':
    createGears(True)

'''
EOF
'''