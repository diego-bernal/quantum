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
#
# The functions in these module were inspired by:
# QuTiP: Quantum Toolbox in Python.
#
#    Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the QuTiP: Quantum Toolbox in Python nor the names
#       of its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
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


__all__ = ['liouvillian', 'lindblad_dissipator', 'spost', 'spre', 'operator_to_vector',
'vector_to_operator', 'mat2vec', 'vec2mat']


import scipy.sparse as sp
import numpy as np
from scipy.sparse import kron
# kronecker product in a sparse matrix format
from qutip.fastsparse import fast_csr_matrix, fast_identity
from qutip.sparse import sp_reshape
from qutip.cy.spmath import zcsr_kron
from qutip.qobj import Qobj
from quantum.qobj import dag


def liouvillian(H, c_ops=[]):
# def liouvillian_ref(H, c_ops=[]):
    """Assembles the Liouvillian superoperator from a Hamiltonian
    and a `list` of collapse operators.

    Parameters
    ----------
    H : qobj
        System Hamiltonian.

    c_ops : array_like
        A 'list' or 'array' of collapse operators.

    Returns
    -------
    L : qobj
        Liouvillian superoperator.
    """
    # \dot{\rho} = -i [H, \rho] = -i (H \rho - \rho H)
    #            =  i [\rho, H] =  i (\rho H - H \rho)

    L = -1.0j * (spre(H) - spost(H)) # Commutation superoperator

    for c in c_ops:
        L += lindblad_dissipator(c)

    return L


def lindblad_dissipator(a, b=None):
    """
    Lindblad dissipator (generalized) for a single pair of collapse operators
    (a, b), or for a single collapse operator (a) when b is not specified:
    .. math::
    \\mathcal{D}[a,b]\\rho = \\frac{1}{2} (2 a \\rho b^\\dagger -
    a^\\dagger b\\rho - \\rho a^\\dagger b)

    Parameters
    ----------
    a : sparse_csr_matrix
        Left part of collapse operator.

    b : sparse_csr_matrix (optional)
        Right part of collapse operator. If not specified, b defaults to a.
    Returns
    -------
    D : sparse_csr_matrix
        Lindblad dissipator superoperator.
    """
    if b is None:
        b = a
    adag = dag(a)
    bdag = dag(b)
    ad_b = adag * b
    D = 2 * spre(a) * spost(bdag) - spre(ad_b) - spost(ad_b)
    return 0.5*D


def spost(A):
    """Superoperator formed from post-multiplication by operator A

    Parameters
    ----------
    A : qobj
        Quantum operator for post multiplication.

    Returns
    -------
    super : qobj
        Superoperator formed from input qauntum object.
    """
    if not isinstance(A, Qobj):
        raise TypeError('Input is not a quantum object')

    if not A.isoper:
        raise TypeError('Input is not a quantum operator')

    S = Qobj(isherm=A.isherm, superrep='super')
    S.dims = [[A.dims[0], A.dims[1]], [A.dims[0], A.dims[1]]]
    S.data = zcsr_kron(fast_identity(np.prod(A.shape[0])), A.dag().data)
    return S


def spre(A):
    """Superoperator formed from pre-multiplication by operator A.

    Parameters
    ----------
    A : qobj
        Quantum operator for pre-multiplication.

    Returns
    --------
    super :qobj
        Superoperator formed from input quantum object.
    """
    if not isinstance(A, Qobj):
        raise TypeError('Input is not a quantum object')

    if not A.isoper:
        raise TypeError('Input is not a quantum operator')

    S = Qobj(isherm=A.isherm, superrep='super')
    S.dims = [[A.dims[0], A.dims[1]], [A.dims[0], A.dims[1]]]
    S.data = zcsr_kron(A.data, fast_identity(np.prod(A.shape[1])))
    return S


# In the following, the uncommented lines correspond to the QuTip original
# assignations
# The creation of a vector from a matrix in QuTip approach is ordering in
# columns, while our approach is to order in rows.
#------------------------------------------------------------------------------
def operator_to_vector(op):
    """
    Create a vector representation of a quantum operator given
    the matrix representation.
    """
    q = Qobj()
    q.dims = [op.dims, [1]]
    q.data = sp_reshape(op.data.T, (np.prod(op.shape), 1))
    # q.data = sp_reshape(op.data, (np.prod(op.shape), 1))
    return q

def vector_to_operator(op):
    """
    Create a matrix representation given a quantum operator in
    vector form.
    """
    q = Qobj()
    q.dims = op.dims[0]
    n = int(np.sqrt(op.shape[0]))
    q.data = sp_reshape(op.data.T, (n, n)).T
    # q.data = sp_reshape(op.data, (n, n))
    return q

