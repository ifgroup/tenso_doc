tenso.bath.star
===============

.. py:module:: tenso.bath.star

.. autoapi-nested-parse::

   Diagonal Correlation function object.



Attributes
----------

.. autoapisummary::

   tenso.bath.star.quad
   tenso.bath.star.EPSILON
   tenso.bath.star.ABSORB_RATE
   tenso.bath.star.N_INT
   tenso.bath.star.beta


Classes
-------

.. autoapisummary::

   tenso.bath.star.StarBosons
   tenso.bath.star.DiscretizationSolver
   tenso.bath.star.Tedopa
   tenso.bath.star.EqualReorganizationEnergy
   tenso.bath.star.LogFourier
   tenso.bath.star.Fourier
   tenso.bath.star.Chebyshev


Module Contents
---------------

.. py:data:: quad

.. py:data:: EPSILON
   :value: 1e-21


.. py:data:: ABSORB_RATE
   :value: 0.1


.. py:data:: N_INT
   :value: 100000


.. py:class:: StarBosons

   .. py:attribute:: couplings
      :type:  list[float | complex]
      :value: []



   .. py:attribute:: conj_couplings
      :type:  list[float | complex]
      :value: []



   .. py:attribute:: frequencies
      :type:  dict[tuple[int, int], complex]


   .. py:attribute:: base_function
      :value: None



   .. py:method:: get_reorganization_energy() -> float


   .. py:method:: filter(underflow: float) -> None


   .. py:method:: degenerate(multiplicity: int)


   .. py:method:: dump(output_file: str) -> None


   .. py:method:: load(input_file: str) -> None


   .. py:property:: k_max


   .. py:method:: add_discrete_vibrations(ph_parameters: list[tuple[float, float]], beta: Optional[float]) -> None

      ph_parameters: list[frequency, coupling]



   .. py:method:: is_diagonalized() -> bool


   .. py:method:: diagonalize() -> None


   .. py:method:: total_reorganization_energy() -> float


   .. py:method:: real_correlation_function(t)


   .. py:method:: imag_correlation_function(t)


   .. py:method:: add_spectral_densities(sds: list[tenso.bath.sd.SpectralDensity], beta: None | float, n: int, method='Fourier', cutoff: float | None = None, n_int: int = N_INT, shift_frequency: bool = True, log_base: int = 10, log_minimum_frequency: float | None = None, absorb_rate: float | None = ABSORB_RATE, int_grid_size: float | None = None, int_lower_bound: float | None = None) -> None

      Add spectral densities to the diagonal correlation function.

      :param sds: The spectral densities.
      :type sds: list[SpectralDensity]
      :param beta: The inverse temperature.
      :type beta: float
      :param n: The number of discrete modes to compute.
      :type n: int
      :param method: The method to compute the diagonal correlation function.
                     Currently, 'TEDOPA', 'Fourier', 'LogFourier', 'EqualReorganizationEnergy' and 'Chebyshev' are supported.
                     'Chebyshev' is not fully implemented yet.
      :type method: str
      :param cutoff: The cutoff frequency. (for the Chebyshev method)
      :type cutoff: float
      :param n_int: The number of points for numerical integration. (for the Chebyshev method)
      :type n_int: int
      :param shift_frequency: Shift the frequency space to avoid the zero-frequency component. (for the Fourier method)
      :type shift_frequency: bool
      :param absorb_rate: The absorption rate. (for the Chebyshev method)
      :type absorb_rate: float



   .. py:method:: __str__() -> None


   .. py:method:: autocorrelation(t: float, t0: float = 0.0) -> complex


.. py:class:: DiscretizationSolver(w: tenso.libs.backend.NDArray, j: tenso.libs.backend.NDArray, beta: float | None, n_max: int)

   .. py:attribute:: underflow
      :value: 1e-14



   .. py:attribute:: frequency_space


   .. py:attribute:: beta


   .. py:attribute:: n_max


   .. py:method:: be_function(x: tenso.libs.backend.NDArray) -> tenso.libs.backend.NDArray
      :staticmethod:



   .. py:method:: __str__() -> str


   .. py:method:: get_star_parameters() -> NotImplementedError
      :abstractmethod:



.. py:class:: Tedopa(w: tenso.libs.backend.NDArray, j: tenso.libs.backend.NDArray, beta: float | None, n_max: int)

   Bases: :py:obj:`DiscretizationSolver`


   .. py:attribute:: _ip


   .. py:attribute:: _ipx


   .. py:attribute:: _alpha


   .. py:attribute:: _beta


   .. py:attribute:: _zeropoints


   .. py:attribute:: _freq_mat


   .. py:method:: get_star_parameters() -> tuple[tenso.libs.backend.NDArray, tenso.libs.backend.NDArray]


   .. py:method:: base_function(k: int, t: tenso.libs.backend.NDArray) -> tenso.libs.backend.NDArray


   .. py:method:: _get_c0() -> float

      Compute the zeroth-order coefficient.



   .. py:method:: _get_chain_frequency() -> tenso.libs.backend.NDArray

      Compute the chain frequencies.



   .. py:method:: _get_chain_coupling() -> tenso.libs.backend.NDArray

      Compute the chain couplings.



   .. py:method:: _get_chain_matrix() -> tenso.libs.backend.NDArray

      Compute the chain matrix.



   .. py:method:: _tridiagonalize() -> tuple[tenso.libs.backend.NDArray, tenso.libs.backend.NDArray]

      Tridiagonalize the chain matrix.



   .. py:method:: _integrate(f: tenso.libs.backend.NDArray) -> float

      Integrate a function with respect to the spectral density.



   .. py:method:: _generate_polynomials() -> None

      Generate the orthogonal polynomials.



