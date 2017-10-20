# This file is part of Quantum.
#
#    Copyright (c) 2017 and later, Diego Nicolas Bernal-Garcia.
#    All rights reserved.
###############################################################################
"""
This module contains a collection of operations commonly used in quantum mechanics.

This module was inspired by:
QuTip: Quantum Toolbox in Python.
Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
All rights reserved.
"""

__all__ = ['dag', 'isherm', 'expm']


from qutip.sparse import sp_expm
from qutip.qobj import Qobj
import qutip.settings as settings


def dag(A):
    """Adjont operator (dagger) of a quantum object.

    Parameters
    ----------
    A : qobj
        Input quantum object.

    Returns
    -------
    oper : qobj
        Adjoint of input operator

    Notes
    -----
    This function is for legacy compatibility only. It is recommended to use
    the ``dag()`` Qobj method.

    """
    if not isinstance(A, Qobj):
        raise TypeError("Input is not a quantum object")

    return A.dag()


def isherm(Q):
    """Determines if given operator is Hermitian.

    Parameters
    ----------
    Q : qobj
        Quantum object

    Returns
    -------
    isherm : bool
        True if operator is Hermitian, False otherwise.

    Examples
    --------
    >>> a = destroy(4)
    >>> isherm(a)
    False

    Notes
    -----
    This function is for legacy compatibility only. Using the `Qobj.isherm`
    attribute is recommended.

    """
    return True if isinstance(Q, Qobj) and Q.isherm else False



def expm(Q, method='sparse'):
    """Matrix exponential of quantum operator.

    Input operator must be square.

    Parameters
    ----------
    method : str {'dense', 'sparse'}
        Use set method to use to calculate the matrix exponentiation. The
        available choices includes 'dense' and 'sparse'.  Since the
        exponential of a matrix is nearly always dense, method='dense'
        is set as default.s

    Returns
    -------
    oper : qobj
        Exponentiated quantum operator.

    Raises
    ------
    TypeError
        Quantum operator is not square.

    """
    if not isinstance(Q, Qobj):
        raise TypeError('Input is not a quantum object')

    if Q.dims[0][0] != Q.dims[1][0]:
        raise TypeError('Invalid operand for matrix exponential')

    if method == 'sparse':
        F = sp_expm(Q.data, sparse=True)

    elif method == 'dense':
        F = sp_expm(Q.data, sparse=False)

    else:
        raise ValueError("method must be 'dense' or 'sparse'.")

    out = Qobj(F, dims=Q.dims)
    return out.tidyup() if settings.auto_tidyup else out
