.. _structure:

===============
TENSO Structure
===============

.. note::
   Most users will only need to interact with **Layer 4 — Templates & Prototypes**.
   The deeper layers are documented here for those who wish to modify the framework
   or extend its functionality. Familiarity with object-oriented programming is
   assumed for Layers 1–3.

``TENSO`` is organized into four distinct layers of abstraction, each building on
the one below it:

.. list-table::
   :widths: 8 22 70
   :header-rows: 1

   * - Layer
     - Name
     - Responsibility
   * - 1
     - **Backend Interfaces**
     - PyTorch / NumPy / torchdiffeq dependencies, hardware targeting, ODE solvers.
   * - 2
     - **TTN Decomposition**
     - General TTN data structures and TDVP-based propagation engine for SoP generators.
   * - 3
     - **Master Equation Implementations**
     - Physics-specific formulations: HEOM (single & multi-bath) and MCTDH / ML-MCTDH.
   * - 4
     - **Templates & Prototypes**
     - Ready-to-run interface functions for common physical problems.

The code structure spans these four layers plus a set of shared helper modules.
An outline of the full package layout is shown in the :ref:`module index <modindex>`.

----

.. _layer1:

Layer 1 — Backend Interfaces
=============================

.. rubric:: Module: ``tenso.backend``

The ``tenso.backend`` module is the foundation upon which all computation in
``TENSO`` rests. It has three responsibilities: managing third-party dependencies,
controlling global package settings (numerical precision, default device), and
registering the integration methods available for time propagation. All higher
layers interact with hardware and solvers exclusively through this module, which
means that changing the ODE solver or hardware target requires touching only this
one file.

Dependencies and design rationale
-----------------------------------

``TENSO`` depends on three external libraries. The choice of each is deliberate:

`PyTorch <https://pytorch.org>`_ — **primary tensor computation engine**
   PyTorch was chosen over NumPy-only or JAX-based alternatives for its
   hardware-agnostic tensor operations — the same code runs on CPU or GPU
   without modification, which is critical for the large tensor contractions
   that arise in TTN propagation. PyTorch's dynamic computation graph and
   automatic differentiation infrastructure also provide a flexible foundation
   for future extensions, such as gradient-based optimization of bath parameters.
   The backend exposes PyTorch's device management so that all ``TENSO`` objects
   (state tensors, operator matrices, propagator buffers) are consistently
   allocated on the same device.

`NumPy <https://numpy.org>`_ — **auxiliary numerics and interoperability**
   NumPy handles operations outside the main propagation loop — such as
   constructing spectral density grids, initializing sparse operator dictionaries,
   and interfacing with external analysis tools. It also serves as the interchange
   format when passing data to and from plotting libraries or other Python
   scientific packages. The backend ensures that NumPy arrays and PyTorch tensors
   can be converted without copying data where possible.

`torchdiffeq <https://github.com/rtqichen/torchdiffeq>`_ — **ODE integration**
   Rather than implementing ODE solvers from scratch, ``TENSO`` delegates time
   integration to ``torchdiffeq``, a library of differentiable ODE solvers built
   on top of PyTorch. This gives access to high-quality adaptive-step solvers with
   error control, all operating natively on PyTorch tensors. The backend imports
   ``torchdiffeq`` and also implements any additional integration methods not
   covered by the library directly.

Global package settings
------------------------

Beyond dependency management, ``tenso.backend`` enforces several global settings
that affect all computations:

- **Floating-point precision** — the default dtype (``torch.float64`` for most
  quantum dynamics problems, where accumulated round-off in long propagations
  is a practical concern).
- **Default device** — CPU or GPU, set once and inherited by all subsequently
  constructed ``TENSO`` objects.
- **Complex number support** — ``TENSO`` works with complex-valued tensors
  throughout; the backend ensures that PyTorch's complex dtype handling is
  configured consistently.

Changing any of these settings after objects have been constructed is not
supported; configure the backend before instantiating any ``TENSO`` objects.

Integration methods
--------------------

