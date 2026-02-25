# Getting Started

This page walks you through a minimal TENSO simulation.
After reading it you will understand the basic workflow and be ready to
explore the [examples](examples/pure_dephasing.ipynb) and the
[code structure](structure.rst).

## Conceptual overview

A TENSO simulation always follows the same four steps:

```
1. Define the bath correlation function C(t) and decompose it into features
2. Define the system Hamiltonian H_S, coupling operator Q_S, and initial state ρ_0
3. Set propagation parameters (TTN topology, rank, depth, time grid)
4. Propagate the system and collect results
```

All four steps are handled by `gen_bcf` and `system_multibath` from
`tenso.prototypes`. The sections below explain each step and show a
complete working example.

---

## Step 1 — The bath and its BCF decomposition

TENSO treats environments described as a collection of harmonic oscillators
coupled to the system via the system-bath interaction Hamiltonian

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
J(\omega) = 
\sum_a J_\textrm{DL}^{(a)}(\omega) + \sum_b J_\textrm{BO}^{(b)}(\omega)
$$

**Drude–Lorentz** — Ohmic bath with reorganization energy $\lambda$ and
cutoff frequency $\omega_c$:

$$
J_\textrm{DL}^{(a)}(\omega) = \frac{2\lambda}{\pi}
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
capture the Bose–Einstein distribution $f_\textrm{BE}(\beta\omega)$ at finite
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
The total number of features $K$ — the number of bexcitons needed
to represent the bath — determines the size of the HEOM hierarchy.
It counts as: 1 per DL component + 2 per BO component + 1 per LTC
term. For the `gen_bcf` call above, $K = 1 + 2 + 1 = 4$.
Increase `n_ltc` if the long-time thermalization is not reproduced
correctly.
```

---

## Step 2 — The system

The system is an $M$-state quantum system, where $M$ is the dimension of its
Hilbert space. Each auxiliary density matrix (ADM) in the HEOM hierarchy has
the same $M \times M$ dimension as $\rho_\textrm{S}(t)$, so $M$ directly sets
the per-matrix cost of the simulation. It is specified through:

- `sys_ham` — the $M \times M$ Hamiltonian $H_\textrm{S}$ (complex128 NumPy array)
- `sys_op` — the $M \times M$ coupling operator $Q_\textrm{S}$ (complex128)
- `init_rdo` — the $M \times M$ initial reduced density operator $\rho_\textrm{S}(0)$

For the spin-boson model with energy gap $\varepsilon$ and tunneling $\Delta$:

$$
H_S = \frac{\varepsilon}{2}\,\sigma_z + \Delta\,\sigma_x
$$

The bath couples to the system through $Q_\textrm{S} = \sigma_x$. Here, $\sigma_x$ and $\sigma_z$ are the Pauli matrices

$$
\sigma_z = \begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
,
\qquad
\sigma_x = \begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
$$

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

Four numerical parameters control the accuracy and cost of a TTN-HEOM
simulation, all traceable to the space complexity formulas derived in the
paper:

| Symbol | Meaning | Set by | Notes |
|---|---|---|---|
| $M$ | Dimension of the system Hilbert space | shape of `sys_ham` | Fixed by the physical model; $M=2$ for a two-level system |
| $K$ | Number of BCF features (bexcitons) | `gen_bcf` output | 1 per DL + 2 per BO + 1 per LTC term; fixed by the bath model |
| $N$ | Truncation depth of each bexciton ladder ($N_k$) | `dim` | Each $n_k$ runs from $0$ to $N_k-1$; must be increased until converged |
| $R$ | Bond rank of the TTN core tensors ($R_s$) | `rank` | Controls compression quality; must be increased until converged |

Without compression, storing the full Extended Density Operator (EDO)
$|\Omega(t)\rangle$ requires

$$
\mathcal{O}(M^2 N^K)
$$

memory — exponential in $K$, the number of bexcitons. For the thymine
spectral density in the paper (1 DL + 8 BO + 3 LTC = $K=20$ features,
$N=20$, $M=2$), the uncompressed EDO would require $4.2 \times 10^{26}$
elements, or roughly 6.7 ronnabytes — far beyond any present computer.

TENSO's TTN decomposition reduces this to

$$
\mathcal{O}(M^2 R + KNR(N+R))
$$

which grows only *polynomially* with $K$. Here, the first term $M^2 R$
is the cost of the root tensor $A^{(0)}$ that holds the uncompressed
system indices $i,j$; the second term $KNR(N+R)$ is the cost of the $K$
semi-unitary core tensors $U^{(s)}$, each of dimension $R \times N \times
(N \text{ or } R)$.

The remaining propagation parameters are:

| Parameter | Argument | Typical value | Effect |
|---|---|---|---|
| HEOM depth | `dim` | 10–20 | Sets $N_k$ for each of the $K$ bexciton ladders |
| Bond rank | `rank` | 5–60+ | Sets $R_s$ for each of the $K-1$ TTN bonds |
| TTN topology | `frame_method` | `'tree2'` or `'train'` | Balanced tree (`tree2`) minimizes the average path from root to each bexciton to $\mathcal{O}(\log K)$, reducing cost vs. tensor train $\mathcal{O}(K)$ for large $K$ |
| Propagation method | `ps_method` | `'ps1'` , `'ps2'` or `'vmf'` | PS2 adapts $R$ automatically during propagation; PS1 keeps $R$ fixed |
| Time step | `step_time` | 0.05 fs | Integration step size $\Delta t$ |
| End time | `end_time` | problem-dependent | Total propagation time in fs |
| Output file | `fname` | any string | Prefix for output files: `{fname}.dat.log`, `{fname}.debug.log`, `{fname}.pt` |

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

`system_multibath` returns the dynamics **generator** that advances the simulation one time
step per iteration. You drive the propagation with a `for` loop:

```python
from math import ceil
from tqdm import tqdm
from tenso.prototypes.heom import spin_boson

