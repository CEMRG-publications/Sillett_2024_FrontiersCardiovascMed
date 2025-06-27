import os
import copy
import numpy as np
import pyvista as pv
import meshio

from py_atrial_fibres.meshtools_utils import *
from py_atrial_fibres.file_utils import *
from py_atrial_fibres.distance_utils import find_point_along_direction

def check_valve_planes(meshname,
					   outmeshname,
					   tags_setup):

	os.system("rm -r ./tmp/*")
	os.system("mkdir ./tmp/")
	
	tag_la = extract_tags(tags_setup,["LA"])
	tag_la = [str(t) for t in tag_la]
	tag_la_string = ",".join(tag_la)

	tag_lspv = extract_tags(tags_setup,["LSPV_vp"])
	tag_lspv = [str(t) for t in tag_lspv]
	tag_lspv_string = ",".join(tag_lspv)

	tag_lipv = extract_tags(tags_setup,["LIPV_vp"])
	tag_lipv = [str(t) for t in tag_lipv]
	tag_lipv_string = ",".join(tag_lipv)

	tag_rspv = extract_tags(tags_setup,["RSPV_vp"])
	tag_rspv = [str(t) for t in tag_rspv]
	tag_rspv_string = ",".join(tag_rspv)

	tag_ripv = extract_tags(tags_setup,["RIPV_vp"])
	tag_ripv = [str(t) for t in tag_ripv]
	tag_ripv_string = ",".join(tag_ripv)

	all_good =  True
	retag_eidx = []

	print('================================================================')
	print('Checking left pulmonary veins...')
	print('================================================================')

	cmd = "meshtool extract mesh -msh="+meshname+" -submsh=./tmp/lspv -tags="+tag_lspv_string
	os.system(cmd)

	cmd = "meshtool extract mesh -msh="+meshname+" -submsh=./tmp/lipv -tags="+tag_lipv_string
	os.system(cmd)

	lipv_nod = read_nod_eidx("./tmp/lspv.nod")
	lspv_nod = read_nod_eidx("./tmp/lipv.nod")
	lspv_lipv_vtx = np.intersect1d(lipv_nod,lspv_nod)

	if len(lspv_lipv_vtx)>0:

		print('================================================================')
		print('Found issue on the left pulmonary veins. Retagging mesh.')
		print('================================================================')

		lipv_eidx = read_nod_eidx("./tmp/lspv.eidx")
		lspv_eidx = read_nod_eidx("./tmp/lipv.eidx")
		lpv_eidx = np.concatenate((lipv_eidx,lspv_eidx))

		elem = read_elem(meshname+".elem",el_type="Tt",tags=True)
		tags = elem[:,-1]
		elem = elem[:,:4]

		retag_eidx = []
		for eidx in lpv_eidx:
			el = elem[eidx,:]
			inter = np.intersect1d(el,lspv_lipv_vtx)

			if len(inter)>0:
				retag_eidx.append(eidx)

		all_good = False

	else:
		print('================================================================')
		print('Left veins are ok.')
		print('================================================================')

	print('================================================================')
	print('Checking right pulmonary veins...')
	print('================================================================')

	cmd = "meshtool extract mesh -msh="+meshname+" -submsh=./tmp/rspv -tags="+tag_rspv_string
	os.system(cmd)

	cmd = "meshtool extract mesh -msh="+meshname+" -submsh=./tmp/ripv -tags="+tag_ripv_string
	os.system(cmd)

	ripv_nod = read_nod_eidx("./tmp/rspv.nod")
	rspv_nod = read_nod_eidx("./tmp/ripv.nod")
	rspv_ripv_vtx = np.intersect1d(ripv_nod,rspv_nod)

	if len(rspv_ripv_vtx)>0:

		print('================================================================')
		print('Found issue on the left pulmonary veins. Retagging mesh.')
		print('================================================================')

		ripv_eidx = read_nod_eidx("./tmp/rspv.eidx")
		rspv_eidx = read_nod_eidx("./tmp/ripv.eidx")
		rpv_eidx = np.concatenate((ripv_eidx,rspv_eidx))

		elem = read_elem(meshname+".elem",el_type="Tt",tags=True)
		tags = elem[:,-1]
		elem = elem[:,:4]

		for eidx in rpv_eidx:
			el = elem[eidx,:]
			inter = np.intersect1d(el,rspv_ripv_vtx)

			if len(inter)>0:
				retag_eidx.append(eidx)

		all_good = False

	else:
		print('================================================================')
		print('Right veins are ok.')
		print('================================================================')

	if not all_good:

		tags[retag_eidx] = int(tags_setup["LA"])

		write_elem(elem,
				   tags,
				   outmeshname+".elem",
				   el_type='Tt')	

		os.system("cp "+meshname+".pts "+outmeshname+".pts")
		os.system("cp "+meshname+".lon "+outmeshname+".lon")	

		os.system("meshtool convert -imsh="+outmeshname+" -omsh="+outmeshname+".vtk")

	os.system("rm -r ./tmp/")

	return all_good

