#!/bin/bash

## Use this script to compute feature tracking

basePath="/media/cs1623/One Touch/Vitaliy"
trackingPath=${basePath}/${formatted_case}/LA/MT/SW-0.0-BE-1e-9

/home/csi20/Software/CemrgApp_v2.1/bin/MLib/register -images ${trackingPath}/imgTimes.lst -parin ${trackingPath}/Final.cfg\
	-dofout ${trackingPath}/tsffd.dof -threads 28 -verbose 3
