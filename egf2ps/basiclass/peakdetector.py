# Copyright (c) 2016 Zhixian MA <zxma_sjtu@qq.com>
# MIT license

"""
Design of a class namely PeakDetector

Parameters
----------
img_mat: np.ndarray
    Two dimensional image matrix
egfilter:EGFilter object
    The elliptical Gaussian filter

Methods
-------
smooth:
    Convolve the img_mat with egfilter
locate_peaks:
    Detect peaks and output peaklist
save_peaks:
    Save peaks to csv files

References
----------
[1] Multidimensioanl convolution
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.
    convolve.html#scipy.ndimage.convolve
[2] Scipy.ndimage.image
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.imread.
    html#scipy.ndimage.imread
"""

from scipy.ndimage import convolve
import numpy as np

from .pointsource import PointSource
from ..utils import utils

# Defination of class
class PeakDetector():
    def __init__(self,Configs,egfilter):
        """Initialization of parameters"""
        self.Configs = Configs
        self.egfilter = egfilter
        self.neighbors = max(self.egfilter.scale_x,self.egfilter.scale_y)
        self.peaklist = []
        self._get_configs()
        self._read_image()
        self.smooth()

    def _get_configs(self):
        """Get configurations from the Configs"""
        self.imgpath = self.Configs.getn_value("input/imgpath")
        self.threshold = self.Configs.getn_value("peaks/threshold")

    def _read_image(self):
        """
        Read image from provided imgpath, the type of image shall be judged.
        The tool img2mat in utils is utlized.
        """
        imgmat = utils.img2mat(self.imgpath)
        self.imgmat = imgmat

    def smooth(self):
        """
        Smooth the image to improve significant of the point sources with
        respect to the parameters of the egfilter.
        """
        psf = self.egfilter.get_filter()
        # Convolve
        imgsmooth = convolve(self.imgmat,psf,mode='constant',cval=0.0)
        self.imgsmooth = imgsmooth

    def locate_peaks(self):
        """Locate peaks with respect to the threshold"""
        # Init
        peaks = []
        cord_x = []
        cord_y = []
        rows,cols = self.imgmat.shape
        # Normalize
        max_value = self.imgmat.max()
        min_value = self.imgmat.min()
        imgnorm = (self.imgmat - min_value)/(max_value-min_value)
        self.imgnorm = imgnorm.copy()
        # Find peaks
        flag = 1
        while flag == 1:
            peak_max = imgnorm.max()
            if peak_max >= self.threshold:
                peak_y,peak_x = np.where(imgnorm==peak_max)
                print(peak_y)
                for i in range(len(peak_x)):
                    # Judge and fill
                    mask_x = np.arange(peak_x[i]-self.neighbors,peak_x[i]+self.neighbors+1,1)
                    mask_y = np.arange(peak_y[i]-1-self.neighbors,peak_y[i]+self.neighbors+1,1)
                    x_b = np.where(mask_x>=0)[0][0]
                    x_e = np.where(mask_x<=cols)[0][-1]
                    y_b = np.where(mask_y>=0)[0][0]
                    y_e = np.where(mask_y<=rows)[0][-1]
                    imgnorm[mask_y[y_b]:mask_y[y_e],mask_x[x_b]:mask_x[x_e]] *= 0.0
                    # append
                    peaks.append(peak_max)
                    cord_x.append(peak_x[i])
                    cord_y.append(peak_y[i])
            else:
                flag = 0

        self.peaklist = [peaks,cord_x,cord_y]


    def get_pslist(self):
        """Get potential point source list
        """
        # Init
        pslist = []
        numps = len(self.peaklist[0])
        # Gen pslist
        radius_x = self.egfilter.radius_x
        radius_y = self.egfilter.radius_y
        angle = self.egfilter.angle
        for i in range(numps):
            ps = PointSource(core=(self.peaklist[1][i],self.peaklist[2][i]),
                             axis=(radius_x,radius_y),peak=self.peaklist[0][i],
                            ang = angle)
            snr = ps.get_snr(self.imgmat)

            ps_temp = ps.get_ps()
            ps_temp.append(snr)
            pslist.append(ps_temp)


        return np.array(pslist)
