"""
Elliptical Gaussian filters to detect point sources in X-ray astronomical images.

Copyright (c) 2016 Zhixian MA <zxma_sjtu@qq.com>
MIT license
"""

# Arguments for setup()
__pkgname__ = "egf2ps"
__version__ = "0.0.1"
__author__ = "Zhixian MA"
__author_email__ = "zxma_sjtu@qq.com"
__license__ = "MIT"
__keywords__ = "point_source filter reognition"
__copyright = "Copyright (c) 2016 Zhixian MA"
__url__ = "https://github.com/myinxd/egf2ps"
__description__ = ("Elliptical Gaussian filters to detect point source in X-ray astronomical images")

# Set logging handle
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
