import pyvista as pv
import numpy as np
from PIL import Image
import os
import math	
import copy
import random
import matplotlib.pyplot as plt

from py_atrial_fibres.file_utils import *
from py_atrial_fibres.mesh_utils import *

def ffmeg_command(video_folder,
				  basename,
				  video_name,
				  frame_rate):

	if os.path.exists(video_name):
		os.system("rm "+video_name)

	cmd = "ffmpeg -r "+str(frame_rate)+" -i "+video_folder+"/"+basename+"%d.png "
	cmd += "-vcodec libx264 "
	cmd += video_name

	os.system(cmd)

def crop_image(imagename,
			   output_imagename):

	cmd = "convert "+imagename+" -trim "+output_imagename
	os.system(cmd)

def composite_imgs(pos_w,
				   pos_h,
				   img_name,
				   output_img):

	cmd="composite  -colorspace srgb -geometry +"+str(pos_w)+"+"+str(pos_h)+" "+img_name+" "+output_img+" "+output_img
	os.system(cmd)

def generate_multipanel_image(image_structure,
							  output_imagename):

	# image_structure is a nested list. 
	# Example [[img1,img2,img3],[img4,img5,img6]]
	# will generate an image like:
	# img1 img2 img3
	# img4 img5 img6

	print("==============================================")
	print("Combining images in "+output_imagename+"...")
	print("==============================================")

	image_list = [img for sublist in image_structure for img in sublist]

	image_widths = np.zeros((len(image_list),),dtype=float)
	image_heights = np.zeros((len(image_list),),dtype=float)
	for i,img in enumerate(image_list):
		crop_image(img,
			       img[:-4]+"_cropped.png")

		with Image.open(img[:-4]+"_cropped.png") as tmp:
			image_widths[i], image_heights[i] = tmp.size

	max_width = np.max(image_widths)
	max_height = np.max(image_heights)

	ncol = 0
	nrow = len(image_structure)
	for row in image_structure:
		if len(row)>ncol:
			ncol=len(row)

	print("Using "+str(nrow)+" rows and "+str(ncol)+" columns.")

	fig_w = ncol*max_width
	fig_h = nrow*max_height

	cmd="convert -size "+str(fig_w)+"x"+str(fig_h)+" -background white xc:white -colorspace srgb "+output_imagename
	os.system(cmd)

	count = 0
	for i,row in enumerate(image_structure):
		for j,img in enumerate(row):

			shift_w = 0.5*(max_width-image_widths[count])
			shift_h = 0.5*(max_height-image_heights[count])

			img = img[:-4]+"_cropped.png"
			composite_imgs(max_width*j+shift_w,
   						   max_height*i+shift_h,
   						   img,
   						   output_imagename)

			count += 1

			os.system("rm "+img)


def carp_to_pyvista(meshname):

	pts = read_pts(meshname+'.pts')
	elem = read_elem(meshname+'.elem',el_type='Tr',tags=False)

	tets = np.column_stack((np.ones((elem.shape[0],),dtype=int)*3,elem)).flatten()
	cell_type = np.ones((elem.shape[0],),dtype=int)*vtk.VTK_TRIANGLE	
    
	plt_msh = pv.UnstructuredGrid(tets,cell_type,pts)

	return plt_msh

def make_activation_video(meshname,
						  activation_file,
						  video_folder,
						  camera_file,
					 	  inactive_color="lightgray",
					 	  active_color="firebrick",
					 	  view="anterior"):
	
	camera_settings = load_json(camera_file)

	plt_msh = carp_to_pyvista(meshname)
	
	act = np.loadtxt(activation_file,dtype=float)

	t0 = 0 
	tend = math.ceil(np.max(act))

	count = 0
	for t in range(t0,tend+1):

		binary_vector = (act<=t)

		print_screenshot_video(plt_msh,
					           binary_vector,
					           video_folder+"/act_"+str(count)+".png",
					           camera_settings,
					           title="time = "+str(t)+" ms",
					           fig_w=1200,
					           fig_h=1200,
					           inactive_color=inactive_color,
					           active_color=active_color,
					           view=view)

		count += 1

