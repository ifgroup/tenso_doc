tenso.heom.multieom
===================

.. py:module:: tenso.heom.multieom

.. autoapi-nested-parse::

   Generating the derivative of the extended rho in SoP formalism.



Attributes
----------

.. autoapisummary::

   tenso.heom.multieom.EPSILON


Classes
-------

.. autoapisummary::

   tenso.heom.multieom.Hierachy
   tenso.heom.multieom.FrameFactory


Module Contents
---------------

.. py:data:: EPSILON
   :value: 1e-14


.. py:class:: Hierachy(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, sys_ket_ends: list[tenso.state.pureframe.End], sys_bra_ends: list[tenso.state.pureframe.End], bath_ends: list[list[tenso.state.pureframe.End]], sys_dims: list[int], bath_dims: list[list[int]], bases: tenso.libs.utils.Optional[dict[tenso.state.pureframe.End, tenso.basis.dvr.DiscreteVariationalRepresentation]] = None)

   .. py:attribute:: sys_ket_ends


   .. py:attribute:: sys_bra_ends


   .. py:attribute:: bath_ends


   .. py:attribute:: dims
      :type:  dict[tenso.state.pureframe.End, int]


   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: _bathops


   .. py:attribute:: _bases
      :type:  dict[tenso.state.pureframe.End, tenso.basis.dvr.DiscreteVariationalRepresentation]
      :value: None



   .. py:attribute:: _terminators
      :type:  dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]


   .. py:attribute:: _terminate_visitor


   .. py:attribute:: _node_axes


   .. py:method:: lvn_list(sys_hamiltonians: list[None | tenso.libs.backend.ArrayLike], sys_couplings: list[dict[int, tenso.libs.backend.ArrayLike]]) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: lindblad_list(sys_ops: list[dict[int, tenso.libs.backend.ArrayLike]], lindblad_rates: list[float | None]) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: _single_lindblad_list(sys_idxs: list[int], sys_ops: list[tenso.libs.backend.ArrayLike], lindblad_rate: float) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: heom_list(sys_ops: list[dict[int, tenso.libs.backend.ArrayLike]], correlations: list[tenso.bath.correlation.Correlation], metric: Literal['re', 'abs'] | complex = 're') -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: _single_heom_list(sys_idxs: list[int], sys_ops: list[tenso.libs.backend.ArrayLike], bath_idx: int, correlation: tenso.bath.correlation.Correlation, metric: Literal['re', 'abs'] | complex) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: _adm_factor(k: int, c: tenso.bath.correlation.Correlation, metric: Literal['re', 'abs'] | complex = 're')
      :staticmethod:



   .. py:method:: initialize_pure_state(local_wfns: list[tenso.libs.backend.ArrayLike], rank: int, local_hs: None | list[None | tenso.libs.backend.ArrayLike] = None) -> tenso.state.puremodel.Model


   .. py:method:: _init_number_basis(k_end: tenso.state.pureframe.End)


   .. py:method:: _init_dvr_basis(state: tenso.state.puremodel.Model, k_end: tenso.state.pureframe.End, basis: tenso.basis.dvr.DiscreteVariationalRepresentation)


   .. py:method:: get_rdo_element(edo: tenso.state.puremodel.Model, sys_is: list[None | int], sys_js: list[None | int]) -> complex


   .. py:method:: get_rdo(edo: tenso.state.puremodel.Model) -> tenso.libs.backend.OptArray
      :abstractmethod:



.. py:class:: FrameFactory(sys_dof: int, bath_dofs: list[int])

   .. py:attribute:: prefix
      :value: '[MH]'



   .. py:attribute:: n_bath


   .. py:attribute:: sys_dof
      :type:  int


   .. py:attribute:: bath_dofs
      :type:  list[int]


   .. py:attribute:: dof


   .. py:attribute:: sys_ket_ends
      :type:  list[tenso.state.pureframe.End]


   .. py:attribute:: sys_bra_ends
      :type:  list[tenso.state.pureframe.End]


   .. py:attribute:: bath_ends
      :type:  list[list[tenso.state.pureframe.End]]


   .. py:attribute:: ends


   .. py:attribute:: _node_counter
      :type:  int
      :value: 0



   .. py:method:: _new_node() -> tenso.state.pureframe.Node


   .. py:method:: naive() -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: tree(importances: None | dict[tenso.state.pureframe.End, int] = None, n_ary: int = 2) -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: train(end_order: list[tenso.state.pureframe.End]) -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


