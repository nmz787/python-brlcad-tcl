# python-brlcad-tcl
So far this is a small subset of the brl-cad primitives with some notion of object-oriented design, being emitted as tcl scripts that mged can directly process into database (.g) files. Requirements are Python and brl-cad.



## An example of a 28BYJ-48 stepper motor, run with:  

* `python motor_28BYJ_48__example.py motor_28BYJ_48__example.tcl`
* `mged motor_28BYJ_48__example.g < motor_28BYJ_48__example.tcl`
* `g-stl -o out.stl motor_28BYJ_48__example.g motor_28BYJ_48__COMPLETE1.r`
** note that `motor_28BYJ_48__COMPLETE1.r` here is the 'region' that was created at the end of the motor's  __init__ function, it is a special type of combination that 'instantiates' all of the non-region 'object definitions' (primitives and combinations).
* `meshlab out.stl`


## Multi-part example

The multi-part example shows how to use two python objects. In addition to emitting the tcl script, it runs mged to create a new geometry database, and then converts that to an STL.

To view the resulting (.g) file in `mged`:
* `python multi_part_example.py multi_part.tcl && mged multi_part.g`
** (if you don't have meshlab installed, you could comment out the line starting with `brl_db.save_stl` to save some run-time time)
I was running this example then opening the resulting (.STL) file in meshlab (because I don't know how/if mged has a real-time raytracing display mode) :
* `python multi_part_example.py multi_part.tcl && meshlab multi_part.stl`

