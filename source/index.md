# Welcome to TENSO!

This repository contains the code for the TENSO algorithm, which is a tensor network based method for generating and integration the master equations for open quantum dynamics in structured thermal environments. The code is written in Python and uses PyTorch for tensor operations. It is designed to be efficient and scalable, allowing for the simulation of large open quantum systems using different tree tensor network topologies. Details of the algorithm can be found in the paper. Detailed documentation is under preparation.

Some of the key features include:

- Hierarchical equations of motion (HEOM) for open quantum systems
- Tree tensor network (TTN) representation for efficient state description
- Time-dependent variational principle (TDVP) for optimizing the dynamics
- Support for structured thermal environments

If you wold like to contribute, you can contact us at {doc}`XChen <contact>`.

```{toctree}
:maxdepth: 2
:caption: Documentation
installation.md
gettingstarted.md
```


```{toctree}
:maxdepth: 1
:caption: Examples
pure_dephasing.ipynb
spin_boson.ipynb
spin_boson_ud.ipynb
structured_spin_boson.ipynb
three_site_FMO.ipynb
time_dependent_no_quantity.ipynb
ESD_different_bath.ipynb
```

```{toctree}
:maxdepth: 1
:caption: Cite this
cite.md
contact.rst
```
