title My Database
units mm
in main_body_cyl.s rcc 0 0 0 0 0 19 14.0
in wire_square.s rpp -7.3 7.3 -17 0 0 19
comb main_body.c  u wire_square.s u main_body_cyl.s
in motor_28BYJ_48__mounting_wings_rect1.s rpp -17.5 17.5 -3.5 3.5 18 19
in left_wing_hole.s rcc -17.5 0 18 0 0 1 2.1
in left_wing_curve.s rcc -17.5 0 18 0 0 1 3.5
in right_wing_hole.s rcc 17.5 0 18 0 0 1 2.1
in right_wing_curve.s rcc 17.5 0 18 0 0 1 3.5
comb wings_chamfered.c   u left_wing_curve.s u right_wing_curve.s u motor_28BYJ_48__mounting_wings_rect1.s
comb wings_left_subtracted.c   u wings_chamfered.c - left_wing_hole.s
comb wings_block.c  u wings_left_subtracted.c - right_wing_hole.s
in body_to_shaft_base.s rcc 0 8 19 0 0 1.5 4.5
in shaft_base.s rcc 0 8 20.5 0 0 2.5 2.5
in shaft_key_cyl.s rcc 0 8 23.0 0 0 6 2.5
in shaft_key_rpp.s rpp -2.5 2.5 6.5 9.5 23.0 29.0
comb shaft_key.c   u shaft_key_cyl.s + shaft_key_rpp.s
comb shaft1.c   u body_to_shaft_base.s u shaft_base.s u shaft_key.c
r motor_28BYJ_48__COMPLETE1.r u main_body.c u wings_block.c u shaft1.c
