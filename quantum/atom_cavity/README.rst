
Atom - Cavity
=============

quantum.atom_cavity.states()
----------------------------
Generates an array with the states for the current problem:
.. math::
\\{ | \\alpha, m \\rangle \\}
being the first entry the corresponding to the atomic qubit, and the second one 
the cavity photon field.

.. note::

    This predefined function could be useful for an easy construction of the state 
    basis, nevertheless, any state basis could be constructed and serve as a basis 
    for the quantum operators.

Parameters
----------
N : int
    Maximum excitation manifold.
    
Returns
-------
states : numpy array


