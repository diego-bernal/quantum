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

__all__ = ['destroy_a_1', 'destroy_x_1', 'create_a_1', 'create_x_1', 'num_a_1',
'num_x_1', 'destroy_a_2', 'destroy_x_2', 'create_a_2', 'create_x_2', 'num_a_2',
'num_x_2']

import numpy as np
import scipy.sparse as sp
from qutip.qobj import Qobj
from quantum.tensor import kron_delta


#------------------------------------------------------------------------------
def destroy_a_1(states):
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
            a[i, j] = _destroy_photons_1(states[i, 0], states[i, 1], states[i, 2],
            states[i, 3], states[j, 0], states[j, 1], states[j, 2], states[j, 3])
    return Qobj(sp.csr_matrix(a, dtype=complex), isherm=False)


def destroy_x_1(states):
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
            sigma[i,j] = _destroy_excitons_1(states[i, 0], states[i, 1], states[i, 2],
            states[i, 3], states[j, 0], states[j, 1], states[j, 2], states[j, 3])
    return Qobj(sp.csr_matrix(sigma, dtype=complex), isherm=False)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def destroy_a_2(states):
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
            a[i, j] = _destroy_photons_2(states[i, 0], states[i, 1], states[i, 2],
            states[i, 3], states[j, 0], states[j, 1], states[j, 2], states[j, 3])
    return Qobj(sp.csr_matrix(a, dtype=complex), isherm=False)


def destroy_x_2(states):
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
            sigma[i,j] = _destroy_excitons_2(states[i, 0], states[i, 1], states[i, 2],
            states[i, 3], states[j, 0], states[j, 1], states[j, 2], states[j, 3])
    return Qobj(sp.csr_matrix(sigma, dtype=complex), isherm=False)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def create_a_1(states):
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
    q0 = destroy_a_1(states)
    return q0.dag()


def create_x_1(states):
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
    q0 = destroy_x_1(states)
    return q0.dag()


def num_a_1(states):
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
    a = destroy_a_1(states)
    return a.dag()*a


def num_x_1(states):
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
    sigmam = destroy_x_1(states)
    sigmap = sigmam.dag()
    return sigmap*sigmam
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def create_a_2(states):
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
    q0 = destroy_a_2(states)
    return q0.dag()


def create_x_2(states):
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
    q0 = destroy_x_2(states)
    return q0.dag()


def num_a_2(states):
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
    a = destroy_a_2(states)
    return a.dag()*a


def num_x_2(states):
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
    sigmam = destroy_x_2(states)
    sigmap = sigmam.dag()
    return sigmap*sigmam
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Internal functions
#
def _destroy_photons_1(alpha, m, beta, n, alpha_p, m_p, beta_p, n_p):
    dp = np.sqrt(m_p) * kron_delta(alpha, alpha_p) *  kron_delta(beta, beta_p) \
    * kron_delta(m, m_p-1) * kron_delta(n, n_p)
    return dp


def _destroy_photons_2(alpha, m, beta, n, alpha_p, m_p, beta_p, n_p):
    dp = np.sqrt(n_p) * kron_delta(alpha, alpha_p) *  kron_delta(beta, beta_p) \
    * kron_delta(m, m_p) * kron_delta(n, n_p-1)
    return dp


def _destroy_excitons_1(alpha, m, beta, n, alpha_p, m_p, beta_p, n_p):
    dx = kron_delta(alpha, 0) * kron_delta(alpha_p, 1) * kron_delta(beta, beta_p) \
    * kron_delta(m, m_p) * kron_delta(n, n_p)
    return  dx


def _destroy_excitons_2(alpha, m, beta, n, alpha_p, m_p, beta_p, n_p):
    dx = kron_delta(alpha, alpha_p) * kron_delta(beta, 0) * kron_delta(beta_p, 1) \
    * kron_delta(m, m_p) * kron_delta(n, n_p)
    return  dx
