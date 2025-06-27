import sys

## Create Final.cfg for TSFFD at Res-2

## Image voxel resolutions
delta_x = float(sys.argv[1])
delta_y = float(sys.argv[2])
delta_z = float(sys.argv[3])

print(f"""[ input ]
Padding value                      = -1024

[ transformation ]
Transformation model               = FFD
Control point spacing in T         = 10

[ optimization ]
Energy preconditioning             = 0.001
Divide data terms by initial value = No
Interpolation mode                 = Linear
Epsilon                            = -1e-7
Image (dis-)similarity measure     = NMI

[ Level 1 ]
Blurring [mm]                      = {2*delta_x}
Resolution [mm]                    = {4*delta_x} {4*delta_y} {4*delta_z}
Minimum length of steps            = 0.01
Maximum length of steps            = 4
[ Level 2 ]
Blurring [mm]                      = {5*delta_x}
Resolution [mm]                    = {10*delta_x} {10*delta_y} {10*delta_z}
Minimum length of steps            = 0.01
Maximum length of steps            = 4
[ Level 3 ]
Blurring [mm]                      = {10*delta_x}
Resolution [mm]                    = {20*delta_x} {20*delta_y} {20*delta_z}
Minimum length of steps            = 0.01
Maximum length of steps            = 4
[ Level 4 ]
Blurring [mm]                      = {20*delta_x}
Resolution [mm]                    = {40*delta_x} {40*delta_y} {40*delta_z}
Minimum length of steps            = 0.01
Maximum length of steps            = 4

[ Grid Search ]
Bending energy weight              = 4e-10
Sparsity weight                    = 3e-3""")