Time propagation in ``TENSO`` reduces to integrating a (large, structured) ODE
of the form :math:`\dot{\Omega} = f(\Omega, t)`. The choice of solver has a
significant effect on both accuracy and wall-clock time. The default is an
adaptive Runge-Kutta solver, which works well for most problems. Stiff hierarchies
— which arise when the bath relaxation timescales are much shorter than the system
dynamics — may require implicit methods.

.. list-table::
   :widths: 22 18 60
   :header-rows: 1

   * - Solver
     - Type
     - When to use
   * - ``dopri5`` *(default)*
     - Explicit, adaptive
     - Dormand–Prince RK45. Step size is controlled automatically by a local error
       estimate. The right choice for most HEOM and MCTDH calculations where the
       hierarchy is not stiff.
   * - ``rk4``
     - Explicit, fixed-step
     - Classical 4th-order Runge-Kutta with a user-specified step size. Useful
       when you need reproducible, deterministic trajectories or when the overhead
       of error estimation outweighs its benefit (e.g. very short propagations).
       Provides no error control — step size must be chosen carefully.
   * - ``adams``
     - Explicit, adaptive
     - Variable-order Adams–Bashforth–Moulton predictor-corrector. More efficient
       than ``dopri5`` for smooth problems where the solution does not change
       rapidly, because it reuses previous function evaluations.
   * - Implicit solvers
     - Implicit, adaptive
     - Necessary when the hierarchy is *stiff* — that is, when some decay rates
       in the bath correlation function decomposition are much larger than others.
       In this regime, explicit solvers require prohibitively small step sizes.
       See ``tenso.backend`` for the specific implicit methods available and their
       configuration options.

.. tip::
   If you are unsure which solver to use, start with the default ``dopri5``.
   If propagation is slow and you observe that the adaptive solver is taking very
   small steps, your hierarchy is likely stiff — switch to an implicit method.
   If propagation is fast but results are inaccurate, tighten the error tolerances
   (``rtol``, ``atol``) passed to the solver rather than changing the method.

.. tip::
   ``tenso.backend`` is extensively commented and serves as the authoritative
   reference for all solver options, tolerance settings, and hardware configuration.
   It is the first file to consult when tuning numerical performance.

----

.. _layer2:

Layer 2 — TTN Decomposition
============================

The general master equations addressed by ``TENSO`` take the form

.. math::

   \frac{\mathrm{d}}{\mathrm{d}t}\,|\Omega(t)\rangle = \mathcal{L}(t)\,|\Omega(t)\rangle

where :math:`|\Omega(t)\rangle` is the **Extended Density Operator (EDO)** — a
high-dimensional tensor that collects the physical reduced density matrix
:math:`\rho_\textrm{S}(t)` together with the full hierarchy of auxiliary density
matrices (ADMs). Concretely, the EDO is organized as

.. math::

   |\Omega(t)\rangle = \sum_{\vec{n}}\, \varrho_{\vec{n}}(t)\,|\vec{n}\rangle,

where :math:`\vec{n} = (n_1, \ldots, n_K)` indexes the bexcitonic occupation
numbers and :math:`\varrho_{\vec{0}}(t) = \rho_\textrm{S}(t)` is the system's
reduced density matrix. :math:`\mathcal{L}(t)` is the Liouvillian superoperator
generating the dynamics. Layer 2 implements the efficient propagation of this
equation without ever forming :math:`|\Omega(t)\rangle` or
:math:`\mathcal{L}(t)` explicitly as dense objects. It does so through two
complementary representations described below.

Why tensor networks? The exponential wall
------------------------------------------

In the HEOM context, the EDO tensor has elements
:math:`[\Omega(t)]_{ij,n_1\cdots n_K}`, where :math:`i,j` index the
:math:`M`-dimensional Hilbert space of the system and each :math:`n_k` indexes
the truncated bexciton ladder of depth :math:`N_k`. The overall space complexity
of storing the EDO directly is :math:`\mathcal{O}(M^2 N^K)` — it grows
*exponentially* with the number of bath features :math:`K`. This is the
fundamental reason why standard HEOM calculations are limited to simple
environmental models: as the spectral density becomes more structured (larger
:math:`K`) or the temperature decreases (requiring more low-temperature correction
terms in the BCF decomposition), the computation rapidly becomes intractable.

