# standard libs
import os
import re
import sys
import math
import inspect
import numbers
import datetime
import subprocess
from itertools import chain
from abc import ABCMeta
from abc import abstractmethod
from collections import OrderedDict, deque

# external libs
import numpy
from PIL import Image

# internal
from . import vmath
from .brlcad_name_tracker import BrlcadNameTracker


def check_cmdline_args(file_path):
    if not len(sys.argv)==2:
        print('usage:\n'\
              '      {} file_name_for_output'.format(file_path))
        sys.exit(1)
    return sys.argv[1]


def coord_avg(c1, c2):
    return (c1+c2)/2.


def get_box_face_center_coord(corner1, corner2, xyz_desired):
    # each 'bit' can be -1, 0, or 1
    x_bit, y_bit, z_bit =  [int(b) for b in xyz_desired]
    # only one non-zero value can be provided
    assert([x_bit!=0, y_bit!=0, z_bit!=0].count(True) == 1)
    out_xyz = [0,0,0]
    away_vect = [0,0,0]
    for i, bit in enumerate([x_bit, y_bit, z_bit]):
        if bit<0:
            out_xyz[i] = min(corner1[i], corner2[i])
            away_vect[i] = -1
        elif bit>0:
            out_xyz[i] = max(corner1[i], corner2[i])
            away_vect[i] = 1
        else:
            out_xyz[i] = min(corner1[i], corner2[i]) + (abs(corner1[i] - corner2[i]) / 2.)
    return out_xyz, away_vect


def is_truple(arg):
    is_numeric_truple = (isinstance(arg, tuple) or isinstance(arg, list)) and all([isinstance(x, numbers.Number) for x in arg])
    assert(is_numeric_truple), arg


def is_number(arg):
    assert(isinstance(arg, numbers.Number))


def two_plus_strings(*args):
    assert(len(args)>2)
    assert(all([isinstance(x, str) for x in args]))


def is_string(name):
    assert(isinstance(name, str))


def union(*args):
    return ' u {}'.format(' u '.join(args))


def subtract(*args):
    return ' u {}'.format(' - '.join(args))


def intersect(*args):
    return ' u {}'.format(' + '.join(args))


