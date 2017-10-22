Quantum: Quantum dynamics solver
================================

[Diego Nicolás Bernal-García](http://github.com/diego-bernal)

Quantum is open-source software for calculating the dynamics of quantum systems. The Quantum library is strongly based and inspired by QuTip: Quantum Toolbox in Python. It takes advantange of the Numpy, Scipy, and Cython packages, as well as Matplotlib.

Quantum differs from QuTip in two essencial features:
1. It allows truncation by excitation manifold for certain specific problems.
2. It uses the theory of Green operators to calculate the two-time correlation functions, as well as the density energy spectrum.

Quantum is freely available for use and/or modification.

Demos
-----
A selection of demonstration notebooks is available here: [github.com/diego-bernal/quantum-notebooks](http://github.com/diego-bernal/quantum-notebooks).


REMARKS
-------

This Quantum library is strongly based and inspired in the QuTip packages. So, it uses the excellent Qobj class for all its purposes.