def print_screenshot_fibres(meshname,
						    screenshot_name,
						    camera_file,
						    color="red",
						    stride=3,
						    tube_radius=0.08,
						    fig_w=1200,
						   	fig_h=1200,
					 	    view="anterior"):
	
	plt_msh = carp_to_pyvista(meshname)

	lon = read_lon(meshname+".lon")
	fibres = copy.deepcopy(lon[:,:3])
    
	nelem = lon.shape[0]
	nelem_nofibres = int(nelem*(1-1./stride))
	exclude = random.sample(range(0, nelem), nelem_nofibres)

	fibres[exclude,:] = np.zeros((nelem_nofibres,3),dtype=float)
	plt_msh["fibres"] = fibres
    
	line = pv.Line()
	glyphs = plt_msh.glyph(orient='fibres',scale=True,factor=2000.0,geom=line.tube(radius=tube_radius))

	plotter = pv.Plotter(off_screen=True)
	plotter.background_color = 'white'

	plotter.add_mesh(glyphs,color=color)

	camera_settings = load_json(camera_file)

	plotter.camera.azimuth = camera_settings[view]["azimuth"]
	plotter.camera.elevation = camera_settings[view]["elevation"]

	plotter.screenshot(filename=screenshot_name, 
					   transparent_background=None, 
					   return_img=True,
					   window_size=[fig_w,fig_h])
	plotter.close()


def print_screenshot_activation(meshname,
						        activation_file,
						        screenshot_name,
						        camera_file,
						        fig_w=1200,
						   		fig_h=1200,
					 	        view="anterior"):
	
	plt_msh = carp_to_pyvista(meshname)
	
	act = np.loadtxt(activation_file,dtype=float)
	plt_msh.point_data["at"] = act
	tend = math.ceil(np.max(act))

	plotter = pv.Plotter(off_screen=True)
	plotter.background_color = 'white'

	sargs = dict(title="AT [ms]",
				 vertical=True,
				 width=0.05,
				 title_font_size=16,
				 label_font_size=16,
	    		 font_family="arial",
	    		 n_labels=2,
	    		 color='black',
	    		 fmt="%.1f",
	    		 position_y=0.3)

	msh = plotter.add_mesh(plt_msh,opacity=1.,
						   scalars="at",
						   cmap=plt.cm.get_cmap("jet_r",256),
						   clim=np.array([0.,tend]),
						   scalar_bar_args=sargs)

	camera_settings = load_json(camera_file)
	plotter.camera.azimuth = camera_settings[view]["azimuth"]
	plotter.camera.elevation = camera_settings[view]["elevation"]

	plotter.screenshot(filename=screenshot_name, 
					   transparent_background=None, 
					   return_img=True,
					   window_size=[fig_w,fig_h])
	plotter.close()


def print_screenshot_regions(meshname,
						     screenshot_name,
						     tags_list,
						     color_list,
						     camera_file,
						     default_color="lightgray",
						     fig_w=1200,
						     fig_h=1200,
						     view="anterior"):
	
	plt_msh = carp_to_pyvista(meshname)
	
	elem = read_elem(meshname+".elem",el_type="Tt",tags=True)
	tags_tmp = elem[:,-1]

	all_tags_list = np.sort(np.unique(tags_tmp))

	colors = [default_color,]+color_list
	opacity = np.ones((tags_tmp.shape[0],),dtype=float)*0.2
	tags = np.zeros((tags_tmp.shape[0],),dtype=float)
	for j,tt in enumerate(tags_list):
		tags[np.where(tags_tmp==tt)[0]] = j+1
		opacity[np.where(tags_tmp==tt)[0]] = 1.0

	plt_msh.cell_data["ID"] = tags
	plt_msh.cell_data["opacity"] = opacity

	plotter = pv.Plotter(off_screen=True)
	plotter.background_color = 'white'

	msh = plotter.add_mesh(plt_msh,
						   opacity="opacity",
						   scalars="ID",
						   n_colors=len(colors)+1,
						   cmap=colors)

	plotter.remove_scalar_bar()

	camera_settings = load_json(camera_file)
	plotter.camera.azimuth = camera_settings[view]["azimuth"]
	plotter.camera.elevation = camera_settings[view]["elevation"]

	plotter.screenshot(filename=screenshot_name, 
					   transparent_background=None, 
					   return_img=True,
					   window_size=[fig_w,fig_h])
	plotter.close()

def print_screenshot_video(plt_msh,
						   binary_vector,
						   screenshot_name,
						   camera_settings,
						   title=None,
						   fig_w=1200,
						   fig_h=1200,
						   inactive_color="gray",
						   active_color="darkred",
						   view="anterior"):

	plotter = pv.Plotter(off_screen=True)
	plotter.background_color = 'white'

	plt_msh.point_data["at"] = binary_vector

	msh = plotter.add_mesh(plt_msh,opacity=1.,
						   scalars="at",
						   cmap=[inactive_color,active_color],
						   clim=np.array([0.,1.]))

	plotter.remove_scalar_bar()

	plotter.camera.azimuth = camera_settings[view]["azimuth"]
	plotter.camera.elevation = camera_settings[view]["elevation"]

	plotter.add_title(title,
					  font_size=12,
					  font="arial",
					  color="black")

	plotter.screenshot(filename=screenshot_name, 
					   transparent_background=None, 
					   return_img=True,
					   window_size=[fig_w,fig_h])
	plotter.close()
