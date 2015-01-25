title My Database
units mm
in _28BYJ_48__main_body_cyl1.s rcc 0 0 0 0 0 19 14.0
in _28BYJ_48__wire_square1.s rpp -7.3 7.3 0 17 0 19
r _28BYJ_48__main_body1.r u _28BYJ_48__wire_square1.s u _28BYJ_48__main_body_cyl1.s
in _28BYJ_48__mounting_wings_rect1.s rpp -17.5 17.5 -3.5 3.5 18 19
in _28BYJ_48__left_wing_hole1.s rcc -17.5 0 18 0 0 1 2.1
in _28BYJ_48__left_wing_curve1.s rcc -17.5 0 18 0 0 1 3.5
in _28BYJ_48__right_wing_hole1.s rcc 17.5 0 18 0 0 1 2.1
in _28BYJ_48__right_wing_curve1.s rcc 17.5 0 18 0 0 1 3.5
r _28BYJ_48__wings_chamfered1.r u _28BYJ_48__left_wing_curve1.s u _28BYJ_48__right_wing_curve1.s u _28BYJ_48__mounting_wings_rect1.s
r _28BYJ_48__wings_left_subtracted1.r u _28BYJ_48__wings_chamfered1.r - _28BYJ_48__left_wing_hole1.s
r _28BYJ_48__wings_block1.r u _28BYJ_48__wings_left_subtracted1.r - _28BYJ_48__right_wing_hole1.s
r _28BYJ_48__COMPLETE1.g u _28BYJ_48__main_body1.r u _28BYJ_48__wings_block1.r
