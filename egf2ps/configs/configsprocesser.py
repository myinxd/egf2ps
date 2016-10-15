# Copyright (c) Zhixian MA <zxma_sjtu@qq.com>
# MIT license
#
# References:
# [1] https://configobj.readthedocs.io/en/latest/configobj.html
# [2] heepts://github.com/liweitianux/fg21sim/fg21sim/configs

"""
A class to process and read configurations.
"""

import os
from functools import reduce

from configobj import ConfigObj, ConfigObjError, flatten_errors
from validate import Validator

from errors import ConfigError

class ConfigsProcesser:
    """Process on the configurations"""
    def __init__(self,configs=None):
        # load configuration specification
        confspec_path = os.path.join(os.path.dirname(__file__),
                                     "confspec.conf")
        # Get specification
        self._configspec = ConfigObj(confspec_path,interpolation=False,
                                     list_values=True,_inspec=True)
        # Default configs
        configs_default = ConfigObj(interpolation=False,list_values=True,
                                  configspec=self._configspec)
        # Configs
        self._configs = self._validate(configs_default)
        # Read custom configs
        if configs:
            self.read_configs(configs)

    def read_configs(self,configs):
        """
        Read configuration file.

        Parameters
        ----------
        configs: str
            Filepath of the config file, for example, '../data/test.conf'

        NOTE
        ----
        The configuration file can be loaded *only once*.
        """
        if hasattr(self,"configs"):
            raise ConfigError("The configurations have been already loaded.")

        try:
            newconfigs = ConfigObj(configs,interpolation=False,
                                      configspec=self._configspec)
        except ConfigObjError as e:
            raise ConfigError(e)
        # Validate
        self._configs = self._validate(newconfigs)


    def _validate(self,configs):
        """
        Validate whether the configs match to the configuration speciation.
        If there exist mistakes, the `ConfigError` shall be raised with
        details.

        Parameters
        ----------
        configs: ConfigObj
            Configuration object
        """
        config_val = Validator()
        try:
            val_result = configs.validate(config_val,preserve_errors=True)
        except ConfigObjError as e:
            raise ConfigError(e.message)
        if val_result is not True:
            error_msg = ""
            for (sec,key,value) in flatten_errors(configs,val_result):
                if key is not None:
                    if value is False:
                        msg = 'key "%s" in section "%s" is missing.'
                        msg = msg % (key, ", ".join(sec))
                    else:
                        msg = 'key "%s" in section "%s" failed validation: %s'
                        msg = msg % (key, ", ".join(sec),value)
                else:
                    msg = 'section "%s" is missing' % ".".join(sec)
                error_msg += msg + "\n"
            raise ConfigError(error_msg)
        return configs

    def get_value(self,key,fallback=None):
        """Get config value by key."""
        return self._config.get(key,fallback)

    def getn_value(self,key,sep="/"):
        """
        Get config value from the nested dictionary configs using a list of
        keys or a "sep"-separated keys strings.

        Parameters
        ----------
        key: str / list[str]
            A string separated by a specific charater (e.g., '/') or a key
            list, which specifies the target item in the configs.

        sep: str
            The separater to be used to split key, if it is a string.

        References
        ----------
        - https://github.com/liweitianux/fg21sim/fg21sim/configs/manager.py
        """
        if isinstance(key,str):
            key = key.split(sep)
        return reduce(dict.get,key,self._configs)
