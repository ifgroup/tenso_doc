tenso.prototypes.qle
====================

.. py:module:: tenso.prototypes.qle


Attributes
----------

.. autoapisummary::

   tenso.prototypes.qle.VecList
   tenso.prototypes.qle.MatList
   tenso.prototypes.qle.inverse_temperature_unit
   tenso.prototypes.qle.time_unit
   tenso.prototypes.qle.energy_unit
   tenso.prototypes.qle.parameters


Functions
---------

.. autoapisummary::

   tenso.prototypes.qle.spin_boson


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

   Spin-Boson model using HEOM in a *QLE* representation with tensor network.
   Assuming one bath.

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
   include_quasi_lindblad: bool
       Whether to include quasi-lindblad terms in the HEOM.
       Calculated from the imaginary system-bath coupling.
       If False, the imaginary part of the system-bath coupling is ignored.
       If True, the quasi-lindblad terms are included in the HEOM,
       but the positivity of the system's density operator is not guaranteed.
       default is True.
   kwargs: dict
       Other settings. See `default_parameters.py` for details.

   Yields:
   -------
   float
       The current time in unit in `default_parameters.py`.


