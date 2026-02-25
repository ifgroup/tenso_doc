tenso.prototypes.bath_colle
===========================

.. py:module:: tenso.prototypes.bath_colle

.. autoapi-nested-parse::

   Correlation function object for specific spectral density



Attributes
----------

.. autoapisummary::

   tenso.prototypes.bath_colle.PI


Functions
---------

.. autoapisummary::

   tenso.prototypes.bath_colle.brownian_oscillator_bcf
   tenso.prototypes.bath_colle.critically_damped_brownian_bcf
   tenso.prototypes.bath_colle.super_critical_damping_3rd_bcf
   tenso.prototypes.bath_colle.super_critical_damping_4th_bcf
   tenso.prototypes.bath_colle.overdamped_brownian_bcf
   tenso.prototypes.bath_colle.jordan_critically_damped_brownian_bcf
   tenso.prototypes.bath_colle.jordan_super_critical_damping_3rd_bcf


Module Contents
---------------

.. py:data:: PI

.. py:function:: brownian_oscillator_bcf(re_b: list[float] | None = None, width_b: list[float] | None = None, freq_b: list[float] | None = None, temperature: float = 300.0, decomposition_method: Literal['Pade', 'Matsubara'] = 'Pade', n_ltc: int = 0, use_ht_function: bool = True) -> tenso.bath.correlation.Correlation

   Factory function for a Brownian oscillator spectral density
   with Ikeda's BCF basis:
       phi_1(t) = g/w1 * e^(-g t) * sin(w1 t) + e^(-g t) * cos(w1 t)
       phi_2(t) = -w0/w1 * e^(-g t) * sin(w1 t)


.. py:function:: critically_damped_brownian_bcf(re_b: list[float] | None = None, width_b: list[float] | None = None, temperature: float = 300.0, decomposition_method: Literal['Pade', 'Matsubara'] = 'Pade', n_ltc: int = 0, use_ht_function: bool = False) -> tenso.bath.correlation.Correlation

   Factory function for a critically damped Brownian spectral density.



.. py:function:: super_critical_damping_3rd_bcf(re_b: list[float] | None = None, width_b: list[float] | None = None, temperature: float = 300.0, decomposition_method: Literal['Pade', 'Matsubara'] = 'Pade', n_ltc: int = 0, use_ht_function: bool = False) -> tenso.bath.correlation.Correlation

   Factory function for a Super Critically damped spectral density of order-3.
   At high temperatures, the BCF (t>0) reads:
       C(t) = (2 l)/(3 beta) ( (g t)^2 + 3 g t + 3 ) e^(-g t)
              - i (l g)/(3) ( (g t)^2 + g t ) e^(-g t)

   Let phi_3(t) = 0.5 * g^2 t^2 e^(-g t), phi_2(t) = -g t e^(-g t), phi_1(t) = e^(-g t),
   then
       d/dt phi_3(t) = -g phi_3(t) - g phi_2(t)
       d/dt phi_2(t) = -g phi_2(t) - g phi_1(t)
       d/dt phi_1(t) = -g phi_1(t)
   and
       C(t) = c1 phi_1(t) + c2 phi_2(t) + c3 phi_3(t)
   where
       c1 = (2 l)/(b)
       c2 = - (2 l)/(b) + i (l g)/(3)
       c3 = (4 l)/(3 b) - i (2 l g)/(3)


.. py:function:: super_critical_damping_4th_bcf(re_b: list[float] | None = None, width_b: list[float] | None = None, temperature: float = 300.0, decomposition_method: Literal['Pade', 'Matsubara'] = 'Pade', n_ltc: int = 0, use_ht_function: bool = False) -> tenso.bath.correlation.Correlation

   Factory function for a Super Critically damped spectral density of order-4.
   At high temperatures, the BCF (t>0) reads:
       C(t) =     \lambda \frac{2(gt)^3 + 6 (gt)^2 + 12 gt + 12}{15 \beta} e^{-gt}
              - i \lambda \frac{g (gt)^3}{15}} e^{-g t}

   Let phi_4(t) = -(1/6) * g^3 t^3 e^(-g t), phi_3(t) = (1/2) * g^2 t^2 e^(-g t),
   phi_2(t) = -g t e^(-g t), phi_1(t) = e^(-g t),
   then
       d/dt phi_4(t) = -g phi_4(t) - g phi_3(t)
       d/dt phi_3(t) = -g phi_3(t) - g phi_2(t)
       d/dt phi_2(t) = -g phi_2(t) - g phi_1(t)
       d/dt phi_1(t) = -g phi_1(t)
   and
       C(t) = c1 phi_1(t) + c2 phi_2(t) + c3 phi_3(t) + c4 phi_4(t)
   where
       c4 = (4 l)/(5 b) - i (2 l g)/(5)
       c3 = (4 l)/(5 b)
       c2 = (4 l)/(5 b)
       c1 = (4 l)/(5 b)


.. py:function:: overdamped_brownian_bcf(re_b: list[float] | None = None, width_b: list[float] | None = None, freq_b: list[float] | None = None, temperature: float = 300.0, decomposition_method: Literal['Pade', 'Matsubara'] = 'Pade', n_ltc: int = 0) -> tenso.bath.correlation.Correlation

   Factory function for an overdamped Brownian spectral density.


.. py:function:: jordan_critically_damped_brownian_bcf(re_b: list[float] | None = None, width_b: list[float] | None = None, temperature: float = 300.0, decomposition_method: Literal['Pade', 'Matsubara'] = 'Pade', n_ltc: int = 0, use_ht_function: bool = False) -> tenso.bath.correlation.Correlation

   Factory function for a critically damped Brownian spectral density.



.. py:function:: jordan_super_critical_damping_3rd_bcf(re_b: list[float] | None = None, width_b: list[float] | None = None, temperature: float = 300.0, decomposition_method: Literal['Pade', 'Matsubara'] = 'Pade', n_ltc: int = 0, use_ht_function: bool = False) -> tenso.bath.correlation.Correlation

   Factory function for a Super Critically damped spectral density of order-3 in Jordan form.
   At high temperatures, the BCF (t>0) reads:
       C(t) = (2 l)/(3 beta) ( (g t)^2 + 3 g t + 3 ) e^(-g t)
              - i (l g)/(3) ( (g t)^2 + g t ) e^(-g t)

   Let phi_3(t) = 0.5 * t^2 e^(-g t), phi_2(t) = t e^(-g t), phi_1(t) = e^(-g t),
   then
       d/dt phi_3(t) = -g phi_3(t) - g phi_2(t)
       d/dt phi_2(t) = -g phi_2(t) - g phi_1(t)
       d/dt phi_1(t) = -g phi_1(t)
   and
       C(t) = c1 phi_1(t) + c2 phi_2(t) + c3 phi_3(t)
   where
       c1 = (2 l)/(b)
       c2 = (2 l g )/(b) - i (l g^2)/(3)
       c3 = (4 l g^2)/(3 b) - i (2 l g^3)/(3)


