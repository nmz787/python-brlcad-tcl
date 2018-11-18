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
stlQuality =0.001# 0.016

#Some variables for creating all of the various components

def createPencilSharpener():

	#Create the two cylinders for the bottom layer
	#Also we're working in Inches
	outFilePathBase = check_cmdline_args(__file__)
	brl = brlcad_tcl(project_filename_prefix = outFilePathBase, title = "Pencil Sharpener Gear",
					 make_g = False, stl_quality = stlQuality, units = 'in')
	brl.stl_quality_method = 'absolute'
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
	
	#Create our cylinders, regions, names, etc...
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
	bottom = brl.rcc(bottomPosition, (0, 0, bottomHeight), bottomOuterRadius, 'b')
	bottomNegative = brl.rcc(bottomPosition, (0, 0, bottomHeight), bottomInnerRadius, 'bn')
	
	#Now subtract inner from outer
	bottomRing = brl.region(subtract(bottom, bottomNegative), 'br')
	
	#Now make the middle and cut it into a ring
	middle = brl.rcc(middlePosition, (0, 0, middleHeight), middleOuterRadius, 'm')
 	middleNegative=brl.rcc(middlePosition, (0, 0, middleHeight), middleInnerRadius, 'mn')
	middleRing = brl.region(subtract(middle, middleNegative), 'mr')
	
	#Now turn the top into a ring
	top = brl.rcc(topPosition, (0, 0, topHeight), topOuterRadius, 't')
	topNegative = brl.rcc(topPosition, (0, 0, topHeight), topInnerRadius, 'tn')
	topRing = brl.region(subtract(top, topNegative), 'tr')
	
	#Now going from top down, we'll turn the top into a top-hat
	middleTop = brl.rcc(middleTopPosition, (0, 0, middleTopHeight), middleTopOuterRadius, 'mt')
	middleTopNegative = brl.rcc(middleTopPosition, (0, 0, middleTopHeight), middleTopInnerRadius, 'mtn')
	middleTopRing = brl.region(subtract(middleTop, middleTopNegative), 'mtr')
	
	#And now add it to the top
	topFinal = brl.region(union(topRing, middleTopRing), 'tf')
	
	#Next we will add the guides to the middle...
	leftGuide = brl.rcc(leftGuidePosition, (0, 0, leftGuideHeight), leftGuideOuterRadius, 'l')
	rightGuide = brl.rcc(rightGuidePosition, (0, 0, rightGuideHeight), rightGuideOuterRadius, 'r')
	
	#Now add them
	middleWithGuide = brl.region(union(middleRing, leftGuide, rightGuide), 'mh')
	
	#And now cut the hole for pencil shavings
	shavingsHole = brl.arb8(holePoints, 'sh')
	middleFinal = brl.region(subtract(middleWithGuide, shavingsHole), 'mf')
	
	#Finally, we'll cut the gears out of the bottom...	
	#Get all the content for the gears
	gearLines, gearName = toothGen.createGears(gearName = 'gf', toFile = False,
											   toothHalfWidth = toothHalfWidth,
											   toothDepth = toothDepth,
											   toothHeight = toothHeight,
											   toothBaseName = 'tooth')
	
	#Now add those lines to the object...
	linesFlat = '\n'.join(gearLines)	
	brl.add_script_string(linesFlat)
	
	#Now we want to subtract the gear from the bottom
	bottomFinal = brl.region(subtract(bottomRing, gearName), 'bf')
	
	#We now have a bunch of final regions. Combine them into the final gear housing
	allFinal = brl.region(union(bottomFinal, middleFinal, topFinal), 'finished')
		
	#Now we can convert the .g into a .stl, using the final region. save_stl requires a list.
	brl.run_and_save_stl([allFinal])
	
if __name__ == '__main__':
    createPencilSharpener()

'''
EOF
'''