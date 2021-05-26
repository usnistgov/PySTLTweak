#!/bin/bash


#python AnalyzeMeshes.py -c -z -f "/home/michalos/src/gz/models/

python AnalyzeMeshes.py -i "$HOME/src/robot-agility/gz/models/gear_support/meshes/new_big_gear_Rotatex_Centered_ZeroZminNoDupFaces.stl"

#python AnalyzeMeshes.py -i "$HOME/src/robot-agility/gz/models/gear_support/meshes/new_small_gear_Rotatex_Centered_ZeroZmin.stl"
#python AnalyzeMeshes.py -i "$HOME/src/robot-agility/gz/models/gear_support/meshes/solid_medium_gear2.stl"


notify-send "AnalyzeMeshes Done"


