tenso.qle.eom
=============

.. py:module:: tenso.qle.eom

.. autoapi-nested-parse::

   Generating the derivative of the pseudo mode rho in SoP formalism.

   The density operator is represented as a tensor network with a "locally entangled" structure.
   That is, for each node attaced to the leaf ends, the tensor of 3 degrees, where the first links
   towards the root node, the second link is one ket end, and the third link the corresponding bra end.
   In this way, the trace of the density operator can be computed by (1) for the leaf nodes A_{ijk}:
       T_i = A_{ijj}
   and (2) for the nodes are not leaf nodes B_{aij}, the trace is computed by contracting
       T_a = B_{aij} T_i T_j
   and suppose the root node is C_{mna} with m and n are the ket and bra ends for the system, then
       rho_{mn} = C_{mna} T_a
   gives the reduced density operator for the system.



Attributes
----------

.. autoapisummary::

   tenso.qle.eom.EPSILON


Classes
-------

.. autoapisummary::

   tenso.qle.eom._BathOp
   tenso.qle.eom._DVRBathOp
   tenso.qle.eom.Hierachy
   tenso.qle.eom.FrameFactory


Functions
---------

.. autoapisummary::

   tenso.qle.eom.local_trace
   tenso.qle.eom.terminate


Module Contents
---------------

.. py:data:: EPSILON
   :value: 1e-14


.. py:function:: local_trace(tensor: tenso.libs.backend.OptArray, bra_ax: int, ket_ax: int) -> tenso.libs.backend.OptArray

   Computing the local trace of a tensor network.

   :param tensor: The tensor to compute the trace.
   :type tensor: OptArray
   :param bra_ax: The axis index for the bra end.
   :type bra_ax: int
   :param ket_ax: The axis index for the ket end.
   :type ket_ax: int

   :returns: The tensor with the bra and ket axes traced out.
   :rtype: OptArray


.. py:function:: terminate(tensor: tenso.libs.backend.OptArray, term_dict: dict[int, tenso.libs.backend.OptArray])

.. py:class:: _BathOp(dim: int)

   .. py:attribute:: up


   .. py:attribute:: down


   .. py:attribute:: number


.. py:class:: _DVRBathOp(dvr: tenso.basis.dvr.DiscreteVariationalRepresentation)

   Bases: :py:obj:`_BathOp`


   .. py:attribute:: up


   .. py:attribute:: down


   .. py:attribute:: number


.. py:class:: Hierachy(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, sys_ket_end: tenso.state.pureframe.End, sys_bra_end: tenso.state.pureframe.End, bath_ket_ends: list[tenso.state.pureframe.End], bath_bra_ends: list[tenso.state.pureframe.End], sys_dim: int, bath_dims: list[int], bases: tenso.libs.utils.Optional[dict[int, tenso.basis.dvr.DiscreteVariationalRepresentation]] = None)

   .. py:attribute:: sys_ket_end


   .. py:attribute:: sys_bra_end


   .. py:attribute:: bath_ket_ends


   .. py:attribute:: bath_bra_ends


   .. py:attribute:: dims
      :type:  dict[tenso.state.pureframe.End, int]


   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: _bases
      :type:  dict[int, tenso.basis.dvr.DiscreteVariationalRepresentation] | None
      :value: None



   .. py:attribute:: _bathops


   .. py:attribute:: _terminate_visitor


   .. py:attribute:: _node_axes


   .. py:method:: lvn_list(sys_hamiltonian: tenso.libs.backend.ArrayLike) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: _uhp_sqrt(c: complex) -> tuple[float, float]
      :staticmethod:


      Get the square root of a complex number in the upper half plane.
      The square root is defined as:
          sqrt(c) = g - i * epsilon,
      where g is real and epsilon >= 0.

      :returns: float
                epsilon: float
      :rtype: g



   .. py:method:: _boolean(z: complex) -> bool
      :staticmethod:



   .. py:method:: quasi_lindblad_list(sys_op: tenso.libs.backend.ArrayLike, correlation: tenso.bath.correlation.Correlation, hermite: bool = False) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]

      Quasi-Lindblad part of the EOM.




   .. py:method:: _ql_list_kj(k, j, w_kj, eta_kj) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]

      Quasi-Lindblad part between the k-th and j-th bath modes.




   .. py:method:: _ql_list_k(sys_op: tenso.libs.backend.OptArray, k: int, w_k: float, eta_k: float, g_k: float, epsilon_k: float, z_k: bool = True) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]

      Quasi-Lindblad part for the k-th bath mode.




   .. py:method:: _qlh_list_k(sys_op: tenso.libs.backend.OptArray, k: int, w_k: float, eta_k: float, g_k: float, epsilon_k: float, z_k: bool = True) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]

      Quasi-Lindblad part for the k-th bath mode.
      Assume sys_op is Hermitian.



   .. py:method:: initialize_state(rdo: tenso.libs.backend.ArrayLike, rank: int) -> tenso.state.puremodel.Model

      Assume Ends sys_i and sys_j are attached to the root node axes 0 and 1.



   .. py:method:: _get_local_trace(model: tenso.state.puremodel.Model) -> dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]

      Initialize the number basis for the bath ends.




   .. py:method:: get_rdo(edo: tenso.state.puremodel.Model) -> tenso.libs.backend.OptArray


.. py:class:: FrameFactory(bath_dof: int)

   .. py:attribute:: prefix
      :value: '[H]'



   .. py:attribute:: bath_dof
      :type:  int


   .. py:attribute:: sys_ket_end
      :type:  tenso.state.pureframe.End


   .. py:attribute:: sys_bra_end
      :type:  tenso.state.pureframe.End


   .. py:attribute:: bath_ket_ends
      :type:  list[tenso.state.pureframe.End]


   .. py:attribute:: bath_bra_ends
      :type:  list[tenso.state.pureframe.End]


   .. py:attribute:: _node_counter
      :type:  int
      :value: 0



   .. py:method:: _new_node() -> tenso.state.pureframe.Node


   .. py:method:: naive() -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: tree(bath_importances: None | list[int] = None, n_ary: int = 2) -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: train() -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


