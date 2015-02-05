title My Database
units mm
in motor_28BYJ_48__main_body_cyl1.s rcc 0 0 0 0 0 19 14.0
in motor_28BYJ_48__wire_square1.s rpp -7.3 7.3 -17 0 0 19
comb motor_28BYJ_48__main_body1.c u motor_28BYJ_48__wire_square1.s u motor_28BYJ_48__main_body_cyl1.s
in motor_28BYJ_48__mounting_wings_rect1.s rpp -17.5 17.5 -3.5 3.5 18 19
in motor_28BYJ_48__left_wing_hole1.s rcc -17.5 0 18 0 0 1 2.1
in motor_28BYJ_48__left_wing_curve1.s rcc -17.5 0 18 0 0 1 3.5
in motor_28BYJ_48__right_wing_hole1.s rcc 17.5 0 18 0 0 1 2.1
in motor_28BYJ_48__right_wing_curve1.s rcc 17.5 0 18 0 0 1 3.5
comb motor_28BYJ_48__wings_chamfered1.c u motor_28BYJ_48__left_wing_curve1.s u motor_28BYJ_48__right_wing_curve1.s u motor_28BYJ_48__mounting_wings_rect1.s
comb motor_28BYJ_48__wings_left_subtracted1.c u motor_28BYJ_48__wings_chamfered1.c - motor_28BYJ_48__left_wing_hole1.s
comb motor_28BYJ_48__wings_block1.c u motor_28BYJ_48__wings_left_subtracted1.c - motor_28BYJ_48__right_wing_hole1.s
in motor_28BYJ_48__body_to_shaft_base1.s rcc 0 8 19 0 0 1.5 4.5
in motor_28BYJ_48__shaft_base1.s rcc 0 8 20.5 0 0 2.5 2.5
in motor_28BYJ_48__shaft_key_cyl1.s rcc 0 8 23.0 0 0 6 2.5
in motor_28BYJ_48__shaft_key_rpp1.s rpp -2.5 2.5 6.5 9.5 23.0 29.0
comb motor_28BYJ_48__shaft_key1.c u motor_28BYJ_48__shaft_key_cyl1.s + motor_28BYJ_48__shaft_key_rpp1.s
comb motor_28BYJ_48__shaft1.c u motor_28BYJ_48__body_to_shaft_base1.s u motor_28BYJ_48__shaft_base1.s u motor_28BYJ_48__shaft_key1.c
r motor_28BYJ_48__COMPLETE1.r u motor_28BYJ_48__main_body1.c u motor_28BYJ_48__wings_block1.c u motor_28BYJ_48__shaft1.c
