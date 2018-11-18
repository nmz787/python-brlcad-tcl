# sys has argv
import sys

#from brlcad.primitives import union, subtract
#import brlcad.wdb as wdb
# sys has argv
import sys
import os
from math import atan
from math import degrees

from python_brlcad_tcl.brlcad_tcl import *


class shed_example(BrlCadModel):
    def __init__(self, brl_db):
        super(shed_example, self). __init__(brl_db)
        ceiling = 10
        peak = 15
        wall_thickness = 0.2

        c1 = [0, 0, 0]
        c2 = [16, 12, ceiling]
        shedbox = brl_db.cuboid(c1, c2, 'shedbox')
        
        c1 = [0+wall_thickness, 0+wall_thickness, 0+wall_thickness]
        c2 = [16-wall_thickness, 12-wall_thickness, ceiling+wall_thickness]
        room_void = brl_db.cuboid(c1, c2, 'room_void')

        c1 = [0, 5, ceiling - wall_thickness]
        c2 = [16, 12, ceiling]
        loft = brl_db.cuboid(c1, c2, 'loft')

        

        def make_roof(roof_name,w,l,x,y,z,z2):
            c1 = (x,   y      , z)
            c2 = (x,   y+l    , z)
            c3 = (x,   y+(l/2), z2)
            c4 = (x+w, y      , z) 
            c5 = (x+w, y+l    , z)
            c6 = (x+w, y+(l/2), z2)  
            return brl_db.arb6(c1, c2,c3,c4,c5,c6, roof_name)

        mainroof =  make_roof('mainroof',16,12,0,0,ceiling,15)
        
        inner_void = make_roof('inner_void',16-(wall_thickness*2), 12-(wall_thickness*2),
                                       0+wall_thickness,0+wall_thickness, 
                                       ceiling-wall_thickness, 15-wall_thickness)

        # finally create a region (a special combination that means it's going to be rendered)
        # by unioning together the main combinations we just created
        # brl_db.region(self.final_name,
        #               'u {}'.format(' u '.join(['shedbox', 'shedroof']))
        #               )

        # brl_db.combination('roof', 'u mainroof - inner_void')
        #brl_db.combination('room', 'u shedbox - room_void')


        def box_window(name,x,y,z,w,h,d, rot_axis=None, degrees=None):
            c1 = [x-(w/2),y-(d/2),z-(h/2)]
            c2 = [x+(w/2),y+(d/2),z+(h/2)]
            cube = brl_db.cuboid(c1, c2, name)
            if rot_axis is not None:
                xx = 1 if rot_axis=='x' else 0
                yy = 1 if rot_axis=='y' else 0
                zz = 1 if rot_axis=='z' else 0
                brl_db.rotate_angle(cube,xx,yy,zz,degrees)
            return cube
    

        def french_door(name,x,y,z,w,h,d,rot):
            c1 = [x-w/2,y-d/2,z-h/2]
            c2 = [x+w/2,y+d/2,z+h/2]
            return brl_db.cuboid(c1, c2, name)

        o = peak - ceiling
        a = 6
        window_rot = atan(float(o)/float(a))
        window_rot = degrees(window_rot)
        box_window1 = box_window('box_window1', 2,  0, 10/2, 2, 4, wall_thickness*3)
        box_window2 = box_window('box_window2', 14, 0, 10/2, 2, 4, wall_thickness*3)

        roof_window1 = box_window('roof_window1', x=2, y=12/4, z=10+(5/2.),
                                  w=2, h=4, d=wall_thickness*3, rot_axis= 'x', degrees=window_rot+90)

        roof_window2 = box_window('roof_window2', x=14, y=12/4, z=10+(5/2.),
                                  w=2, h=4, d=wall_thickness*3, rot_axis= 'x', degrees=window_rot+90)
        french_door = french_door('french_door', x=8, y=0, z=3+wall_thickness, w=5.5,h=6,d=wall_thickness*3,rot=0)


        room = brl_db.combination(union(shedbox - box_window1 - box_window2 -
                                        room_void - french_door),
                                  'room')
        #brl_db.combination('room', 'u shedbox - room_void')
        roof = brl_db.combination(subtract(mainroof - inner_void - roof_window1 - roof_window2),
                                  'roof')
        shed = brl_db.combination(union(room, roof, loft),
                                  'shed')
        print('done')


def main(argv):
    #with wdb.WDB(argv[1], "My Database") as brl_db:
    with brlcad_tcl(argv[1], "My Database") as brl_db:
        shed = shed_example(brl_db)
        # All units in the database file are stored in millimeters. This constrains
        # the arguments to the mk_* routines to also be in millimeters.
    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    # process the g database into an STL file with a list of regions
    #brl_db.save_stl(['room', 'mainroof', 'roof_window1', 'roof_window2'])  
    brl_db.save_stl(['shed'])

if __name__ == "__main__":
    main(sys.argv)
