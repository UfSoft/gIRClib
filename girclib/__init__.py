"""
====================
 gEvent IRC Library
====================

gEvent IRC Library

"""

__version__      = '0.1-dev'
__package_name__ = 'gIRClib'
__summary__      = "gEvent IRC Library"
__author__       = 'Pedro Algarvio'
__email__        = 'pedro@algarvio.me'
__license__      = 'BSD'
__url__          = 'https://github.com/s0undt3ch/girclib'
__description__  = __doc__


from gevent import monkey
monkey.patch_socket()
