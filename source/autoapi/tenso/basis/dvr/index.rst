tenso.basis.dvr
===============

.. py:module:: tenso.basis.dvr

.. autoapi-nested-parse::

   A Simple DVR Program

   .. rubric:: References

   .. [1] http://www.pci.uni-heidelberg.de/tc/usr/mctdh/lit/NumericalMethods.pdf



Attributes
----------

.. autoapisummary::

   tenso.basis.dvr.b


Classes
-------

.. autoapisummary::

   tenso.basis.dvr.DiscreteVariationalRepresentation
   tenso.basis.dvr.SincDVR
   tenso.basis.dvr.SineDVR


Module Contents
---------------

.. py:class:: DiscreteVariationalRepresentation(num: int)

   .. py:attribute:: n


   .. py:attribute:: grid_points


   .. py:attribute:: dvr2fbr_mat
      :type:  Optional[tenso.libs.backend.NDArray]
      :value: None



   .. py:property:: q_mat
      :type: tenso.libs.backend.NDArray


      q in DVR basis.


   .. py:property:: dq_mat
      :type: tenso.libs.backend.NDArray



   .. py:property:: dq2_mat
      :type: tenso.libs.backend.NDArray



   .. py:property:: creation_mat
      :type: tenso.libs.backend.NDArray



   .. py:property:: annihilation_mat
      :type: tenso.libs.backend.NDArray



   .. py:property:: fock2dvr_mat
      :type: tenso.libs.backend.NDArray



   .. py:method:: eigen2dvr_mat(ham) -> tenso.libs.backend.NDArray


   .. py:method:: fbr_func(i: int) -> Callable[[tenso.libs.backend.NDArray], tenso.libs.backend.NDArray]

      `i`-th FBR basis function.



   .. py:property:: numberer_mat
      :type: tenso.libs.backend.NDArray



.. py:class:: SincDVR(start: float, stop: float, num: int)

   Bases: :py:obj:`DiscreteVariationalRepresentation`


   .. py:attribute:: length


   .. py:attribute:: grid_points


   .. py:attribute:: n


   .. py:attribute:: delta


   .. py:property:: dq_mat
      :type: tenso.libs.backend.NDArray



   .. py:property:: dq2_mat
      :type: tenso.libs.backend.NDArray



.. py:class:: SineDVR(start: float, stop: float, num: int)

   Bases: :py:obj:`DiscreteVariationalRepresentation`


   .. py:attribute:: grid_points


   .. py:attribute:: n


   .. py:attribute:: length


   .. py:attribute:: dvr2fbr_mat


   .. py:property:: q_mat
      :type: tenso.libs.backend.NDArray


      q in DVR basis.


   .. py:property:: abs_q_mat
      :type: tenso.libs.backend.NDArray


      q in DVR basis.


   .. py:property:: abs_dq_mat
      :type: tenso.libs.backend.NDArray


      q in DVR basis.


   .. py:property:: dq_mat
      :type: tenso.libs.backend.NDArray


      d/dq in DVR basis.


   .. py:property:: dq2_mat
      :type: tenso.libs.backend.NDArray


      d^2/dq^2 in DVR basis.


   .. py:property:: t_mat

      Return the kinetic energy matrix in DVR.
      :returns: A 2-d matrix.
      :rtype: (n, n) np.ndarray


   .. py:property:: fock2dvr_mat
      :type: tenso.libs.backend.NDArray



   .. py:property:: height


   .. py:method:: fbr_func(i: int) -> Callable[[tenso.libs.backend.NDArray], tenso.libs.backend.NDArray]

      `i`-th FBR basis function.



   .. py:method:: fbr2cont(vec)

      Transform a vector from FBR to the spatial function.




   .. py:method:: dvr2cont(vec)


.. py:data:: b

