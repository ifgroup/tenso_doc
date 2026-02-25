tenso.mctdh.eom
===============

.. py:module:: tenso.mctdh.eom

.. autoapi-nested-parse::

   Generating the derivative of the extended rho in SoP formalism.



Attributes
----------

.. autoapisummary::

   tenso.mctdh.eom.EPSILON
   tenso.mctdh.eom.PREFIX
   tenso.mctdh.eom.PREFIX_SYS


Classes
-------

.. autoapisummary::

   tenso.mctdh.eom._BathOp
   tenso.mctdh.eom.Hierachy
   tenso.mctdh.eom.FrameFactory


Functions
---------

.. autoapisummary::

   tenso.mctdh.eom.trace


Module Contents
---------------

.. py:data:: EPSILON
   :value: 1e-14


.. py:data:: PREFIX
   :value: '[HS]'


.. py:data:: PREFIX_SYS
   :value: '[S]'


.. py:function:: trace(tensor1: tenso.libs.backend.OptArray, tensor2: tenso.libs.backend.OptArray, ax: int) -> tenso.libs.backend.OptArray

   Complex conjugate not included



.. py:class:: _BathOp(dim: int)

   .. py:attribute:: up


   .. py:attribute:: down


   .. py:attribute:: number


.. py:class:: Hierachy(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, sys_ends: list[tenso.state.pureframe.End], bath_ends: list[list[tenso.state.pureframe.End]], sys_dims: list[int], bath_dims: list[list[int]])

   .. py:attribute:: sys_ends


   .. py:attribute:: bath_ends


   .. py:attribute:: dims
      :type:  dict[tenso.state.pureframe.End, int]


   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: _bathops


   .. py:attribute:: _terminators
      :type:  dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]


   .. py:attribute:: _point_visitor


   .. py:attribute:: _node_axes


   .. py:method:: get_densities(state: tenso.state.puremodel.Model) -> dict[tenso.state.pureframe.Point, tenso.libs.backend.OptArray]


   .. py:method:: tdse_list(sys_hamiltonians: list[None | tenso.libs.backend.ArrayLike], sys_couplings: list[dict[int, tenso.libs.backend.ArrayLike]]) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: heom_list(sys_ops: list[dict[int, tenso.libs.backend.ArrayLike]], correlations: list[tenso.bath.star.StarBosons]) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: bath_q_list(correlations: list[tenso.bath.star.StarBosons]) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: bath_q2_list(correlations: list[tenso.bath.star.StarBosons]) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: _single_heom_list(sys_idxs: list[int], sys_ops: list[tenso.libs.backend.ArrayLike], bath_idx: int, correlation: tenso.bath.star.StarBosons) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: initialize_pure_state(local_wfns: list[tenso.libs.backend.ArrayLike], rank: int, local_hs: None | list[None | tenso.libs.backend.ArrayLike] = None) -> tenso.state.puremodel.Model


   .. py:method:: _init_number_basis(k_end: tenso.state.pureframe.End)


   .. py:method:: _init_dvr_basis(state: tenso.state.puremodel.Model, k_end: tenso.state.pureframe.End, basis: tenso.basis.dvr.DiscreteVariationalRepresentation)


.. py:class:: FrameFactory(sys_dof: int, bath_dofs: list[int])

   .. py:attribute:: prefix
      :value: '[HS]'



   .. py:attribute:: n_bath


   .. py:attribute:: sys_dof
      :type:  int


   .. py:attribute:: bath_dofs
      :type:  list[int]


   .. py:attribute:: dof


   .. py:attribute:: sys_ends
      :type:  list[tenso.state.pureframe.End]


   .. py:attribute:: bath_ends
      :type:  list[list[tenso.state.pureframe.End]]


   .. py:attribute:: ends
      :type:  list[tenso.state.pureframe.End]


   .. py:attribute:: _node_counter
      :type:  int
      :value: 0



   .. py:method:: _new_node() -> tenso.state.pureframe.Node


   .. py:method:: naive() -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: tree(importances: None | dict[tenso.state.pureframe.End, int] = None, n_ary: int = 2) -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: train(end_order: list[tenso.state.pureframe.End]) -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


