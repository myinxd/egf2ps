# Copyright (c) Zhixian MA <zxma_sjtu@qq.com>
# MIT license

"""
Some I/O and processing tools are provied in this utils module.

Methods
-------
reg2mat:
    Read point sources list from the region file, and translate it into np.ndarray
mat2reg:
    Print PS list matrix to ds9 region files
compare:
    Compare detected PS with the references
img2mat:
    read image from the provided path
	
References
------------
[1] scipy.ndimage
	  http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.
	  imread.html#scipy.ndimage.imread
"""

import os
import sys
import numpy as np
import pyregion
from astropy.io import fits
from scipy.ndimage import imread

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
    num_ps = len(pslist)
    ps = []
    for i in range(num_ps):
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

def compare(ps,ps_ref):
    """
    Compare detected ps with the real one or reference

    Parameters
    ----------
    ps: np.ndarray
        Detected point source list
    ps_ref: np.ndarray
        Referenced point source list

    Returns
    -------
    num_same: int
        Number of same PS
    cord_x,cord_y: list
        Coordinates of the same PS
    err_rate: float
        Error rate
    """

    # Init
    num_same = 0
    err_rate = 0.0
    cord_x = []
    cord_y = []

    # Extract coordinates of ps and ps_ref
    ps_x = list(ps[:,1])
    ps_y = list(ps[:,2])
    ps_ref_x = list(ps_ref[:,1])
    ps_ref_y = list(ps_ref[:,2])

    # Compare
    i = 1
    while  i <= len(ps_ref_x):
        j = 1
        while j <= len(ps_ref_x):
            d = np.sqrt((ps_x[j]-ps_ref_x[i])**2 + (ps_y[j]-ps_ref_y[i])**2)
            if d <= 5:
                num_same += 1
                cord_x.append(ps_x[j])
                cord_y.append(ps_y[j])
                ps_x.remove(ps_x[j])
                ps_y.remove(ps_y[j])
                break
            j += 1
        i += 1

    len_ps = ps.shape[0]
    err_rate = (abs(len_ps - len(ps_ref_x)) + len(ps_ref_x) - num_same)/ len(ps_ref_x)

    return num_same,err_rate,cord_x,cord_y

def img2mat(imgpath):
    """
    Load image

    Parameter
    ---------
    imgpath: str
        path of the image,the image can be fits or other image type files
    """
    # Judge type of path
    postfix = os.path.splitext(imgpath)[-1]
    if postfix == '.fits':
        try:
            img = fits.open(imgpath)
        except IOError:
            sys.exit("The image can't be loaded.")
        img_mat = img[0].data
    else:
        try:
            img_mat = imread(imgpath,flattern=True,mode='L')
        except IOError:
            sys.exit("The image can't be loaded.")
        img_mat = np.array(img_mat,dtype=float)/255

    return img_mat