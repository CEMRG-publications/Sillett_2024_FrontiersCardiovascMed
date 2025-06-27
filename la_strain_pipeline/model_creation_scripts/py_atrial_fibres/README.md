
This is my version of Marina's py_atrial_fibres code. The main thing that I have changed is the automatic landmark generation - to make it more relevant in my case for LA with PVs. 
Also will read in the MV landmark location file - Note: If in the GUI, you have altered the MV landmark location by clicking 'C' and dragging the location it will fail as this code 
will look for pvClipper_${vertexnumber}.vtk (the ${vertexnumber} is the initial point defined on the LA mesh as the center point of the MV sphere). 