``TENSO`` addresses this by decomposing the high-order EDO tensor into a
**Tree Tensor Network (TTN)** — a contraction of :math:`K` low-order core
tensors :math:`A^{(0)}(t), U^{(1)}(t), \ldots, U^{(K-1)}(t)`:

.. math::

   [\Omega(t)]_{ijn_1\cdots n_K}
   = \sum_{a_1 \cdots a_{K-1}}
     A^{(0)}_{ija_1}(t)\;
     U^{(1)}_{a_1\beta_1\gamma_1}(t)\;\cdots\;
     U^{(K-1)}_{a_{K-1}\beta_{K-1}\gamma_{K-1}}(t).

For bond dimensions :math:`R_s = \mathcal{O}(R)` and bexciton depth
:math:`N_k = \mathcal{O}(N)`, the space complexity of the TTN is
:math:`\mathcal{O}(M^2 R + KNR(N + R))`, which grows only *polynomially*
with :math:`K`. The root tensor :math:`A^{(0)}(t)` carries the system indices
:math:`i,j` and the compressed index :math:`a_1`, so the system's unitary
dynamics is treated exactly while the bexciton influence is captured in
compressed form. The semi-unitary core tensors :math:`U^{(s)}(t)` satisfy the
orthogonality condition

.. math::

   \sum_{\beta\gamma} [U^{(s)}(t)]^*_{a'_s,\beta\gamma}\,[U^{(s)}(t)]_{a_s,\beta\gamma} = \delta_{a'_s a_s},

which is enforced throughout the propagation via the **gauge condition** and is
essential for numerical stability.

The underlying graph of the TTN is a *tree* — there are no loops. This is the
natural structure for both HEOM (where bexcitons are organized hierarchically)
and ML-MCTDH. The absence of loops makes the key operations — tensor
contractions, TDVP sweeps, singular value decompositions — computationally
efficient, since information propagates through the tree without the costly
gauge-fixing required by loopy networks. ``TENSO`` supports two canonical TTN
topologies: the **balanced tensor tree** (minimizes the average path length
between the system and each bexciton to :math:`\mathcal{O}(\log K)`) and the
**tensor train** / matrix product state form (linear chain, average path length
:math:`\mathcal{O}(K)`).

The Sum-of-Product generator
------------------------------

Even with a compact TTN representation of :math:`|\Omega(t)\rangle`, applying
:math:`\mathcal{L}(t)` is only efficient if :math:`\mathcal{L}(t)` itself has a
structured form. In the bexcitonic formulation, the Liouvillian superoperator
takes a natural Sum-of-Product (SoP) form:

.. math::

   \mathcal{L}(t) = \sum_{m=1}^{5K+2}
           h^>_m(t) \otimes h^<_m(t)
           \otimes h^{(1)}_m \otimes \cdots \otimes h^{(K)}_m,

where each product term consists of a component :math:`h^>_m(t)` acting on the
ket index :math:`|i\rangle`, a component :math:`h^<_m(t)` acting on the bra
index :math:`\langle j|`, and local operators :math:`h^{(k)}_m` acting on the
:math:`k`-th bexciton space :math:`|n_k\rangle`. Each dissipator
:math:`\mathcal{D}_k` in the bexcitonic master equation contributes five product
terms, and the system Liouvillian :math:`-iH_\textrm{S}^\times(t)` contributes
two more, giving :math:`5K+2` terms in total.

This factored structure means that applying one product term to the TTN requires
only a sequence of small local contractions — one per node — rather than a global
dense matrix-vector product. The SoP form is not an approximation: it follows
exactly from the structure of the bexcitonic equations of motion, and an identical
design principle underlies ML-MCTDH.

The propagation pipeline
-------------------------

Layer 2 implements three objects that together form the propagation pipeline:

.. code-block:: text

   Frame  ──(topology)──►  Model  |Ω(t)⟩  =  Con(A⁽⁰⁾, U⁽¹⁾, …, U⁽ᴷ⁻¹⁾)
                                      │
                          SparseSPO   ℒ(t) = Σₘ h>ₘ ⊗ h<ₘ ⊗ h⁽¹⁾ₘ ⊗ … ⊗ h⁽ᴷ⁾ₘ
                                      │
                                      ▼
                        SparsePropagator ──► |Ω(t + Δt)⟩

