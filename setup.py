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
import girclib

setup(name = girclib.__package_name__,
      version = girclib.__version__,
      author = girclib.__author__,
      author_email = girclib.__email__,
      url = girclib.__url__,
      download_url = 'http://python.org/pypi/%s' % girclib.__package_name__,
      description = girclib.__summary__,
      long_description = girclib.__description__,
      license = girclib.__license__,
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