class brlcad_tcl():
    def __init__(self, tcl_filepath, title, make_g=False, make_stl=False, stl_quality=None, units='mm', verbose=False):
        #if not os.path.isfile(self.output_filepath):
        #    abs_path = os.path.abspath(self.output_filepath)
        #    if not
        self.make_stl = make_stl
        self.make_g = make_g
        self.g_path = None
        self.tcl_filepath = tcl_filepath
        self.stl_quality = stl_quality
        self._input_file_path_no_ext = self._remove_file_extension(self.tcl_filepath)

        self.script_string = 'title {}\nunits {}\n'.format(title, units)
        self.units = units
        self.name_tracker = BrlcadNameTracker()
        self.verbose = verbose

    def _remove_file_extension(self, file_path):
        return os.path.splitext(file_path)[0]
    

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save_tcl()

        if self.make_g or self.make_stl:
            self.save_g()
        if self.make_stl:
            self.save_stl()
            
    def add_script_string(self, to_add):
        # In case the user does some adding on their own
        self.script_string += '\n' + str(to_add) + '\n'

    def save_tcl(self):
        with open(self.tcl_filepath, 'w') as f:
            f.write(self.script_string)

    def save_g(self):
        self.g_path = self._input_file_path_no_ext + '.g'
        # try to remove a database file of the same name if it exists
        try:
            os.remove(self.g_path)
        except Exception as e:
            if not e.errno == 2:
                print('WARNING: could not remove: {}\nuse different file name, or delete the file manually first!'.format(self.g_path))
                raise (e)
        
        cmd = 'mged {} < {}'.format(self.g_path, self.tcl_filepath)
        if self.verbose:
            proc = subprocess.Popen(cmd, shell=True)
        else:
            proc = subprocess.Popen(cmd, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        
    def run_and_save_stl(self, objects_to_render):
        # Do all of them in one go
        self.save_tcl()
        self.save_g()
        self.save_stl(objects_to_render)

    def save_stl(self, objects_to_render, output_path=None):
        if output_path is None:
            stl_path = self._input_file_path_no_ext + '.stl'
        else:
            stl_path = output_path if output_path.endswith('.stl') else '{}.stl'.format(output_path)
        obj_str = ' '.join(objects_to_render)
        cmd = 'g-stl -o {}'.format(stl_path)

        # Add the quality
        """   from http://sourceforge.net/p/brlcad/support-requests/14/#0ced
        The "-a" option specifies an absolute tessellation tolerance
        - the maximum allowed distance (mm) between the real surface
        and the facets
        The "-r" option specifies a relative tessellation tolerance
        - an absolute tolerance is calculated as the relative
        tolerance times the "size" of the object being tessellated
        (for a sphere, the "size" is the radius).
        The "-n" option specifies the maximum surface normal error
        (in radians).
        By default, tessellations are performed using a relative
        tolerance of 0.01. Try using the -r option with values other
        than 0.01.
        """
        """  from http://permalink.gmane.org/gmane.comp.cad.brlcad.devel/4600
        For example, setting g-stl -n 1.0 should create a polygon for every 1-degree difference in curvature. 
        Since your model has a lot of circular edges, this should me a considerable visual improvement.  Setting
        the absolute tolerance to some sub-zero value should have a similar effect, but be careful to not specify a
        number too small or you may inadvertently create many GB of polygons (or worse).
        """

        if self.stl_quality and self.stl_quality > 0:
            cmd = '{} -a {}'.format(cmd, self.stl_quality)

        # Add the paths
        cmd = '{} {} {}'.format(cmd, self.g_path, obj_str)

        print('running: {}'.format(cmd))
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.communicate()

    def export_image_from_Z(self, item_name, width, height, output_path=None, azimuth=None, elevation=None):
        if output_path is None:
            output_path = '{}.png'.format(self._input_file_path_no_ext)
        if azimuth is None:
            azimuth = -90
        if elevation is None:
            elevation = -90
        # on Linux, use 'man rt' on the command-line to get all the info... 
        # (it is still not terribly straight-forward)
        cmd = 'rt -a {} -e {} -w {} -n {} -o {} {} {}'\
              .format(azimuth, elevation, width, height, output_path, self.g_path, item_name)
        print('\nrunning: {}'.format(cmd))
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.communicate()
        return output_path

    def create_slice_regions(self, slice_thickness, max_slice_x, max_slice_y, output_format=''):
        tl_names = self.get_top_level_object_names()
        xyz1, xyz2 = self.get_opposing_corners_bounding_box(self.get_bounding_box_coords_for_entire_db(tl_names))
        #print 'bb of all items {} to {}'.format(xyz1, xyz2)

        if abs(xyz1[0] - xyz2[0]) > max_slice_x:
            raise Exception('x dimension exceeds buildable bounds')
        if abs(xyz1[1] - xyz2[1]) > max_slice_y:
            raise Exception('y dimension exceeds buildable bounds')

        slice_coords = list(self.get_object_slice_coords(slice_thickness, xyz1, xyz2))
        self.slice_coords = []
        temps_to_kill = []

        for i, object_slice_bb_coords in enumerate(slice_coords):
            # = self.name_tracker.get_next_name(self, 'slice_bb{}_num.s'.format(i))
            slice_bb_temp = self.cuboid(object_slice_bb_coords[0], object_slice_bb_coords[1])
            temps_to_kill.append(slice_bb_temp)
            # finally create a region (a special combination that means it's going to be rendered)
            # by unioning together the main combinations we just created
            tl_name_plussed = ' + '.join(tl_names)
            # slice_reg_name = self.name_tracker.get_next_name(self, 'slice{}_num.c'.format(i))
            
            slice_reg_name = self.region('slice{}_num.r'.format(i),
                                              'u {} + {}'.format(slice_bb_temp, tl_name_plussed)
                                              )
            temps_to_kill.append(slice_reg_name)
            self.slice_coords.append((slice_reg_name, object_slice_bb_coords))
        self.save_tcl()
        self.save_g()
        # [self.kill(temp_bb) for temp_bb in temps_to_kill]
        # self.save_tcl()
        # self.save_g()
        return self.slice_coords, temps_to_kill

    def get_object_raster_from_z_projection(self,
                                            slice_region_name,
                                            model_min,
                                            model_max,
                                            slice_thickness,
                                            ray_destination_dir_xyz=[0, 0, -1],
                                            bmp_output_name=None,
                                            num_pix_x=1024,
                                            num_pix_y=1024,
                                            output_greyscale=True,
                                            threading_event=None):
        num_pix_x = math.ceil(num_pix_x)
        num_pix_y = math.ceil(num_pix_y)
        # each 'bit' can be -1, 0, or 1
        x_bit, y_bit, z_bit = [int(b) for b in ray_destination_dir_xyz]
        # only one non-zero value can be provided
        assert([x_bit!=0, y_bit!=0, z_bit!=0].count(True) == 1)

        model_width = model_max[0] - model_min[0]
        model_length = model_max[1] - model_min[1]
        x_offset = (0-model_min[0])
        y_offset = (0-model_min[1])

        x_scale = num_pix_x/model_width
        y_scale = num_pix_y/model_length

        x_step = model_width/num_pix_x
        y_step = model_length/num_pix_y

        step_size = max(x_step, y_step)
        # the -s command might speed things up???
        args = ['nirt', '-s', self.g_path, slice_region_name]
        print('\nrunning: {}'.format(' '.join(args)))
        p = subprocess.Popen(args,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        if threading_event:
            threading_event.set()
        # create a list for the NIRT command lines to be queued
        lins=[]
        # set the direction to fire rays in
        lins.append('dir {} {} {}'.format(x_bit, y_bit, z_bit))
        lins.append('units {}'.format(self.units))
        x = model_min[0]
        z = model_max[2]

        xstepcount = 0
        # the raster loops, loop over each Y for each X location
        while x < model_max[0]:
            # start Y at the minimum for each Y loop
            y = model_min[1]
            ystepcount = 0
            # loop while Y is less than the model's max Y
            while y < model_max[1]:
                # move around the model in X and Y axes, using the determined step-size
                lins.append('xyz {} {} {}'.format(x, y, z))
                # fire a ray
                lins.append('s')
                # step in Y
                y += step_size
                ystepcount += 1
            # make sure we aren't going out-of-bounds
            assert ystepcount <= num_pix_y, (ystepcount, num_pix_y)
            # step in X
            x += step_size
            xstepcount += 1
        # make sure we aren't going out-of-bounds
        assert xstepcount <= num_pix_x, (xstepcount, num_pix_x)

        # pass the commands to NIRT, get NIRT's response
        outp = p.communicate('\n'.join(lins))

        chunks = []
        # break up NIRT's response by newline
        out_lines = outp[0].split('\n')
        err_lines = outp[1].split('\n')
        
        im = numpy.zeros((num_pix_x, num_pix_y))
        # r = re.compile(r'\((\s*-?\d+\.?\d+)\s+(-?\d+\.?\d+)\s+(-?\d+\.?\d+)\)')
        r = re.compile(r'\((\s*-?\d+\.?\d+)\s+(-?\d+\.?\d+)\s+(-?\d+\.?\d+)\)\s+(-?\d+\.?\d+)')
        hit_description_header = '    Region Name               Entry (x y z)              LOS  Obliq_in Attrib'
        missed_target = 'You missed the target'
        state = 0

        decade = len(out_lines)/10
        for il, l in enumerate(out_lines):
            # if il%decade==0:
            #     print '{}% completed parsing NIRT output'.format(float(il)/len(out_lines)*100)

            # check if we are starting a new section IF:
            # we are just starting, or we got at least one coordinate
            if (state == 0 or state == 3) and l.startswith('Origin'):
                    # and out_lines[out_lines.index(l)+1].startswith('Direction'):
                state = 1
                chunks.append({'Origin': l, 'Coords': []})
            elif state == 1:
                state = 2
                chunks[-1]['Direction'] = l
            elif state == 2:
                if l.startswith(hit_description_header) or (not l):
                    continue
                # we got a hit or miss
                state = 3
                if missed_target in l:
                    continue
                # store the line for later
                chunks[-1]['Coords'].append(l)
                m = r.search(l)
                if not m:
                    print('first 10 lines out:\n{}'.format(out_lines[:10]))
                    print('first err:\n{}'.format(err_lines[:1]))
                    raise Exception("regex didn't work to find coordinates! report this bug. on input line {}".format(l))
                x, y, z, depth_of_hit = m.groups()

                zeroed_x = (float(x) - model_min[0])
                zeroed_y = (float(y) - model_min[1])
                if zeroed_x:
                    floated_x = zeroed_x/step_size
                    int_x = int(round(floated_x))
                    # enable this if you are paranoid about the math
                    # numpy.testing.assert_approx_equal(floated_x, int_x, 4, 'these were not equal:\n{}\n{}'.format(floated_x, int_x))
                else:
                    int_x = 0
                if zeroed_y:
                    floated_y = zeroed_y/step_size
                    int_y = int(round(floated_y))
                    # enable this if you are paranoid about the math
                    # numpy.testing.assert_approx_equal(floated_y, int_y, 4, 'these were not equal:\n{}\n{}'.format(floated_y, int_y))
                else:
                    int_y = 0

                if output_greyscale:
                    im[int_x, int_y] = (float(depth_of_hit)/slice_thickness)*255
                else:
                    im[int_x, int_y] = 1

            elif state==3:
                # we already got a hit for this spot, so we don't need to check again
                continue

        if output_greyscale:
            result = Image.fromarray(im.astype(numpy.uint8))
        else:
            result = Image.fromarray((im * 255).astype(numpy.uint8))
        result.save(bmp_output_name)

    def export_model_slices(self,
                            num_slices_desired,
                            max_slice_x, max_slice_y,
                            output_format='stl', output_option_kwargs={}, output_path_format=None):
        """

        :param num_slices_desired:    the number of equal-sized slices you want to end up with
        :param max_slice_x:           the maximum X dimension you want to export (in model units)
        :param max_slice_y:           the maximum Y dimension you want to export (in model units)
        :param output_format:         either 'raster' or 'stl' currently
        :param output_option_kwargs:  i.e. 'raster' format supports 'greyscale_output':True/False
        :param output_path_format:    a string with two {} that the g-database path and slice-num are inserted into
        :return:                      nothing
        """
        orig_path = self._input_file_path_no_ext
        orig_tcl = self.script_string
        self.save_tcl()
        self.save_g()
        # calculate the slice thickness needed to get the number of slices requested
        tl_names = self.get_top_level_object_names()
        print('top level names about to be exported: {}'.format(tl_names))
        xyz1, xyz2 = self.get_opposing_corners_bounding_box(self.get_bounding_box_coords_for_entire_db(tl_names))
        print('top level items bounding-box: {} to {}'.format(xyz1, xyz2))

        slice_thickness = abs(xyz2[2] - xyz1[2]) / float(num_slices_desired)

        # now create the slice regions
        slice_coords, temps_to_kill = self.create_slice_regions(slice_thickness, max_slice_x, max_slice_y)

        import threading
        threads = []
        for i, (slice_obj_name, sc) in enumerate(slice_coords):
            if output_format == 'raster':
                if not output_path_format:
                    output_path_format='{}{}.jpg'
                e = threading.Event()
                output_filename = output_path_format.format(self._input_file_path_no_ext, i)
                default_raster_kwargs = {'bmp_output_name': output_filename,
                                         'threading_event': e}
                default_raster_kwargs.update(output_option_kwargs)
                t = threading.Thread(target=self.get_object_raster_from_z_projection,
                                     args=(slice_obj_name,
                                           sc[0],
                                           sc[1],
                                           slice_thickness),
                                     kwargs=default_raster_kwargs)
                t.daemon = True
                t.start()
                # try waiting for NIRT to finish, before starting the next thread
                e.wait()
                # TODO: improve speed of NIRT jobs if possible
                # calling multiple NIRT processes at once doesn't seem to work
                # just wait for each thread to finish
                t.join()
                threads.append(t)
                # allow a max of 4 NIRT process threads
                while len(threads) >= 4:
                    threads.pop(0).join()
            elif output_format == 'stl':
                if not output_path_format:
                    output_path_format = '{}{}'

                self._input_file_path_no_ext = output_path_format.format(orig_path, i)

                if i == 0:
                    self.run_and_save_stl([slice_obj_name])
                else:
                    self.save_stl([slice_obj_name])

        # post-loop output-format specific stuff
        if output_format == 'raster':
            while threads:
                threads.pop(0).join()
            self.script_string = ''
            # get rid of the slices, so they don't show up as top-level objects if user exports slices again
            # destroy the objects in the reverse order of how they were created
            # [self.kill(temp_bb) for temp_bb in reversed(temps_to_kill)]
            # self.save_tcl()
            # self.save_g()
            self.script_string = orig_tcl
            self.save_tcl()
        elif output_format == 'stl':
            self._input_file_path_no_ext = orig_path

    @staticmethod
    def get_object_slice_coords(slice_thickness, xyz1, xyz2):
        lz = min(xyz1[2], xyz2[2])
        mz = max(xyz1[2], xyz2[2])
        iz = lz
        while iz < mz:
            c1 = [c for c in xyz1]
            c1[2] = iz
            c2 = [c for c in xyz2]
            iz += slice_thickness
            if iz > mz:
                iz = mz
            c2[2] = iz
            for i in range(3):
                if c1[i] > c2[i]:
                    g = c1[i]
                    c1[i] = c2[i]
                    c2[i] = g
            yield (c1, c2)

    def get_top_level_object_names(self):
        """
        The "tops" command displays a list of all the top-level objects in the current database.
        The top-level objects are all those objects that are not referenced by some other combination.
        The hierarchical structure of BRL-CAD databases usually means that there will be a top-level 
        object that includes all (or at least most) of the objects in the database.
        The -g option shows only geometry objects. The -n option specifies that no "decoration" 
        (e.g., "/" and "/R") be shown at the end of each object name. 
        The -u option will not show hidden objects. See also the hide command.
        """
        proc = subprocess.Popen('mged {} "tops"'.format(self.g_path),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        (stdoutdata, stderrdata) = proc.communicate()
        # print stdoutdata
        # print stderrdata
        flattened = [segment.strip().rstrip('/R') for segment in stderrdata.strip().split()]
        # print 'tops found: {}'.format(flattened)
        return flattened

    def get_bounding_box_coords_for_entire_db(self, name_list):
        part_names = ' '.join(name_list)
        return self.get_bounding_box_coords(part_names)

    def get_bounding_box_coords(self, obj_name):
        """
        The "l" command displays a verbose description about the specified list of objects.
        If a specified object is a path, then any transformation matrices along that path are applied.
        If the final path component is a combination, the command will list the Boolean formula for the 
        combination and will indicate any accumulated transformations (including any in that combination).
        If a shader and/or color has been assigned to the combination, the details will be listed.
        For a region, its ident, air code, material code, and LOS will also be listed.
        For primitive shapes, detailed shape parameters will be displayed with the accumulated transformation 
        applied. If the -r (recursive) option is used, then each object on the command line will be treated 
        as a path. If the path does not end at a primitive shape, then all possible paths from that point 
        down to individual shapes will be considered. The shape at the end of each possible path will be 
        listed with its parameters adjusted by the accumulated transformation.
        """
        proc = subprocess.Popen('mged {} "make_bb temp_box {}; l temp_box"'.format(self.g_path, obj_name),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        
        (stdoutdata, stderrdata) = proc.communicate()
        # print (stdoutdata, stderrdata)
        subprocess.Popen('mged {} "kill temp_box"'.format(self.g_path), shell=True).communicate()

        bb_coords = []
        # print 'stderrdata.split {}'.format(stderrdata.split('\n')[1:])
        for segment in stderrdata.split('\n')[1:]:
            if '(' not in segment:
                continue
            first_paren = segment.index('(')
            second_paren = segment.index(')')
            x, y, z = segment[first_paren+1:second_paren].split(',')
            
            x = float(x)
            y = float(y)
            z = float(z)
            bb_coords.append((x, y, z))
            # print '(x, y, z) {}'.format((x, y, z))
        # print bb_coords
        return bb_coords

    def get_opposing_corners_bounding_box(self, bb_coords):
        _bb_coords = sorted(list(bb_coords))
        # take any of corners
        first = _bb_coords.pop()
        # now find one that opposes it
        for axis in {0: 'x', 1: 'y', 2: 'z'}:
            for coord in list(_bb_coords):
                if coord[axis] == first[axis]:
                    _bb_coords.remove(coord)
        second = _bb_coords[0]
        return (first, second)

    def set_combination_color(self, obj_name, R, G, B):
        is_string(obj_name)
        self.script_string += 'comb_color {} {} {} {}'.format(obj_name, R, G, B)

    def combination(self, name, operation):
        is_string(name)
        name = self._default_name_(name)
        self.script_string += 'comb {} {}\n'.format(name, operation)
        return name

    def group(self, name, operation):
        is_string(name)
        name = self._default_name_(name)
        self.script_string += 'g {} {}\n'.format(name, operation)
        return name

    def region(self, name, operation):
        is_string(name)
        name = self._default_name_(name)
        self.script_string += 'r {} {}\n'.format(name, operation)
        return name

    def begin_combination_edit(self, combination_to_select, path_to_center):
        if not path_to_center.endswith('.s'):
            (frame, filename, line_number,
                function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
            print('WARNING: right-hand-side arg to begin_combination_edit does not have the .s file extension, which indicates a primitive may not have been passed! Watch out for errors!!!')
            print('(in file: {}, line: {}, function-name: {})'.format(filename, line_number, function_name))
        self.script_string += 'Z\n'
        self.script_string += 'draw {}\n'.format(combination_to_select)
        self.script_string += 'oed / {0}/{1}\n'.format(combination_to_select, path_to_center)

    def begin_primitive_edit(self, name):
        #self.script_string += 'Z\n'
        #self.script_string += 'draw {}\n'.format(name)
        self.script_string += 'sed {0}\n'.format(name)

    def end_combination_edit(self):
        self.script_string += 'accept\n'

    def remove_object_from_combination(self, combination, object_to_remove):
        self.script_string += 'rm {} {}\n'.format(combination, object_to_remove)

    def translate(self, x, y, z, relative=False):
        cmd = 'translate'
        if relative:
            cmd = 'tra'
        self.script_string += '{} {} {} {}\n'.format(cmd, x, y, z)

    def translate_relative(self, dx, dy, dz):
        self.translate(dx, dy, dz, relative=True)

    def rotate_combination(self, x, y, z):
        self.script_string += 'orot {} {} {}\n'.format(x, y, z)

    def rotate_primitive(self, name, x, y, z, angle=None):
        is_string(name)
        self.begin_primitive_edit(name)
        self.script_string += 'keypoint {} {} {}\n'.format(x, y, z)
        if angle:
            self.script_string += 'arot {} {} {} {}\n'.format(x, y, z, angle)
        else:
            self.script_string += 'rot {} {} {}\n'.format(x, y, z)
        self.end_combination_edit()

    def rotate_angle(self, name, x, y, z, angle, obj_type='primitive'):
        if obj_type=='primitive':
            self.script_string += 'Z\n'
            self.script_string += 'draw {}\n'.format(name)
            self.script_string += 'sed {}\n'.format(name)
        else:
            raise NotImplementedError('add non primitive editing start command')
        self.script_string += 'arot {} {} {} {}\n'.format(x,y,z, angle)
        self.script_string += 'accept\n'
        # self.script_string += 'Z\n'

    def kill(self, name):
        if isinstance(name, list):
            for _name in name:
                self.script_string += 'kill {}\n'.format(_name)
        else:
            self.script_string += 'kill {}\n'.format(name)

    def _default_name_(self, name):
        caller_func_name = inspect.stack()[1][3]
        if name is None or name is '':
            nname = self.name_tracker.get_next_name(self, '{}.s'.format(caller_func_name))
            #print('_default_name_ generated: {}'.format(nname))
        else:
            nname = self.name_tracker.get_next_name(self, name)
        return nname

    def _check_name_unused_(self, name):
        if name in self.name_tracker.num_parts_in_use_by_part_name:
            (frame, filename, line_number,
                function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
            raise Exception('name: {} already used! (in file: {}, line: {}, function-name: {})'.format(name, filename, line_number, function_name))
    
    def tgc(self, name, base, height,
            ellipse_base_radius_part_A, ellipse_base_radius_part_B,
            top_radius_scaling_A, top_radius_scaling_B):
        name = self._default_name_(name)
        is_string(name)
        is_truple(base)
        is_truple(height)
        is_truple(ellipse_base_radius_part_A)
        is_truple(ellipse_base_radius_part_B)
        is_number(top_radius_scaling_A)
        is_number(top_radius_scaling_B)
        
        basex, basey, basez = base
        hx, hy, hz = height
        ax, ay, az = ellipse_base_radius_part_A
        bx, by, bz = ellipse_base_radius_part_B
        self.script_string += 'in {} tgc {} {} {} '\
                                       ' {} {} {}'\
                                       ' {} {} {}'\
                                       ' {} {} {}'\
                                       ' {} {}\n'.format(name,
                                                         basex, basey, basez,
                                                         hx, hy, hz,
                                                         ax, ay, az,
                                                         bx, by, bz,
                                                         top_radius_scaling_A,
                                                         top_radius_scaling_B)
        return name

    def rcc(self, name, base, height, radius):
        name = self._default_name_(name)
        is_string(name)
        is_truple(base)
        is_truple(height)
        is_number(radius)
        bx, by, bz = base
        hx, hy, hz = height
        self.script_string += 'in {} rcc {} {} {} {} {} {} {}\n'.format(name,
                                                                        bx, by, bz,
                                                                        hx, hy, hz,
                                                                        radius)
        return name

    def rpc(self, name, vertex, height_vector, base_vector, half_width):
        name = self._default_name_(name)
        is_string(name)
        is_truple(vertex)
        is_truple(height_vector)
        is_truple(base_vector)
        is_number(half_width)
        vx, vy, vz = vertex
        hx, hy, hz = height_vector
        bx, by, bz = base_vector
        self.script_string += 'in {} rpc {} {} {} {} {} {} {} {} {} {}\n'.format(name,
                                                                                 vx,vy,vz,
                                                                                 hx,hy,hz,
                                                                                 bx,by,bz,
                                                                                 half_width)
        return name

    def box_by_opposite_corners(self, name, pmin, pmax):
        return self.rpp(self, name, pmin, pmax)

    def circular_cylinder(self, name, base_center_point, top_center_point, radius):
        return self.rcc(name, base_center_point, top_center_point, radius)

    def rpp(self, name, pmin, pmax):
        name = self._default_name_(name)
        is_string(name)
        is_truple(pmin)
        is_truple(pmax)
        minx,miny,minz = pmin
        maxx,maxy,maxz = pmax
        self.script_string += 'in {} rpp {} {} {} {} {} {}\n'.format(name,
                                                                     minx,maxx,
                                                                     miny,maxy,
                                                                     minz,maxz)
        return name

    def cuboid(self, corner_point, opposing_corner_point, name=None):
        return self.rpp(name, corner_point, opposing_corner_point)

    def arb4(self, name, v1, v2, v3, v4):
        is_string(name)
        name = self._default_name_(name)

        return name

    def arb5(self, name, v1, v2, v3, v4, v5):
        is_string(name)
        name = self._default_name_(name)
        
        return name

    def arb6(self, name, v1, v2, v3, v4, v5, v6):
        is_string(name)
        name = self._default_name_(name)
        [is_truple(v) for v in [v1, v2, v3, v4, v5, v6]]
        vs = [str(v) for xyz in [v1, v2, v3, v4, v5, v6] for v in xyz]
        assert len(vs)==6*3
        self.script_string += 'in {} arb6 {}\n'.format(name,
                                                       ' '.join(vs))
        return name

    def arb7(self, name, v1, v2, v3, v4, v5, v6, v7):
        is_string(name)
        name = self._default_name_(name)

    def arb8(self, name, points):
        name = self._default_name_(name)
        is_string(name)
        check_args = [is_truple(x) for x in points]
        assert(len(points)==8)
        points_list =  ' '.join([str(c) for c in chain.from_iterable(points)])
        
        #print 'arb8 points list: {}\n\n{}'.format(points, points_list)
        
        self.script_string += 'in {} arb8 {} \n'.format(name,
                                                        points_list
                                                        )
        return name
                                                        
    def arbX(self, name, vList):
        #Detect which function to use, and feed in the parameters
        if len(vList) in range(4, 9):
            arbFunction = getattr(self, "arb" + str(len(vList)))
            
            #Execute it
            arbFunction(name, *vList)
        
    def Cone(self, name, trc, vertex, height_vector, base_radius, top_radius):
        is_string(name)

    def Cone_elliptical(self, name, tec, vertex, height_vector, major_axis, minor_axis, ratio):
        is_string(name)

    def cone_general(self, name, vertex, height_vector, avector, bvector, cscalar, dscalar):
        return self.tgc(name, vertex, height_vector, avector, bvector, cscalar, dscalar)

    def cylinder(self, name, vertex, height_vector, radius):
        return self.rcc(name, vertex, height_vector, radius)

    def Cylinder_elliptical(self, name, rec, vertex, height_vector, major_axis, minor_axis):
        is_string(name)

    def Cylinder_hyperbolic(self, name, rhc,vertex, height_vector, bvector, half_width, apex_to_asymptote):
        is_string(name)

    def Cylinder_parabolic(self, name, rpc, vertex, height_vector, bvector, half_width):
        is_string(name)

    def Ellipsoid(self, name, ell, vertex, avector, bvector, cvector):
        is_string(name)

    def Hyperboloid_elliptical(self, name, ehy, vertex, height_vector, avector, bscalar, apex_to_asymptote):
        is_string(name)

    def Paraboloid_elliptical(self, name, epa, vertex, height_vector, avector, bscalar):
        is_string(name)

    def Ellipsoid_radius(self, name, ell1, vertex, radius):
        is_string(name)

    def Particle(self, name, part, vertex, height_vector, radius_at_v_end, radius_at_h_end):
        is_string(name)

    def sph(self, name, vertex, radius):
        name = self._default_name_(name)
        is_truple(vertex)
        is_number(radius)
        x, y, z = vertex
        self.script_string += 'in {} sph {} {} {} {}'.format(name, x, y, z, radius)
        return name

    def Sphere(self, name, vertex, radius):
        return self.sph(name, vertex, radius)

    def Torus(self, name, tor, vertex, normal, radius_1, radius_2):
        is_string(name)

    def Torus_elliptical(self, name, eto, vertex, normal_vector, radius, cvector, axis):
        is_string(name)

    def pipe_point(self, x, y, z, inner_diameter, outer_diameter, bend_radius):
        return OrderedDict(
                           [('x', x),
                            ('y', y),
                            ('z', z),
                            ('inner_diameter', inner_diameter),
                            ('outer_diameter', outer_diameter),
                            ('bend_radius', bend_radius)
                           ]
                          )

    def pipe(self, name, pipe_points):
        is_string(name)
        num_points = len(pipe_points)
        assert(num_points>1)

        if isinstance(pipe_points[0], dict):
            points_str_list = ['{} {} {} {} {} {}'.format(*points.values()) for points in pipe_points]
        # handle the way the hilbert_3d example from python-brlcad was using the Vector class
        elif isinstance(pipe_points[0][0], vmath.vector.Vector):
            def rotate_tuple(x): d = deque(list(x)); d.rotate(2); return d
            points_str_list = ['{} {} {} {} {} {}'.format(*(list(points[0]) + list(rotate_tuple(points[1:]))) ) for points in pipe_points]
        self.script_string += 'in {} pipe {} {}\n'.format(name, num_points, ' '.join(points_str_list))
        """ # this worked for me as a spring
        in spring.s pipe 10 -500 -500 250 10 200 500 -500 500 350 100 200 500 500 500 450 100 200 500 500 -500 550 100 200 500 -500 -500 650 100 200 500 -500 500 750 100 200 500 500 500 850 100 200 500 500 -500 950 100 200 500 -500 -500 1050 100 200 500 -500 500 1150 100 200 500 0 500 1200 100 200 500
        r s.r u spring.s
        """


class BrlCadModel(object):
    __metaclass__ = ABCMeta

    def __init__(self, brl_db):
        self.brl_db = brl_db
        self.name_tracker = brl_db.name_tracker
        self.get_next_name = self.name_tracker.get_next_name
        self.final_name = None
        self.connection_points = []

    def register_new_connection_point(self, name, coord, away_vector):
        self.connection_points.append((name, coord, away_vector))

    def get_connection(self, name):
        for item in self.connection_points:
            if item[0] == name:
                return item
        return None

    @property
    def connections_available(self):
        return [item[0] for item in self.connection_points]
