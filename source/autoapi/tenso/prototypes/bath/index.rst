tenso.prototypes.bath
=====================

.. py:module:: tenso.prototypes.bath


Attributes
----------

.. autoapisummary::

   tenso.prototypes.bath.cmap


Functions
---------

.. autoapisummary::

   tenso.prototypes.bath.gen_comb_bcf
   tenso.prototypes.bath.gen_bcf
   tenso.prototypes.bath.gen_tedopa_bcf
   tenso.prototypes.bath.gen_heom_like_star_boson
   tenso.prototypes.bath.gen_star_boson


Module Contents
---------------

.. py:function:: gen_comb_bcf(include_drude: bool, re_d: float, width_d: float, include_brownian: bool, dof_b: int, freq_max_b: float, re_b: float, width_b: float, include_discrete: bool, dof_v: int, freq_max_v: float, re_v: float, temperature: float, decomposition_method: str, n_ltc: int, **kwargs) -> tenso.bath.correlation.Correlation

   Generate a correlation function for a comb-like spectral density.

   :param include_drude: Whether to include the Drude term for the low-frequency modes.
   :type include_drude: bool
   :param re_d: Reorganization energy of the Drude term.
   :type re_d: float
   :param width_d: Cutoff frequency of the Drude term.
   :type width_d: float
   :param include_brownian: Whether to include the Brownian term for the high-frequency modes.
   :type include_brownian: bool
   :param dof_b: Number of Brownian modes.
   :type dof_b: int
   :param freq_max_b: Maximum frequency space that the Brownian modes span.
   :type freq_max_b: float
   :param re_b: Reorganization energy of the Brownian modes.
   :type re_b: float
   :param width_b: Cutoff frequency of the Brownian modes.
   :type width_b: float
   :param include_discrete: Whether to include the discrete vibrational modes.
   :type include_discrete: bool
   :param dof_v: Number of discrete vibrational modes.
   :type dof_v: int
   :param freq_max_v: Maximum frequency space that the discrete vibrational modes span.
   :type freq_max_v: float
   :param re_v: Reorganization energy of the discrete vibrational modes.
   :type re_v: float
   :param temperature: Temperature of the bath.
   :type temperature: float
   :param decomposition_method: Method to decompose the Bose-Einstein distribution.
   :type decomposition_method: str
   :param n_ltc: Number of low-temperature correction terms in the decomposition of the Bose-Einstein distribution.
   :type n_ltc: int
   :param \*\*kwargs: Ignored arguments.
   :type \*\*kwargs: dict

   :returns: The correlation function for the comb-like spectral density.
   :rtype: Correlation


.. py:function:: gen_bcf(include_drude: bool = True, re_d: list[float] | None = None, width_d: list[float] | None = None, include_brownian: bool = True, freq_b: list[float] | None = None, re_b: list[float] | None = None, width_b: list[float] | None = None, include_discrete: bool = True, freq_v: list[float] | None = None, re_v: list[float] | None = None, temperature: float = 300.0, decomposition_method: str = 'Pade', n_ltc: int = 0, include_lindblad: bool = False, use_cross: bool = False, use_ht_function: bool = False, **kwargs) -> tenso.bath.correlation.Correlation

   Generate a correlation function for a composite spectral density for HEOM.

   :param include_drude: Whether to include the Drude term for the low-frequency modes.
   :type include_drude: bool
   :param re_d: Reorganization energies of every Drude modes.
   :type re_d: list[float]
   :param width_d: Cutoff frequencies of every Drude modes.
   :type width_d: list[float]
   :param include_brownian: Whether to include the Brownian term for the high-frequency modes.
   :type include_brownian: bool
   :param freq_b: Frequencies of every Brownian modes.
   :type freq_b: list[float]
   :param re_b: Reorganization energies of every Brownian modes.
   :type re_b: list[float]
   :param width_b: Broadening of every Brownian modes.
   :type width_b: list[float]
   :param include_discrete: Whether to include the discrete vibrational modes.
   :type include_discrete: bool
   :param freq_v: Frequencies of every discrete vibrational modes.
   :type freq_v: list[float]
   :param re_v: Reorganization energies of every discrete vibrational modes.
   :type re_v: list[float]
   :param temperature: Temperature of the bath.
   :type temperature: float
   :param decomposition_method: Method to decompose the Bose-Einstein distribution.
   :type decomposition_method: str
   :param n_ltc: Number of low-temperature correction terms in the decomposition of the Bose-Einstein distribution.
   :type n_ltc: int
   :param include_lindblad: Whether to include the Lindblad rate as in Tanimura's HEOM.
   :type include_lindblad: bool
   :param use_cross: Whether to use the cross-correlation that includes the trigonometric functions.
   :type use_cross: bool
   :param use_ht_function: Whether to use the high-temperature approximation [2 / (beta omega)] of the Bose-Einstein distribution
                           instead of the hyperbolic tangent function.
   :type use_ht_function: bool

   :returns: The correlation function for the composite spectral density.
   :rtype: Correlation