A ``Frame`` defines the *topology* of the TTN (which nodes exist, how they connect,
which bonds carry system vs. bexciton indices). A ``Model`` fills that topology with
concrete tensor data — the root tensor :math:`A^{(0)}(t)` and the semi-unitary core
tensors :math:`U^{(s)}(t)`. A ``SparseSPO`` encodes the Liouvillian superoperator
:math:`\mathcal{L}(t)` in SoP form. A ``SparsePropagator`` takes a ``Model`` and a
``SparseSPO`` and advances :math:`|\Omega(t)\rangle` in time.

.. _layer2-state:

tenso.state — State Representation
------------------------------------

This module implements the data structure for :math:`|\Omega(t)\rangle`, organized
into two submodules: ``pureframe`` for the abstract graph infrastructure and
``puremodel`` for the concrete TTN vector.

``tenso.state.pureframe``
~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the graph structure of the tensor network independently of any numerical
data. Separating topology from data allows the same ``Frame`` to be reused across
multiple ``Model`` instances (e.g. during a basis change or when restarting from
a checkpoint).

.. list-table::
   :widths: 16 84
   :header-rows: 1

   * - Class
     - Description
   * - :class:`Point`
     - Abstract base class for all graph elements. Defines the link-tracking
       interface (the set of edges connecting a graph element to its neighbors)
       that both :class:`Node` and :class:`End` inherit. Direct instantiation is
       not intended; subclass instead.
   * - :class:`Node`
     - An internal vertex of the TTN graph. Each ``Node`` is associated with one
       of the core tensors in the TTN decomposition: either the root tensor
       :math:`A^{(0)}(t)` (which carries the system indices :math:`i,j` and the
       compressed index :math:`a_1`) or one of the semi-unitary tensors
       :math:`U^{(s)}(t)` (which carry bexciton indices :math:`n_k` and/or
       contracted bond indices :math:`a_s`). A ``Node`` may hold any number of
       links; the order of its core tensor equals the number of links.
   * - :class:`End`
     - A leaf of the TTN graph representing a single **open bond** — a physical
       system index (:math:`i` or :math:`j`) or a bexciton index :math:`n_k`.
       An ``End`` must have exactly one link (to its parent ``Node``).
   * - :class:`Frame`
     - The complete graph topology: a container for all ``Node`` and ``End``
       objects and the links between them. A ``Frame`` determines the computational
       cost of all TTN operations via the bond dimensions :math:`\{R_s\}` of its
       contracted indices :math:`\{a_s\}`. The two canonical topologies —
       **balanced tensor tree** and **tensor train** — are provided by
       :class:`FrameFactory` in ``tenso.heom``.

``tenso.state.puremodel``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 16 84
   :header-rows: 1

   * - Class
     - Description
   * - :class:`Model`
     - The TTN representation of the EDO :math:`|\Omega(t)\rangle`. A ``Model``
       binds a ``Frame`` (topology) to concrete tensor valuations for every
       ``Node``: the root tensor :math:`A^{(0)}(t)` and the collection of
       semi-unitary tensors :math:`\{U^{(s)}(t)\}`. It tracks the
       **orthogonality center** — the node with respect to which all other
       tensors satisfy the semi-unitary condition — which is essential for
       numerically stable TDVP sweeps. The physical reduced density matrix
       :math:`\rho_\textrm{S}(t) = \varrho_{\vec{0}}(t)` is recovered from the ``Model``
       by contracting all bexciton indices at :math:`n_k = 0`.

.. _layer2-operator:

tenso.operator.sparse — Generator & Propagator
------------------------------------------------

