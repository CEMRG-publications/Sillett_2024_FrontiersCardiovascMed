import os
import numpy as np
import sys

def Spherical_Clipper_Params(p1, p2, p3):

	x_tot = 0.0
	y_tot = 0.0
	z_tot = 0.0

	tuple_list = (p1, p2, p3)

	for i in range(0, len(tuple_list)):

		x_tot += tuple_list[i][0]
		y_tot += tuple_list[i][1]
		z_tot += tuple_list[i][2]

	x_ave = x_tot/len(tuple_list)
	y_ave = y_tot/len(tuple_list)
	z_ave = z_tot/len(tuple_list)

	distances = []

	for i in range(0, len(tuple_list)):

		dist = CalcDist((x_ave, y_ave, z_ave), tuple_list[i])
		distances.append(dist)

	radius = max(distances)
	centre = (x_ave, y_ave, z_ave)

	return radius, centre


def CalcDist(p1, p2):

	x1 = p1[0]
	y1 = p1[1]
	z1 = p1[2]

	x2 = p2[0]
	y2 = p2[1]
	z2 = p2[2]

	d_sq = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2

	dist = np.sqrt(d_sq)

	return dist

if __name__ == "__main__":

    r1 = (sys.arg[1], sys.arg[2], sys.arg[3])
	r2 = (sys.arg[4], sys.arg[5], sys.arg[6])
	r3 = (sys.arg[7], sys.arg[8], sys.arg[9])

	print(r1)