.. py:function:: gen_tedopa_bcf(re_d: list[float], width_d: list[float], freq_b: list[float], re_b: list[float], width_b: list[float], temperature: float, frequency_cutoff: float, n_frequency: int, n_discretization: int, cutoff_type: str = 'Lorentz', include_brownian: bool = True, include_drude: bool = True, **kwargs) -> tenso.bath.star.StarBosons

   Generate a correlation function for a composite spectral density based on TEDOPA-type of decompostion
   but without changing to the chain-like picture.

   :param include_drude: Whether to include the Drude term for the low-frequency modes.
   :type include_drude: bool
   :param re_d: Reorganization energy of the Drude term.
   :type re_d: float
   :param width_d: Cutoff frequency of the Drude term.
   :type width_d: float
   :param cutoff_type: Type of cutoff function for the Drude term.
                       Allowed values are 'Lorentz' (Drude-Lorentz) and 'Exp' (Ohmic with exponential cutoff).
   :type cutoff_type: str
   :param include_brownian: Whether to include the Brownian term for the high-frequency modes.
   :type include_brownian: bool
   :param freq_b: Frequencies of the Brownian modes.
   :type freq_b: list[float]
   :param re_b: Reorganization energies of the Brownian modes.
   :type re_b: list[float]
   :param width_b: Broadening of the Brownian modes.
   :type width_b: list[float]
   :param temperature: Temperature of the bath.
   :type temperature: float
   :param frequency_cutoff: Cutoff frequency for the spectral density.
   :type frequency_cutoff: float
   :param n_frequency: Number of frequency points for the spectral density.
   :type n_frequency: int
   :param n_discretization: Number of discretization points for the spectral density.
   :type n_discretization: int
   :param \*\*kwargs: Ignored arguments.
   :type \*\*kwargs: dict

   :returns: The correlation function for the composite spectral density.
   :rtype: StarBosons


