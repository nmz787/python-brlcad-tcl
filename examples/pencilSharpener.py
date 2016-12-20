#Imports
import os, sys

#Import sister module.
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-brlcad-tcl')))
from python_brlcad_tcl.brlcad_tcl import *
from examples import toothGen

#Some constants
endl = '\n'
spc = ' '

#The path to output to, based on the location of the current file
scriptPath = os.path.dirname(__file__)
outFilePathBase = scriptPath + r'/output/pencilSharpener'
outFileTCL = outFilePathBase + '.tcl'
outFileSTL = outFilePathBase + '.stl'

#The quality for the STL output. 0.5 is worse, 0.1 is pretty good, 0.01 makes files large but really good quality...
stlQuality = 0.001

#Some variables for creating all of the various components

def createPencilSharpener():

	#Create the two cylinders for the bottom layer
	#Also we're working in Inches
	brl = brlcad_tcl(tcl_filepath = outFileTCL, title = "Pencil Sharpener Gear", make_g = False, make_stl = True, stl_quality = stlQuality, units = 'in')
	
	#Create our cylinders, regions, names, etc...
	bottom 			= 'b'
	bottomNegative 	= 'bn'
	bottomRing		= 'br'
	bottomFinal		= 'bf'
	
	middle			= 'm'
	middleNegative 	= 'mn'
	middleRing		= 'mr'
	middleWithGuide	= 'mh'
	middleFinal		= 'mf'
	
	middleTop			= 'mt'
	middleTopNegative	= 'mtn'
	middleTopRing		= 'mtr'
	
	top				= 't'
	topNegative		= 'tn'
	topRing			= 'tr'
	topFinal		= 'tf'
	
	shavingsHole	= 'sh'
	
	leftGuide		= 'l'
	rightGuide		= 'r'
	
	gearName		= 'gf'
	toothName		= 'tooth'
	
	allFinal		= 'finished'

	#Variables for their sizes and positions, in inches
	bottomOuterRadius	= 0.650
	bottomInnerRadius	= 0.460
	bottomHeight 		= 0.262
	bottomPosition		= (0, 0, 0)
	
	middleOuterRadius	= 0.502
	middleInnerRadius	= 0.4575
	middleHeight		= 0.275
	middlePosition		= (0, 0, bottomHeight)	#Placed right on top of the bottom one
	
	topOuterRadius		= 0.49/2	#Measured diameter with Callipers
	topInnerRadius		= 0.3937/2	#Measured diameter with Callipers
	topHeight			= 0.383
	topPosition			= (0, 0, bottomHeight + middleHeight)
	
	middleTopOuterRadius	= middleOuterRadius		#This acts as the top for the middle, since it is too thin
	middleTopInnerRadius	= topInnerRadius		#This is the hole that goes through the top, so the bushel can go through
	middleTopHeight			= -middleHeight*0.25	#Negative because we're going from the top downward
	middleTopPosition		= (0, 0, bottomHeight + middleHeight)
	
	leftGuideOuterRadius	= 0.0625	#GET BETTER MEASUREMENT?!?
	rightGuideOuterRadius	= leftGuideOuterRadius
	leftGuideHeight			= topHeight/2 #ALSO GET BETTER
	rightGuideHeight		= leftGuideHeight
	leftGuideYOffset			= -leftGuideOuterRadius/2 #Apparently they are offset a little.
	leftGuidePosition		= (middleOuterRadius - leftGuideOuterRadius, leftGuideYOffset, bottomHeight + middleHeight)
	rightGuidePosition		= (-leftGuidePosition[0], leftGuidePosition[1], leftGuidePosition[2]) #Put it on the other side
	
	#Now we need the box that'll make our pencil shavings hole
	holeWidthFull	= 0.75
	holeWidth		= holeWidthFull/2
	holeHeightFull	= middleHeight
	holeHeight		= holeHeightFull/2
	holeDepthFull	= middleOuterRadius
	
	holeCenterHeight = bottomHeight + (middleHeight/2)
	
	#Create the 8 points that make the box
	holePoints	= (
					(-holeWidth	, 0	, holeCenterHeight - holeHeight),
					(holeWidth	, 0	, holeCenterHeight - holeHeight),
					(holeWidth	, 0	, holeCenterHeight + holeHeight),
					(-holeWidth	, 0	, holeCenterHeight + holeHeight),
					
					(-holeWidth	, holeDepthFull	, holeCenterHeight - holeHeight),
					(holeWidth	, holeDepthFull	, holeCenterHeight - holeHeight),
					(holeWidth	, holeDepthFull	, holeCenterHeight + holeHeight),
					(-holeWidth	, holeDepthFull	, holeCenterHeight + holeHeight),
				)
					
	#Get the lines for the gears
	toothHalfWidth = 0.27
	toothDepth = bottomInnerRadius + ((bottomOuterRadius - bottomInnerRadius)/2)
	toothHeight = bottomHeight*0.75	#3/4 of the height
	
	#Now we start building all of our shapes
	
	#Start with bottom...
	brl.rcc(bottom, bottomPosition, (0, 0, bottomHeight), bottomOuterRadius)
	brl.rcc(bottomNegative, bottomPosition, (0, 0, bottomHeight), bottomInnerRadius)
	
	#Now subtract inner from outer
	brl.region(bottomRing, subtract(bottom, bottomNegative))
	
	#Now make the middle and cut it into a ring
	brl.rcc(middle, middlePosition, (0, 0, middleHeight), middleOuterRadius)
	brl.rcc(middleNegative, middlePosition, (0, 0, middleHeight), middleInnerRadius)
	brl.region(middleRing, subtract(middle, middleNegative))
	
	#Now turn the top into a ring
	brl.rcc(top, topPosition, (0, 0, topHeight), topOuterRadius)
	brl.rcc(topNegative, topPosition, (0, 0, topHeight), topInnerRadius)
	brl.region(topRing, subtract(top, topNegative))
	
	#Now going from top down, we'll turn the top into a top-hat
	brl.rcc(middleTop, middleTopPosition, (0, 0, middleTopHeight), middleTopOuterRadius)
	brl.rcc(middleTopNegative, middleTopPosition, (0, 0, middleTopHeight), middleTopInnerRadius)
	brl.region(middleTopRing, subtract(middleTop, middleTopNegative))
	
	#And now add it to the top
	brl.region(topFinal, union(topRing, middleTopRing))
	
	#Next we will add the guides to the middle...
	brl.rcc(leftGuide, leftGuidePosition, (0, 0, leftGuideHeight), leftGuideOuterRadius)
	brl.rcc(rightGuide, rightGuidePosition, (0, 0, rightGuideHeight), rightGuideOuterRadius)
	
	#Now add them
	brl.region(middleWithGuide, union(middleRing, leftGuide, rightGuide))
	
	#And now cut the hole for pencil shavings
	brl.arb8(shavingsHole, holePoints)
	brl.region(middleFinal, subtract(middleWithGuide, shavingsHole))
	
	#Finally, we'll cut the gears out of the bottom...	
	#Get all the content for the gears
	gearLines, gearName = toothGen.createGears(gearName = gearName, toFile = False, toothHalfWidth = toothHalfWidth, toothDepth = toothDepth, toothHeight = toothHeight, toothBaseName = toothName)
	
	#Now add those lines to the object...
	linesFlat = '\n'.join(gearLines)	
	brl.add_script_string(linesFlat)
	
	#Now we want to subtract the gear from the bottom
	brl.region(bottomFinal, subtract(bottomRing, gearName))
	
	#We now have a bunch of final regions. Combine them into the final gear housing
	brl.region(allFinal, union(bottomFinal, middleFinal, topFinal))
		
	#Now we can convert the .g into a .stl, using the final region. save_stl requires a list.
	brl.run_and_save_stl([allFinal])
	
if __name__ == '__main__':
    createPencilSharpener()

'''
EOF
'''