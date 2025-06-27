'''
This script prints out the radius and centre of the spherical clipper for the MV from the 3 coordinates selected via the MV-Clip steps using CEMRGAPP.

This enables one to create the spherical clipper in Paraview and clip the resampled mesh to give the MV-Clipper.vtp
'''

import numpy as np

r1 = (31.3158182882, 148.654229583, 167.194643856)
r2 = (13.6978230635, 137.568119676, 156.641682996)
r3 = (18.571889487, 129.873226136, 174.837049770)

def PrintClipMesh( point_1, point_2, point_3):
    x_c = 0
    y_c = 0
    z_c = 0
    landmarks = (point_1, point_2, point_3)

    for i in range(0, len(landmarks)):
        x_c = x_c + landmarks[i][0]
        y_c = y_c + landmarks[i][1]
        z_c = z_c + landmarks[i][2]

    x_c /= len(landmarks)
    y_c /= len(landmarks)
    z_c /= len(landmarks)

    distance = []

    for i in range(0, len(landmarks)):
        x_d = landmarks[i][0] - x_c
        y_d = landmarks[i][1] - y_c
        z_d = landmarks[i][2] - z_c
        distance.append(np.sqrt(pow(x_d,2) + pow(y_d,2) + pow(z_d,2)))

    radius = max(distance)
    centre = (x_c, y_c, z_c)

    print("Radius: ", radius)
    print("Centre: ", centre[0], " ", centre[1], " ", centre[2])

if __name__ == "__main__":
	PrintClipMesh(r1, r2, r3)