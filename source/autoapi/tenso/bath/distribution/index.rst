tenso.bath.distribution
=======================

.. py:module:: tenso.bath.distribution

.. autoapi-nested-parse::

   Decomposition of Bose-Einstein distribution



Attributes
----------

.. autoapisummary::

   tenso.bath.distribution.PI
   tenso.bath.distribution.as_array


Classes
-------

.. autoapisummary::

   tenso.bath.distribution.BoseEinstein


Functions
---------

.. autoapisummary::

   tenso.bath.distribution._tridiag_eigsh


Module Contents
---------------

.. py:data:: PI

.. py:data:: as_array

.. py:function:: _tridiag_eigsh(subdiag: numpy.typing.NDArray) -> numpy.typing.NDArray

.. py:class:: BoseEinstein(n: int = 0, beta: Optional[float] = None)

   Bases: :py:obj:`object`


   .. py:attribute:: decomposition_method
      :type:  Literal['Pade', 'Matsubara']
      :value: 'Pade'



   .. py:attribute:: pade_type
      :type:  Literal['(N-1)/N']
      :value: '(N-1)/N'



   .. py:attribute:: underflow
      :value: 1e-14



   .. py:attribute:: n
      :value: 0



   .. py:attribute:: beta
      :value: None



   .. py:method:: __str__() -> str


   .. py:method:: ht_function(w: numpy.typing.NDArray) -> numpy.typing.NDArray


   .. py:method:: function(w: numpy.typing.NDArray) -> numpy.typing.NDArray


   .. py:method:: odd(w: numpy.typing.NDArray) -> numpy.typing.NDArray


   .. py:method:: even(w: numpy.typing.NDArray) -> numpy.typing.NDArray


   .. py:method:: get_residues_poles() -> tuple[list[complex], list[complex]]

      The list of (-2 PI I) * residues and poles of the Bose-Einstein distribution
      with some rational approximant/expansion specified in `decomposition_method`.

      :returns: tuple[list[complex], list[complex]]
                ((-2 PI I) * residues, poles) in the lower half-plane.



   .. py:method:: matsubara(n: int) -> tuple[numpy.typing.NDArray, numpy.typing.NDArray]
      :staticmethod:



   .. py:method:: pade1(n: int) -> tuple[numpy.typing.NDArray, numpy.typing.NDArray]
      :staticmethod:



