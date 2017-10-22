#!/usr/bin/env python
# -*- coding: utf-8 -*-



# This file is part of Quantum.
#
#    Copyright (c) 2017, Diego Nicolás Bernal-García
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
"""Quantum: Quantum dynamics solver

Quantum is open-source software for calculating the dynamics of quantum systems.
The Quantum library is strongly based and inspired by QuTip: Quantum Toolbox in Python.
Besides, it takes advantange of the Numpy, Scipy, and Cython packages, as well as Matplotlib.
"""

# import statements
import os
import sys
from setuptools import setup


DOCLINES = __doc__.split('\n')

CLASSIFIERS = """\
Development Status :: 0 - Beta
Intended Audience :: Science/Research
License :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Operating System :: Linux
"""


# all information about QuTiP goes here
MAJOR = 0
MINOR = 3
MICRO = 2
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
REQUIRES = ['numpy (>=1.8)', 'scipy (>=0.15)', 'cython (>=0.21)', 'qutip (>=4.0)']
INSTALL_REQUIRES = ['numpy>=1.8', 'scipy>=0.15', 'cython>=0.21', 'qutip>=4.0']
PACKAGES = ['quantum', 'quantum/atom_cavity', 'quantum/coupled_cavities']
NAME = "quantum"
AUTHOR = "Diego Nicolas Bernal-Garcia"
AUTHOR_EMAIL = "dnbernalg@unal.edu.co"
LICENSE = "MIT"
KEYWORDS = "quantum dynamics solver"
DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])
CLASSIFIERS = [_f for _f in CLASSIFIERS.split('\n') if _f]
PLATFORMS = ["Linux"]


# # always rewrite _version
# if os.path.exists('qutip/version.py'):
#     os.remove('qutip/version.py')
#
# write_version_py()


# Setup commands go here
setup(
    name = NAME,
    version = VERSION,
    packages = PACKAGES,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    license = LICENSE,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    keywords = KEYWORDS,
    classifiers = CLASSIFIERS,
    platforms = PLATFORMS,
    requires = REQUIRES,
    zip_safe = False,
    install_requires=INSTALL_REQUIRES,
)