This module encodes :math:`\mathcal{L}(t)` in SoP form and implements its action on a
:class:`Model`. Both classes work together: ``SparseSPO`` describes *what*
operator to apply; ``SparsePropagator`` describes *how* and *when* to apply it.

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - Class
     - Description
   * - :class:`~tenso.operator.sparse.SparseSPO`
     - Encodes :math:`\mathcal{L}(t)` in Sum-of-Product form as a **list of
       dictionaries**. Each dictionary represents one product term
       :math:`h^>_m \otimes h^<_m \otimes h^{(1)}_m \otimes \cdots \otimes h^{(K)}_m`:
       keys are degree-of-freedom names (system ket ``>``; system bra ``<``; or
       bexciton index :math:`k`) matching those used in the ``Frame``, and values
       are the corresponding local operator matrices. Terms acting on only a subset
       of indices are handled naturally — missing keys are treated as identity
       operators. This sparse representation avoids explicitly constructing the
       full :math:`M^2 N^K \times M^2 N^K` Liouvillian matrix.
   * - :class:`~tenso.operator.sparse.SparsePropagator`
     - The **Dirac–Frenkel TDVP propagator**. Given a
       :class:`~tenso.state.puremodel.Model` and a
       :class:`~tenso.operator.sparse.SparseSPO`, it
       constructs all intermediate quantities needed for the TDVP sweep: the
       compressed environment matrices :math:`f^{(s)}_m(t)` (computed leaf-to-root)
       and, for direct integration, the regularized inverse matrices
       :math:`\bar{D}^{(s)}_m(t)` (computed root-to-leaf). Specific propagation
       algorithms are implemented as methods of this class.

What is the Dirac–Frenkel TDVP and why use it?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **Dirac–Frenkel Time-Dependent Variational Principle (TDVP)** determines the
optimal equations of motion for the core tensors :math:`A^{(0)}(t)` and
:math:`\{U^{(s)}(t)\}` by requiring that the residual
:math:`\mathcal{L}(t)|\Omega(t)\rangle - \frac{d}{dt}|\Omega(t)\rangle` is
orthogonal to all allowed variations of :math:`|\Omega(t)\rangle` within the
TTN ansatz:

.. math::

   \sum_{ij,n_1\cdots n_K}
   [\delta\Omega(t)]^*_{ijn_1\cdots n_K}
   \left[\left(\mathcal{L}(t) - \frac{\mathrm{d}}{\mathrm{d}t}\right)\Omega(t)\right]_{ijn_1\cdots n_K}
   = 0.

This projection guarantees that the propagated state remains on the TTN manifold
(bond dimensions stay bounded) while capturing the dynamics as accurately as
possible for the given TTN ansatz. The equations of motion for the root tensor
:math:`A^{(0)}(t)` and for each semi-unitary tensor :math:`U^{(s)}(t)` are
derived from this principle together with the gauge condition that enforces
semi-unitarity of the :math:`U^{(s)}(t)` throughout the propagation.

Propagation algorithms
~~~~~~~~~~~~~~~~~~~~~~~

Three propagation algorithms are implemented as methods of :class:`SparsePropagator`.
All three are numerically stable and yield equivalent dynamics; the choice
between them involves tradeoffs in memory, accuracy, and computational cost.

**Direct Integration**
   All core tensor ODEs — for :math:`A^{(0)}(t)` and all :math:`U^{(s)}(t)` —
   are integrated *simultaneously* using the ODE solver configured in
   ``tenso.backend`` (default: adaptive RK45). This enables high-order time
   integration (:math:`\mathcal{O}(\Delta t^n)` for an order-:math:`n` method)
   and adaptive time stepping. Because the matrix :math:`D^{(s)}(t)` in the
   semi-unitary equation of motion is singular at :math:`t = 0` (for initially
   separable states), a **regularization scheme** is applied: singular values
   of :math:`D^{(s)}` below a threshold :math:`\epsilon` are replaced by
   :math:`\epsilon`, introducing an error of only :math:`\mathcal{O}(\epsilon^2)`.
   The singularity resolves after a brief initial transient (typically :math:`<2` fs).

**PS1 — Fixed-rank Projector-Splitting**
   Based on a second-order symmetric Lie–Trotter splitting of :math:`\mathcal{L}(t)`.
   Instead of propagating all tensors simultaneously, the algorithm sweeps through
   the TTN sequentially: at each split-step, the root is moved to the next tensor
   via SVD, and that tensor is propagated in isolation using Eq. (43) of the
   paper. The forward and backward sweeps together constitute one time step
   :math:`\Delta t`, achieving second-order (:math:`\mathcal{O}(\Delta t^3)`)
   Trotter accuracy. Bond dimensions remain **constant** throughout — PS1 is a
   fixed-rank method. It requires no regularization but is harder to parallelize
   than direct integration due to the sequential SVD structure.

