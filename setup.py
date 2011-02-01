#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
"""
    setup.py
    ~~~~~~~~


    :copyright: © 2011 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

from setuptools import setup, find_packages
import ircliblet

setup(name = ircliblet.__package_name__,
      version = ircliblet.__version__,
      author = ircliblet.__author__,
      author_email = ircliblet.__email__,
      url = ircliblet.__url__,
      download_url = 'http://python.org/pypi/%s' % ircliblet.__package_name__,
      description = ircliblet.__summary__,
      long_description = ircliblet.__description__,
      license = ircliblet.__license__,
      platforms = "OS Independent - Anywhere Eventlet is known to run.",
      keywords = "Eventlet IRC Library",
      packages = find_packages(),
      install_requires = [
        "Distribute", "eventlet>=0.9.14", "blinker>=1.1"
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Communications :: Chat :: Internet Relay Chat',
      ]
)
