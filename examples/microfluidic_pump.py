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

        self.f2 = self.get_next_name(self, "f2.s")
        c1[0] += self.finger_pitch
        c2[0] += self.finger_pitch
        brl_db.cuboid(self.f2, c1, c2)

        self.f3 = self.get_next_name(self, "f3.s")
        c1[0] += self.finger_pitch
        c2[0] += self.finger_pitch
        brl_db.cuboid(self.f3, c1, c2)

        self.flowtube = self.get_next_name(self, "flowtube.s")
        # (x,
        #  y,
        #  z)
        c3 = [0 - self.flow_tube_stub_length,
              (self.length/2)-self.flow_tube_width/2,
              0-self.flow_tube_depth]
        c4 = [c2[0] + self.flow_tube_stub_length,
              (self.length/2)+self.flow_tube_width/2,
              0]
        brl_db.cuboid(self.flowtube, c3, c4)
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
        # All units in the database file are stored in millimeters. This constrains
        # the arguments to the mk_* routines to also be in millimeters.
    # process the tcl script into a g database by calling mged
    brl_db.save_g()
    # process the g database into an STL file with a list of regions
    brl_db.save_stl([pump.final_name])#, aerosol_can_cap.final_name])


if __name__ == "__main__":
    main(sys.argv)