def split_valve_plane(meshname,
					  outmeshname,
					  tags_setup,
					  vp_to_split,
					  ring_to_split,
					  width=2000.0,
					  retag_vp=25):

	pts = read_pts(meshname+".pts")
	elem = read_elem(meshname+".elem",el_type="Tt",tags=True)
	tags = elem[:,-1]
	elem = elem[:,:4]

	print('================================================================')
	print('Splitting the valve plane with tag '+str(vp_to_split)+'.')
	print('================================================================')

	tag_la = tags_setup["LA"]

	eidx_vp_split = np.where(tags==vp_to_split)[0]
	elem_vp_split = elem[eidx_vp_split,:]
	vtx_vp_split = np.unique(elem_vp_split.flatten())

	eidx_ring_split = np.where(tags==ring_to_split)[0]
	elem_ring_split = elem[eidx_ring_split,:]
	vtx_ring_split = np.unique(elem_ring_split.flatten())

	eidx_la = np.where(tags==tag_la)[0]
	elem_la = elem[eidx_la,:]
	vtx_la = np.unique(elem_la.flatten())

	vtx_ring_vp = np.intersect1d(vtx_ring_split,vtx_vp_split)
	vtx_la_vp = np.intersect1d(vtx_la,vtx_vp_split)

	cog_split = np.mean(pts[vtx_vp_split,:],axis=0)
	distance = np.linalg.norm(pts[vtx_ring_vp,:]-cog_split,axis=1)

	closest = vtx_ring_vp[np.argmin(distance)]

	short_axis = cog_split-pts[closest,:]
	short_axis = short_axis/np.linalg.norm(short_axis)

	opposite = find_point_along_direction(pts,vtx_ring_vp,short_axis,cog_split)

	short_axis = pts[opposite,:]-pts[closest,:]
	short_axis = short_axis/np.linalg.norm(short_axis)

	N=20
	short_axis_points = np.zeros((N+7,3),dtype=float)
	short_axis_l = np.linalg.norm(pts[opposite,:]-pts[closest,:])
	for i in range(N-1):
		short_axis_points[i,:] = pts[closest,:] + short_axis*short_axis_l*i/N
	short_axis_points[N,:] = pts[opposite,:]
	short_axis_points[N+1,:] = pts[closest,:] - short_axis*short_axis_l/N
	short_axis_points[N+2,:] = pts[closest,:] - 2.*short_axis*short_axis_l/N
	short_axis_points[N+3,:] = pts[closest,:] - 3.*short_axis*short_axis_l/N
	short_axis_points[N+4,:] = pts[opposite,:]+ short_axis*short_axis_l/N
	short_axis_points[N+5,:] = pts[opposite,:]+ 2.*short_axis*short_axis_l/N
	short_axis_points[N+6,:] = pts[opposite,:]+ 3.*short_axis*short_axis_l/N

	write_pts(short_axis_points,meshname+"_short_axis.pts")

	retag_vtx = []
	for p in short_axis_points:
		distance = np.linalg.norm(pts[vtx_vp_split,:]-p,axis=1)
		retag_vtx += list(vtx_vp_split[np.where(distance<=width)[0]])	

	retag_eidx = []
	for i,tt in enumerate(elem_vp_split):
		if len(np.intersect1d(tt,retag_vtx))>0:
			retag_eidx.append(eidx_vp_split[i])
	retag_eidx = np.array(retag_eidx)
	keep_vp_eidx = np.setdiff1d(eidx_vp_split,retag_eidx)

	tags[retag_eidx] = int(tag_la)

	print('================================================================')
	print('Saving the element indices that were retagged.')
	print('================================================================')

	np.savetxt(outmeshname+"_LA_retagged.txt",retag_eidx,fmt="%d")

	# ---------------------------------------------------
	keep_vp_elem = elem[keep_vp_eidx,:]
	keep_vp_vtx = np.unique(keep_vp_elem.flatten())
	keep_vp_pts = pts[keep_vp_vtx,:]
	keep_vp_elem_reindexed = reindex_elem(keep_vp_vtx,keep_vp_elem)
	tags_vp = tags[keep_vp_eidx]

	write_elem(keep_vp_elem_reindexed,tags_vp,outmeshname+"_vp.elem",el_type='Tt')
	write_pts(keep_vp_pts,outmeshname+"_vp.pts")

	os.system("meshtool convert -imsh="+outmeshname+"_vp -omsh="+outmeshname+"_vp.vtk")

	cmd = "meshtool extract unreachable -msh="+outmeshname+"_vp -submsh="+outmeshname+"_vp_cc -ofmt=vtk"
	os.system(cmd)

	eidx_cc_0 = read_nod_eidx(outmeshname+"_vp_cc.part0.eidx")
	eidx_cc_1 = read_nod_eidx(outmeshname+"_vp_cc.part1.eidx")
	nod_cc_0 = read_nod_eidx(outmeshname+"_vp_cc.part0.nod")
	nod_cc_1 = read_nod_eidx(outmeshname+"_vp_cc.part1.nod")

	eidx_laa = np.where(tags==tags_setup["LAA"])[0]
	elem_laa = elem[eidx_laa,:]
	vtx_laa = np.unique(elem_laa.flatten())
	cog_laa = np.mean(pts[vtx_laa,:],axis=0)

	cog_cc_0 = np.mean(keep_vp_pts[nod_cc_0,:],axis=0)
	cog_cc_1 = np.mean(keep_vp_pts[nod_cc_1,:],axis=0)

	distance_0 = np.linalg.norm(cog_laa-cog_cc_0)
	distance_1 = np.linalg.norm(cog_laa-cog_cc_1)

	if distance_0<distance_1:
		tag_0 = vp_to_split
		tag_1 = retag_vp
	else:
		tag_0 = retag_vp
		tag_1 = vp_to_split	

	tags_vp[eidx_cc_0] = tag_0
	tags_vp[eidx_cc_1] = tag_1

	tags[keep_vp_eidx] = tags_vp

	write_elem(elem,
			   tags,
			   outmeshname+".elem",
			   el_type='Tt')	

	os.system("cp "+meshname+".pts "+outmeshname+".pts")
	os.system("cp "+meshname+".lon "+outmeshname+".lon")	

	os.system("meshtool convert -imsh="+outmeshname+" -omsh="+outmeshname+".vtk")

	print('================================================================')
	print('Updated tag setup to account for split.')
	print('================================================================')

	tags_setup["LIPV_vp"] = retag_vp
	tags_setup["PV_planes"] = np.append (tags_setup["PV_planes"], [retag_vp])

	os.system("rm "+outmeshname+"_vp.*")
	os.system("rm "+outmeshname+"_vp_cc.*")

	return tags_setup