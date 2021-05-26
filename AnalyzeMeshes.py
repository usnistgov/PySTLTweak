#!/usr/bin/python

import sys
from xml.dom import minidom
import configparser
import os, errno
import math
import numpy
import stl
import glob
import fnmatch
import argparse

class CGloblals(object):
    def __init__(self):
        self.myfilename = os.path.realpath(__file__)
        self.inifilename=self.Path(self.myfilename)+self.Title(self.myfilename)+".ini"
        self.bCenterMesh = False
        self.bZeroMesh = False
        self.bZeroTopMesh=False
        self.bIniCollation=True
        self.bRotate=False
        self.Axes=""
        self.bAppend = False
        self.scale = 1.0

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-v", "--verbose", help="increase output verbosity",
                                 action="store_true")
        self.parser.add_argument("-a", "--append", help="append file info to end of ini file",
                                 action="store_true")

        self.parser.add_argument("-c", "--center", help="center mesh around (0,0,0) origin",
                                 action="store_true")
        self.parser.add_argument("-maxz", "--maxz", help="maximum z at (0,0,0) origin",
                                 action="store_true")
        self.parser.add_argument("-minz", "--minz", help="minimum z at (0,0,0) origin",
                                 action="store_true")
        self.parser.add_argument('-p', action="store", dest="pattern", help="regex pattern for matching file",
                                 default="*.stl")
        self.parser.add_argument('-i', action="store", dest="inputfile", help="input file name")
        self.parser.add_argument('-o', action="store", dest="outputfile", help="output file name")
        self.parser.add_argument('-f', action="store", dest="folder", help="base file folder")
        self.parser.add_argument('-rx', action="store", dest="rotx", type=float, default=0.0,
                                 help="rotation around X angle in degrees")
        self.parser.add_argument('-ry', action="store", dest="roty", type=float, default=0.0,
                                 help="rotation around Y angle in degrees")
        self.parser.add_argument('-rz', action="store", dest="rotz", type=float, default=0.0,
                                 help="rotation around Z angle in degrees")
        self.parser.add_argument('-tx', action="store", dest="transx", type=float, default=0.0,
                                 help="translation along X axis in meters")
        self.parser.add_argument('-ty', action="store", dest="transy", type=float, default=0.0,
                                 help="translation along Y axis in meters")
        self.parser.add_argument('-tz', action="store", dest="transz", type=float, default=0.0,
                                 help="translation along Z axis in meters")
        self.parser.add_argument('-sx', action="store", dest="scalex", type=float, default=1.0,
                                 help="scale X relative to 1")
        self.parser.add_argument('-sy', action="store", dest="scaley", type=float, default=1.0,
                                 help="scale Y relative to 1")
        self.parser.add_argument('-sz', action="store", dest="scalez", type=float, default=1.0,
                                 help="scale Z relative to 1")

        self.parser.add_argument('-s', action="store", dest="scale", type=float, default=1.0,
                                 help="scale XYZ relative to 1")

    def Path(self, filename):
        if  not filename:
            return filename
        return os.path.dirname(filename) + os.path.sep
    def Title(self, filename):
        return os.path.splitext(os.path.basename(filename))[0]

    def NewStlFileName(self, filename,bCentered,bZeroZmin,bZeroTopMesh,bRotate,scale=1.0):
        path=self.Path(filename)
        title=self.Title(filename)
        augment=""
        if bCentered:
            augment=augment + "_Centered"
        if bZeroZmin:
            augment=augment + "_ZeroZmin"
        if bZeroTopMesh:
            augment = augment + "_ZeroZmax"
        if bRotate:
            augment = augment + "_Rotate"+self.Axes
        if (scale!=1.0):
            augment = augment + "_Scaled_"+ str(int(scale)) + "X"
        return path+title+augment+".stl"


    def ParseCommandLine(self):
        args = self.parser.parse_args()

        self.inputfile = args.inputfile
        self.outputfile = args.outputfile

        self.rotx = args.rotx
        self.roty = args.roty
        self.rotz = args.rotz
        self.transx = args.transx
        self.transy = args.transy
        self.transz = args.transz
        self.scalex = args.scalex
        self.scaley = args.scaley
        self.scalez = args.scalez
        self.pattern = args.pattern
        self.bAppend=args.append
        self.scale = args.scale

        if (args.scale != 0):
            self.bScale = True
        if(args.rotx != 0 ):
            self.bRotate=True
            self.Axes=self.Axes+"x"
        if(args.roty != 0 ):
            self.bRotate=True
            self.Axes = self.Axes + "y"
        if(args.rotz != 0 ):
            self.bRotate=True
            self.Axes = self.Axes + "z"

        self.bCenterMesh = args.center
        self.bZeroTopMesh = args.maxz
        self.bZeroMesh = args.minz

        if self.inputfile:
            self.filelist = []
            self.folder = self.Path(self.inputfile)
            self.filelist.append(self.inputfile)
        if args.folder:
            if (not args.folder.endswith(os.path.sep)):
                args.folder = args.folder + os.path.sep
            self.folder = args.folder
            self.filelist = []
            for root, dirnames, filenames in os.walk(self.folder):
                for filename in fnmatch.filter(filenames, '*.stl'):
                    self.filelist.append(os.path.join(root, filename))
            print( self.filelist)



