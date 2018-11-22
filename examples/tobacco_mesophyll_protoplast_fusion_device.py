#if __name__ == "__main__":
    #import os
    #import sys
    #sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-brlcad-tcl')))

from math import pi, cos, sin, asin
from python_brlcad_tcl.brlcad_tcl import *


class tobacco_mesophyll_protoplast_fusion_device(BrlCadModel):
    def __init__(self,
                 input_port_diameter,
                 input_symmetric_bifurcation_inner_width,
                 input_symmetric_bifurcation_outer_width,
                 symmetric_bifurcation_post_w,
                 symmetric_bifurcation_post_h,
                 symmetric_bifurcation_post_roundness,
                 symmetric_bifurcation_post_pitch,
                 length_catcher,
                 width_catcher,
                 catcher_post_w,
                 catcher_post_h,
                 catcher_post_roundness,
                 catcher_post_pitch,
                 distance_output_port_from_center,
                 dist_center_catcher_to_center_device,
                 io_height,
                 protoplast_chamber_height,
                 output_port_diameter,
                 num_output_ports,
                 brl_db):
        super(tobacco_mesophyll_protoplast_fusion_device, self).__init__(brl_db)
        self.outlets = []

        pdms_slab = self.pdms_slab(distance_output_port_from_center, io_height)

        self.center_input = self._center_input(input_port_diameter, io_height)

        bot = self.protoplast_bottom_layer_2d(input_port_diameter,
                                              input_symmetric_bifurcation_inner_width,
                                              input_symmetric_bifurcation_outer_width,
                                              symmetric_bifurcation_post_w,
                                              symmetric_bifurcation_post_h,
                                              symmetric_bifurcation_post_roundness,
                                              symmetric_bifurcation_post_pitch,
                                              length_catcher,
                                              width_catcher,
                                              catcher_post_w,
                                              catcher_post_h,
                                              catcher_post_roundness,
                                              catcher_post_pitch,
                                              distance_output_port_from_center,
                                              dist_center_catcher_to_center_device,
                                              io_height,
                                              protoplast_chamber_height,
                                              output_port_diameter,
                                              num_output_ports)
        # at this point, this is pretty much a 'negative' of what we want to create
        bot_and_io = brl_db.region('u {} u {}'
                                   .format(bot, self.center_input), 
                                   'bot_and_io.c',)
        self.negative = bot_and_io
        self.final_name = brl_db.region('u {} - {}'
                                        .format(pdms_slab, bot_and_io),
                                        'slab_minus_bot_and_io',)

    def pdms_slab(self, distance_output_port_from_center, io_height):
        width = distance_output_port_from_center * 3
        p1 = ((width / -2), (width / -2), 0)
        p2 = ((width / -2) + width, (width / -2) + width, io_height)
        return brl_db.cuboid(p1, p2)

    def radial_outlet(self,
                      input_port_diameter,
                      len_funnel,
                      length_catcher,
                      output_port_diameter,
                      height
                      ):
        outlet_xoff_from_center = (input_port_diameter / 2) + len_funnel + length_catcher

        return self.brl_db.rcc(name=None,
                               base=(outlet_xoff_from_center, 0, 0),
                               height=(0, 0, height),
                               radius=(output_port_diameter / 2.0))

    def single_radial_protoplast_catcher(self,
                                         input_port_radius,
                                         length_catcher,
                                         width_catcher,
                                         catcher_post_w,
                                         catcher_post_h,
                                         catcher_post_roundness,
                                         catcher_post_pitch,
                                         len_funnel,
                                         catcher_height):
        y_neg = width_catcher / -2;
        xoff = (input_port_radius + len_funnel)

        p1 = (xoff,
              y_neg,
              0)
        p2 = (xoff + length_catcher,
              y_neg + width_catcher,
              catcher_height)
        first = brl_db.cuboid(p1, p2)
        to_group = []

        for i in range(int((width_catcher / catcher_post_pitch))):
            xt = length_catcher * 3 / 4
            yt = (i * catcher_post_pitch)
            def make_post():
              base = (xoff + xt + (catcher_post_h/2),
                      y_neg + yt + (catcher_post_w/2),
                      0)
              height = (0,
                        0,
                        catcher_height)
              ellipse_base_radius_part_A = (catcher_post_h/2, 0, 0)
              ellipse_base_radius_part_B = (0, catcher_post_w/2, 0)
              top_radius_scaling_A = ellipse_base_radius_part_A[0]
              top_radius_scaling_B = ellipse_base_radius_part_B[1]
              post = brl_db.tgc(base,
                                height,
                                ellipse_base_radius_part_A,
                                ellipse_base_radius_part_B,
                                top_radius_scaling_A,
                                top_radius_scaling_B)
              to_group.append(post)
            make_post()
            xt += catcher_post_pitch + (catcher_post_h/2)
            yt += (catcher_post_pitch/2)
            make_post()

        g = brl_db.group(to_group, 'catcher_cubes.g',)
        return brl_db.combination(
                           'u {} - {}'
                           .format(first, g), name='catcher_cubes_minus.c')
    
    def bifurcated_posts(self,
                         num_posts_across_min,
                         half_offset,
                         symmetric_bifurcation_post_w,
                         symmetric_bifurcation_post_h,
                         symmetric_bifurcation_post_roundness,
                         symmetric_bifurcation_post_pitch,
                         num_rows,
                         post_height):
        even_odd = 0
        to_group = []
        for r in range(int(num_rows)):
            row_num_posts = (num_posts_across_min + r * 2)
            even_odd_row_offset = 0
            if (even_odd == 1):
                even_odd = 0
                even_odd_row_offset = (symmetric_bifurcation_post_pitch / 2)

            else:
                even_odd = 1
                row_num_posts = row_num_posts + 1

            for i in range(int(row_num_posts)):
                xt = r * symmetric_bifurcation_post_pitch
                yt = (half_offset +
                      (i * symmetric_bifurcation_post_pitch) -
                      (r * symmetric_bifurcation_post_pitch) -
                      (symmetric_bifurcation_post_w / 2) +
                      (even_odd_row_offset)
                      )

                base = (xt + (symmetric_bifurcation_post_h/2),
                        yt + (symmetric_bifurcation_post_w/2),
                        0)
                height = (0,
                          0,
                          post_height)
                ellipse_base_radius_part_A = (symmetric_bifurcation_post_h/2, 0, 0)
                ellipse_base_radius_part_B = (0, symmetric_bifurcation_post_w/2, 0)
                top_radius_scaling_A = ellipse_base_radius_part_A[0]
                top_radius_scaling_B = ellipse_base_radius_part_B[1]
                post = brl_db.tgc(base,
                                  height,
                                  ellipse_base_radius_part_A,
                                  ellipse_base_radius_part_B,
                                  top_radius_scaling_A,
                                  top_radius_scaling_B)
                to_group.append(post)
        return brl_db.group(to_group, 'bifurcated_posts.g')

    def single_symmetrical_bifurcation_funnel(self,
                                              input_port_radius_from_center,
                                              input_symmetric_bifurcation_inner_width,
                                              input_symmetric_bifurcation_outer_width,
                                              symmetric_bifurcation_post_w,
                                              symmetric_bifurcation_post_h,
                                              symmetric_bifurcation_post_roundness,
                                              symmetric_bifurcation_post_pitch,
                                              num_posts_across_min,
                                              num_rows,
                                              len_funnel,
                                              funnel_height):
        y_neg = input_symmetric_bifurcation_outer_width / -2;
        half_offset = ((input_symmetric_bifurcation_outer_width - input_symmetric_bifurcation_inner_width) / 2);

        first_sect = brl_db.cuboid((-input_port_radius_from_center,
                                    half_offset,
                                    0),
                                   (0,
                                    half_offset + input_symmetric_bifurcation_inner_width,
                                    funnel_height))

        pg = brl_db.arb8([[0, half_offset, 0],
                          [0, half_offset + input_symmetric_bifurcation_inner_width, 0],
                          [len_funnel, input_symmetric_bifurcation_outer_width, 0],
                          [len_funnel, 0, 0],
                          [0, half_offset, funnel_height],
                          [0, half_offset + input_symmetric_bifurcation_inner_width, funnel_height],
                          [len_funnel, input_symmetric_bifurcation_outer_width, funnel_height],
                          [len_funnel, 0, funnel_height]
                          ])
        
        lengthened_polygon = brl_db.combination('u {} u {}'
                                                .format(first_sect, pg), name='lengthened_polygon.c')
        bfp = self.bifurcated_posts(num_posts_across_min,
                                    half_offset,
                                    symmetric_bifurcation_post_w,
                                    symmetric_bifurcation_post_h,
                                    symmetric_bifurcation_post_roundness,
                                    symmetric_bifurcation_post_pitch,
                                    num_rows, funnel_height)
        
        x = brl_db.combination('u {} - {}'
                               .format(lengthened_polygon, bfp), name='funnel.c')
        brl_db.begin_combination_edit(x, '{}/{}'.format(lengthened_polygon, pg))
        brl_db.translate_relative(input_port_radius_from_center, y_neg, 0)
        brl_db.end_combination_edit()
        return x, pg

    def single_radial_symmetrical_bifurcation_funnel(self,
                                                     radius_from_center,
                                                     input_symmetric_bifurcation_inner_width,
                                                     input_symmetric_bifurcation_outer_width,
                                                     symmetric_bifurcation_post_w,
                                                     symmetric_bifurcation_post_h,
                                                     symmetric_bifurcation_post_roundness,
                                                     symmetric_bifurcation_post_pitch,
                                                     num_posts_across_min,
                                                     num_rows,
                                                     len_funnel,
                                                     column_height):
        tangent_chord_offset = (radius_from_center -
                                (radius_from_center *
                                 cos(asin(input_symmetric_bifurcation_inner_width / radius_from_center))
                                )
                               ) / 4

        x, pg = self.single_symmetrical_bifurcation_funnel(radius_from_center,
                                                           input_symmetric_bifurcation_inner_width,
                                                           input_symmetric_bifurcation_outer_width,
                                                           symmetric_bifurcation_post_w,
                                                           symmetric_bifurcation_post_h,
                                                           symmetric_bifurcation_post_roundness,
                                                           symmetric_bifurcation_post_pitch,
                                                           num_posts_across_min,
                                                           num_rows,
                                                           len_funnel,
                                                           column_height)
        return x

    def _center_input(self, input_port_diameter, height):
        return self.brl_db.rcc(name=None,
                               base=(0, 0, 0),
                               height=(0, 0, height),
                               radius=(input_port_diameter / 2.0))

    def protoplast_bottom_layer_2d(self,
                                   input_port_diameter,
                                   input_symmetric_bifurcation_inner_width,
                                   input_symmetric_bifurcation_outer_width,
                                   symmetric_bifurcation_post_w,
                                   symmetric_bifurcation_post_h,
                                   symmetric_bifurcation_post_roundness,
                                   symmetric_bifurcation_post_pitch,
                                   length_catcher,
                                   width_catcher,
                                   catcher_post_w,
                                   catcher_post_h,
                                   catcher_post_roundness,
                                   catcher_post_pitch,
                                   distance_output_port_from_center,
                                   dist_center_catcher_to_center_device,
                                   io_height,
                                   protoplast_chamber_height,
                                   output_port_diameter,
                                   num_output_ports):
        num_posts_across_min = input_symmetric_bifurcation_inner_width / symmetric_bifurcation_post_pitch
        num_posts_across_max = input_symmetric_bifurcation_outer_width / symmetric_bifurcation_post_pitch

        num_rows = (num_posts_across_max - num_posts_across_min) / 2
        len_funnel = num_rows * symmetric_bifurcation_post_pitch

        column_height = protoplast_chamber_height
        symmetric_bifurcation_start_radius = input_port_diameter / 2

        all_items = []
        combinations = []
        for current_output_num in range(1, num_output_ports+1):
            angle_rad = (2. * pi) / num_output_ports * current_output_num
            angle_deg = ((2.) / num_output_ports * current_output_num) * (180)
            tangent_chord_offset = (symmetric_bifurcation_start_radius - (symmetric_bifurcation_start_radius * cos(
                asin(input_symmetric_bifurcation_inner_width / symmetric_bifurcation_start_radius)))) / 4;
            to_union = []

            fun = self.single_radial_symmetrical_bifurcation_funnel(symmetric_bifurcation_start_radius,
                                                                    input_symmetric_bifurcation_inner_width,
                                                                    input_symmetric_bifurcation_outer_width,
                                                                    symmetric_bifurcation_post_w,
                                                                    symmetric_bifurcation_post_h,
                                                                    symmetric_bifurcation_post_roundness,
                                                                    symmetric_bifurcation_post_pitch,
                                                                    num_posts_across_min,
                                                                    num_rows,
                                                                    len_funnel,
                                                                    column_height)
            to_union.append(fun)
            rpc = self.single_radial_protoplast_catcher(symmetric_bifurcation_start_radius,
                                                        length_catcher,
                                                        width_catcher,
                                                        catcher_post_w,
                                                        catcher_post_h,
                                                        catcher_post_roundness,
                                                        catcher_post_pitch,
                                                        len_funnel,
                                                        column_height)
            to_union.append(rpc)
            r_o = self.radial_outlet(input_port_diameter,
                                     len_funnel,
                                     length_catcher,
                                     output_port_diameter,
                                     io_height
                                    )
            self.outlets.append(r_o)
            to_union.append(r_o)
            print(to_union)
            tu = union(to_union)
            combination_name = brl_db.combination(union(tu, self.center_input))
                                                 #.format(join_as_str(' u ', to_union), self.center_input))
            brl_db.begin_combination_edit(combination_name, self.center_input)
            brl_db.rotate_combination(0, 0, angle_deg)
            brl_db.translate_relative((-tangent_chord_offset) * cos(angle_rad),
                                      (-tangent_chord_offset) * sin(angle_rad), 0)
            brl_db.remove_object_from_combination(combination_name, self.center_input)
            brl_db.end_combination_edit()

            all_items += to_union
            combinations.append(combination_name)
        
        all_arms = brl_db.combination(union(combinations))
        return all_arms


