#Imports
import os, sys

#Import sister module.
sys.path.append('../python-brlcad-tcl')
import brlcad_tcl
import toothGen

#Some constants
endl = '\n'
spc = ' '

#The path to output to, based on the location of the current file
scriptPath = os.path.dirname(__file__)
outFilePath = scriptPath + r'/output/toothGen.tcl'

#Some variables for creating all of the various components

def createPencilSharpener():

    #Create the two cylinders for the bottom layer
    brl = brlcad_tcl()
    brl.


    #Get the lines for the gears
    gearLines, gearName = toothGen.createGears()

'''
EOF
'''