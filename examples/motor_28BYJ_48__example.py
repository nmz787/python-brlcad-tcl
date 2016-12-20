"""
A small example of a motor in python-brlcad syntax, but using python-brlcad-tcl as the backend.

Run with:
python motor_28BYJ_48__example.py 28BYJ_48__motor_example.tcl
mged 28BYJ_48__motor_example.g < 28BYJ_48__motor_example.tcl
g-stl -o out.stl 28BYJ_48__motor_example.g motor_28BYJ_48__COMPLETE1.g
meshlab out.stl

TODO:
Add the shaft, maybe screw helices (if present on actual motor)

"""

from python_brlcad_tcl.brlcad_tcl import *


class motor_28BYJ_48():
    def __init__(self, brl_db):
        self.brl_db = brl_db
        self.get_next_name = brl_db.name_tracker.get_next_name

        self.final_name = None
        self.center_name = None

        # part properties
        self.diameter=28
        self.depth=19
        self.wire_square_width = 14.6
        self.wire_square_len_from_center = -17

        # mounting wings
        self.wing_thickness = 1
        self.screw_hole_diameter = 4.2
        self.wing_width = 7
        self.wing_hole_center_to_center = 35

        # shaft
        self.shaft_y_offset = 8
        self.body_to_shaft_base = 1.5
        self.shaft_base_diameter = 9

        self.shaft_tip_to_body = 10
        self.shaft_tip_to_keyway_base = 6
        self.shaft_base_to_keyway_base = self.shaft_tip_to_body - self.body_to_shaft_base - self.shaft_tip_to_keyway_base
        self.keyway_base_diameter = 5

        self.key_width = 3

        # create the part sections
        body = self.body()
        print 'Body DONE: {}\n'.format(body)

        mounting = self.mounting_wings()
        print 'Mounting wings DONE: {}\n'.format(mounting)
        shaft = self.shaft()
        print 'Shaft DONE: {}\n'.format(shaft)

        self.final_name = self.get_next_name(self, "COMPLETE.r")

        # finally create a region (a special combination that means it's going to be rendered)
        # by unioning together the main combinations we just created
        brl_db.region(self.final_name,
                      'u {} u {} u {}'.format(body,
                                              mounting,
                                              shaft)
                      )
        print 'Motor COMPLETED AND COMBINED into part name: {}'.format(self.final_name)

    def body(self):

        main_body_cyl = self.get_next_name(self, 'main_body_cyl.s')
        # create the motor body centered at x0,y0,z0
        self.brl_db.rcc(main_body_cyl,
                   base=(0, 0, 0),
                   height=(0, 0, self.depth),
                   radius=self.diameter/2.0)

        wire_square = self.get_next_name(self, "wire_square.s")
        self.brl_db.rpp(wire_square,
                   pmin=(self.wire_square_width/-2.0,  # x
                         self.wire_square_len_from_center,                                     # y
                         0),     # z
                   pmax=(self.wire_square_width/2.0,                       # x
                         0,   # y
                         self.depth)                            # z
                   )
        # Make a region that is the union of these two objects. To accomplish
        # this, we don't need anymore to create any linked list of the items ;-).
        main_body = self.get_next_name(self, "main_body.c")
        self.brl_db.combination(main_body,
                                'u {} u {}'.format(wire_square,
                                                   main_body_cyl)
        )

        # before returning, assemble the path to the center of the cylinder
        # this seems like a reasonable point of rotation/translation
        self.center_name = main_body + '/' + main_body_cyl

        return main_body

    def mounting_wings(self):

        # Make an rpp under the sphere (partly overlapping). Note that this really
        # makes an arb8, but gives us a shortcut for specifying the parameters.
        wing_block_name = self.get_next_name(self, "mounting_wings_rect.s")
        self.brl_db.rpp(wing_block_name,
                   pmin=(self.wing_hole_center_to_center/-2.0,  # x
                         self.wing_width/-2.0,                                     # y
                         self.depth - self.wing_thickness),     # z
                   pmax=(self.wing_hole_center_to_center/2.0,                       # x
                         self.wing_width/2.0,   # y
                         self.depth)                            # z
                   )

        print 'Completed step 0 of wings, part name: {}'.format(wing_block_name)

        #start the screw holes at z= (depth - thickness), with height thickness
        right_hole_x = self.wing_hole_center_to_center/2.0
        left_hole_x = right_hole_x * -1
        curves_and_holes = {'left_wing_curve.s':{'brldb_name':None,
                                                 'x':left_hole_x,
                                                 'r':self.wing_width/2.0},
                            'left_wing_hole.s':{'brldb_name':None,
                                                'x':left_hole_x,
                                                'r':self.screw_hole_diameter/2.0},
                            'right_wing_curve.s':{'brldb_name':None,
                                                  'x':right_hole_x,
                                                  'r':self.wing_width/2.0},
                            'right_wing_hole.s':{'brldb_name':None,
                                                 'x':right_hole_x,
                                                 'r':self.screw_hole_diameter/2.0}}
        for item_name, item in curves_and_holes.iteritems():
            item['brldb_name'] = self.get_next_name(self, item_name)
            self.brl_db.rcc(item['brldb_name'],
                       base=(item['x'],
                             0,
                             self.depth - self.wing_thickness),
                       height=(0,
                               0,
                               self.wing_thickness),
                       radius=item['r'])

        print 'Completed step 1 of wings.'
        
 
        # Make a region that is the union of these two objects. To accomplish
        # this, we don't need anymore to create any linked list of the items ;-).
        wings_block_chamfered = self.get_next_name(self, "wings_chamfered.c")
        self.brl_db.combination(wings_block_chamfered,
                                'u {} u {} u {}'.format(curves_and_holes['left_wing_curve.s']['brldb_name'],
                                                        curves_and_holes['right_wing_curve.s']['brldb_name'],
                                                        wing_block_name)
        )
        print 'Completed step 2 of wings, part name: {}'.format(wings_block_chamfered)

        # now subtract the holes away
        wings_block_left_hole_subtracted = self.get_next_name(self, "wings_left_subtracted.c")
        self.brl_db.combination(wings_block_left_hole_subtracted,
                           'u {} - {}'.format(wings_block_chamfered,
                                              curves_and_holes['left_wing_hole.s']['brldb_name'])
        )


        print 'Completed step 3 of wings, part name: {}'.format(wings_block_left_hole_subtracted)

        wings_block = self.get_next_name(self, "wings_block.c")
        self.brl_db.combination(wings_block,
                           'u {} - {}'.format(wings_block_left_hole_subtracted,
                                              curves_and_holes['right_wing_hole.s']['brldb_name'])
        )
        print 'Completed step 4 of wings, part name: {}'.format(wings_block)
        return wings_block

        # Makes the two screw holes
        # Note that you can provide a single combination name or a list in the
        # obj_list parameter, it will be handled correctly, all the tedious list
        # building is done under the hood:
        """
        brl_db.hole(
            hole_start=(0, 0, 0),
            hole_depth=(2, 4, 2.5),
            hole_radius=0.75,
            obj_list="mounting_wings.r"
        )
        """

    def shaft(self):    
        shaft1 = self.get_next_name(self, 'body_to_shaft_base.s')
        # create the motor body centered at x0,y0,z0
        self.brl_db.rcc(shaft1,
                   base=(0,
                         self.shaft_y_offset,
                         self.depth),
                   height=(0,
                           0,
                           self.body_to_shaft_base),
                   radius=self.shaft_base_diameter/2.0)
        print 'Completed step 1 of shaft, part name: {}'.format(shaft1)

        shaft2 = self.get_next_name(self, "shaft_base.s")
        self.brl_db.rcc(shaft2,
                        base=(0,  # x
                              self.shaft_y_offset,                                     # y
                              self.depth+self.body_to_shaft_base),     # z
                        height=(0,                       # x
                                0,   # y
                                self.shaft_base_to_keyway_base),                           # z
                        radius=self.keyway_base_diameter/2.0
                        )
        print 'Completed step 2 of shaft, part name: {}'.format(shaft2)

        key_start = self.depth + self.body_to_shaft_base + self.shaft_base_to_keyway_base
        key_end = key_start + self.shaft_tip_to_keyway_base

        shaft3 = self.get_next_name(self, "shaft_key_cyl.s")
        self.brl_db.rcc(shaft3,
                        base=(0,  # x
                              self.shaft_y_offset,                                     # y
                              key_start),     # z
                        height=(0,                       # x
                                0,   # y
                                self.shaft_tip_to_keyway_base),                           # z
                        radius=self.keyway_base_diameter/2.0
                        )
        print 'Completed step 3 of shaft, part name: {}'.format(shaft3)

        shaft4 = self.get_next_name(self, "shaft_key_rpp.s")
        self.brl_db.rpp(shaft4,
                        pmin=(self.keyway_base_diameter/-2.0,  # x
                              self.shaft_y_offset-(self.key_width/2.0),                                     # y
                              key_start),     # z
                        pmax=(self.keyway_base_diameter/2.0,                       # x
                              self.shaft_y_offset+(self.key_width/2.0),   # y
                              key_end)                           # z
                        )
        print 'Completed step 4 of shaft, part name: {}'.format(shaft4)

        shaft_key = self.get_next_name(self, "shaft_key.c")
        self.brl_db.combination(shaft_key,
                                'u {} + {}'.format(shaft3,
                                                   shaft4
                                                 )
        )
        print 'Completed step 5 of shaft, part name: {}'.format(shaft_key)

        # Make a region that is the union of these two objects. To accomplish
        # this, we don't need anymore to create any linked list of the items ;-).
        shaft = self.get_next_name(self, "shaft.c")
        self.brl_db.combination(shaft,
                                'u {} u {} u {}'.format(shaft1,
                                                        shaft2,
                                                        shaft_key)
        )
        return shaft

    def wires(self):
        pass


if __name__ == "__main__":
    #with wdb.WDB(argv[1], "My Database") as brl_db:
    g_path_out = check_cmdline_args(__file__)
    with brlcad_tcl(g_path_out, "My Database", make_g=True) as brl_db:
        motor = motor_28BYJ_48(brl_db)
        # All units in the database file are stored in millimeters. This constrains
        # the arguments to the mk_* routines to also be in millimeters.
    brl_db.save_stl([motor.final_name])