end_time = 100.0   # fs
dt       = 0.05    # fs

propagator = spin_boson(
    fname            = 'out',        # output prefix → out.dat.log, out.debug.log, out.pt
    init_rdo         = init_rdo,
    sys_ham          = sys_ham,
    sys_op           = sys_op,
    bath_correlation = bath,
    dim              = 20,           # bexciton depth N_k
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

When the loop finishes, three output files are written:

| File | Contents |
|---|---|
| `out.dat.log` | Space-separated text file (complex128). Each row is one time step with 5 columns: `t`, `[ρ_S]_11`, `ρ_eg`, `ρ_ge`, `[ρ_S]_00`. |
| `out.debug.log` | Human-readable log of convergence diagnostics printed during the run. |
| `out.pt` | PyTorch checkpoint of the full TTN state $|\Omega(t)\rangle$ at the final time step, loadable with `torch.load`. |

The system density matrix $\rho_\textrm{S}(t) = \varrho_{\vec{0}}(t)$
is read from `out.dat.log` using `numpy.loadtxt`:

```python
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('out.dat.log', dtype=np.complex128)

t       = data[:, 0].real    # time (fs)
pop_exc = data[:, 1].real    # excited state population  [ρ_S(t)]_11
coh_eg  = data[:, 2]         # coherence ρ_eg = [ρ_S(t)]_10  (complex)
coh_ge  = data[:, 3]         # coherence ρ_ge = [ρ_S(t)]_01 = ρ_eg*  (complex)
pop_gnd = data[:, 4].real    # ground state population   [ρ_S(t)]_00

fig, axes = plt.subplots(1, 2, figsize=(8, 3))

axes[0].plot(t, pop_exc, label=r'$[\rho_\mathrm{S}]_{11}$')
axes[0].plot(t, pop_gnd, '--', label=r'$[\rho_\mathrm{S}]_{00}$')
axes[0].set(xlabel='Time (fs)', ylabel='Population')
axes[0].legend()

axes[1].plot(t, np.abs(coh_eg), color='tab:purple')
axes[1].set(xlabel='Time (fs)', ylabel=r'$|\rho_{eg}|$')

plt.tight_layout()
plt.show()
```

To reload the full TTN state from the PyTorch checkpoint:

```python
import torch

state = torch.load('out.pt')
```

---

## Checking convergence

TTN-HEOM converges to the exact HEOM as $N$ and $R$ increase, and to
the exact open quantum dynamics as $K$ increases. Always verify convergence
with respect to all three:

1. **Bexciton depth** `dim` ($N_k$) — each of the $K$ bexciton ladders is
   truncated at occupation $N_k - 1$. The uncompressed EDO cost is
   $\mathcal{O}(M^2 N^K)$, so insufficient $N$ leads to a truncation of the
   hierarchy. Increase `dim` until $\rho_\textrm{S}(t)$ is stable.
2. **Bond rank** `rank` ($R_s$) — each of the $K-1$ TTN bonds is compressed
   to dimension $R_s$. The TTN cost is $\mathcal{O}(M^2 R + KNR(N+R))$; 
   insufficient $R$ means the compression is lossy. Increase `rank` until
   $\rho_\textrm{S}(t)$ is stable.
3. **Low-temperature corrections** `n_ltc` (adds to $K$) — each LTC term
   adds one bexciton to the hierarchy. Increase until the long-time
   thermalization $\rho_\textrm{S}(t \to \infty)$ is correct.

A typical rank convergence sweep compares multiple values of `rank`, you can choose between and n-ary tree, a TT or your custom TTN:

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

This produces one `{method}_rank{rank}.dat.log` file per `(method, rank)` pair.
Load and overlay them to verify that $\rho_\textrm{S}(t)$ has converged:

```python
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for method in ['train', 'tree2']:
    for rank in [5, 10, 20, 32]:
        data    = np.loadtxt(f'{method}_rank{rank}.dat.log', dtype=np.complex128)
        t       = data[:, 0].real
        pop_exc = data[:, 1].real
        ax.plot(t, pop_exc, label=f'{method} R={rank}')

ax.set(xlabel='Time (fs)', ylabel=r'$[\rho_\mathrm{S}]_{11}$')
ax.legend(fontsize=7)
plt.show()

---

## Next steps

- Explore the worked **[Examples](examples/pure_dephasing.ipynb)** for
  pure dephasing, spin-boson models, structured baths, and multi-site systems.
- Read the **[Code Structure](structure.rst)** page to understand the
  four-layer architecture and all key classes.
- Consult the **[API Reference](autoapi/index.rst)** for full documentation
  of all functions and classes.
