import numbers
from itertools import chain
import datetime
import subprocess
import os

def is_truple(arg):
    is_numeric_truple = isinstance(arg, tuple) and all([isinstance(x, numbers.Number) for x in arg])
    assert(is_numeric_truple)

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
    def __init__(self, tcl_filepath, title, make_g=False, make_stl=False, stl_quality=None, units = 'mm'):
        #if not os.path.isfile(self.output_filepath):
        #    abs_path = os.path.abspath(self.output_filepath)
        #    if not
        self.make_stl = make_stl
        self.make_g = make_g
        self.tcl_filepath = tcl_filepath
        self.stl_quality = stl_quality
        self.now_path = os.path.splitext(self.tcl_filepath)[0]

        self.script_string = 'title {}\nunits {}\n'.format(title, units)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save_tcl()

        if self.make_g or self.make_stl:
            self.save_g()
        if self.make_stl:
            self.save_stl()
            
    def add_script_string(self, to_add):
        #In case the user does some adding on their own
        self.script_string += '\n' + str(to_add) + '\n'

    def save_tcl(self):
        with open(self.tcl_filepath, 'w') as f:
            f.write(self.script_string)

    def save_g(self):
        self.g_path = self.now_path + '.g'
        # try to remove a databse file of the same name if it exists
        os.remove(self.g_path)
		
        proc = subprocess.Popen('mged {} < {}'.format(self.g_path, self.tcl_filepath), shell=True)
        proc.communicate()
        
    def run_and_save_stl(self, objects_to_render):
        #Do all of them in one go
        self.save_tcl()
        self.save_g()
        self.save_stl(objects_to_render)

    def save_stl(self, objects_to_render):
        stl_path = self.now_path + '.stl'
        obj_str = ' '.join(objects_to_render)
        cmd = 'g-stl -o {}'.format(stl_path)

        #Add the quality
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

        #Add the paths
        cmd = '{} {} {}'.format(cmd, self.g_path, obj_str)

        print cmd
        proc = subprocess.Popen(cmd, shell=True)
        proc.communicate()

    def combination(self, name, operation):
        is_string(name)
        self.script_string += 'comb {} {}\n'.format(name, operation)

    def region(self, name, operation):
        is_string(name)
        self.script_string += 'r {} {}\n'.format(name, operation)

    def begin_combination_edit(self, combination_to_select, path_to_center):
        self.script_string += 'Z\n'
        self.script_string += 'draw {}\n'.format(combination_to_select)
        self.script_string += 'oed / {0}/{1}\n'.format(combination_to_select, path_to_center)

    def end_combination_edit(self):
        self.script_string += 'accept\n'

    def translate(self, x, y, z, relative=False):
        cmd = 'translate'
        if relative:
            cmd = 'tra'
        self.script_string += '{} {} {} {}\n'.format(cmd, x, y, z)

    def translate_relative(self, dx, dy, dz):
        self.translate(dx, dy, dz, relative=True)

    def rotate_combination(self, x, y, z):
        self.script_string += 'orot {} {} {}\n'.format(x,y,z)

    def kill(self, name):
        if isinstance(name, list):
            for _name in name:
                self.script_string += 'kill {}\n'.format(_name)
        else:
            self.script_string += 'kill {}\n'.format(name)

    def rcc(self, name, base, height, radius):
        is_string(name)
        is_truple(base)
        is_truple(height)
        is_number(radius)
        bx, by,bz=base
        hx,hy,hz=height
        self.script_string += 'in {} rcc {} {} {} {} {} {} {}\n'.format(name,
                                                                     bx,by,bz,
                                                                     hx,hy,hz,
                                                                     radius)

    def rpp(self, name, pmin, pmax):
        is_string(name)
        is_truple(pmin)
        is_truple(pmax)
        minx,miny,minz = pmin
        maxx,maxy,maxz = pmax
        self.script_string += 'in {} rpp {} {} {} {} {} {}\n'.format(name,
                                                                     minx,maxx,
                                                                     miny,maxy,
                                                                     minz,maxz)

    def arb4(self, name, v1, v2, v3, v4):
        is_string(name)


    def arb5(self, name, v1, v2, v3, v4, v5):
        is_string(name)


    def arb6(self, name, v1, v2, v3, v4, v5, v6):
        is_string(name)


    def arb7(self, name, v1, v2, v3, v4, v5, v6, v7):
        is_string(name)

    def arb8(self, name, points):
        is_string(name)
        check_args = [is_truple(x) for x in points]
        assert(len(points)==8)
        points_list =  ' '.join([str(c) for c in chain.from_iterable(points)])
        
        #print 'arb8 points list: {}\n\n{}'.format(points, points_list)
        
        self.script_string += 'in {} arb8 {} \n'.format(name,
                                                        points_list
                                                        )

                                                        
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


    def Cone_general(self, name, tgc, vertex, height_vector, avector, bvector, cscalar, dscalar):
        is_string(name)


    def Cylinder(self, name, rcc, vertex, height_vector, radius):
        is_string(name)


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


    def Sphere(self, name, sph, vertex, radius):
        is_string(name)


    def Torus(self, name, tor, vertex, normal, radius_1, radius_2):
        is_string(name)


    def Torus_elliptical(self, name, eto, vertex, normal_vector, radius, cvector, axis):
        is_string(name)


