# This file is part of Quantum.
#
#    Copyright (c) 2017 and later, Diego Nicolas Bernal-Garcia.
#    All rights reserved.
###############################################################################
"""
Command line output of information on QuTiP and dependencies.

Note the functions in these module were inspired by:
QuTip: Quantum Toolbox in Python.
Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
All rights reserved.
"""

__all__ = ['about']

import sys
import os
import platform
import numpy
import scipy
import inspect
from qutip.utilities import _blas_info
import qutip.settings
from qutip.hardware_info import hardware_info
from quantum.version import __version__


def about():
    """
    About box for Quantum. Gives version numbers for
    Quantum, QuTiP, NumPy, SciPy, Cython, and MatPlotLib.
    """
    print("")
    print("Quantum: Quantum dynamics solver")
    print("Copyright (c) 2017 and later.")
    print(("D. N. Bernal-Garcia"))
    print("")
    print("Quantum Version:    %s" % __version__)
    print("QuTiP Version:      %s" % qutip.__version__)
    print("Numpy Version:      %s" % numpy.__version__)
    print("Scipy Version:      %s" % scipy.__version__)
    try:
        import Cython
        cython_ver = Cython.__version__
    except:
        cython_ver = 'None'
    print("Cython Version:     %s" % cython_ver)
    try:
        import matplotlib
        matplotlib_ver = matplotlib.__version__
    except:
        matplotlib_ver = 'None'
    print("Matplotlib Version: %s" % matplotlib_ver)
    print("Python Version:     %d.%d.%d" % sys.version_info[0:3])
    print("Number of CPUs:     %s" % hardware_info()['cpus'])
    print("BLAS Info:          %s" % _blas_info())
    print("OPENMP Installed:   %s" % str(qutip.settings.has_openmp))
    print("INTEL MKL Ext:      %s" % str(qutip.settings.has_mkl))
    print("Platform Info:      %s (%s)" % (platform.system(),
                                           platform.machine()))
    #quantum_install_path = os.path.dirname(inspect.getsourcefile(quantum))
    #print("Installation path:  %s" % quantum_install_path)
    print("")

if __name__ == "__main__":
    about()