.. py:class:: EqualReorganizationEnergy(sds: list[tenso.bath.sd.SpectralDensity], distr: tenso.bath.distribution.BoseEinstein, n: int, int_grid_size: float | None = None)

   Bases: :py:obj:`DiscretizationSolver`


   Discretize the spectral density into finite modes with equal reorganization energy.
   Ref: https://doi.org/10.1002/jcc.24527


   .. py:attribute:: lower_bound


   .. py:attribute:: upper_bound


   .. py:attribute:: distr


   .. py:attribute:: n


   .. py:attribute:: sds


   .. py:attribute:: _freqencies


   .. py:attribute:: _zeropoints


   .. py:method:: _iterative_positive_solver() -> tuple[list[float], list[float]]


   .. py:method:: _iterative_negative_solver() -> tuple[list[float], list[float]]


   .. py:method:: lambda_w(w: float) -> float


   .. py:method:: jw(w)


   .. py:method:: get_star_parameters() -> tuple[tenso.libs.backend.NDArray, tenso.libs.backend.NDArray]


   .. py:method:: base_function(k: int, t: tenso.libs.backend.NDArray) -> tenso.libs.backend.NDArray


.. py:class:: LogFourier(sds: list[tenso.bath.sd.SpectralDensity], distr: tenso.bath.distribution.BoseEinstein, cutoff_frequency: float, n: int, base: float = 10.0, minimum_frequency: float | None = None, _vibrations: Optional[list[tuple[float, float]]] = None)

   Bases: :py:obj:`DiscretizationSolver`


   .. py:attribute:: distr


   .. py:attribute:: omega


   .. py:attribute:: minimum_frequency
      :value: None



   .. py:attribute:: n


   .. py:attribute:: base
      :value: 10.0



   .. py:attribute:: sds


   .. py:attribute:: _freqencies


   .. py:attribute:: _zeropoints


   .. py:method:: get_star_parameters() -> tuple[tenso.libs.backend.NDArray, tenso.libs.backend.NDArray]


   .. py:method:: jw(w)


   .. py:method:: _log_space()


   .. py:method:: base_function(k: int, t: tenso.libs.backend.NDArray) -> tenso.libs.backend.NDArray


.. py:class:: Fourier(sds: list[tenso.bath.sd.SpectralDensity], distr: tenso.bath.distribution.BoseEinstein, cutoff_frequency: float, n: int, shift: bool = True, zero_derivative: Optional[float] = None, _vibrations: Optional[list[tuple[float, float]]] = None)

   Bases: :py:obj:`DiscretizationSolver`


   .. py:attribute:: distr


   .. py:attribute:: omega


   .. py:attribute:: n


   .. py:attribute:: sds


   .. py:attribute:: _freqencies


   .. py:attribute:: _zeropoints


   .. py:method:: get_star_parameters() -> tuple[tenso.libs.backend.NDArray, tenso.libs.backend.NDArray]


   .. py:method:: jw(w)


   .. py:method:: _freq_space()


   .. py:method:: _shift_freq_space()


   .. py:method:: base_function(k: int, t: tenso.libs.backend.NDArray) -> tenso.libs.backend.NDArray


.. py:class:: Chebyshev(w: tenso.libs.backend.NDArray, j: tenso.libs.backend.NDArray, beta: float | None, n_max: int, cutoff_frequency: float | None, absorb_rate: float | None = None)

   Bases: :py:obj:`DiscretizationSolver`


   .. py:attribute:: absorb_rate
      :value: None



   .. py:attribute:: cutoff_frequency


   .. py:attribute:: singular_values


   .. py:attribute:: u_mat


   .. py:method:: get_star_parameters() -> tuple[tenso.libs.backend.NDArray, tenso.libs.backend.NDArray]


   .. py:method:: base_function(k: int, t: tenso.libs.backend.NDArray) -> tenso.libs.backend.NDArray


   .. py:method:: _freq_basis(k: int)


   .. py:method:: _time_basis(k: int)


   .. py:method:: _gen_d_mat()

      Integrals of J_beta(Omega x) eta_i(x) eta_j(x).




   .. py:method:: _gen_c_mat()

      Derivatives connetions bewteen u_k(t).




.. py:data:: beta

