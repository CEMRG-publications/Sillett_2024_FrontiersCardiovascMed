import numpy as np
import os
import natsort

def compute_tat(act_times):

	return np.max(act_times)-np.min(act_times)

def compute_dispersion(act_times):

	return np.std(act_times)

def compute_output_folder(folder,
						  output_file,
						  sorted=True,
						  activation_files=None):
	
	files = os.listdir(folder)

	if sorted: 
		files = natsort.natsorted(files)

	if activation_files is None:
		activation_file_list = []
		for f in files:
			if f[-4:] == '.dat':
				activation_file_list.append(folder+'/'+f)

		print('Found '+str(len(activation_file_list))+' activation files to analyse.')

	else:
		activation_file_list = []
		for at in activation_files:
			act_file = results_folder+'/'+at

			if at in files:
				print('Found activation file '+at+'.')
				activation_file_list.append(act_file)
			else:
				print('You asked to compute output of file '+at+' but it does not exists.')

	response = np.zeros((len(activation_file_list),2))
	for i,at in enumerate(activation_file_list):
		act_times = np.loadtxt(at,dtype=float)

		response[i,0] = compute_tat(act_times)
		response[i,1] = compute_dispersion(act_times)

	print('Saving results in '+output_file+'.')
	np.savetxt(output_file,response,fmt="%g")

def compute_conduction_velocity(meshname,
							    activation_file):

	
	cmd = "meshtool extract gradient "
	cmd += "-msh="+meshname+" "
	cmd += "-idat "+activation_file+" "
	cmd += "-odat "+activation_file[:-4]+" "
	cmd += "-mode=0 "

	os.system(cmd)

	gradient = np.loadtxt(activation_file[:-4]+".gradmag.dat",dtype=float)

	conduction_velocity = 1./gradient*0.001

	np.savetxt(activation_file[:-4]+"_cv.dat",conduction_velocity,fmt="%g")