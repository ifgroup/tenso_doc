tenso.bath.correlation
======================

.. py:module:: tenso.bath.correlation

.. autoapi-nested-parse::

   Correlation function object



Attributes
----------

.. autoapisummary::

   tenso.bath.correlation.PI
   tenso.bath.correlation.unit


Classes
-------

.. autoapisummary::

   tenso.bath.correlation.Correlation


Functions
---------

.. autoapisummary::

   tenso.bath.correlation.get_corr_from_aaa
   tenso.bath.correlation.get_corr_from_esprit


Module Contents
---------------

.. py:data:: PI

.. py:class:: Correlation

   Bases: :py:obj:`object`


   Object encapsulating a correlation function decomposition such that C(t) = sum_k c_k e^{-a_k t}
   or the discretized sorts of baths used in MCTDH/TEDOPA


   .. py:attribute:: coefficients
      :type:  list[complex]
      :value: []



   .. py:attribute:: conj_coefficents
      :type:  list[complex]
      :value: []



   .. py:attribute:: zeropoints
      :type:  list[complex]
      :value: []



   .. py:attribute:: derivatives
      :type:  dict[tuple[int, int], complex]


   .. py:attribute:: lindblad_rate
      :type:  Optional[float]
      :value: None



   .. py:method:: manual_corr_setup(c_ks: list[complex], gamma_ks: list[complex], unit_convert_gamma: bool = False)

      Method to initialize the correlation function object if the form of the
      correlation function in exponential breakdown is already known. This is for
      an HEOM style bath, not a star boson style bath, and zeropoints will be set to 1.

      Parameters:
      c_ks: list of c coefficients in the correlation function breakdown
      gamma_ks: list of gamma exponential coefficients in the correlation function breakdown
      unit_convert_gamma: whether to convert gammas (units of 1/time) to internal units
      returns: nothing



   .. py:method:: dump(output_file: str) -> None


   .. py:method:: remove_heom_terms() -> None


   .. py:method:: load(input_file: str) -> None


   .. py:property:: k_max


   .. py:method:: add_discrete_vibration(frequency: float, coupling: float, beta: Optional[float]) -> None


   .. py:method:: add_discrete_trigonometric(frequency: float, coupling: float, beta: Optional[float]) -> None


   .. py:method:: _add_ltc(sds: list[tenso.bath.sd.SpectralDensity], distribution: tenso.bath.distribution.BoseEinstein)

      Add LTC terms for spectral densities with poles.




   .. py:method:: add_spectral_densities(sds: list[tenso.bath.sd.SpectralDensity], distribution: tenso.bath.distribution.BoseEinstein, zeropoint=1.0, use_ht_function=False)


   .. py:method:: add_trigonometric(sds: list[tenso.bath.sd.SpectralDensity], distribution: tenso.bath.distribution.BoseEinstein)


   .. py:method:: real_correlation_function(t)


   .. py:method:: imag_correlation_function(t)


   .. py:method:: __str__() -> str


.. py:function:: get_corr_from_aaa(spfs: list[Callable[[numpy.typing.NDArray], numpy.typing.NDArray]], freq_space, beta, dual=False, tol=1e-13, k_max=100)

   Get the correlation function from the spectral functions.


.. py:function:: get_corr_from_esprit(samples, h: float, start_time: float, point_num: int, feat_num: int, esprit_tol=0.001)

   Performs an ESPRIT time domain fitting of the correlation function.
   Initially performs an AAA fit and then uses that correlation function to
   find points in the time domain that are used in the ESPRIT fitting.

   Parameters
   samples: np.array of point_num complex numbers to fit
   h: float, distance between the points
   start_time: float, time of the first sample point
   beta: temperature of the bath
   start_time: initial time for the ESPRIT fit to evalute C(t)
   end_time: final time for the ESPRIT fit to evaluate C(t)
   point_num: number of discrete points for the ESPRIT fit
   feat_num: absolute number of features limit; hard limit
   esprit_tol: relative tolerance for which features to include


.. py:data:: unit
   :value: 1000


