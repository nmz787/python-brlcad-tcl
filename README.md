# python-brlcad-tcl
So far this is a small subset of the brl-cad primitives with some notion of object-oriented design, being emitted as tcl scripts that mged can directly process into database (.g) files. Requirements are Python and brl-cad.


## An example of a 28BYJ-48 stepper motor, run with:  
* `# git clone this repository`
* `cd python-brlcad-tcl`
* `python -m examples.motor_28BYJ_48__example    output.tcl`
  * note that `motor_28BYJ_48__COMPLETE1.r` here is the 'region' that was created at the end of the motor's  __init__ function, it is a special type of combination that 'instantiates' all of the non-region 'object definitions' (primitives and combinations).
* `meshlab output.stl`


## Multi-part example

The multi-part example shows how to use two python-brlcad-tcl objects (including `motor_28BYJ_48__example.py`). In addition to emitting the tcl script, it runs mged to create a new geometry database, and then converts that to an STL.

To view the resulting (.g) file in `mged`:
* `# git clone this repository`
* `cd python-brlcad-tcl`
* `python -m examples.multi_part_example.py multi_part.tcl`
* `mged multi_part.g`
  * (if you don't have meshlab installed, you could comment out the line starting with `brl_db.save_stl` to save some run-time time)
I was running this example then opening the resulting (.STL) file in meshlab (because I don't know how/if mged has a real-time raytracing display mode) :
* `meshlab multi_part.stl`

## Example of slicing a model and exporting to individual STL files:
Looking at the stack of STL files emitted:

![Alt text](examples/output/microfluidic_pump/microfluidic_pump_slices_manually_created_animation.gif?raw=true "Animated GIF of the STL slices being shown and hidden")

Looking at the raster output, with greyscale output option:

![Alt text](examples/output/microfluidic_pump/microfluidic_pump_greyscale.gif?raw=true "")

Looking at the raster output:

![Alt text](examples/output/microfluidic_pump/microfluidic_pump_bw.gif?raw=true "")

# Developers section
## Adding support to python-brlcad-tcl for new operations or shapes/primitives
### If it is an mged command
* find the usage syntax - <https://brlcad.org/wiki/MGED_Commands>
* add a new method that users will use to call the new feature from their scripts
* code the method to use string-formatting, then append it to the `self.script_string_list` object

#### Conventions
* `name = self._default_name_(name)`
  * this will do a few things
    * checks if the name is empty-string or `None`
      * if so, then uses the `inspect` module to learn the caller-function name, and uses that function name as a "new name"
    * checks if the name is in a lookup-table of already-used names
      * if so, appends a number to the name, then adds this name to the lookup-table
* `return name`
  * return the name of the final object or primitive so the users can use it if they want
 
