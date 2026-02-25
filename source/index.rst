.. _index:

Welcome to TENSO
================

**TENSO** (Tensor Equations for Non-Markovian Structured Open systems) is a
general-purpose Python package for simulating the exact open quantum dynamics
of driven quantum systems interacting with structured bosonic thermal
environments.

TENSO combines the **bexcitonic generalization of the Hierarchical Equations
of Motion (HEOM)** with a **Tree Tensor Network (TTN)** decomposition,
enabling numerically exact simulations for environments of chemical complexity
— far beyond what is accessible with standard HEOM. The dynamics is propagated
using equations of motion derived from the **Dirac–Frenkel Time-Dependent
Variational Principle (TDVP)**, the same principle underlying the
ML-MCTDH method for closed quantum systems.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🚀 Getting Started
      :link: gettingstarted
      :link-type: doc

      New to TENSO? Start here for a minimal working example and an overview
      of the main workflow.

   .. grid-item-card:: 📦 Installation
      :link: installation
      :link-type: doc

      Instructions for installing TENSO and its dependencies.

   .. grid-item-card:: 🏗️ Code Structure
      :link: structure
      :link-type: doc

      A detailed description of the four-layer architecture and all key
      classes and modules.

   .. grid-item-card:: 📚 API Reference
      :link: autoapi/index
      :link-type: doc

      Full auto-generated API documentation for all public modules,
      classes, and functions.

Key features
------------

* **Numerically exact open quantum dynamics** — TTN-HEOM captures the
  non-Markovian dissipative dynamics to all orders in the system–bath
  interaction, for environments of arbitrary spectral complexity.

* **Tree tensor network compression** — replaces the exponential
  :math:`\mathcal{O}(M^2 N^K)` memory cost of standard HEOM with a
  polynomial :math:`\mathcal{O}(M^2 R + KNR(N+R))` TTN representation.

* **Three propagation strategies** — direct integration (fixed rank, adaptive
  time step), PS1 (fixed rank, projector-splitting), and PS2 (adaptive rank,
  projector-splitting) — which can be combined on-the-fly.

* **Flexible TTN topology** — supports balanced tensor trees, tensor trains,
  and arbitrary user-defined topologies.

* **Multi-bath support** — systems coupled to multiple independent baths
  through non-commuting system operators.

* **Arbitrary time dependence** — the system Hamiltonian :math:`H_S(t)` may
  have any time dependence, enabling simulation of driven qubits and molecules.

* **GPU acceleration** — all tensor operations are implemented in PyTorch and
  run transparently on CPU or CUDA-enabled GPU.

How to cite
-----------

If you use TENSO in your research, please cite the following papers.
See :doc:`cite` for full citation details.

* Chen, X. & Franco, I. *Tree tensor network hierarchical equations of motion
  based on time-dependent variational principle for efficient open quantum
  dynamics in structured thermal environments.*
  J. Chem. Phys. **163**, 104109 (2025).

* Chen, X. & Franco, I. *Bexcitonics: Quasiparticle approach to open quantum
  dynamics.*
  J. Chem. Phys. **160**, 204116 (2024).

.. toctree::
   :maxdepth: 2
   :caption: Documentation
   :hidden:

   installation
   gettingstarted
   structure

.. toctree::
   :maxdepth: 2
   :caption: Examples
   :hidden:

   examples/pure_dephasing
   examples/spin_boson
   examples/spin_boson_ud
   examples/structured_spin_boson
   examples/three_site_FMO
   examples/time_dependent_no_quantity
   examples/ESD_different_bath

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :hidden:

   autoapi/index

.. toctree::
   :maxdepth: 1
   :caption: About
   :hidden:

   cite
   contact


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
