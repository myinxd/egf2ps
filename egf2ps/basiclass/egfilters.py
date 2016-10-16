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
class EGFilter:
    # __init__
    def __init__(self,scale = (8,8),sigma = (1,2),angle = 0):
        self.scale_x,self.scale_y = scale
        self.sigma_x,self.sigma_y = sigma
        self.angle = angle
        self._get_radius()

    def _get_radius(self):
        """
        Calculate the radii
        """
        self.radius_x = np.sqrt(2*np.log(10))*self.sigma_x
        self.radius_y = np.sqrt(2*np.log(10))*self.sigma_y

    def get_filter(self):
        """
        Generate the filter

        Reference
        ---------
        [1] Gaussian function
            https://en.wikipedia.org/wiki/Gaussian_function
        """
        # Init
        psf = np.zeros((self.scale_x+1,self.scale_y+1))

        # Fill with Gaussian distribution
        half_x = int(np.round(self.scale_x/2))
        half_y = int(np.round(self.scale_y/2))
        # coordinates
        x = np.arange(-half_x,half_x+1,1)
        y = np.arange(-half_y,half_y+1,1)
        # Grid
        [X,Y] = np.meshgrid(x,y)
        # Get a,b,c
        a = (np.cos(self.angle)**2/(2*self.sigma_x**2) +
             np.sin(self.angle)**2/(2*self.sigma_y**2))
        b = (-np.sin(2*self.angle)**2/(4*self.sigma_x**2) -
             np.cos(2*self.angle)**2/(4*self.sigma_y**2))
        c = (np.sin(self.angle)**2/(2*self.sigma_x**2) +
             np.cos(self.angle)**2/(2*self.sigma_y**2))

        # Get psf
        A = 1 # amplitude
        psf = A * np.exp(-(a*(X**2)-2*b*X*Y+c*(Y**2)))

        return psf


