# This file is part of Quantum.
#
#    Copyright (c) 2017 and later, Diego Nicolas Bernal-Garcia.
#    All rights reserved.
###############################################################################
"""
This module contains a collection of tensor routines used mainly
to manipulate and construct operators.

Note the functions in these module were inspired by:
QuTip: Quantum Toolbox in Python.
Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
All rights reserved.
"""

__all__ = ['kron_delta']


def kron_delta(i,j):
    """Calculate de kronecker delta of two given indexes
    Parameters
    ----------
    i, j : int
        ''indexes''.
    Returns
    -------
    dij : int, bool
        Kronecker delta.
    """
    i = int(i); j = int(j)
    if i == j:
        return 1
    else:
        return 0
