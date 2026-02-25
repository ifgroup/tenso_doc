tenso.bath.tedopa
=================

.. py:module:: tenso.bath.tedopa

.. autoapi-nested-parse::

   Computing the chain map coefficients used in the (T-)TEDOPA algorithm.



Attributes
----------

.. autoapisummary::

   tenso.bath.tedopa.energy_unit


Classes
-------

.. autoapisummary::

   tenso.bath.tedopa.Tedopa


Module Contents
---------------

.. py:class:: Tedopa(w: numpy.typing.NDArray, j: numpy.typing.NDArray, beta: Optional[None], n_max: int)

   .. py:attribute:: underflow
      :value: 1e-14



   .. py:method:: be_function(beta: float, w: numpy.typing.NDArray) -> numpy.typing.NDArray
      :staticmethod:



   .. py:attribute:: beta


   .. py:attribute:: n_max


   .. py:attribute:: ip


   .. py:attribute:: ipx


   .. py:attribute:: alpha


   .. py:method:: c0() -> float

      Compute the zeroth-order coefficient.



   .. py:method:: chain_frequency() -> numpy.typing.NDArray

      Compute the chain frequencies.



   .. py:method:: chain_coupling() -> numpy.typing.NDArray

      Compute the chain couplings.



   .. py:method:: chain_matrix() -> numpy.typing.NDArray

      Compute the chain matrix.



   .. py:method:: _tridiagonalize() -> tuple[numpy.typing.NDArray, numpy.typing.NDArray]

      Tridiagonalize the chain matrix.



   .. py:method:: star_parameters() -> numpy.typing.NDArray


   .. py:method:: int(f: numpy.typing.NDArray) -> float

      Integrate a function with respect to the spectral density.



   .. py:method:: generate_polynomials() -> None

      Generate the orthogonal polynomials.



.. py:data:: energy_unit

