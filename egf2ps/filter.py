#!/usr/bin/env python3
#
# Copyright (c) 2016 Zhixian MA <zxma_sjtu@qq.com>
# MIT liscense

"""
The elliptical Gaussian filter class

Parameters
----------
scale_x,scale_y: float
    Scale of the filter, x and y are the two orthogonal direction
sigma_x,sigma_y: float
    Variances of the filter, x and y direction
raidus_x,radius_y: float
    The FHTM radii of the two dimensional filter
psf: np.ndarray
    The two dimensional mat

Functions
---------
get_radius: calculate the FHTM radius

get_filter: gen the filter
"""

# Modules
import numpy as np
# import astropy
# custom designed

# Defination of class
class filter:
    # Inital of parameters
    scale_x = 0
    scale_y = 0
    sigma_x = 0
    sigma_y = 0
    radius_x = 0
    radiux_y = 0

    # __init__
    def __init__(self,scale = (16,16),sigma = (1,2)):
        self.scale_x,self.scale_y = scale
        self.sigma_x,self.sigma_y = sigma

    def get_radius(self):
        """
        Calculate the radii
        """
        self.radius_x = np.sqrt(2*np.log(10))*self.sigma_x
        self.radius_y = np.sqrt(2*np.log(10))*self.sigma_y

    def get_filter(self):
        """
        Generate the filter
        """
        # Init
        psf = np.zeros((self.scale_x,self.scale_y))

        # Fill with Gaussian distribution
        half_x = np.round(self.scale_x)
        half_y = np.round(self.scale_y)
        # coordinates
        x = np.arange(-half_x,half_x+1,1)
        y = np.arange(-half_y,half_y+1,1)
        for i in range(len(x)):
            for j in range((len(y))):
                psf[i,j] = 1 * np.exp(x[i]/(self.sigma_x**2)+
                            y[j]/self.sigma_y**2 )

        return psf


