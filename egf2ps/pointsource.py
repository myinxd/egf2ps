#!/usr/bin/evn/python3
#
# Copyright (c) 2016 Zhixian MA <zxma_sjtu@qq.com>
# MIT license

"""
The point source class

Parameters
----------
ps: list
    The ps list in which hosts the core, major and min axes and peak.
    | Param     | Comment    |
    | :-------: | ---------  |
    | core_x    | core       |
    | core_y    | core       |
    | axis_maj  | major axis |
    | axis_min  | minor axis |
    | peak      | peak       |

Functions
---------
reg2mat: read region file and transform to mat
mat2reg: save mat as region

"""

# Modules
import numpy as np
import os
import pyregion

# Defination of point source class
class pointsource:

    def __init__(self,core=(0,0),axis=(0,0),peak=0,ang = 0):
        self.core_x,self.core_y = core
        self.axis_maj,self.axis_min = axis
        self.peak = peak
        self.ang = 0

    def get_ps(self):
        """
         Generate the point source list
        """
        ps = [self.core_x,self.core_y,self.axis_maj,self.axis_min,self.ang,self.peak]
        ps = np.array(ps)

        return ps

# Defination of functions
def reg2mat(filename):
    """
    Read region files and transform to matrix,the pyregion module is used.
    """
    # Init
    if os.path.exists(filename):
        pslist = pyregion.open(filename)
    else:
        return 0
    # Split and get the numbers
    NumPS = len(pslist)
    ps = []
    for i in range(NumPS):
        ps.append(pslist[i].coord_list)

    ps = np.array(ps)
    return ps

def mat2reg(ps,outfile,pstype = 'elp'):
    """
    Transform ps mat to region file

    Parameters
    ----------
    ps: np.ndarray
        A two dimensional matrix holds the information of point sources
    outfile: str
        Name of the output file
    pstype: str
        Type of region, can be 'elp','cir','box'
    """

    reg = open(outfile,'w+')
    if pstype is 'elp':
        for i in range(ps.shape[0]):
            ps_str = 'ellipse(' + str(ps[i,0])+','+ str(ps[i,1])+\
                ','+str(ps[i,2])+','+str(ps[i,3])+','+str(ps[i,4])+')\n'
            reg.write(ps_str)
    elif pstype is 'cir':
        for i in range(ps.shape[0]):
            ps_str = 'circle(' + str(ps[i,0])+','+ str(ps[i,1])+','+str(ps[i,2])+')\n'
            reg.write(ps_str)
    else:
        for i in range(ps.shape[0]):
            ps_str = 'box(' + str(ps[i,0])+','+ str(ps[i,1])+','+str(ps[i,2])+','+str(ps[i,3])+',0)\n'
            reg.write(ps_str)



