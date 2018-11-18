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

"""
21:52 < DaRock> oh I see. I'll have a proper look at the github code then a bit later. I'm not a github user, so how would I post a patch then?
21:53 < DaRock> no idea... I'll probably download the code and have tweak and see what the algorithm would need to be to work effectively
21:54 < DaRock> it would have to be related to radius, I believe, to adjust the number of blocks used to make up the radius
21:55 < DaRock> so... that would also depend on the size of the blocks used too
21:56 < DaRock> size of the blocks wouldn't have to change, so... 2<pi>r/<size of block>
21:57 < DaRock> wrap a coefficient around that to ensure overlap
21:59 < DaRock> I might be going backwards there... we're working out that coefficient aren't we? ...
22:04 < DaRock> not radius_interval - degree interval!
22:12 < DaRock> scratch that... needs more thinking :-) looking at the full code now and its not following the same path I had thought
22:46 < DaRock> nmz787_: got it (I think) - try degree_interval/inner_radius. That keeps your arc length the same throughout, and adjust the radians you're using to generate the shapes' location
22:47 < DaRock> arc length is calculated using theta*r so rearranging as above should sort it
22:47 < DaRock> in theory :-P
22:50 < DaRock> give that a spin and post the stl if you can. Unfortunately I haven't the ability to setup the python to run it right now...
22:53 < DaRock> if the outer blocks connect, then you should be able to use intersection then, and then your result should be smoother just as you envisioned :-)
"""

def spiral_channel(brl_db, width, height, inner_radius, outer_radius, degree_interval=0.1, radius_interval=0.5):
    x = None
    y = None
    t=0.0
    ang = 0 
    method = 'use_square'
    # default keypoint is bottom corner, the box base center is at x: 0, y: 0
    xkey = 0
    ykey = 0

    segments = []
    while inner_radius < outer_radius:
        x = inner_radius * math.cos(t)
        y = inner_radius * math.sin(t)
        inner_radius += radius_interval
        ang = 90.0 - math.atan2(y, x) * 180.0 / math.pi

        shape_name = "spiral_segment_{}_{}.s".format(ang, inner_radius)
        #shape_name = "spiral_segment_{}_{}.s".format(t, inner_radius)
        if method == 'use_cylinder':
            shape_name = brl_db.rcc((x,y,0),(0, 0, height), width/2.0, shape_name)
        else:
            shape_name = brl_db.rpp((x - width/2.0, y - width/2.0, 0),
                                    (x + width/2.0, y + width/2.0, height),
                                    shape_name)
            #brl_db.rotate_primitive(shape_name, 0,0, 1, t%360.0)

            brl_db.rotate_primitive(shape_name, 0,0, ang)
            
            #ang+=45
            #brl_db.rotate_primitive(shape_name, 1,1, 0, degree_interval)
        t+=degree_interval
        segments.append(shape_name)
    final_region = brl_db.region(union(segments), 'spiral.r')
    #region_name = "hilbert_pipe_{}{}{}{}{}.r".format(o1, o2, *crt_dir)
    #brl_db.region(region_name, 'u {}'.format(shape_name))
    return final_region


if __name__ == "__main__":
    g_path_out = check_cmdline_args(__file__, "spiral.tcl")
    with brlcad_tcl(g_path_out, "Spiral", stl_quality=0.5) as brl_db:
        final_region = spiral_channel(brl_db, 8,10, 10, 100)

    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    # process the g database into an STL file with a list of regions
    brl_db.save_stl([final_region])