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

from python_brlcad_tcl.brlcad_tcl import *

from examples.motor_28BYJ_48__example import motor_28BYJ_48


class aerosol_can_snap_cap(object):
    def __init__(self, brl_db):
        #cap_height = 40
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
        # create the outer cylinder
        main_body_cyl = self.brl_db.rcc(
                            base=(0, 0, 0),
                            height=(0, 0, self.twice_sprayer_height),
                            radius=((self.lower_rim_outer_diameter/2.0)+
                                    self.shell_thickness),
                            name='main_body_cyl.s')

        # create the inner cylinder to be subtracted
        inner_main_body_cyl =self.brl_db.rcc(
                   base=(0, 0, 0),
                   height=(0, 0, self.twice_sprayer_height - self.shell_thickness),
                   radius=(self.lower_rim_outer_diameter/2.0),
                   name='inner_main_body_cyl.s')

        # make a union of the subtraction of the inner from the outer
        # also make it a region (a special combination that means it's going to be rendered)
        cap_shell = self.brl_db.region(subtract(main_body_cyl,
                                                inner_main_body_cyl),
                                       "aerosol_can_snap_cap__cap_shell1.r"
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

if __name__ == "__main__":
    g_path_out = check_cmdline_args(__file__)
    with brlcad_tcl(g_path_out, "My Database1") as brl_db:
        motor = motor_28BYJ_48(brl_db)
        aerosol_can_cap = aerosol_can_snap_cap(brl_db)

        brl_db.begin_combination_edit(motor.final_name, motor.center_name)
        brl_db.rotate_combination(180,0,0)
        brl_db.translate_relative(0,(aerosol_can_cap.lower_rim_outer_diameter )*.25 - aerosol_can_cap.shell_thickness , aerosol_can_cap.twice_sprayer_height- aerosol_can_cap.shell_thickness )
        brl_db.end_combination_edit()
    
    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    # process the g database into an STL file with a list of regions
    brl_db.save_stl([motor.final_name, aerosol_can_cap.final_name])
