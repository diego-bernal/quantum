#!/usr/bin/env python
"""Quantum: Quantum dynamics solver

Quantum is open-source software for simulating the dynamics of closed and open
quantum systems. The Quantum library uses the excellent Numpy, Scipy, and
Cython packages as numerical backend, and graphical output is provided by
Matplotlib. Quantum aims to provide user-friendly and efficient numerical
simulations of a wide variety of quantum mechanical problems, including those
with Hamiltonians and/or collapse operators with arbitrary time-dependence,
commonly found in a wide range of physics applications. Quantum is freely
available for use and/or modification, and it can be used on Linux.
Being free of any licensing fees, Quantum is ideal for exploring quantum
mechanics in research as well as in the classroom.

This library was inspired by:
QuTip: Quantum Toolbox in Python.
Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
All rights reserved.
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
MICRO = 0
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