.. py:function:: gen_heom_like_star_boson(include_drude: bool = True, re_d: list[float] | None = None, width_d: list[float] | None = None, include_brownian: bool = True, freq_b: list[float] | None = None, re_b: list[float] | None = None, width_b: list[float] | None = None, include_discrete: bool = True, freq_v: list[float] | None = None, re_v: list[float] | None = None, temperature: float = 300.0, decomposition_method: str = 'Pade', n_ltc: int = 0, include_lindblad: bool = False, use_cross: bool = False, use_ht_function: bool = False, **kwargs) -> tenso.bath.star.StarBosons

   Generate a correlation function for a composite spectral density for HSEOM but based on HEOM-style BCF decompostion.

   :param include_drude: Whether to include the Drude term for the low-frequency modes.
   :type include_drude: bool
   :param re_d: Reorganization energies of every Drude modes.
   :type re_d: list[float]
   :param width_d: Cutoff frequencies of every Drude modes.
   :type width_d: list[float]
   :param include_brownian: Whether to include the Brownian term for the high-frequency modes.
   :type include_brownian: bool
   :param freq_b: Frequencies of every Brownian modes.
   :type freq_b: list[float]
   :param re_b: Reorganization energies of every Brownian modes.
   :type re_b: list[float]
   :param width_b: Broadening of every Brownian modes.
   :type width_b: list[float]
   :param include_discrete: Whether to include the discrete vibrational modes.
   :type include_discrete: bool
   :param freq_v: Frequencies of every discrete vibrational modes.
   :type freq_v: list[float]
   :param re_v: Reorganization energies of every discrete vibrational modes.
   :type re_v: list[float]
   :param temperature: Temperature of the bath.
   :type temperature: float
   :param decomposition_method: Method to decompose the Bose-Einstein distribution.
   :type decomposition_method: str
   :param n_ltc: Number of low-temperature correction terms in the decomposition of the Bose-Einstein distribution.
   :type n_ltc: int
   :param include_lindblad: Whether to include the Lindblad rate as in Tanimura's HEOM.
   :type include_lindblad: bool
   :param use_cross: Whether to use the cross-correlation that includes the trigonometric functions.
   :type use_cross: bool
   :param use_ht_function: Whether to use the high-temperature approximation [2 / (beta omega)] of the Bose-Einstein distribution
                           instead of the hyperbolic tangent function.
   :type use_ht_function: bool

   :returns: The correlation function for the composite spectral density.
   :rtype: Correlation


.. py:function:: gen_star_boson(temperature: float, cutoff: float, n_discretization: int, re_d: list[float] = None, width_d: list[float] = None, freq_b: list[float] = None, re_b: list[float] = None, width_b: list[float] = None, freq_v: list[float] = None, re_v: list[float] = None, include_drude: bool = True, include_brownian: bool = True, include_discrete: bool = True, discretization_method: str = 'Fourier', ohmic_type: str = 'Lorentz', shift_frequency: bool = True, absorb_rate: None | float = None, log_base: int = 10, log_minimum_frequency: None | float = None, int_grid_size: float | None = None, int_lower_bound: float | None = None, **kwargs) -> tenso.bath.star.StarBosons

   Generate a correlation function for a composite spectral density for the star-like decomposition as in spin-boson model.

   :param include_drude: Whether to include the Drude term for the low-frequency modes.
   :type include_drude: bool
   :param re_d: Reorganization energies of the Drude modes.
   :type re_d: list[float]
   :param width_d: Cutoff frequencies of the Drude modes.
   :type width_d: list[float]
   :param include_brownian: Whether to include the Brownian term for the high-frequency modes.
   :type include_brownian: bool
   :param freq_b: Frequencies of the Brownian modes.
   :type freq_b: list[float]
   :param re_b: Reorganization energies of the Brownian modes.
   :type re_b: list[float]
   :param width_b: Broadening of the Brownian modes.
   :type width_b: list[float]
   :param include_discrete: Whether to include the discrete vibrational modes.
   :type include_discrete: bool
   :param freq_v: Frequencies of the discrete vibrational modes.
   :type freq_v: list[float]
   :param re_v: Reorganization energies of the discrete vibrational modes.
   :type re_v: list[float]
   :param temperature: Temperature of the bath.
   :type temperature: float
   :param cutoff: Cutoff frequency for the spectral density.
   :type cutoff: float
   :param n_discretization: Number of discretization points for the spectral density.
   :type n_discretization: int
   :param discretization_method: Method to discretize the spectral density.
                                 Allowed values are 'Fourier', 'LogFourier', 'EqualReorganizationEnergy', 'Chebyshev', and 'TEDOPA'.
                                 Currently, only 'Fourier', 'LogFourier', 'EqualReorganizationEnergy' are tested.
   :type discretization_method: str
   :param ohmic_type: Type of the Drude term.
                      Allowed values are 'Lorentz' (Drude-Lorentz) and 'Exp' (Ohmic with exponential cutoff).
   :type ohmic_type: str
   :param shift_frequency: Whether to shift the frequency to the positive domain.
   :type shift_frequency: bool
   :param \*\*kwargs: Ignored arguments.
   :type \*\*kwargs: dict

   :returns: The correlation function for the composite spectral density.
   :rtype: StarBosons


.. py:data:: cmap

