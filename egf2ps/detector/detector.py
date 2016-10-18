# Copyright (c) 2016 Zhixian MA <zxma_sjtu@qq.com>
# MIT license

"""
A class namely Detector is designed to detect and extract results

Methods
-------

"""

import os
import sys
import numpy as np

from ..utils import utils
from ..basiclass import PointSource
from ..basiclass import EGFilter
from ..basiclass import PeakDetector

class Detector:
    def __init__(self,Configs):
        self.Configs = Configs
        self._get_configs()

    def _get_configs(self):
        """Get configurations from configs"""
        # Input
        self.imgpath = self.Configs.getn_value('input/imgpath')
        self.refpath = self.COnfigs.getn_value('input/refpath')
        # Filters
        scale_type = self.Configs.getn_value('filter/scale_type')
        if scale_type == 'custom':
            self.scale_x = self.Configs.getn_value('filter/scale_x')
            self.scale_y = self.Configs.getn_value('filter/scale_y')
        elif scale_type == 'calcrange':
            start = self.Configs.getn_value('filter/scale_start')
            stop = self.Configs.getn_value('filter/scale_stop')
            step = self.Configs.getn_value('filter/scale_step')
            scale = np.arange(start,stop+1,step)
            self.scale_x = 2 ** scale
            self.scale_y = 2 ** scale
        else:
            print('Wrong option,the default will be set.')
            self.scale_x = [4,8]
            self.scale_y = [4,8]
        # variances
        sigma_type = self.Configs.getn_value('filter/sigma_type')
        if sigma_type == 'custom':
            self.sigma_x = self.Configs.getn_value('filter/sigma_x')
            self.sigma_y = self.Configs.getn_value('filter/sigma_y')
        elif sigma_type == 'calcrange':
            start = self.Configs.getn_value('filter/sigma_start')
            stop = self.Configs.getn_value('filter/sigma_stop')
            step = self.Configs.getn_value('filter/sigma_step')
            sigma = np.arange(start,stop+1,step)
            self.sigma_x = 2 ** sigma
            self.sigma_y = 2 ** sigma
        else:
            print('Wrong option,the default will be set.')
            self.sigma_x = [4,8]
            self.sigma_y = [4,8]
        # Angle
        angle_step = self.Configs.getn_value('filter/angle_step')
        self.angle = np.array(0,2*np.pi,angle_step)

        # Peaks
        self.threshold = self.Configs.getn_value('peaks/threshold')
        
        # Snr
        self.snrthrs = self.Configs.getn_value('snr/threshold')
        
        # Output
        self.dirname = self.Configs.getn_value('output/dirname')
        self.save = self.Configs.getn_value('output/save')

    def get_potential(self):
        """Detect and get potential point sources """
        # Init
        pd = PeakDetector(self.Configs)
        for s in self.scale_x:
            for var_x in self.sigma_x:
                for var_y in self.sigma_y:
                    for ang in self.angle:
                        egf = EGFilter(scale=(s,s),sigma=(var_x,var_y),angle=ang)
                        pd.egfilter = egf
                        if 'pot_list' not in locals().keys():       
                            pot_list = pd.get_pslist()
                        else:
                            pot_list = np.row_stack((pot_list,pd.get_pslist()))
      
        return pot_list
        
    def get_final(self):
        """Discard false detections and clustering ps"""
        # Init
        pot_list = self.get_potential()
        snr_list = pot_list[:,-1]
        # Normalize snr and discard false
        max_snr = snr_list.max()
        min_snr = snr_list.min()
        snr_list = (snr_list - min_snr)/(max_snr-min_snr)
        # Discard
        snr_idx = np.where(snr_list >= self.snrthrs)
        pslist_snr = pot_list[:,snr_idx]

        # Clustering
        pslist = utils.cluster(pslist_snr)
        
        if self.save:
            filepath = os.path.join(self.dirname,'pslist.reg')
            utils.mat2reg(pslist,filepath)
        
        return pslist
    
    def get_performance(self,pslist):
        """Compare detected pslist with the reference"""
        reflist = utils.reg2mat(self.refpath)
        # Compare
        num_same,err_rate,cord_x,cord_y = utils.compare(pslist,reflist)
        # Print result
        print("==========Performance=======")
        print("Error rate: %f" % err_rate)
        print("Numer of same: %d" % num_same)