tenso.prototypes.mctdh
======================

.. py:module:: tenso.prototypes.mctdh

.. autoapi-nested-parse::

   MCTDH prototype for the spin-boson model.



Attributes
----------

.. autoapisummary::

   tenso.prototypes.mctdh.VecList
   tenso.prototypes.mctdh.MatList
   tenso.prototypes.mctdh.parameters


Functions
---------

.. autoapisummary::

   tenso.prototypes.mctdh.spin_boson
   tenso.prototypes.mctdh.spin_boson_bath_q
   tenso.prototypes.mctdh.system_multibath


Module Contents
---------------

.. py:data:: VecList

.. py:data:: MatList

.. py:data:: parameters

.. py:function:: spin_boson(fname: str, init_wfn: VecList, sys_ham: MatList, sys_op: MatList, bath: tenso.bath.star.StarBosons, td_f: Callable[[float], float] | None = None, td_op: MatList | None = None, **kwargs) -> Generator[float, None, None]

   Spin-boson model with MCTDH.

   :param fname: The filename prefix for the output files.
   :type fname: str
   :param init_wfn: The initial wavefunction.
   :type init_wfn: VecList
   :param h: The system Hamiltonian.
   :type h: MatList
   :param op: The observable.
   :type op: MatList
   :param boson_bath: The boson bath.
   :type boson_bath: StarBosons
   :param td_f: The time-dependent field, by default None.
   :type td_f: Callable[[float], float], optional
   :param td_op: The time-dependent operator, by default None.
   :type td_op: MatList, optional
   :param \*\*kwargs: The parameters for the simulation.

   :Yields: *float* -- Current time in unit in `default_parameters.py`.


.. py:function:: spin_boson_bath_q(fname: str, init_wfn: VecList, sys_ham: MatList, sys_op: MatList, bath: tenso.bath.star.StarBosons, td_f: Callable[[float], float] | None = None, td_op: MatList | None = None, **kwargs) -> Generator[float, None, None]

   Spin-boson model with MCTDH.

   :param fname: The filename prefix for the output files.
   :type fname: str
   :param init_wfn: The initial wavefunction.
   :type init_wfn: VecList
   :param h: The system Hamiltonian.
   :type h: MatList
   :param op: The observable.
   :type op: MatList
   :param boson_bath: The boson bath.
   :type boson_bath: StarBosons
   :param td_f: The time-dependent field, by default None.
   :type td_f: Callable[[float], float], optional
   :param td_op: The time-dependent operator, by default None.
   :type td_op: MatList, optional
   :param \*\*kwargs: The parameters for the simulation.

   :Yields: *float* -- Current time in unit in `default_parameters.py`.


.. py:function:: system_multibath(fname: str, init_wfn: VecList, sys_ham: MatList, sys_ops: list[MatList], baths: list[tenso.bath.star.StarBosons], td_f: Callable[[float], float] | None = None, td_op: MatList | None = None, **kwargs) -> Generator[float, None, None]

   Spin-boson-model-like model with one system DOF and multiple baths with MCTDH.

   :param fname: The filename prefix for the output files.
   :type fname: str
   :param init_wfn: The initial wavefunction.
   :type init_wfn: VecList
   :param h: The system Hamiltonian.
   :type h: MatList
   :param op: The observable.
   :type op: MatList
   :param boson_bath: The boson bath.
   :type boson_bath: StarBosons
   :param td_f: The time-dependent field, by default None.
   :type td_f: Callable[[float], float], optional
   :param td_op: The time-dependent operator, by default None.
   :type td_op: MatList, optional
   :param \*\*kwargs: The parameters for the simulation.

   :Yields: *float* -- Current time in unit in `default_parameters.py`.


