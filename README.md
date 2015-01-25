# python-brlcad-tcl
So far a small subset of the brl-cad primitives, using python-brlcad syntax, being emitted as tcl scripts that mged can directly process into database (.g) files.

An example is included, run with:  

python 28BYJ_48__motor_example.py 28BYJ_48__motor_example.tcl  

mged 28BYJ_48__motor_example.g < 28BYJ_48__motor_example.tcl  

g-stl -o out.stl 28BYJ_48__motor_example.g _28BYJ_48__COMPLETE1.g  

meshlab out.stl