**PS2 — Adaptive-rank Projector-Splitting**
   Extends PS1 with a two-site move that combines adjacent core tensors into a
   fourth-order tensor, propagates it, and then decomposes it back via a
   **truncated SVD** with threshold :math:`\epsilon'`. This allows bond dimensions
   to grow or shrink adaptively during propagation, with the rank at each bond
   controlled by the SVD truncation error. PS2 is the recommended starting point
   when the required ranks are not known in advance: it determines the appropriate
   computational resources automatically from the early-time dynamics.

.. tip::
   The three methods can be **combined on-the-fly**. A practical mixed strategy
   is to begin with PS2 (which avoids the initial singularity and determines
   appropriate ranks automatically) and switch to direct integration once the
   adaptive ranks have stabilized. This approach has been shown to achieve
   converged results with lower computational cost than either method alone.

.. list-table:: Algorithm comparison
   :widths: 22 26 26 26
   :header-rows: 1

   * - Property
     - Direct Integration
     - PS1
     - PS2
   * - **Rank during propagation**
     - Fixed
     - Fixed
     - Adaptive
   * - **Time accuracy**
     - :math:`\mathcal{O}(\Delta t^n)`, solver-dependent
     - :math:`\mathcal{O}(\Delta t^3)` (Trotter)
     - :math:`\mathcal{O}(\Delta t^3)` (Trotter)
   * - **Regularization needed**
     - Yes (near :math:`t=0`)
     - No
     - No
   * - **Parallelizable**
     - Yes (all tensors simultaneously)
     - Difficult (sequential SVD)
     - Difficult (sequential SVD)
   * - **Best for**
     - Bulk dynamics; high-order time steps
     - Known ranks; robust propagation
     - Unknown ranks; automatic compression

----

.. _layer3:

Layer 3 — Master Equation Implementations
==========================================

``TENSO`` currently provides built-in implementations for two major quantum dynamics
methods. Both are cast as special cases of the general TTN master equation and share
an identical downstream interface: a :class:`Hierarchy` object constructs the required
:class:`~tenso.operator.sparse.SparsePropagator` and
:class:`~tenso.state.puremodel.Model` for the given physical problem.

.. _layer3-heom:

tenso.heom — Hierarchical Equations of Motion
-----------------------------------------------

HEOM is an exact, non-perturbative method for simulating the open quantum dynamics
of driven quantum systems coupled to bosonic thermal baths. ``TENSO`` implements
the **bexcitonic generalization** of HEOM, which provides a unified framework for
all HEOM variants and admits arbitrary time-dependence in the system Hamiltonian
:math:`H_\textrm{S}(t)`.

**Physical background.** The influence of a thermal bath on the system is
completely characterized by its Bath Correlation Function (BCF):

.. math::

   C(t) = \sum_{k=1}^{K} c_k\, e^{\gamma_k t}, \qquad
   C^*(t) = \sum_{k=1}^{K} \bar{c}_k\, e^{\gamma_k t},

where :math:`c_k`, :math:`\bar{c}_k`, :math:`\gamma_k \in \mathbb{C}` are
obtained by decomposing the spectral density :math:`J(\omega)` via Padé or
Matsubara expansion of the Bose–Einstein factor
:math:`f_\textrm{BE}(\beta\omega) = (1 - e^{-\beta\omega})^{-1}`.
Each :math:`k` in this sum defines a **feature** of the bath. The number of
features :math:`K` grows with the complexity of :math:`J(\omega)` and with the
number of low-temperature correction terms required. The bexcitonic picture
associates a fictitious bosonic quasiparticle — a *bexciton* of label :math:`k`
— with each feature. The bexciton creation and annihilation operators
:math:`\hat{\alpha}^\dagger_k`, :math:`\hat{\alpha}_k` connect the ADMs in the
hierarchy and give the bexcitonic master equation its ladder structure.
The full bexcitonic equation of motion is

.. math::

   \frac{\mathrm{d}}{\mathrm{d}t}|\Omega(t)\rangle
   = \left(-iH_\textrm{S}^\times(t) + \sum_{k=1}^{K} \mathcal{D}_k\right)|\Omega(t)\rangle,

