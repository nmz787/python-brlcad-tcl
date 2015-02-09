title Pencil Sharpener Gear
units in
in b rcc 0 0 0 0 0 0.262 0.65
in bn rcc 0 0 0 0 0 0.262 0.46
r br  u b - bn
in m rcc 0 0 0.262 0 0 0.275 0.502
in mn rcc 0 0 0.262 0 0 0.275 0.4575
r mr  u m - mn
in t rcc 0 0 0.537 0 0 0.383 0.245
in tn rcc 0 0 0.537 0 0 0.383 0.19685
r tr  u t - tn
in mt rcc 0 0 0.537 0 0 -0.06875 0.502
in mtn rcc 0 0 0.537 0 0 -0.06875 0.19685
r mtr  u mt - mtn
r tf  u tr u mtr
in l rcc 0.4395 -0.03125 0.537 0 0 0.1915 0.0625
in r rcc -0.4395 -0.03125 0.537 0 0 0.1915 0.0625
r mh  u mr u l u r
in sh arb8 -0.375 0 0.262 0.375 0 0.262 0.375 0 0.537 -0.375 0 0.537 -0.375 0.502 0.262 0.375 0.502 0.262 0.375 0.502 0.537 -0.375 0.502 0.537 
r mf  u mh - sh

in tooth0 arb6 -0.27 0 0 0.27 0 0 0.27 0 0.1965 -0.27 0 0.1965 0 0.555 0 0 0.555 0.1965


cp tooth0 tooth1
e tooth1
sed tooth1
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth1 tooth2
e tooth2
sed tooth2
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth2 tooth3
e tooth3
sed tooth3
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth3 tooth4
e tooth4
sed tooth4
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth4 tooth5
e tooth5
sed tooth5
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth5 tooth6
e tooth6
sed tooth6
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth6 tooth7
e tooth7
sed tooth7
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth7 tooth8
e tooth8
sed tooth8
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth8 tooth9
e tooth9
sed tooth9
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth9 tooth10
e tooth10
sed tooth10
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth10 tooth11
e tooth11
sed tooth11
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth11 tooth12
e tooth12
sed tooth12
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth12 tooth13
e tooth13
sed tooth13
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth13 tooth14
e tooth14
sed tooth14
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth14 tooth15
e tooth15
sed tooth15
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth15 tooth16
e tooth16
sed tooth16
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth16 tooth17
e tooth17
sed tooth17
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth17 tooth18
e tooth18
sed tooth18
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth18 tooth19
e tooth19
sed tooth19
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth19 tooth20
e tooth20
sed tooth20
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth20 tooth21
e tooth21
sed tooth21
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth21 tooth22
e tooth22
sed tooth22
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth22 tooth23
e tooth23
sed tooth23
keypoint 0 0 0
rot 0 0 14.4
accept


cp tooth23 tooth24
e tooth24
sed tooth24
keypoint 0 0 0
rot 0 0 14.4
accept


r gf u tooth0 u tooth1 u tooth2 u tooth3 u tooth4 u tooth5 u tooth6 u tooth7 u tooth8 u tooth9 u tooth10 u tooth11 u tooth12 u tooth13 u tooth14 u tooth15 u tooth16 u tooth17 u tooth18 u tooth19 u tooth20 u tooth21 u tooth22 u tooth23 u tooth24 
r bf  u br - gf
r finished  u bf u mf u tf