def translate(_solid, step, padding, multiplier, axis):
    if axis == 'x':
        items = [0, 3, 6]
    elif axis == 'y':
        items = [1, 4, 7]
    elif axis == 'z':
        items = [2, 5, 8]
    for p in _solid.points:
        # point items are ((x, y, z), (x, y, z), (x, y, z))
        for i in range(3):
            p[items[i]] += (step * multiplier) + (padding * multiplier)

def zero_zmin_mesh(_solid):
    minx, maxx, miny, maxy, minz, maxz = find_boundingbox(_solid)
    print(math.fabs(minz))
    if(math.fabs(minz) > 0.0):
        translate(_solid, -minz, 0, 1, 'z')

def zero_zmax_mesh(_solid):
    minx, maxx, miny, maxy, minz, maxz = find_boundingbox(_solid)
    print( math.fabs(maxz))
    if(math.fabs(maxz) > 0.0):
        translate(_solid, -maxz, 0, 1, 'z')

# fixme: add amount of rotation
def rotate_mesh(_solid,axes):
    if 'x' in axes:
        _solid.rotate([0.5, 0.0, 0.0], math.radians(Globals.rotx))
    if 'y' in axes:
        _solid.rotate([0.0, 0.5,  0.0], math.radians(Globals.roty))
    if 'z' in axes:
        _solid.rotate([0.0,  0.0, 0.5], math.radians(Globals.rotz))

def scale_mesh(_solid,multiplier):
    items = [0,1,2,3,4, 5,6,7, 8]
    for p in _solid.points:
        # point items are ((x, y, z), (x, y, z), (x, y, z))
        for i in range(9):
            p[items[i]] *=  multiplier

def zero_origin_mesh(_solid):
    minx, maxx, miny, maxy, minz, maxz = find_boundingbox(_solid)
    print("Minx= {0}".format(minx))
    print("Maxx= {0}".format(maxx))
    print("Miny= {0}".format(miny))
    print("Maxy= {0}".format(maxy))
    print("Minz= {0}".format(minz))
    print("Maxz= {0}".format(maxz))
    x=(maxx+minx)/2.
    y=(maxy+miny)/2.
    z=(maxz+minz)/2.
    if(math.fabs(x) >.0000001):
        translate(_solid, -x, 0, 1, 'x')
    if(math.fabs(y) > 0.0000001):
        translate(_solid, -y, 0, 1, 'y')
    if(math.fabs(z) > 0.0000001):
        translate(_solid, -z, 0, 1, 'z')
    minx, maxx, miny, maxy, minz, maxz = find_boundingbox(_solid)
    print("Minx= {0}".format(minx))
    print("Maxx= {0}".format(maxx))
    print("Miny= {0}".format(miny))
    print("Maxy= {0}".format(maxy))
    print("Minz= {0}".format(minz))
    print("Maxz= {0}".format(maxz))


# find the max dimensions, so we can know the bounding box,
# getting the height, width, length (because these are the step size)...
def find_boundingbox(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

#myMesh = stl.Mesh.from_file('/home/isd/michalos/.gazebo/models/gear_support/meshes/large_gear_centered_zge0.stl')


#opens file to log mesh data for every file found as stl
Globals=CGloblals()
Globals.ParseCommandLine()

flags="w"
if Globals.bAppend:
    flags="a"

if Globals.bIniCollation:
    f = open(Globals.inifilename,flags)

for file in Globals.filelist:
    myMesh = stl.Mesh.from_file(file)
    print (file)
    if Globals.bRotate:
        rotate_mesh(myMesh, Globals.Axes)
    if Globals.bCenterMesh:
        zero_origin_mesh(myMesh)
    if Globals.bZeroMesh:
        zero_zmin_mesh(myMesh)
    if Globals.bZeroTopMesh:
        zero_zmax_mesh(myMesh)
    if Globals.bScale:
        scale_mesh(myMesh, Globals.scale)

    # Save file with modifications
    if (Globals.scale!=0) or Globals.bCenterMesh or Globals.bZeroMesh or Globals.bZeroTopMesh or Globals.bRotate:
        myMesh.save(Globals.NewStlFileName(file,Globals.bCenterMesh,
                                           Globals.bZeroMesh,
                                           Globals.bZeroTopMesh,
                                           Globals.bRotate,
                                           Globals.scale
                                           ), mode=stl.Mode.BINARY)

    if Globals.bIniCollation:
        volume, cog, inertia = myMesh.get_mass_properties()
        f.write("[{0}]\n".format(Globals.Title(file)))
        f.write("Path={0}\n".format(file))
        f.write("Volume = {0}\n".format(volume))
        f.write("Position of the center of gravity (COG) = {0}\n".format(cog))
        f.write("Inertia matrix at expressed at the COG\n")
        f.write(" {0}\n".format(inertia[0,:]))
        f.write(" {0}\n".format(inertia[1,:]))
        f.write(" {0}\n".format(inertia[2,:]))

        minx, maxx, miny, maxy, minz, maxz = find_boundingbox(myMesh)
        f.write("x= ({0}, {1})\n".format(minx,maxx))
        f.write("y= ({0}, {1})\n".format(miny,maxy))
        f.write("z= ({0}, {1})\n".format(minz,maxz))

if Globals.bIniCollation:
    f.close()

print ("Done")