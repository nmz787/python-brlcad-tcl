"""
needs much work, scaling or dimensions of somethign seems off
"""
from python_brlcad_tcl.brlcad_tcl import *

from examples.microfluidic_pump import peristaltic_3_finger_pump__pdms


class mems_hello_world(BrlCadModel):
    """
    Product Code: SN100-P20Q05
    $32.00 (each, minimum purchase quantity 10)

    Nanoporous Amorphous film
    100 micron thick frame, fits 3 mm sample holders
    Dimensions: (1) 500 x 500 micron window
    20 nm thick low-stress silicon nitride
    Average pore diameter is 30 nm and porosity is ~25%
    """
    def __init__(self, brl_db):
        self.brl_db = brl_db

        pump = peristaltic_3_finger_pump__pdms(brl_db)

        # tack on some pipes to the pneumatic and hydraluic connections
        # scale the 'away vector' dimension by 5000 to get some length
        # the 'away vector' will contain ONLY a single non-zero item
        # so the multiplication has no effect on non-set directions
        # (at least for cube faces, in the current implementation)
        a = pump.get_connection('flow_control_a_coord')
        c0 = brl_db.circular_cylinder(
                a[1],
                [_c*5000 for _c in a[2]],
                radius=750)
        # inner_diameter = 0
        # outer_diameter = 750
        # bend_radius = 50
        # pipe_points = [brl_db.pipe_point(x=a[1][0], y=a[1][1], z=a[1][2],
        #                                  inner_diameter=inner_diameter, outer_diameter=outer_diameter, bend_radius=bend_radius),
        #                brl_db.pipe_point(x=a[2][0], y=a[2][1]+5000, z=a[2][2],
        #                                  inner_diameter=inner_diameter, outer_diameter=outer_diameter, bend_radius=bend_radius)]
        # pip = brl_db.pipe(pipe_points)

        b = pump.get_connection('flow_control_b_coord')
        c1 = brl_db.circular_cylinder(b[1],
                                 [_c*5000 for _c in b[2]],
                                 radius=750,
                                 name='bp.s')

        c = pump.get_connection('flow_control_c_coord')
        c2 = brl_db.circular_cylinder(c[1],
                                 [_c*5000 for _c in c[2]],
                                 radius=750, 
                                 name='cp.s')


        c = pump.get_connection('flow_in')
        c3 = brl_db.circular_cylinder(c[1],
                                 [_c*5000 for _c in c[2]],
                                 radius=100, 
                                 name='fi.s')

        c = pump.get_connection('flow_out')
        c4 = brl_db.circular_cylinder(c[1],
                                 [_c*5000 for _c in c[2]],
                                 radius=100,
                                 name='fo.s')

        final_name = 'new_' + str(pump.final_name)
        pump_region = brl_db.region(
                union(
                    pump.final_name,
                    c0,
                    c1,
                    c2,
                    c3,
                    c4),
                    name=final_name)

        brl_db.begin_combination_edit(pump_region, c2)
        brl_db.translate_relative(0,
                                  -5000,
                                  0)
        brl_db.end_combination_edit()

        # assume units in mcrons
        f = brl_db.cuboid((0,0,0),
                          (3000, 3000, 100))
        
        half_frame = (3000/2.)

        #half_nanoporous = (500/2.)
        #half_nanoporous = (500/2.)/ 1000.
        nm_wide = 500#*1000
        half_nanoporous = self.nm_to_um(nm_wide/2.)
        npf_overhang_on_frame = self.nm_to_um(nm_wide/10.)


        npf = brl_db.cuboid((half_frame - half_nanoporous,
                             half_frame - half_nanoporous,
                             100),
                            (half_frame + half_nanoporous,
                             half_frame + half_nanoporous,
                             100.02))
        
        t1 = half_frame - half_nanoporous + npf_overhang_on_frame
        t1 = (t1, t1, 100)
        t2 = t1[0] - npf_overhang_on_frame + half_nanoporous + half_nanoporous - npf_overhang_on_frame
        t2 = (t2, t1[0], 100)
        t3 = (t2[0],t2[0], 100)
        t4 = (t1[0],t2[0], 100)
        b1 = (half_frame - 500, half_frame - 500, 0)
        b2 = (3000 - b1[0], b1[0], 0)
        b3 = (b2[0], b2[0], 0)
        b4 = (b1[0], b2[0], 0)
        npf_cutout = brl_db.arb8([t1, t2, t3, t4, b1, b2, b3, b4])

        # loop over the porous area, in nanometers, attempting to simulate 25% porosity with 30nm average diameter pore
        nm_between_pores = 30*4 
        tot_sq_nm = nm_wide * nm_wide
        pores_list = []
        print('tot_sq_nm: {}'.format(tot_sq_nm))
        for x in range(1, nm_wide, nm_between_pores):
            xx = x/1000.
            for y in range(1, nm_wide, nm_between_pores):
                p = brl_db.rcc((xx,
                                y/1000.,
                                100),
                               (0, 0, 0.02), 30 / 1000.)
                pores_list.append(p)
                
        print(pores_list)
        pores_negative = brl_db.group(join_as_str(' ', pores_list), name='pore_negative_array.g')

        brl_db.begin_combination_edit(pores_negative, pores_list[0])
        brl_db.translate_relative(half_frame - (half_nanoporous ),
                                  half_frame - (half_nanoporous ),
                                  0)
        brl_db.end_combination_edit()

        nps = brl_db.combination('u {} - {}'.format(npf, pores_negative), 'pores.c')
        self.final_name = brl_db.region('u {} u {} u {} - {}'.format(nps, pump_region, f, npf_cutout), 'sieve.r')


    def mm_to_um(self, mm):
        # 1000 microns per mm
        return mm * 1000.

    def nm_to_um(self, nm):
        return nm / 1000.


if __name__ == "__main__":
    g_path_out = check_cmdline_args(__file__)
    with brlcad_tcl(g_path_out, "My Database", make_g=True, verbose=True, stl_quality=1.0, units='mm') as brl_db:
        ns = mems_hello_world(brl_db)
    brl_db.save_stl([ns.final_name])
