O0400 ( G7.1,Cylindrical Interpolation, M13, M52,D38.2L100, W-right ) 
( Chon goc phoi W tai dau ben phai)
N15 G71 G90 G94 G97
N25 M06 T0505 S1000 F200 (Endmill D5mm, in X direction (Ridial))
N30 M13 (driven-Endmill)
N35 M52 (C-axis active)
N36 G7.1 C19.1 (Start of Cylindrical Interpolation, D=38.2mm)
N40 G00 X45 Z-5 (Start point)
N45 G01 X35 C0 (cut into X35mm)
N50 Z-15 C22.5 (P1)
N55 Z-5 C45 (P2)
N60 Z-15 C67.5 (P3)
N65 Z-5 C90
N70 Z-15 C112.5
N75 Z-5 C135
N80 Z-15 C157.5
N85 Z-5 C180
N90 Z-15 C202.5
N95 Z-5 C225
N100 Z-15 C247.5
N105 Z-5 C270
N110 Z-15 C292.5
N115 Z-5 C315 
N120 Z-15 C337.5 (P16)
N125 Z-5 C360 (P1)
N130 X45 (Tool out)
(Ket thuc bien dang)
(Gia cong ranh then 1 doc theo Z)
M1
N135 Z-25 
N136 C90
N140 G01 X35
N145 Z-40 ( ranh then dai 15)
N150 X45 (Tool out)

(Gia cong ranh then 2 doc theo Z)
M1
N135 Z-25 
N136 C270
N140 G01 X35
N145 Z-40 ( ranh then dai 15)
N150 X45 (Tool out)

M1
(Gia cong ranh cong tren be mat tru ngoai)
N155 C80
N135 Z-35 
N140 G01 X35
N145 C180
N150 X45 (Tool out)
(Gia cong ranh cong tren be mat dau)
M06 T0707 (Dao phay ngon 5 mm)
N155 X20 Z5 C80
N140 G01 Z-5
N145 C180
N150 Z5 (Tool out)

N155 G7.1 C0 (End of Cylindrical Interpolation)
M30 


