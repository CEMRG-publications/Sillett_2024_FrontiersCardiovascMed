import os
import sys
from py_atrial_fibres.pyvista_utils import *

meshname = "./mesh/biatrial_fibres_l"
activation_file = "./mesh/0.dat"

view = "anterior"
camera_file = "./camera_angles/10.json"

video_folder = "./video_imgs_"+view+"/"
figure_folder = "./imgs_"+view+"/"

os.system("mkdir "+video_folder)
os.system("mkdir "+figure_folder)

print_screenshot_regions(meshname,
						 figure_folder+"/regions.png",
						 [30,31,32],
						 ["deepskyblue","darkorange","forestgreen"],
						 camera_file,
						 fig_w=1200,
						 fig_h=1200,
						 view=view)

print_screenshot_activation(meshname,
						    activation_file,
						    figure_folder+"/activation.png",
						    camera_file,
						    view=view)

print_screenshot_fibres(meshname,
						figure_folder+"/fibres.png",
						camera_file,
						color="deepskyblue",
						stride=4,
						tube_radius=0.08,
						view=view)

make_activation_video(meshname,
				      activation_file,
				      video_folder,
				      camera_file,
				      inactive_color="lightgray",
				      active_color="firebrick",
				      view=view)

ffmeg_command(video_folder,
			  "act_",
			  video_folder+"/activation.avi",
			  30)

############################################################
# multipanel figure : example 1

image_structure = [["./imgs_anterior/regions.png","./imgs_anterior/fibres.png"],
				   ["./imgs_posterior/regions.png","./imgs_posterior/fibres.png"]]

generate_multipanel_image(image_structure,
						  "./regions_fibres.png")

############################################################
# multipanel figure : example 2

image_structure = [["./video_imgs_anterior/act_0.png","./video_imgs_anterior/act_35.png","./video_imgs_anterior/act_70.png","./video_imgs_anterior/act_105.png","./video_imgs_anterior/act_141.png"],
				   ["./video_imgs_posterior/act_0.png","./video_imgs_posterior/act_35.png","./video_imgs_posterior/act_70.png","./video_imgs_posterior/act_105.png","./video_imgs_posterior/act_141.png"]]

generate_multipanel_image(image_structure,
						  "./activation_image.png")
