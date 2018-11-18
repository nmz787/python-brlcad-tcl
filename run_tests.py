"""
export PATH=$PATH:/usr/brlcad/bin
"""
import os
import sys
import md5
import pkgutil
import shutil
import subprocess
import examples
import hashlib

pkg_path = os.path.dirname(examples.__file__)
example_list = pkgutil.iter_modules([pkg_path])
example_list = [name for _type, name, unknown in example_list]

example_list = [('motor_28BYJ_48__example','motor_28BYJ_48__example.stl'),
                ('multi_part_example','multi_part_example.stl'),
                ('spring','spring.stl'),
                ('hilbert_3d','hilbert_3d.stl'),
                ('shed','shed.stl'),
                ('mems_hello_world','mems_hello_world.stl'),
                #('tobacco_mesophyll_protoplast_fusion_device','tobacco_mesophyll_protoplast_fusion_device__negative.stl'),
                #('pencilSharpener','pencilSharpener.stl'),
                #('spiral','spiral.stl'),
                ('microfluidic_pump', os.path.join('microfluidic_pump','microfluidic_pump.stl'))]

# start from a specific test
i=0
if len(sys.argv)>=2:
  try:
    i=int(sys.argv[1])
  except:
    import traceback
    traceback.print_exc()
    i=0

test_results_folder = 'run_tests_results'
if os.path.exists(test_results_folder):
  shutil.rmtree(test_results_folder)
os.mkdir(test_results_folder)

for example,committed_output_filename  in example_list[i:]:
  #print(example,output_stl_filename)
  # run example
  test_results_folder_path = os.path.join(test_results_folder, example)
  output_g_filename = '{}_output'.format(test_results_folder_path)
  output_stl_filename = '{}_output.stl'.format(test_results_folder_path)
  committed_output = os.path.join('examples', 'output', '{}'.format(committed_output_filename))
  cmd = 'python -m examples/{} {}'.format(example, output_g_filename)
  print('about to run: {}'.format(example))
  proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
  out, err = proc.communicate()

  if not proc.returncode==0:
    print('TEST FAILED: {} output to follow\n{}\n{}\n\n'.format(example, out, err))
    sys.exit(-1)
  else:
    print('TEST RAN WITHOUT OBVIOUSLY CRASHING: {}'.format(example))
  print('committed filepath {} -  {}'.format(committed_output, 
                                   os.path.isfile(committed_output)))
  print('test-output filepath {} -  {}'.format(output_stl_filename, 
                                   os.path.isfile(output_stl_filename)))
  if os.path.isfile(committed_output):
    # check output matches 
    with open(output_stl_filename) as f:
      hash1=hashlib.md5(f.read()).digest()
    with open(committed_output) as f:
      hash2=hashlib.md5(f.read()).digest()

    if not hash1==hash2:
      print('TEST FAILED (STLs don\'t match): {} - committed_output, test_output filesizes ({}, {}) hashes ({}, {})\npaths ({}, {})\n\n'
            .format(example,
                    os.path.getsize(committed_output),
                    os.path.getsize(output_stl_filename),
                    str(hash2),
                    str(hash1),
                    committed_output,
                    output_stl_filename
                    ))
      sys.exit(-1)
    else:
      print('Hashes matched for STL files {}\n'.format(example))

  # for tempfile in [output_g_filename, output_stl_filename]:
  #   if os.path.isfile(tempfile):
  #     os.remove(tempfile)
  

# if __name__ == "__main__":
#     g_path_out = check_cmdline_args(__file__)
#     with brlcad_tcl(g_path_out, "My Database", stl_quality=0.1,verbose=True) as brl_db:
#         rc = rounded_cube(brl_db)
#         final_name = brl_db.region('u {}'.format(rc.final_name))
#     # process the g database into an STL file with a list of regions
#     brl_db.run_and_save_stl([union([final_name])])
