# python-brlcad-tcl
So far this is a small subset of the brl-cad primitives with some notion of object-oriented design, being emitted as tcl scripts that mged can directly process into database (.g) files. Requirements are Python and brl-cad.



## An example of a 28BYJ-48 stepper motor, run with:  

* `python motor_28BYJ_48__example.py 28BYJ_48__motor_example.tcl`
* `mged 28BYJ_48__motor_example.g < 28BYJ_48__motor_example.tcl`
* `g-stl -o out.stl 28BYJ_48__motor_example.g motor_28BYJ_48__COMPLETE1.g`
* `meshlab out.stl`


## Multi-part example

The multi-part example shows how to use two python objects. In addition to emitting the tcl script, it runs mged to create a new geometry database, and then converts that to an STL.

I was running this example then opening the result in meshlab if the python script succeeded:
* `python multi_part_example.py multi_part.tcl && meshlab multi_part.stl`

of course if you don't have meshlab, then you can just view the resulting .g file in mged (and you should comment out `brl_db.save_stl` to save some run-time time) i.e. :
* `python multi_part_example.py multi_part.tcl && mged multi_part.g`