if __name__ == "__main__":
    g_path_out = check_cmdline_args(__file__)
    with brlcad_tcl(g_path_out, "My Database", make_g=True, verbose=False, stl_quality=0.01) as brl_db:
        device = tobacco_mesophyll_protoplast_fusion_device(input_port_diameter=1200,
                                                            input_symmetric_bifurcation_inner_width=200,
                                                            input_symmetric_bifurcation_outer_width=900,
                                                            symmetric_bifurcation_post_w=20,
                                                            symmetric_bifurcation_post_h=30,
                                                            symmetric_bifurcation_post_roundness=15,
                                                            symmetric_bifurcation_post_pitch=40,
                                                            length_catcher=3200,
                                                            width_catcher=900,
                                                            catcher_post_w=20,
                                                            catcher_post_h=30,
                                                            catcher_post_roundness=20,
                                                            catcher_post_pitch=20 + (20 / 2),
                                                            distance_output_port_from_center=3200 + 200 + 800,
                                                            dist_center_catcher_to_center_device=(3200 / 2) + 800,
                                                            io_height=500,
                                                            protoplast_chamber_height=55,
                                                            output_port_diameter=1200,
                                                            num_output_ports=5,
                                                            brl_db=brl_db
                                                            )
    print('*' * 80)
    print('device.negative     {}'.format(device.negative))
    print('*' * 80)
    print('device.final_name   {}'.format(device.final_name))
    print('*' * 80)
    c1, c2 = brl_db.get_opposing_corners_bounding_box(brl_db.get_bounding_box_coords(device.negative))
    print('bounding box of device.negative (negative, what the photoresist would be in'\
          ' hardened form for soft-lithography):\n{}\n{}\n'.format(c1, c2))
    
    width_in_microns = abs(c1[1] - c2[1])
    height_in_microns = abs(c1[0] - c2[0])
    print('model width  {}'.format(width_in_microns))
    print('model height {}'.format(height_in_microns))
    # saved_file_path = brl_db.export_image_from_Z(device.negative, width_in_microns*2, height_in_microns*2)
    #saved_file_path = brl_db.export_image_from_Z(device.negative, width_in_microns/8, height_in_microns/8)
    #print('saved output to: {}'.format(saved_file_path))
    print('*' * 80)
    brl_db.save_stl(device.negative)
