"""
A small python-brlcad-tcl example that imports a motor then creates a cylindrical cup,
 then rotates and translates the motor so the back is at the bottom of the cup.
It creates a tcl file, then sends it to mged which creates and populates a .g file database,
 then the .g file is converted with g-stl to produce an STL file.

Run with:
python multi_part_example.py out.tcl

TODO:
add toroid or revolved wegde-shape lip so the lid can click into an aerosol-type can (spray paint, whipped cream)

"""

# sys has argv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-brlcad-tcl')))
from brlcad_tcl import *
from brlcad_name_tracker import BrlcadNameTracker

from motor_28BYJ_48__example import motor_28BYJ_48


class aerosol_can_snap_cap(object):
    def __init__(self, brl_db, name_tracker):
        #cap_height = 40
        self.get_next_name = name_tracker.get_next_name
        self.brl_db = brl_db

        self.lower_rim_inner_diamater = 61.1 # may need to change to 61.0mm
        self.lower_rim_lip_height = 3
        self.lower_rim_trough_height = 2
        self.lower_rim_outer_diameter = 63.1
        self.lower_rim_outer_top__to_sprayer_bottom = 24.5
        self.sprayer_height = 12
        self.sprayer_diameter = 10.5

        self.shell_thickness = 2

        self.twice_sprayer_height = self.lower_rim_lip_height + self.lower_rim_trough_height + self.lower_rim_outer_top__to_sprayer_bottom + self.sprayer_height

        self.shell()

    def shell(self):
        main_body_cyl = self.get_next_name(self, 'main_body_cyl.s')
        # create the outer cylinder
        self.brl_db.rcc(main_body_cyl,
                   base=(0, 0, 0),
                   height=(0, 0, self.twice_sprayer_height),
                   radius=(self.lower_rim_outer_diameter/2.0)+self.shell_thickness)

        inner_main_body_cyl = self.get_next_name(self, 'inner_main_body_cyl.s')
        # create the inner cylinder to be subtracted
        self.brl_db.rcc(inner_main_body_cyl,
                   base=(0, 0, 0),
                   height=(0, 0, self.twice_sprayer_height - self.shell_thickness),
                   radius=(self.lower_rim_outer_diameter/2.0))

        cap_shell = self.get_next_name(self, "cap_shell.r")
        # make a union of the subtraction of the inner from the outer
        # also make it a region (a special combination that means it's going to be rendered)
        self.brl_db.region(cap_shell,
                           'u {} - {}'.format(main_body_cyl,
                                              inner_main_body_cyl)
        )
        self.final_name = cap_shell
        '''
        self.brl_db.arb8(
            "arb8.s",
            points=[
                (-1, -1, 5), (1, -1, 5), (1, 1, 5), (-1, 1, 5),
                (-0.5, -0.5, 6.5), (0.5, -0.5, 6.5), (0.5, 0.5, 6.5), (-0.5, 0.5, 6.5)
            ]
        )
        self.brl_db.translate_relative("arb8.s", -100,0,0)
        '''

def main(argv):
    #with wdb.WDB(argv[1], "My Database") as brl_db:
    with brlcad_tcl(argv[1], "My Database1") as brl_db:
        name_tracker = BrlcadNameTracker()
        
        motor = motor_28BYJ_48(brl_db, name_tracker)
        aerosol_can_cap = aerosol_can_snap_cap(brl_db, name_tracker)

        brl_db.begin_combination_edit(motor.final_name, motor.center_name)
        brl_db.rotate_combination(180,0,0)
        brl_db.translate_relative(0,(aerosol_can_cap.lower_rim_outer_diameter )*.25 - aerosol_can_cap.shell_thickness , aerosol_can_cap.twice_sprayer_height- aerosol_can_cap.shell_thickness )
        brl_db.end_combination_edit()
    
    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    # process the g database into an STL file with a list of regions
    brl_db.save_stl([motor.final_name, aerosol_can_cap.final_name])


if __name__ == "__main__":
    main(sys.argv)
