#!/bin/bash

Case=17

## Master script outlining steps for creating data needed for error calculations

## At this stage, have deformation fields and segmentations, meshes

Data_Creation_Path=~/Projects/LA_Tracking/Data_Creation

## Deform Mesh for ASD and DHD Errors
$Data_Creation_Path/Deform_Mesh.sh $Case

## Deform Unclipped segmentation for unclipped Dice Errors
$Data_Creation_Path/DeformSeg.sh $Case

## Deform Clipped segmentation for clipped Dice Errors
$Data_Creation_Path/Deform-ClippedSegmentation.sh $Case

## Post-process PV Clippers

## Transform Prod Cutter
$Data_Creation_Path/Transform_RPIImages_ProdCutter_Loop.sh $Case
## Clean Prod Cutter
$Data_Creation_Path/Clean_ProdCutters_Loop.sh $Case

## Deform PV Clippers for PV local errors
$Data_Creation_Path/Deform-ProdCutter.sh $Case

## WIP: MV local Errors