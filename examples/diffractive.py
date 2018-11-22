from math import pi, cos, sin, asin
from python_brlcad_tcl.brlcad_tcl import *
import math


class diffractive(BrlCadModel):
    def __init__(self,
                 design_wavelength, focal_len, lens_diameter,
                 fin_w, fin_l, fin_h, img_w, img_h,
                 brl_db):
        super(diffractive, self).__init__(brl_db)
        # h = img_h
        # w = img_w
        half_height = fin_h/2.

        focal = focal_len #/scaling
        diameter = lens_diameter
        half_lens_width = half_lens_height = lens_diameter/2.
        h=w=diameter
        diameter_to_image_scaling = float(diameter)/max(h,w)

        _l = fin_l#/diameter_to_image_scaling)#/scaling)
        _w = fin_w#/diameter_to_image_scaling)#/scaling)
        
        leftlen = _x1 = _l/-2.
        lowerw = _y1 = _w/-2.
        half_fin_l = rightlen = _x3 = _l/2.
        half_fin_w = upperw = _y3 = _w/2.
        _x2 = _x3
        _y2 = _y1
        _x4 = _x1
        _y4 = _y3

        spacing = 430 #int(round(430))#/diameter_to_image_scaling))
        #img = np.zeros((h, w, 3), np.uint8)

        to_group = []
        # step along Y
        #for i in xrange(0, int(round(h*scaling)), spacing):
        for iy in range(0, h+spacing, spacing):
            # now step along X
        #    for j in xrange(0, int(round(w*scaling)), spacing):
            for jx in range(0, w+spacing, spacing):
                #xx = (j-w/2)
                #yy = (i-h/2)
                xx = (jx-half_lens_width) #* diameter_to_image_scaling
                yy = (iy-half_lens_height) #* diameter_to_image_scaling
                #print (xx, yy)
                angle = (math.pi/design_wavelength) * (focal - math.sqrt(xx**2 + yy**2 + focal**2))
                #angle = (math.pi/design_wavelength) * (focal - math.sqrt((j)**2 + (i)**2 + focal**2))

                #angle_radians = angle #* math.pi / 180.0

                # rx1 = math.cos(angle_radians) * _x1 - math.sin(angle_radians) * _y1
                # ry1 = math.sin(angle_radians) * _x1 + math.cos(angle_radians) * _y1

                # rx2 = math.cos(angle_radians) * _x2 - math.sin(angle_radians) * _y2
                # ry2 = math.sin(angle_radians) * _x2 + math.cos(angle_radians) * _y2

                # rx3 = math.cos(angle_radians) * _x3 - math.sin(angle_radians) * _y3
                # ry3 = math.sin(angle_radians) * _x3 + math.cos(angle_radians) * _y3

                # rx4 = math.cos(angle_radians) * _x4 - math.sin(angle_radians) * _y4
                # ry4 = math.sin(angle_radians) * _x4 + math.cos(angle_radians) * _y4

                # cv2.line(img, (int(rx1 + (j/scaling) + _x3) , int(ry1 + (i/scaling) + _y3)), (int(rx2 + (j/scaling) + _x3), int(ry2 + (i/scaling) + _y3)), 255, 1)
                # cv2.line(img, (int(rx2 + (j/scaling) + _x3) , int(ry2 + (i/scaling) + _y3)), (int(rx3 + (j/scaling) + _x3), int(ry3 + (i/scaling) + _y3)), 255, 1)
                # cv2.line(img, (int(rx3 + (j/scaling) + _x3) , int(ry3 + (i/scaling) + _y3)), (int(rx4 + (j/scaling) + _x3), int(ry4 + (i/scaling) + _y3)), 255, 1)
                # cv2.line(img, (int(rx4 + (j/scaling) + _x3) , int(ry4 + (i/scaling) + _y3)), (int(rx1 + (j/scaling) + _x3), int(ry1 + (i/scaling) + _y3)), 255, 1)
                

                # p1 = (int(rx1 + j + _x3) , int(ry1 + i + _y3), fin_h)
                # p2 = (int(rx3 + j + _x3), int(ry3 + i + _y3), fin_h)



                p1 = (jx - half_fin_l, iy - half_fin_w, 0)
                p2 = (jx + half_fin_l, iy + half_fin_w, fin_h)
                
                # minp = (min(p1[0], p2[0]), min(p1[1], p2[1]), 0)
                # maxp = (max(p1[0], p2[0]), max(p1[1], p2[1]), fin_h)
                
                to_group.append(brl_db.cuboid(p1, p2))
                #brl_db.rotate_primitive(to_group[-1], 0, 0, 1, angle)
                brl_db.begin_primitive_edit(name=to_group[-1])
                brl_db.keypoint(jx, iy, half_height)
                brl_db.script_string_list.append('arot {} {} {} {}\n'.format(0, 0, 1, angle))#math.degrees(angle)))
                brl_db.end_combination_edit()
                #brl_db.script_string_list.append('keypoint reset\n')

                # coords = [(int(rx1 + j + _x3), int(ry1 + i + _y3), 0),
                #           (int(rx2 + j + _x3), int(ry2 + i + _y3), 0),
                #           (int(rx3 + j + _x3), int(ry3 + i + _y3), 0),
                #           (int(rx4 + j + _x3), int(ry4 + i + _y3), 0),
                #           (int(rx1 + j + _x3), int(ry1 + i + _y3), fin_h),
                #           (int(rx2 + j + _x3), int(ry2 + i + _y3), fin_h),
                #           (int(rx3 + j + _x3), int(ry3 + i + _y3), fin_h),
                #           (int(rx4 + j + _x3), int(ry4 + i + _y3), fin_h)]

                #pp1, pp2 = brl_db.get_opposing_corners_bounding_box(coords)
                

                # cv2.line(img, (int(rx1 + j + _x3) , int(ry1 + i + _y3)), (int(rx2 + j + _x3), int(ry2 + i + _y3)), 255, 1)
                # cv2.line(img, (int(rx2 + j + _x3) , int(ry2 + i + _y3)), (int(rx3 + j + _x3), int(ry3 + i + _y3)), 255, 1)
                # cv2.line(img, (int(rx3 + j + _x3) , int(ry3 + i + _y3)), (int(rx4 + j + _x3), int(ry4 + i + _y3)), 255, 1)
                # cv2.line(img, (int(rx4 + j + _x3) , int(ry4 + i + _y3)), (int(rx1 + j + _x3), int(ry1 + i + _y3)), 255, 1)

                # cv2.line(img, (int((rx1 + j + _x3)/scaling), int((ry1 + i + _y3)/scaling)), (int((rx2 + j + _x3/scaling)), int((ry2 + i + _y3)/scaling)), 255, 1)
                # cv2.line(img, (int((rx2 + j + _x3)/scaling), int((ry2 + i + _y3)/scaling)), (int((rx3 + j + _x3/scaling)), int((ry3 + i + _y3)/scaling)), 255, 1)
                # cv2.line(img, (int((rx3 + j + _x3)/scaling), int((ry3 + i + _y3)/scaling)), (int((rx4 + j + _x3/scaling)), int((ry4 + i + _y3)/scaling)), 255, 1)
                # cv2.line(img, (int((rx4 + j + _x3)/scaling), int((ry4 + i + _y3)/scaling)), (int((rx1 + j + _x3/scaling)), int((ry1 + i + _y3)/scaling)), 255, 1)
        #cv2.imwrite('diffractive_lens.png', img)

        # at this point, this is pretty much a 'negative' of what we want to create
        self.final_name = brl_db.group(join_as_str(' ', to_group), 'pillars.g')
        

