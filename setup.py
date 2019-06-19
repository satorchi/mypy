#!/usr/bin/env python
'''
$Id: setup.py<mypy>
$auth: Steve Torchinsky <satorchi@apc.in2p3.fr>
$created: Tue 26 Sep 2017 10:11:40 CEST
$license: GPLv3 or later, see https://www.gnu.org/licenses/gpl-3.0.txt

          This is free software: you are free to change and
          redistribute it.  There is NO WARRANTY, to the extent
          permitted by law.

setup for my python packages
'''
import os,sys
from setuptools import setup


DISTNAME         = 'satorchipy'
DESCRIPTION      = "Steve's Python stuff"
AUTHOR           = 'Steve Torchinsky'
AUTHOR_EMAIL     = 'steve@satorchi.net'
MAINTAINER       = 'Steve Torchinsky'
MAINTAINER_EMAIL = 'steve@satorchi.net'
URL              = 'https://github.com/satorchi/mypy'
LICENSE          = 'GPL'
DOWNLOAD_URL     = 'https://github.com/satorchi/mypy'
VERSION          = '1.0'

with open('README.md') as f:
    long_description = f.read()


setup(name=DISTNAME,
      version=VERSION,
      packages=[DISTNAME],
      zip_safe=False,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      download_url=DOWNLOAD_URL,
      long_description=long_description,
      platforms=['GNU/Linux'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Scientific/Engineering']
)
