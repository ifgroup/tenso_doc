tenso.prototypes.heom
=====================

.. py:module:: tenso.prototypes.heom


Attributes
----------

.. autoapisummary::

   tenso.prototypes.heom.VecList
   tenso.prototypes.heom.MatList
   tenso.prototypes.heom.inverse_temperature_unit
   tenso.prototypes.heom.time_unit
   tenso.prototypes.heom.energy_unit
   tenso.prototypes.heom.parameters


Functions
---------

.. autoapisummary::

   tenso.prototypes.heom.spin_boson
   tenso.prototypes.heom.system_multibath
   tenso.prototypes.heom.holstein_model


Module Contents
---------------

.. py:data:: VecList

.. py:data:: MatList

.. py:data:: inverse_temperature_unit
   :value: '/K'


.. py:data:: time_unit
   :value: 'fs'


.. py:data:: energy_unit
   :value: '/cm'


.. py:data:: parameters

.. py:function:: spin_boson(fname: str, init_rdo: MatList, sys_ham: MatList, sys_op: MatList, bath_correlation: tenso.bath.correlation.Correlation, td_f: Callable[[float], float] | None = None, td_op: MatList | None = None, **kwargs) -> Generator[float, None, None]

   Spin-Boson model using HEOM with tensor network.
   Assuming one bath correlation function.

   Parameters:
   -----------
   fname: str
       The output file name.
   init_rdo: MatList
       The initial reduced density operator.
   h: MatList
       The system Hamiltonian.
   op: MatList
       The system operator in the system-bath interaction hamiltonian.
   bath_correlation: Correlation
       The bath correlation function for HEOM.
   td_f: Callable[[float], float] | None
       The time-dependent field.
   td_op: MatList | None
       The operator associated with the time-dependent field.
   kwargs: dict
       Other settings. See `default_parameters.py` for details.

   Yields:
   -------
   float
       The current time in unit in `default_parameters.py`.


.. py:function:: system_multibath(fname: str, init_rdo: MatList, sys_ham: MatList, sys_ops: list[MatList], bath_correlations: list[tenso.bath.correlation.Correlation], td_f: Callable[[float], float] | None = None, td_op: MatList | None = None, **kwargs) -> Generator[float, None, None]

   Spin-Boson model using HEOM with tensor network.
   Assuming one bath correlation function.

   Parameters:
   -----------
   fname: str
       The output file name.
   init_rdo: MatList
       The initial reduced density operator.
   h: MatList
       The system Hamiltonian.
   op: MatList
       The system operator in the system-bath interaction hamiltonian.
   bath_correlation: Correlation
       The bath correlation function for HEOM.
   td_f: Callable[[float], float] | None
       The time-dependent field.
   td_op: MatList | None
       The operator associated with the time-dependent field.
   kwargs: dict
       Other settings. See `default_parameters.py` for details.

   Yields:
   -------
   float
       The current time in unit in `default_parameters.py`.


.. py:function:: holstein_model(fname: str, init_wfns: list[VecList], sys_hs: list[None | MatList], sys_couplings: list[dict[int, MatList]], sys_ops: list[MatList], bath_correlations: list[tenso.bath.correlation.Correlation], tracking_indices: list[tuple[int, int]], td_fields: list[Callable[[float], float]] | None = None, td_ops: list[dict[int, MatList]] | None = None, **kwargs) -> Generator[float, None, None]

   Holstein model using HEOM with tensor network.
   Assuming multiple bath correlation functions.


