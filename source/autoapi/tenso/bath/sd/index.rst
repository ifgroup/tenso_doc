tenso.bath.sd
=============

.. py:module:: tenso.bath.sd

.. autoapi-nested-parse::

   Spectral density factory



Attributes
----------

.. autoapisummary::

   tenso.bath.sd.unit


Classes
-------

.. autoapisummary::

   tenso.bath.sd.SpectralDensity
   tenso.bath.sd.Drude
   tenso.bath.sd.OhmicExp
   tenso.bath.sd.OhmicTruncated
   tenso.bath.sd.OhmicSemicircular
   tenso.bath.sd.UnderdampedGaussian
   tenso.bath.sd.UnderdampedBrownian
   tenso.bath.sd.OverdampedBrownian
   tenso.bath.sd.CriticallyDampedBrownian
   tenso.bath.sd.BrownianOscillator
   tenso.bath.sd.SuperCriticalDamping


Module Contents
---------------

.. py:class:: SpectralDensity

   Template for a spectral density.


   .. py:attribute:: FREQ_MIN
      :value: 1e-14



   .. py:attribute:: FREQ_MAX
      :value: 1000.0



   .. py:method:: autocorrelation(t: float, beta: Optional[float] = None) -> complex


   .. py:method:: function(w: complex) -> complex
      :abstractmethod:



   .. py:method:: get_residues_poles() -> tuple[list[complex], list[complex]]
      :abstractmethod:


      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:class:: Drude(reorganization_energy: float, relaxation: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: l


   .. py:attribute:: g


   .. py:method:: function(w: complex) -> complex


   .. py:method:: get_residues_poles() -> tuple[list[complex], list[complex]]

      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:class:: OhmicExp(reorganization_energy: float, cutoff: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: l


   .. py:attribute:: g


   .. py:method:: function(w: complex) -> complex


   .. py:method:: get_residues_poles()

      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:class:: OhmicTruncated(reorganization_energy: float, cutoff: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: l


   .. py:attribute:: g


   .. py:method:: function(w: complex) -> complex


.. py:class:: OhmicSemicircular(reorganization_energy: float, cutoff: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: h


   .. py:attribute:: g


   .. py:method:: function(w: complex) -> complex


.. py:class:: UnderdampedGaussian(reorganization_energy: float, frequency: float, relaxation: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: omega


   .. py:attribute:: gamma


   .. py:attribute:: lambda_


   .. py:method:: function(w: complex) -> complex


.. py:class:: UnderdampedBrownian(reorganization_energy: float, frequency: float, relaxation: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: omega


   .. py:attribute:: gamma


   .. py:attribute:: lambda_


   .. py:method:: function(w: complex) -> complex


   .. py:method:: get_residues_poles() -> tuple[list[complex], list[complex]]

      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:class:: OverdampedBrownian(reorganization_energy: float, frequency: float, relaxation: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: omega


   .. py:attribute:: gamma


   .. py:attribute:: lambda_


   .. py:method:: function(w: complex) -> complex


   .. py:method:: get_residues_poles() -> tuple[list[complex], list[complex]]

      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:class:: CriticallyDampedBrownian(reorganization_energy: float, relaxation: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: gamma


   .. py:attribute:: lambda_


   .. py:method:: function(w: complex) -> complex


   .. py:method:: get_residues_poles()

      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:class:: BrownianOscillator(reorganization_energy: float, relaxation: float, intrinsic_frequency: float)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: gamma


   .. py:attribute:: lambda_


   .. py:attribute:: omega0


   .. py:attribute:: omega1


   .. py:method:: function(w: complex) -> complex


   .. py:method:: get_residues_poles()

      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:class:: SuperCriticalDamping(reorganization_energy: float, relaxation: float, order=3)

   Bases: :py:obj:`SpectralDensity`


   Template for a spectral density.


   .. py:attribute:: gamma


   .. py:attribute:: lambda_


   .. py:attribute:: order
      :value: 3



   .. py:attribute:: norm
      :value: 0.6366197723675814



   .. py:method:: function(w: complex) -> complex


   .. py:method:: get_residues_poles()

      Get (-2 PI I * residues) and poles of the spectral density in the lower half-plane.

      :returns: List of (-2 PI I * residues) and poles.
      :rtype: tuple[list[complex], list[complex]]



.. py:data:: unit

