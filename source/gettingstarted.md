# Getting Started

This page walks you through a minimal TENSO simulation from scratch.
After reading it you will understand the basic workflow and be ready to
explore the [examples](examples/pure_dephasing.ipynb) and the
[code structure](structure.rst).

## Conceptual overview

A TENSO simulation always follows the same four steps:

```
1. Define the system Hamiltonian H_S and the coupling operator Q_S
2. Define the bath via its spectral density J(ω) → BCF parameters {c_k, γ_k}
3. Set propagation parameters (TTN topology, rank, depth, time grid)
4. Run the simulation and extract ρ_S(t)
```

All four steps are handled by a single call to
`tenso.prototypes.heom.system_multibath` for most common problems.
The sections below explain each step and then show a complete example.

---

## Step 1 — The system Hamiltonian

The system is a finite-dimensional quantum system described by an
$M \times M$ Hamiltonian matrix $H_S$ (and optionally a time-dependent
drive). For a two-level system (qubit):

$$
H_S = \frac{E}{2}(|1\rangle\langle 1| - |0\rangle\langle 0|)
     + V(|1\rangle\langle 0| + |0\rangle\langle 1|)
$$

where $E$ is the energy gap and $V$ is the electronic coupling.
In TENSO this is passed as a NumPy or PyTorch matrix.

## Step 2 — The bath and its correlation function

The bath is characterized by its **spectral density** $J(\omega)$.
TENSO supports two standard models out of the box:

**Drude–Lorentz** (Ohmic bath with Lorentzian cutoff):

$$
J_\text{DL}(\omega) = \frac{2\lambda_0}{\pi}\frac{\gamma_0\,\omega}{\omega^2+\gamma_0^2}
$$

**Underdamped Brownian oscillator** (discrete vibrational mode):

$$
J_B^{(b)}(\omega) = \frac{4\lambda_b}{\pi}
\frac{\gamma_b\,\omega_b^2\,\omega}{(\omega^2-\omega_b^2)^2+4\gamma_b^2\omega^2}
$$

A realistic bath can be a **composite** of these two, for example one
Drude–Lorentz component for the solvent and several Brownian oscillators
for intramolecular vibrations.

The helper function `gen_bcf` converts $J(\omega)$ into the BCF
decomposition parameters $\{c_k, \bar{c}_k, \gamma_k\}_{k=1}^K$ that
TENSO needs internally:

$$
C(t) = \sum_{k=1}^{K} c_k\, e^{\gamma_k t}
$$

```{tip}
The number of features $K$ grows with the complexity of $J(\omega)$
and with the number of low-temperature correction terms.
A typical calculation at room temperature with one Drude–Lorentz and
eight Brownian oscillators requires $K = 20$ features.
```

## Step 3 — Propagation parameters

The key numerical parameters are:

| Parameter | Symbol | Typical value | Effect |
|---|---|---|---|
| Bexciton depth | $N_k$ | 10–20 | Truncation of each bexciton ladder; increase until converged |
| Bond rank | $R$ | 20–80 | TTN compression; increase until converged |
| TTN topology | — | balanced tree | Balanced tree recommended for large $K$ |
| Propagator | — | PS2 → direct | PS2 determines ranks, then direct integration takes over |
| Time grid | $t_\text{max}, \Delta t$ | problem-dependent | Adaptive step size with `dopri5` |

## Step 4 — Running a simulation

The recommended entry point is `system_multibath` from
`tenso.prototypes.heom`. Here is a complete minimal example:

```python
import numpy as np
from tenso.prototypes.heom import system_multibath
from tenso.prototypes.bath import gen_bcf

# ── System ────────────────────────────────────────────────────────────────────
# Two-level system: energy gap E = 1000 cm⁻¹, coupling V = 1000 cm⁻¹
E = 1000.0   # cm⁻¹
V = 1000.0   # cm⁻¹

H_S = np.array([[E / 2,    V   ],
                [  V,   -E / 2 ]])

# Coupling operator Q_S = (1/2)(|1><1| - |0><0|)
Q_S = np.array([[0.5,  0.0],
                [0.0, -0.5]])

# Initial state: pure superposition (|0> + |1>) / sqrt(2)
rho0 = np.array([[0.5, 0.5],
                 [0.5, 0.5]])

# ── Bath ──────────────────────────────────────────────────────────────────────
# Single Drude–Lorentz bath at room temperature
temperature = 300.0   # K
lambda_0    = 715.73  # cm⁻¹  (reorganization energy)
gamma_0     =  54.45  # cm⁻¹  (bath relaxation rate)

bcf_params = gen_bcf(
    model       = 'drude-lorentz',
    lambda_     = lambda_0,
    gamma       = gamma_0,
    temperature = temperature,
    n_pade      = 3,          # number of low-temperature correction terms
)

# ── Propagation ───────────────────────────────────────────────────────────────
t_output = np.linspace(0, 500, 501)   # fs

result = system_multibath(
    H_S        = H_S,
    Q_S        = [Q_S],
    rho0       = rho0,
    bcf_params = [bcf_params],
    t_output   = t_output,
    topology   = 'tree',       # 'tree' or 'train'
    rank       = 40,
    depth      = 20,
    propagator = 'ps2-direct', # 'direct', 'ps1', 'ps2', or 'ps2-direct'
)

# ── Results ───────────────────────────────────────────────────────────────────
# result.rho_S has shape (len(t_output), M, M)
rho_t   = result.rho_S
pop_0   = rho_t[:, 0, 0].real          # population of state |0>
purity  = np.trace(rho_t @ rho_t, axis1=1, axis2=2).real

import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(t_output, pop_0)
axes[0].set(xlabel='Time (fs)', ylabel='Population of |0⟩')
axes[1].plot(t_output, purity)
axes[1].set(xlabel='Time (fs)', ylabel='Purity')
plt.tight_layout()
plt.show()
```

## Checking convergence

Always verify convergence with respect to:

1. **Bexciton depth** $N_k$ — increase until the dynamics does not change.
2. **Bond rank** $R$ — increase until the dynamics does not change.
3. **Number of low-temperature correction terms** — increase `n_pade` until
   the long-time thermalization is correct.

```{tip}
Use the **PS2 propagator** first: it determines the required rank
automatically by adaptively growing the TTN. Once the adaptive rank
stabilizes, you know the minimum rank needed and can switch to
`ps2-direct` or `direct` for efficiency.
```

## Next steps

- Explore the worked **[Examples](examples/pure_dephasing.ipynb)** for
  pure dephasing, spin-boson models, structured baths, and multi-site systems.
- Read the **[Code Structure](structure.rst)** page to understand the
  four-layer architecture and the key classes.
- Consult the **[API Reference](autoapi/index.rst)** for the full
  documentation of all functions and classes.
