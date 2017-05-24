"""
Spiral
Run with:
python spiral.py
"""

# sys has argv
import sys
import os
import math
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-brlcad-tcl')))
from python_brlcad_tcl.brlcad_tcl import *

def spiral_channel(width, height, inner_radius, outer_radius, degree_interval=0.1, radius_interval=0.5):
    x = None
    y = None
    t=0
    ang = 0 
    method = 'use_square'
    # default keypoint is bottom corner, the box base center is at x: 0, y: 0
    xkey = 0
    ykey = 0
    with brlcad_tcl("spiral.tcl", "Spiral", stl_quality=0.5) as brl_db:
        segments = []
        while inner_radius < outer_radius:
            x = inner_radius * math.cos(t)
            y = inner_radius * math.sin(t)
            inner_radius += radius_interval
            ang = 90.0 - math.atan2(y, x) * 180.0 / math.pi

            shape_name = "spiral_segment_{}_{}.s".format(ang, inner_radius)
            #shape_name = "spiral_segment_{}_{}.s".format(t, inner_radius)
            if method == 'use_cylinder':
                brl_db.rcc(shape_name, (x,y,0),(0, 0, height), width/2.0)
            else:
                brl_db.rpp(shape_name, 
                           (x - width/2.0, y - width/2.0, 0),
                           (x + width/2.0, y + width/2.0, height)
                          )
                #brl_db.rotate_primitive(shape_name, 0,0, 1, t%360.0)

                brl_db.rotate_primitive(shape_name, 0,0, ang)
                
                #ang+=45
                #brl_db.rotate_primitive(shape_name, 1,1, 0, degree_interval)
            t+=degree_interval
                
            segments.append(shape_name)
        brl_db.region('spiral.r', 'u ' + ' u '.join(segments))
        #region_name = "hilbert_pipe_{}{}{}{}{}.r".format(o1, o2, *crt_dir)
        #brl_db.region(region_name, 'u {}'.format(shape_name))

    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    # process the g database into an STL file with a list of regions
    brl_db.save_stl(['spiral.r'])


if __name__ == "__main__":
    # hilbert_3D_test()
    spiral_channel(8,10, 10, 100)