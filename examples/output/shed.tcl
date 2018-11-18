title My Database
units mm
in shedbox rpp 0 16 0 12 0 10
in room_void rpp 0.2 15.8 0.2 11.8 0.2 10.2
in loft rpp 0 16 5 12 9.8 10
in mainroof arb6 0 0 10 0 12 10 0 6 15 16 0 10 16 12 10 16 6 15
in inner_void arb6 0.2 0.2 9.8 0.2 11.8 9.8 0.2 6.0 14.8 15.8 0.2 9.8 15.8 11.8 9.8 15.8 6.0 14.8
in box_window1 rpp 1 3 -0.3 0.3 3 7
in box_window2 rpp 13 15 -0.3 0.3 3 7
in roof_window1 rpp 1 3 2.7 3.3 10.5 14.5
Z
draw roof_window1
sed roof_window1
arot 1 0 0 129.805571092
accept
in roof_window2 rpp 13 15 2.7 3.3 10.5 14.5
Z
draw roof_window2
sed roof_window2
arot 1 0 0 129.805571092
accept
in french_door rpp 5.25 10.75 -0.3 0.3 0.2 6.2
comb room   u shedbox - box_window1 - box_window2 - room_void - french_door
comb roof   u mainroof - inner_void - roof_window1 - roof_window2
comb shed   u room u roof u loft
