"""
A small python-brlcad-tcl example that creates a spring with the pipe primitive
It creates a tcl file, then sends it to mged which creates and populates a .g file database,
 then the .g file is converted with g-stl to produce an STL file.

Run with:
python spring.py spring.tcl
"""

from python_brlcad_tcl.brlcad_tcl import *

        
if __name__ == "__main__":
    g_path_out = check_cmdline_args(__file__)
    with brlcad_tcl(g_path_out, "My Database1") as brl_db:

        # create a lookup table for 4 X,Y points on the spring circumference
        spring_outline_x_y_tuples = [(-50,-50), (-50,50), (50,50), (50,-50)]
        # create points, using the 10 for the z-step between points on the circumference.
        # the number of circumference points (4) times the z-step (10) yields 40, which is used to mod the z-value
        # this gets a series of 0,1,2,3 repeating, which is used as an index to the circumference X,Y values list
        # these tuples then get unpacked into the two x and y values using the * notation
        z_step = 10
        points = []
        for z in range(0, 110, 10):
            circumference_xy_index = (z%(len(spring_outline_x_y_tuples)*z_step)) / z_step 
            x, y = spring_outline_x_y_tuples[circumference_xy_index]
            point = brl_db.pipe_point(x=x,
                                      y=y,
                                      z=z,
                                      inner_diameter=2,
                                      outer_diameter=5,
                                      bend_radius=50)
            points.append(point)
        spring1 = brl_db.pipe(points,'spring1.s')
        spring = brl_db.region(union(spring1), 'spring.r')
        
    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    # process the g database into an STL file with a list of regions
    brl_db.save_stl([spring])
