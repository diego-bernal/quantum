# This file is part of Quantum.
#
#    Copyright (c) 2017 and later, Diego Nicolas Bernal-Garcia.
#    All rights reserved.
###############################################################################
"""
This module contains a collection of functions used to construct the fundamental
quantum optics operators.

Note the functions in these module were inspired by:
QuTip: Quantum Toolbox in Python.
Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
All rights reserved.
"""

__all__ = ['destroy_a', 'destroy_x', 'create_a', 'create_x', 'num_a', 'num_x']

import numpy as np
import scipy.sparse as sp
from qutip.qobj import Qobj
from quantum.tensor import kron_delta


def destroy_a(states):
    """
    Destruction (lowering) operator for photonic excitations.

    Parameters
    ----------
    states : list/array
    List of states of the Hilbert space.

    Returns
    -------
    oper : qobj
        Qobj for destruction operator for photonic excitations.
    """
    nstates = len(states)
    a = np.eye(nstates)
    for i in range(nstates):
        for j in range(nstates):
            a[i, j] = _destroy_photons(states[i, 0], states[i, 1], states[j, 0],
            states[j, 1])
    return Qobj(sp.csr_matrix(a, dtype=complex), isherm=False)



def destroy_x(states):
    """
    Destruction (lowering) operator for atomic excitations.

    Parameters
    ----------
    states : array
    List of states of the Hilbert space.

    Returns
    -------
    oper : qobj
        Qobj for destruction operator for atomic excitations.
    """
    nstates = len(states)
    sigma = np.eye(nstates)
    for i in range(nstates):
        for j in range(nstates):
            sigma[i,j] = _destroy_excitons(states[i,0],states[i,1],states[j,0],states[j,1])
    return Qobj(sp.csr_matrix(sigma, dtype=complex), isherm=False)


def create_a(states):
    """
    Creation (rising) operator for photonic excitations.

    Parameters
    ----------
    states : array
    List of states of the Hilbert space.

    Returns
    -------
    oper : qobj
    Qobj for creation operator of photonic excitations.
    """
    q0 = destroy_a(states)
    return q0.dag()


def create_x(states):
    """
    Creation (rising) operator for atomic excitations.

    Parameters
    ----------
    states : array
    List of states of the Hilbert space.

    Returns
    -------
    oper : qobj
    Qobj for creation operator of atomic excitations.
    """
    q0 = destroy_x(states)
    return q0.dag()


def num_a(states):
    """
    Number operator for photonic excitations

    Parameters
    ----------
    states : array
    List of states of the Hilbert space.

    Returns
    -------
    oper : qobj
    Qobj for number operator of photonic excitations.
    """
    a = destroy_a(states)
    return a.dag()*a


def num_x(states):
    """
    Number operator for photonic excitations

    Parameters
    ----------
    states : array
    List of states of the Hilbert space.

    Returns
    -------
    oper : qobj
    Qobj for number operator of atomic excitations.
    """
    sigmam = destroy_x(states)
    sigmap = sigmam.dag()
    return sigmap*sigmam


#------------------------------------------------------------------------------
# Internal functions
#
# DESTROY_PHOTONS works for the specific problem of the Jaynes-Cummings model.
# Proper generalization must be done un the future.
#
def _destroy_photons(alpha, m, beta, n):
    dp = np.sqrt(n) * kron_delta(alpha, beta) * kron_delta(m, n-1)
    return dp

#
# DESTROY_EXCITONS works for the specific problem of the Jaynes-Cummings model.
# Proper generalization must be done un the future.
#
def _destroy_excitons(alpha, m, beta, n):
    dx = kron_delta(alpha, 0) * kron_delta(beta, 1) * kron_delta(m, n)
    return  dx
