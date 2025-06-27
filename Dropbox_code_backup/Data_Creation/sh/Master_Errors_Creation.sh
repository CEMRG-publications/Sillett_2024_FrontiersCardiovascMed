#!/bin/bash

Case=17

## Master script outlining steps to get numeric errors

Data_Analysis_Path=/home/csi20local/Projects/LA_Tracking/Data_Analysis

## Calculate ASD 
## OUTPUT: normal-distance.txt
$Data_Analysis_Path/NormalDistanceResults.sh $Case 

## Calculate DHD
## OUTPUT: hausdorff-distance.txt
$Data_Analysis_Path/HausdorffDistanceResults.sh $Case

## Calculate Unclipped Dice
## OUTPUT: dice.txt
$Data_Analysis_Path/DiceResults.sh $Case

## Calculate Clipped Dice
## OUTPUT: dice-PVeinsCropped.txt
$Data_Analysis_Path/DiceCropResults.sh $Case

## Calculate PV Absolute Distance errors [mm]
## OUTPUT: pC{Num}-distance.txt
$Data_Analysis_Path/SinglePV-DistLoop.sh $Case

## Calculate PV-PV Dist Percentage errors
## OUTPUT: pC{Num}-pC{Num}-distance.txt
$Data_Analysis_Path/PV-PV-DistLoop.sh $Case

## WIP: MV Dist Errors