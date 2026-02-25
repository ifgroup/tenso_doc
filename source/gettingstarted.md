# Getting Started

This page walks you through a minimal TENSO simulation from scratch.
After reading it you will understand the basic workflow and be ready to
explore the [examples](examples/pure_dephasing.ipynb) and the
[code structure](structure.rst).

## Conceptual overview

A TENSO simulation always follows the same four steps:

```
1. Define the bath correlation function C(t) and decompose it into features
2. Define the system Hamiltonian H_S, coupling operator Q_S, and initial state ρ_0
3. Set propagation parameters (TTN topology, rank, depth, propagation scheme)
4. Iterate the propagator and collect results
```

All four steps are handled by `gen_bcf` and `system_multibath` from
`tenso.prototypes`. The sections below explain each step and show a
complete working example.

---

## Step 1 — The bath and its BCF decomposition

TENSO treats environments described as a collection of harmonic oscillators
coupled to the system via

$$
H_\textrm{SB} = Q_\textrm{S} \otimes X_\textrm{B},
\qquad X_\textrm{B} = \sum_j c_j x_j,
$$

where $Q_\textrm{S}$ is the system coupling operator and $X_\textrm{B}$ is
a collective bath coordinate. For such environments, all dynamical
information about the bath is contained in the **Bath Correlation Function
(BCF)**:

$$
C(t) = \langle \tilde{X}_\textrm{B}(t)\,\tilde{X}_\textrm{B}(0)\rangle
$$

Using the residue theorem, the BCF is decomposed exactly into a sum of
$K$ complex decaying exponentials — the **features**:

$$
C(t) = \sum_{k=1}^{K} c_k\, e^{\gamma_k t}, \qquad
C^*(t) = \sum_{k=1}^{K} \bar{c}_k\, e^{\gamma_k t},
\qquad c_k,\,\bar{c}_k,\,\gamma_k \in \mathbb{C}.
$$

`gen_bcf` performs this decomposition from a spectral density
$J(\omega)$ built from **Drude–Lorentz (DL)** and/or
**Brownian oscillator (BO)** components:

$$
J(\omega) = J_\textrm{DL}(\omega) + \sum_b J_\textrm{BO}^{(b)}(\omega)
$$

**Drude–Lorentz** — Ohmic bath with reorganization energy $\lambda$ and
cutoff frequency $\omega_c$:

$$
J_\textrm{DL}(\omega) = \frac{2\lambda}{\pi}
\frac{\omega_c\,\omega}{\omega^2 + \omega_c^2}
$$

Each DL component contributes **one feature** (a simple decaying
exponential with timescale $\omega_c^{-1}$).

**Brownian oscillator** — discrete vibrational mode with reorganization
energy $\lambda$, natural frequency $\omega_0$, and damping rate $\eta$:

$$
J_\textrm{BO}^{(b)}(\omega) = \frac{4\lambda}{\pi}
\frac{\eta\,\omega_0^2\,\omega}
{(\omega^2 - \omega_0^2)^2 + 4\eta^2\omega^2}
$$

Each BO component contributes **two features** (oscillatory-decaying
exponentials).

The total number of features $K$ also grows with the number of
**low-temperature correction (LTC)** terms required to accurately
capture the Bose–Einstein factor $f_\textrm{BE}(\beta\omega)$ at finite
temperature.

```python
from tenso.prototypes.bath import gen_bcf

bath = gen_bcf(
    re_d    = [540],    # λ for DL component (cm⁻¹)
    width_d = [70],     # ωc for DL component (cm⁻¹)
    freq_b  = [1663],   # ω0 for BO component (cm⁻¹)
    re_b    = [330],    # λ  for BO component (cm⁻¹)
    width_b = [4],      # η  for BO component (cm⁻¹)
    temperature          = 300,    # K
    decomposition_method = 'Pade', # 'Pade' or 'Matsubara'
    n_ltc                = 1,      # number of low-temperature correction terms
)
```

```{tip}
The total number of features $K$ determines the size of the HEOM
hierarchy. A DL component contributes 1 feature, each BO component
contributes 2, and each LTC term adds 1 more. Increase `n_ltc` if
the long-time thermalization is not reproduced correctly.
Standard HEOM methods are only feasible for $K \lesssim 5$; TENSO's
TTN compression makes large $K$ tractable.
```

---

## Step 2 — The system

The system is an $M$-state quantum system described by:

- `sys_ham` — the $M \times M$ Hamiltonian $H_S$ (complex128 NumPy array)
- `sys_op` — the $M \times M$ coupling operator $Q_\textrm{S}$ (complex128)
- `init_rdo` — the $M \times M$ initial reduced density operator $\rho_\textrm{S}(0)$

For the spin-boson model with energy gap $\varepsilon$ and tunneling $\Delta$:

$$
H_S = \frac{\varepsilon}{2}\,\sigma_z + \Delta\,\sigma_x
$$

The bath couples to the system through $Q_\textrm{S} = \sigma_x$.

```python
import numpy as np

eps   = 1500.0   # cm⁻¹  energy gap ε
delta =  300.0   # cm⁻¹  tunneling Δ

sys_ham = np.array([[ eps/2,  delta],
                    [ delta, -eps/2]], dtype=np.complex128)

# Q_S — system-bath coupling operator
sys_op  = np.array([[0.0, 1.0],
                    [1.0, 0.0]], dtype=np.complex128)

# Initial state: |↑⟩ (excited state)
wfn      = np.array([1.0, 0.0], dtype=np.complex128)
init_rdo = np.outer(wfn, wfn.conj())
```