def mat2vec(mat):
    """
    Private function reshaping matrix to vector.
    Not allowed for dense matrices.
    """
    return mat.T.reshape(np.prod(np.shape(mat)), 1)
    # return mat.reshape(np.prod(np.shape(mat)), 1)

def vec2mat(vec):
    """
    Private function reshaping vector to matrix.
    Not allowed for dense matrices.
    """
    n = int(np.sqrt(len(vec)))
    return vec.reshape((n, n)).T
    # return vec.reshape((n, n))
#------------------------------------------------------------------------------



# Under construction
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# def liouvillian(H, c_ops=[], data_only=False, chi=None):
#     """Assembles the Liouvillian superoperator from a Hamiltonian
#     and a 'list' of collapse operators. Like liouvillian, but with an
#     experimental implementation which avoids creating extra Qobj instances,
#     which can be advantageous for large systems.
#
#     Parameters
#     ----------
#     H : qobj
#         System Hamiltonian.
#
#     c_ops : array_like
#         A 'list' or 'array' of collapse operators.
#
#     Returns
#     -------
#     L : qobj
#         Liouvillian superoperator.
#
#     """
#
#     if chi and len(chi) != len(c_ops):
#         raise ValueError('chi must be a list with same length as c_ops')
#
#     if H is not None:
#         if H.isoper:
#             op_dims = H.dims
#             op_shape = H.shape
#         elif H.issuper:
#             op_dims = H.dims[0]
#             op_shape = [np.prod(op_dims[0]), np.prod(op_dims[0])]
#         else:
#             raise TypeError("Invalid type for Hamiltonian.")
#     else:
#         # no hamiltonian given, pick system size from a collapse operator
#         if isinstance(c_ops, list) and len(c_ops) > 0:
#             c = c_ops[0]
#             if c.isoper:
#                 op_dims = c.dims
#                 op_shape = c.shape
#             elif c.issuper:
#                 op_dims = c.dims[0]
#                 op_shape = [np.prod(op_dims[0]), np.prod(op_dims[0])]
#             else:
#                 raise TypeError("Invalid type for collapse operator.")
#         else:
#             raise TypeError("Either H or c_ops must be given.")
#
#     sop_dims = [[op_dims[0], op_dims[0]], [op_dims[1], op_dims[1]]]
#     sop_shape = [np.prod(op_dims), np.prod(op_dims)]
#
#
#     # L = -1.0j * (spre(H) - spost(H)) # Commutation superoperator
#     #
#     # spost: S.data = zcsr_kron(fast_identity(np.prod(A.shape[0])), A.dag().data)
#     # spre:  S.data = zcsr_kron(A.data, fast_identity(np.prod(A.shape[1])))
#
#     spI = fast_identity(op_shape[0])
#
#     if H:
#         if H.isoper:
#             Hdg = H.dag()
#             data = -1j*zcsr_kron(H.data, spI)
#             data += 1j*zcsr_kron(spI, Hdg.data)
#             # Ht = H.data.T
#             # data = -1j * zcsr_kron(spI, H.data)
#             # data += 1j * zcsr_kron(Ht, spI)
#         else:
#             data = H.data
#     else:
#         data = fast_csr_matrix(shape=(sop_shape[0], sop_shape[1]))
#
#     for idx, c_op in enumerate(c_ops):
#         if c_op.issuper:
#             data = data + c_op.data
#         else:
#             cd = c_op.data.H # Hermitian conjugate (Transpose conjugate)
#             c = c_op.data
#             if chi: #???
#                 data = data + np.exp(1j * chi[idx]) * \
#                                 zcsr_kron(c.conj(), c)
#             else:
#                 # data = data + zcsr_kron(c.conj(), c)
#                 data += zcsr_kron(c, spI)*zcsr_kron(spI,cd)
#             cdc = cd * c
#             cdcd = cd.H
#             # cdct = cdc.T
#             # data = data - 0.5 * zcsr_kron(spI, cdc)
#             # data = data - 0.5 * zcsr_kron(cdct, spI)
#             data += -0.5 * zcsr_kron(cdc, spI)
#             data += -0.5 * zcsr_kron(spI, cdcd)
#
#             # D = 0.5*( 2*spre(a)*spost(bdag) - spre(ad_b) - spost(ad_b) )
#
#     if data_only:
#         return data
#     else:
#         L = Qobj()
#         L.dims = sop_dims
#         L.data = data
#         L.isherm = False
#         L.superrep = 'super'
#         return L
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
