Welcome to TENSO!
=================

This repository contains the code for the TENSO algorithm, which is a tensor network based method for generating and integration the master equations for open quantum dynamics in structured thermal environments. The code is written in Python and uses PyTorch for tensor operations. It is designed to be efficient and scalable, allowing for the simulation of large open quantum systems using different tree tensor network topologies. Details of the algorithm can be found in the paper. Detailed documentation is under preparation.

Some of the key features include:

* **Hierarchical equations of motion (HEOM)** for open quantum systems
* **Tree tensor network (TTN)** representation for efficient state description
* **Time-dependent variational principle (TDVP)** for optimizing the dynamics
* **Support for structured thermal environments**

If you would like to contribute, you can contact us at :doc:`Xinxian Chen <contact>`.

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   installation.md
   gettingstarted.md

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/pure_dephasing.ipynb
   examples/spin_boson.ipynb
   examples/spin_boson_ud.ipynb
   examples/structured_spin_boson.ipynb
   examples/three_site_FMO.ipynb
   examples/time_dependent_no_quantity.ipynb
   examples/ESD_different_bath.ipynb

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   autoapi/index

.. toctree::
   :maxdepth: 1
   :caption: Cite this

   cite.md
   contact.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
