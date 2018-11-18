from python_brlcad_tcl.brlcad_tcl import *


class peristaltic_3_finger_pump__pdms(BrlCadModel):
    def __init__(self, brl_db):
        super(peristaltic_3_finger_pump__pdms, self). __init__(brl_db)
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
        self.valve_membrane_thickness = 0.1

        self.f1 = self.get_next_name(self, "f1.s")
        c1 = [0, 0, 0]
        c2 = [self.width, self.length, self.depth]
        brl_db.cuboid(c1, c2, self.f1)
        self.register_new_connection_point('flow_control_a_coord',
                                           *get_box_face_center_coord(c1, c2,
                                                                      xyz_desired=[0,-1,0]))

        self.f2 = self.get_next_name(self, "f2.s")
        c1[0] += self.finger_pitch
        c2[0] += self.finger_pitch
        brl_db.cuboid(c1, c2, self.f2)
        self.register_new_connection_point('flow_control_b_coord',
                                           *get_box_face_center_coord(c1, c2,
                                                                      xyz_desired=[0,-1,0]))

        self.f3 = self.get_next_name(self, "f3.s")
        c1[0] += self.finger_pitch
        c2[0] += self.finger_pitch
        brl_db.cuboid(c1, c2, self.f3)
        self.register_new_connection_point('flow_control_c_coord',
                                           *get_box_face_center_coord(c1, c2,
                                                                      xyz_desired=[0,-1,0]))
        self.flowtube = self.get_next_name(self, "flowtube.s")
        # (x,
        #  y,
        #  z)
        c3 = [0 - self.flow_tube_stub_length,
              (c2[1]/2)-self.flow_tube_width/2,
              0-self.flow_tube_depth-self.valve_membrane_thickness]
        self.controlled_flow_in_coord = [c3[0]]

        c4 = [c2[0] + self.flow_tube_stub_length,
              (c2[1]/2)+self.flow_tube_width/2,
              0-self.valve_membrane_thickness]
        brl_db.cuboid(c3, c4, self.flowtube)
        self.register_new_connection_point('flow_in',
                                           *get_box_face_center_coord(c3, c4,
                                                                      xyz_desired=[-1,0,0]))
        self.register_new_connection_point('flow_out',
                                           *get_box_face_center_coord(c3, c4,
                                                                      xyz_desired=[1,0,0]))
        self.final_name = self.get_next_name(self, "COMPLETE.r")

        # finally create a region (a special combination that means it's going to be rendered)
        # by unioning together the main combinations we just created
        self.final_name=brl_db.region(union(self.f1, self.f2, self.f3, self.flowtube), name=self.final_name)
        print('pump done')


if __name__ == "__main__":
    g_path_out = check_cmdline_args(__file__)
    with brlcad_tcl(g_path_out, "My Database", make_g=True) as brl_db:
        pump = peristaltic_3_finger_pump__pdms(brl_db)

        # tack on some pipes to the pneumatic and hydraluic connections
        # scale the 'away vector' dimension by 5000 to get some length
        # the 'away vector' will contain ONLY a single non-zero item
        # so the multiplication has no effect on non-set directions
        # (at least for cube faces, in the current implementation)
        a = pump.get_connection('flow_control_a_coord')
        brl_db.circular_cylinder(a[1], [_c*5000 for _c in a[2]], radius=750, name='ap.s')

        b = pump.get_connection('flow_control_b_coord')
        brl_db.circular_cylinder(b[1], [_c*5000 for _c in b[2]], radius=750, name='bp.s')

        c = pump.get_connection('flow_control_c_coord')
        brl_db.circular_cylinder(c[1], [_c*5000 for _c in c[2]], radius=750, name='cp.s')


        c = pump.get_connection('flow_in')
        brl_db.circular_cylinder(c[1], [_c*5000 for _c in c[2]], radius=100, name='fi.s')

        c = pump.get_connection('flow_out')
        brl_db.circular_cylinder(c[1], [_c*5000 for _c in c[2]], radius=100, name='fo.s')

        final_name = 'pump_and_connections.r'
        brl_db.region(union(pump.final_name,
                            'ap.s',
                            'bp.s',
                            'cp.s',
                            'fi.s',
                            'fo.s'),
                      final_name)
    print '*' * 80
    # brl_db.export_model_slices(num_slices_desired=10,
    #                            max_slice_x=30000,
    #                            max_slice_y=30000,
    #                            output_format='raster',
    #                            output_option_kwargs={'output_greyscale': True}
    #                            )
    # print '*' * 80
    # brl_db.export_model_slices(num_slices_desired=10,
    #                            max_slice_x=30000,
    #                            max_slice_y=30000,
    #                            output_format='raster',
    #                            output_option_kwargs={'output_greyscale': False},
    #                            output_path_format='{}_bw_{}.jpg'
    #                            )
    # print '*' * 80
    brl_db.export_model_slices(num_slices_desired=3,
                               max_slice_x=30000,
                               max_slice_y=30000,
                               output_format='stl',
                               output_path_format='{}_slice_{}'
                               )
    print '*' * 80
    # process the g database into an STL file with a list of regions
    brl_db.save_stl([final_name])
