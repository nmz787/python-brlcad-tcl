# sys has argv
import sys

#from brlcad.primitives import union, subtract
#import brlcad.wdb as wdb
# sys has argv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-brlcad-tcl')))

from brlcad_tcl import *
from brlcad_name_tracker import BrlcadNameTracker


class peristaltic_3_finger_pump(BrlCadModel):
    def __init__(self, brl_db, name_tracker):
        super(peristaltic_3_finger_pump, self). __init__(brl_db, name_tracker)
        self.center_name = None

        # units are in microns
        self.layer_thickness = 1000

        # finger properties
        self.width=1000
        self.length=4000
        self.depth=1000

        self.finger_pitch = 2000

        self.finger_supply_trace_width_and_depth=500


        self.flow_tube_width = 2000
        self.flow_tube_depth = 500
        self.flow_tube_stub_length = 1000

        self.f1 = self.get_next_name(self, "f1.s")
        c1 = [0, 0, 0]
        c2 = [self.width, self.length, self.depth]
        brl_db.cuboid(self.f1, c1, c2)
        self.register_new_connection_point('flow_control_a_coord',
                                           *get_box_face_center_coord(c1, c2,
                                                                      xyz_desired=[0,-1,0]))

        self.f2 = self.get_next_name(self, "f2.s")
        c1[0] += self.finger_pitch
        c2[0] += self.finger_pitch
        brl_db.cuboid(self.f2, c1, c2)
        self.register_new_connection_point('flow_control_b_coord',
                                           *get_box_face_center_coord(c1, c2,
                                                                      xyz_desired=[0,-1,0]))

        self.f3 = self.get_next_name(self, "f3.s")
        c1[0] += self.finger_pitch
        c2[0] += self.finger_pitch
        brl_db.cuboid(self.f3, c1, c2)
        self.register_new_connection_point('flow_control_c_coord',
                                           *get_box_face_center_coord(c1, c2,
                                                                      xyz_desired=[0,-1,0]))
        self.flowtube = self.get_next_name(self, "flowtube.s")
        # (x,
        #  y,
        #  z)
        c3 = [0 - self.flow_tube_stub_length,
              (c2[1]/2)-self.flow_tube_width/2,
              0-self.flow_tube_depth]
        self.controlled_flow_in_coord = [c3[0]]

        c4 = [c2[0] + self.flow_tube_stub_length,
              (c2[1]/2)+self.flow_tube_width/2,
              0]
        brl_db.cuboid(self.flowtube, c3, c4)
        self.register_new_connection_point('flow_in',
                                           *get_box_face_center_coord(c3, c4,
                                                                      xyz_desired=[-1,0,0]))
        self.register_new_connection_point('flow_out',
                                           *get_box_face_center_coord(c3, c4,
                                                                      xyz_desired=[1,0,0]))
        self.final_name = self.get_next_name(self, "COMPLETE.r")

        # finally create a region (a special combination that means it's going to be rendered)
        # by unioning together the main combinations we just created
        brl_db.region(self.final_name,
                      'u {} u {} u {} u {}'.format(self.f1, self.f2, self.f3, self.flowtube)
                      )
        print('pump done')


def main(argv):
    #with wdb.WDB(argv[1], "My Database") as brl_db:
    with brlcad_tcl(argv[1], "My Database") as brl_db:
        name_tracker = BrlcadNameTracker()
        pump = peristaltic_3_finger_pump(brl_db, name_tracker)

        # tack on some pipes to the pneumatic and hydraluic connections
        # scale the 'away vector' dimension by 5000 to get some length
        # the 'away vector' will contain ONLY a single non-zero item
        # so the multiplication has no effect on non-set directions
        # (at least for cube faces, in the current implementation)
        a = pump.get_connection('flow_control_a_coord')
        brl_db.circular_cylinder('ap.s',a[1], [_c*5000 for _c in a[2]], radius=750)

        b = pump.get_connection('flow_control_b_coord')
        brl_db.circular_cylinder('bp.s',b[1], [_c*5000 for _c in b[2]], radius=750)

        c = pump.get_connection('flow_control_c_coord')
        brl_db.circular_cylinder('cp.s',c[1], [_c*5000 for _c in c[2]], radius=750)


        c = pump.get_connection('flow_in')
        brl_db.circular_cylinder('fi.s',c[1], [_c*5000 for _c in c[2]], radius=100)

        c = pump.get_connection('flow_out')
        brl_db.circular_cylinder('fo.s',c[1], [_c*5000 for _c in c[2]], radius=100)

        final_name = 'new_' + pump.final_name
        brl_db.region(final_name,
                      'u {} u {} u {} u {} u {} u {}'
                      .format(pump.final_name,
                              'ap.s', 
                              'bp.s', 
                              'cp.s', 
                              'fi.s', 
                              'fo.s')
                      )


        

        # All units in the database file are stored in millimeters. This constrains
        # the arguments to the mk_* routines to also be in millimeters.
    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    orig_path = brl_db.now_path
    slice_coords = brl_db.export_slices(300, 30000,30000)
    
    for i, sc in enumerate(slice_coords):
      brl_db.now_path = orig_path + str(i)
      if i==0:
        brl_db.run_and_save_stl(['slice{}.r'.format(i)])
      else:
        brl_db.save_stl(['slice{}.r'.format(i)])
    
    brl_db.now_path = orig_path
    # process the g database into an STL file with a list of regions
    brl_db.save_stl([final_name])#, aerosol_can_cap.final_name])
    

if __name__ == "__main__":
    main(sys.argv)
