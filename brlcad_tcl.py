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