if __name__ == "__main__":
    g_path_out = check_cmdline_args(__file__)
    with brlcad_tcl(g_path_out, "My Database", make_g=True, verbose=False, units='mm') as brl_db:
        device = diffractive(design_wavelength = 600, focal_len = 1000,
                             lens_diameter = 1000*20,# 100*1000,
                             fin_w = 85, fin_l = 410, fin_h = 600, 
                             img_h=100, #4096, #1000
                             img_w=100, #4096, #1000
                             brl_db=brl_db
                                                            )
    print('device.final_name   {}'.format(device.final_name))
    print('*' * 80)
    c1, c2 = brl_db.get_opposing_corners_bounding_box(brl_db.get_bounding_box_coords(device.final_name))
    print('bounding box of device.final_name:\n{}\n{}\n'.format(c1, c2))
    
    width_in_nm = abs(c1[1] - c2[1])
    height_in_nm = abs(c1[0] - c2[0])
    print('model width  {}'.format(width_in_nm))
    print('model height {}'.format(height_in_nm))
    #slice_coords, slices = brl_db.create_slice_regions(10,max([c1[1], c2[1]])+1, max([c1[0], c2[0]])+1 )
    slice_coords, slices = brl_db.create_slice_regions(10,height_in_nm, width_in_nm )
    #saved_file_path = brl_db.export_image_from_Z(slices[0], width_in_nm, height_in_nm)
    #saved_file_path = brl_db.export_image_from_Z(slices[-1], width_in_nm/5., height_in_nm/5.)
    saved_file_path = brl_db.export_image_from_Z(slices[-1], 1024, 1024)
    #saved_file_path = brl_db.export_image_from_Z(device.final_name, width_in_nm/10, height_in_nm/10)
    # saved_file_path = brl_db.get_object_raster_from_z_projection(device.final_name,
    #                                                       (min(c1[0], c2[0]), min(c1[1], c2[1]), min(c1[2], c2[2])),
    #                                                       (max(c1[0], c2[0]), max(c1[1], c2[1]), max(c1[2], c2[2])),
    #                                                       600,
    #                                                       ray_destination_dir_xyz=[0, 0, -1],
    #                                                       bmp_output_name=brl_db.project_filename_prefix + '_Z.png',
    #                                                       num_pix_x=4096,
    #                                                       num_pix_y=4096,
    #                                                       output_greyscale=True,
    #                                                       threading_event=None)
    print('saved output to: {}'.format(saved_file_path))
    print('*' * 80)
    brl_db.save_stl(device.final_name)
