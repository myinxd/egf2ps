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
    | axis_x    | axis       |
    | axis_y    | axis       |
    | peak      | peak       |

"""
import numpy as np

# Defination of point source class
class PointSource:

    def __init__(self, core=(0,0), axis=(0.0,0.0), peak=0.0, ang=0.0):
        self.core_x,self.core_y = core
        self.axis_x,self.axis_y = axis
        self.peak = peak
        self.ang = ang
        self._get_foci()

    def get_ps(self):
        """Generate the point source list"""
        ps = [self.core_x,self.core_y,self.axis_x,self.axis_y,self.ang,self.peak]

        return ps

    def _get_foci(self):
        """Get foci of the elliptical point source"""
        # major axis
        if self.axis_x > self.axis_y:
            c = np.sqrt(self.axis_x**2 - self.axis_y**2)
            self.f1 = c*np.array([np.cos(self.ang),np.sin(self.ang)])
            self.f2 = - self.f1
        else:
            c = np.sqrt(self.axis_y**2 - self.axis_x**2)
            self.f1 = c*np.array([-np.sin(self.ang),np.cos(self.ang)])
            self.f2 = -self.f1

    def get_power(self,img_mat):
        """Calculate power and real area"""
        # Init
        rows,cols = img_mat.shape
        area = 0
        power = 0.0
        # Spread
        sp_x = round(self.axis_x)
        sp_y = round(self.axis_y)
        sp = int(max(sp_x,sp_y))
        # calc power
        x = np.arange(-sp,sp+1,1)
        y = np.arange(-sp,sp+1,1)
        for i in x:
            for j in y:
                if ((i+self.core_x-1)>=0 and (i+self.core_x-1)<=cols and
                    (j+self.core_y-1)>=0 and (j+self.core_y-1)<=rows):
                    d = (np.sqrt((i-self.f1[0])**2 + (j-self.f1[1])**2) +
                         np.sqrt((i-self.f2[0])**2+(j-self.f2[1])**2))
                    if d <= 2*sp:
                        area+=1
                        power+=img_mat[j+self.core_y,i+self.core_x]

        return power,area

    def get_snr(self,img_mat):
        """Calculate signal-to-noise ratio"""
        # Init
        rows,cols = img_mat.shape
        # get indices
        sp_x = round(self.axis_x)
        sp_y = round(self.axis_y)
        sp = 2*int(max(sp_x,sp_y))
        # get indices
        x = np.arange(self.core_x-1-sp,self.core_x+sp,1)
        y = np.arange(self.core_y-1-sp,self.core_y+sp,1)
        x_b = np.where(x>=0)[0][0]
        x_e = np.where(x<=cols)[0][-1]
        y_b = np.where(y>=0)[0][0]
        y_e = np.where(y<=rows)[0][-1]
        # get region
        region = img_mat[y[y_b]:y[y_e],x[x_b]:x[x_e]]
        power_ps,area = self.get_power(img_mat)
        # Power of neighbor
        power_nb = np.sum(region)- power_ps
        # Average power of bkg
        bkg_avg =  power_nb/((x[x_e]-x[x_b]+1)*(y[y_e]-y[y_b]+1) - area)
        power_bkg = bkg_avg * area
        # snr
        snr = 20*np.log10(power_ps/power_bkg)

        return snr
