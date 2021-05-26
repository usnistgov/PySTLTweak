

INSTALLATION
Install jetbrains pycharm (or Python IDE of your choice)
Set python interpreter:  add 3.7 so that its part of Pycharm NOT Windows
https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#interpreter

ImportError: No module named numpy-stl
> pip install numpy-stl
This is the major STL mesh analysis library.




Setting command line args: https://www.askpython.com/python/python-command-line-arguments
-f "C:\Users\michalos\Documents\agilityperformancemetrics\TaskBoard\BinPicking\Binpickingtaskboard-pegarray1-1.STL"

In the folder PyAnalyzeMeshes is a pythhon script to analyze and make minor changes to STL meshes. It is based on the python library stl.Mesh (https://pypi.python.org/pypi/numpy-stl/1.3.5). Instructions for installing it are there.


 It will automatically generate a mesh analysis report containing volume, COG, Inertial Frame, and min/max xyz. For gears I tried to center and translate the mesh so that the minimum z is 0, and when this is done it automatically generates a new file name with "_Centered"or "_ZeroZmin" or "_ZeroZmax" or "_Rotate" axes appended to original file name.
 


AnalyzeMeshes.py use stl-mesh python library to 

usage: AnalyzeMeshes.py [-h] [-v] [-c] [-maxz] [-minz] [-p PATTERN]
                        [-i INPUTFILE] [-o OUTPUTFILE] [-f FOLDER] [-rx ROTX]
                        [-ry ROTY] [-rz ROTZ] [-tx TRANSX] [-ty TRANSY]
                        [-tz TRANSZ] [-sx SCALEX] [-sy SCALEY] [-sz SCALEZ]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
  -c, --center   center mesh around (0,0,0) origin
  -maxz, --maxz  maximum z at (0,0,0) origin
  -minz, --minz  minimum z at (0,0,0) origin
  -p PATTERN     regex pattern for matching file
  -i INPUTFILE   input file name
  -o OUTPUTFILE  output file name
  -f FOLDER      base file folder
  -rx ROTX       rotation around X angle in degrees
  -ry ROTY       rotation around Y angle in degrees
  -rz ROTZ       rotation around Z angle in degrees
  -tx TRANSX     translation along X axis in meters
  -ty TRANSY     translation along Y axis in meters
  -tz TRANSZ     translation along Z axis in meters
  -sx SCALEX     scale X relative to 1
  -sy SCALEY     scale Y relative to 1
  -sz SCALEZ     scale Z relative to 1
 
Example use of  AnalyzeMeshes.py
python AnalyzeMeshes.py -c -minz -i "/home/isd/michalos/src/robot-agility/gz/models/gear_support/meshes/newKitTray_1Large_2Medium.stl"

 
Example of mesh analysis output stored in AnalyzeMeshes.ini

[MOTOMAN_BASE]
Path=/home/isd/michalos/.gazebo/models/motoman_sia20d_support/meshes/sia20d/visual/MOTOMAN_BASE.stl
Volume = 0.0125931014935
Position of the center of gravity (COG) = [-0.05163974 -0.00045489  0.07095483]
Inertia matrix at expressed at the COG
 [ 9.96199282e-05 -4.52000122e-07  1.60925900e-05]
 [-4.52000122e-07  1.35525559e-04  6.60169707e-09]
 [1.60925900e-05 6.60169707e-09 1.85722231e-04]
x= (-0.20000000298, 0.143000304699)
y= (-0.143000006676, 0.140000000596)
z= (0.0, 0.17499999702)

and more ini sections based on number of file titles. So each section corresponds to a file title found in a folder or the filename title.


