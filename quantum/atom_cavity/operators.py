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
