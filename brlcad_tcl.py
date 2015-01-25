import numbers 
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
    return [' u ', args]

def subtract(*args):
    return [' - ', args]

def intersect(*args):
    return [' + ', args]

class brlcad_tcl():
    def __init__(self, output_filepath, title):
        #if not os.path.isfile(self.output_filepath):
        #    abs_path = os.path.abspath(self.output_filepath)
        #    if not 
        self.output_filepath = output_filepath
        self.script_string = 'title {}\nunits mm\n'.format(title)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        with open(self.output_filepath, 'w') as f:
            f.write(self.script_string)

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
    
    def combination(self, name, tree):
        is_string(name)
        self.script_string += 'r {} u {}\n'.format(name, tree[0].join(tree[1]))

    def Arb4(self, name, arb4, v1, v2, v3, v4):
        is_string(name)


    def Arb5(self, name, arb5, v1, v2, v3, v4, v5):
        is_string(name)


    def Arb6(self, name, arb6, v1, v2, v3, v4, v5, v):
        is_string(name)


    def Arb7(self, name, arb7, v1, v2, v3, v4, v5, v6, v7):
        is_string(name)


    def Arb8(self, name, arb8, v1, v2, v3, v4, v5, v6, v7, v8):
        is_string(name)


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


