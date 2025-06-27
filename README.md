# Sillett_Frontiers_2024

This repo contains code used for the following publication:

Sillett C , Razeghi O , Lee AWC , Solis Lemus JA , Roney C , Mannina C et al. A three-dimensional left atrial motion
estimation from retrospective gated computed tomography: application in heart failure patients with atrial fibrillation. Front
Cardiovasc Med 2024;11:1359715.

Link: https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2024.1359715/full

## Notes:
The LA motion tracking and strain calculation pipeline can be found in /la_strain_pipeline/, which have previously been integrated into CemrgApp by Bei.
The main pipeline scripts are la_strain_pipeline/model_creation_scripts/py/uac_pipeline.py, which describes the main steps for creating LA models, and la_strain_pipeline/img_analysis_scripts/py/la_motion_tracking_pipeline.py, which details the steps for applying the motion tracking and calculating strains. These would be useful to anyone interested in the pipeline. Virtual environments are listed in /venvs/ and parameter files are listed in /param_files/

## iPython Notebooks
A lot of exploratory data analysis. The most pertinent files that detail analysis for the publication have are name P1_*.ipynb.

## TSFFD
Latest code used for analysing motion tracking data can be found here.