where :math:`\mathcal{D}_k = \gamma_k\hat{\alpha}^\dagger_k\hat{\alpha}_k
+ (c_k Q_\textrm{S}^> - \bar{c}_k Q_\textrm{S}^<)\hat{z}_k^{-1}\hat{\alpha}^\dagger_k
- Q_\textrm{S}^\times\hat{\alpha}_k\hat{z}_k` is the dissipator associated with
the :math:`k`-th bath feature and :math:`\hat{z}_k` is an invertible metric
operator. The standard HEOM is recovered as the specific case with number
representation and :math:`\hat{z}_k = i(\hat{\alpha}^\dagger_k\hat{\alpha}_k)^{-1/2}`.

Two submodules are provided depending on the number of baths:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Submodule
     - Scope
   * - ``tenso.heom.eom``
     - TTN-HEOM for a system coupled to a **single bath**. Implements the full
       bexcitonic hierarchy with :math:`K` features, each truncated at depth
       :math:`N_k`, giving an EDO of space complexity
       :math:`\mathcal{O}(M^2 N^K)` that is compressed to
       :math:`\mathcal{O}(M^2 R + KNR(N+R))` by the TTN.
   * - ``tenso.heom.meom``
     - TTN-HEOM for a system coupled to **multiple independent baths** through
       system operators :math:`\{Q_\textrm{S}^{(d)}\}` that need not commute. Implements
       the extended multi-bath hierarchy and its SoP generator.

**Key classes** (available in both ``eom`` and ``meom``):

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Class
     - Description
   * - :class:`~tenso.heom.eom.Hierarchy`
     - Central data structure for TTN-HEOM. Given the BCF parameters
       :math:`\{c_k, \bar{c}_k, \gamma_k\}_{k=1}^K` and the truncation depths
       :math:`\{N_k\}`, it constructs the full bexcitonic operator structure,
       generates the SoP representation of the Liouvillian
       :math:`-iH_\textrm{S}^\times(t) + \sum_k \mathcal{D}_k`, and initializes
       the root tensor :math:`A^{(0)}(0)` and semi-unitary tensors
       :math:`\{U^{(s)}(0)\}` with the correct initial conditions for a separable
       system–bath state. Also provides methods to extract
       :math:`\rho_\textrm{S}(t)` from the EDO via the recursive contraction
       :math:`[\rho_\textrm{S}(t)]_{ij} = \sum_{a_1} [A^{(0)}(t)]_{ij,a_1}\,[t^{(1)}(t)]_{a_1}`.
   * - :class:`FrameFactory`
     - Constructs the TTN topology for the EDO :math:`|\Omega(t)\rangle`.
       Supports two canonical topologies: the **balanced tensor tree** — which
       minimizes the average path length between the system root
       :math:`A^{(0)}` and each bexciton index :math:`n_k` to
       :math:`\mathcal{O}(\log K)`, leading to more compact TTNs under
       PS2 compression — and the **tensor train** (MPS form, average path
       :math:`\mathcal{O}(K)`).

.. _layer3-mctdh:

tenso.mctdh — MCTDH and ML-MCTDH
-----------------------------------

The Multiconfiguration Time-Dependent Hartree (MCTDH) method and its multilayer
extension (ML-MCTDH) are implemented in ``tenso.mctdh``. As noted in the TTN-HEOM
paper, the three core design principles of TTN-HEOM — a Sum-of-Product generator,
a TTN decomposition of the state, and the Dirac–Frenkel TDVP — are identical to
those of ML-MCTDH. The key difference is that ML-MCTDH targets *unitary* dynamics
of closed quantum systems (wavefunctions :math:`|\psi(t)\rangle` propagated by the
Schrödinger equation), whereas TTN-HEOM targets *non-unitary* dissipative dynamics
of open quantum systems (the EDO :math:`|\Omega(t)\rangle` propagated by the
bexcitonic master equation). Both are implemented in ``TENSO`` through the same
:class:`~tenso.state.puremodel.Model` / :class:`~tenso.operator.sparse.SparsePropagator`
interface, with the physical differences encoded entirely in the ``SparseSPO`` and
the initial conditions of the ``Model``.