---

## Step 3 — Propagation parameters

The key numerical parameters for `spin_boson` are:

| Parameter | Argument | Typical value | Effect |
|---|---|---|---|
| Bexciton depth | `dim` | 10–20 | Truncation depth $N_k$ for each bexciton ladder; increase until converged |
| Bond rank | `rank` | 5–32+ | TTN bond dimension $R$; increase until converged |
| TTN topology | `frame_method` | `'tree2'` or `'train'` | Balanced tree (`tree2`) recommended for large $K$ |
| Propagation method | `ps_method` | `'ps1'` or `'ps2'` | PS2 adapts $R$ automatically; PS1 keeps it fixed |
| Time step | `step_time` | 0.05 fs | Integration step size $\Delta t$ |
| End time | `end_time` | problem-dependent | Total propagation time in fs |
| Output file | `fname` | any string | Results written to `{fname}.npz` |

The memory cost of the EDO without compression scales as
$\mathcal{O}(M^2 N^K)$. TENSO's TTN reduces this to
$\mathcal{O}(M^2 R + KNR(N+R))$, eliminating the exponential
dependence on $K$.

```{tip}
`frame_method='tree2'` builds a balanced binary tree, minimizing the
average path from the system root $A^{(0)}$ to each bexciton index to
$\mathcal{O}(\log K)$, giving more compact TTNs for large $K$.
`frame_method='train'` uses a tensor train (MPS) topology with path
length $\mathcal{O}(K)$, which is simpler but less efficient for
structured baths.
```

---

## Step 4 — Running a simulation

`spin_boson` returns a **generator** that advances the simulation one time
step per iteration. You drive the propagation with a `for` loop:

```python
from math import ceil
from tqdm import tqdm
from tenso.prototypes.heom import spin_boson

end_time = 100.0   # fs
dt       = 0.05    # fs

propagator = spin_boson(
    fname            = 'my_simulation',  # results saved to my_simulation.npz
    init_rdo         = init_rdo,
    sys_ham          = sys_ham,
    sys_op           = sys_op,
    bath_correlation = bath,
    dim              = 20,               # bexciton depth N_k
    end_time         = end_time,
    step_time        = dt,
    frame_method     = 'tree2',
    rank             = 20,
    stepwise_method  = 'simple',
    ps_method        = 'ps1',
)

bar = tqdm(propagator, total=ceil(end_time / dt))
for t in bar:
    bar.set_description(f't = {t:.2f} fs')
```

When the loop finishes, the results are saved to `my_simulation.npz`.
The system density matrix $\rho_\textrm{S}(t) = \varrho_{\vec{0}}(t)$
is extracted directly — it corresponds to all bexciton indices $n_k = 0$
in the EDO $|\Omega(t)\rangle$:

```python
import matplotlib.pyplot as plt

data  = np.load('my_simulation.npz')
t     = data['time']
rho_t = data['rdo']              # shape (n_steps, M, M)

pop_excited = rho_t[:, 0, 0].real   # ρ_S(t)_{00}

plt.plot(t, pop_excited)
plt.xlabel('Time (fs)')
plt.ylabel(r'$[\rho_\mathrm{S}(t)]_{00}$')
plt.show()
```

---

## Checking convergence

Always verify convergence with respect to:

1. **Bexciton depth** `dim` ($N_k$) — the EDO has memory cost
   $\mathcal{O}(M^2 N^K)$; increase `dim` until results are stable.
2. **Bond rank** `rank` ($R$) — the TTN has cost
   $\mathcal{O}(M^2 R + KNR(N+R))$; increase `rank` until stable.
3. **Low-temperature corrections** `n_ltc` — increase until the
   long-time thermalization $\rho_\textrm{S}(t \to \infty)$ is correct.

A typical rank convergence sweep compares multiple values of `rank`
and both TTN topologies:

```python
from math import ceil
from tqdm import tqdm
from tenso.prototypes.heom import spin_boson
from tenso.prototypes.bath import gen_bcf

bath = gen_bcf(
    re_d=[540], width_d=[70],
    freq_b=[1663], re_b=[330], width_b=[4],
    temperature=300, decomposition_method='Pade', n_ltc=1,
)

ranks         = [5, 10, 15, 20, 25, 32]
frame_methods = ['train', 'tree2']

for method in frame_methods:
    for rank in ranks:
        fname = f'{method}_rank{rank}'
        propagator = spin_boson(
            fname=fname, init_rdo=init_rdo,
            sys_ham=sys_ham, sys_op=sys_op,
            bath_correlation=bath,
            dim=20, end_time=100.0, step_time=0.05,
            frame_method=method, rank=rank,
            stepwise_method='simple', ps_method='ps1',
        )
        bar = tqdm(propagator, total=ceil(100.0 / 0.05),
                   desc=f'{method} rank={rank}')
        for t in bar:
            bar.set_description(f'{method} rank={rank} @{t:.2f} fs')
```

This produces one `.npz` file per `(method, rank)` pair, which you can
overlay to verify that $\rho_\textrm{S}(t)$ has converged.

---

## Next steps

- Explore the worked **[Examples](examples/pure_dephasing.ipynb)** for
  pure dephasing, spin-boson models, structured baths, and multi-site systems.
- Read the **[Code Structure](structure.rst)** page to understand the
  four-layer architecture and all key classes.
- Consult the **[API Reference](autoapi/index.rst)** for full documentation
  of all functions and classes.
