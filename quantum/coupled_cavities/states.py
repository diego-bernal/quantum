# This file is part of Quantum.
#
#    Copyright (c) 2017 and later, Diego Nicolas Bernal-Garcia.
#    All rights reserved.
###############################################################################
"""
This module contains the functions necessary to get the states basis and consequent
arrays.

Note the functions in these module were inspired by:
QuTip: Quantum Toolbox in Python.
"""

__all__ = ['states', 'elements', 'kets']


import numpy as np
from qutip.states import basis

def states(N):
    """Generates an array with the states for the current problem.

    Parameters
    ----------
    N : int
        Maximum excitation manifold.

    Returns
    -------
    states : array
    """
    s = []
    for n in range(N+1):
        for j in range(n+1):
            for beta in range(2):
                for i in range(n+1):
                    for alpha in range(2):
                        if (alpha+i+beta+j==n):
                            s.append((alpha, i, beta, j))
    return np.array(s)

# For Px truncation!
# if (alpha+i+beta+j==n) and not ((n==N and (alpha==0 or beta==0))
# or  (n==N-1 and (alpha==0 and beta==0))):

def elements(s):
    """Generates an array with the indexes of the elements of the density matrix.

    Parameters
    ----------
    s : States array
        States in Hilbert space.

    Returns
    -------
    elements : array
        Indexes of the density matrix elements.
    """
    nstates = len(s)
    elements = []
    for i in range(nstates):
        for j in range(nstates):
            elements.append((s[i,0], s[i,1], s[i,2], s[i,3], s[j,0], s[j,1],
            s[j,2], s[j,3]))
    return np.array(elements)


def kets(s):
    """Generates a list of column vectors that corresponds to the states in
    Hilbert space.

    Parameters
    ----------
    s : States array
        States in Hilbert space.

    Returns
    -------
    state : array of  qobj column_vectors
        column_vector representing the requested number state ``|n>``.
    """
    N = len(s)
    kets = []
    for n in range(N):
        kets.append(basis(N,n))
    return np.array(kets)