----

.. _layer4:

Layer 4 — Templates for Common Problems
=========================================

.. rubric:: Subpackage: ``tenso.prototypes``

The ``tenso.prototypes`` subpackage provides ready-to-use interface templates for
the most common physical problems. These functions abstract away all details of
tensor network construction, hierarchy generation, and propagator setup.

.. list-table::
   :widths: 30 25 45
   :header-rows: 1

   * - Object / Function
     - Location
     - Purpose
   * - :func:`~tenso.prototypes.heom.system_multibath`
     - ``prototypes.heom``
     - Primary simulation entry point for spin-boson HEOM calculations. Sets up
       the system state, bath model, TTN topology, and propagator in a single call,
       and returns a **generator** that advances the state one time step per
       iteration. Results are written to a file specified by ``fname``.
   * - :func:`~tenso.prototypes.bath.gen_bcf`
     - ``prototypes.bath``
     - Generates the BCF decomposition parameters :math:`\{c_k, \bar{c}_k, \gamma_k\}_{k=1}^K`
       from a given spectral density :math:`J(\omega)`. Accepts Drude–Lorentz
       parameters (``re_d``, ``width_d``) and underdamped Brownian oscillator
       parameters (``freq_b``, ``re_b``, ``width_b``), with either Padé or
       Matsubara expansion of the Bose–Einstein factor
       :math:`f_\textrm{BE}(\beta\omega)`
       via ``decomposition_method`` and ``n_ltc`` low-temperature correction
       terms. The output is directly compatible with the ``spin_boson`` and
       ``Hierarchy`` constructors.
   * - ``default_parameters``
     - ``prototypes.default_parameters``
     - Stores default values for coupling strengths, temperature, cutoff
       frequencies, hierarchy depth, and time propagation settings. All prototype
       functions draw defaults from here.

.. note::
   ``tenso.prototypes`` is the recommended starting point for new users.
   The functions in this layer are the only ones most users will ever need to call
   directly.

----

.. _helpers:

Helper & Auxiliary Modules
============================

Several auxiliary modules provide supporting capabilities shared across multiple
layers.

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Module
     - Description
   * - ``tenso.libs.utils``
     - Algorithms for traversing the TTN graph and visiting all nodes in a specified
       order. Used internally by propagation routines to sweep through the network
       during TDVP updates.
   * - ``tenso.basis``
     - Provides a **Discrete Variable Representation (DVR)** basis as an alternative
       to the default number (Fock) basis. Useful for continuum degrees of freedom
       with localized wavefunctions or when a DVR offers superior convergence.
   * - ``tenso.bath.correlation``
     - Implements the :class:`Correlation` object responsible for computing and
       storing the BCF :math:`C(t) = \sum_{k=1}^K c_k e^{\gamma_k t}` — the
       central input quantity for constructing the bexcitonic dissipators
       :math:`\{\mathcal{D}_k\}` and the HEOM hierarchy.
   * - ``tenso.bath.distribution``
     - Contains the Padé and Matsubara decompositions of the Bose–Einstein
       factor :math:`f_\textrm{BE}(\beta\omega) = (1 - e^{-\beta\omega})^{-1}`
       required to express :math:`C(t)` as a finite sum of exponentials at
       finite temperature, including low-temperature correction terms.
   * - ``tenso.bath.sd``
     - Defines spectral density functions :math:`J(\omega)`: Drude–Lorentz
       :math:`J_\textrm{DL}(\omega) = \frac{2\lambda}{\pi}\frac{\omega_c\,\omega}{\omega^2+\omega_c^2}`
       with reorganization energy :math:`\lambda` and cutoff frequency
       :math:`\omega_c`; underdamped Brownian oscillator
       :math:`J_\textrm{BO}^{(b)}(\omega) = \frac{4\lambda}{\pi}\frac{\eta\,\omega_0^2\,\omega}{(\omega^2-\omega_0^2)^2+4\eta^2\omega^2}`
       with reorganization energy :math:`\lambda`, natural frequency
       :math:`\omega_0`, and damping rate :math:`\eta`; and support for
       user-defined forms.
