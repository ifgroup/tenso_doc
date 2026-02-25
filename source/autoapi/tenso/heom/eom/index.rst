tenso.heom.eom
==============

.. py:module:: tenso.heom.eom

.. autoapi-nested-parse::

   Generating the derivative of the extended rho in SoP formalism.



Attributes
----------

.. autoapisummary::

   tenso.heom.eom.EPSILON


Classes
-------

.. autoapisummary::

   tenso.heom.eom._BathOp
   tenso.heom.eom._DVRBathOp
   tenso.heom.eom.Hierachy
   tenso.heom.eom.FrameFactory


Functions
---------

.. autoapisummary::

   tenso.heom.eom.terminate


Module Contents
---------------

.. py:data:: EPSILON
   :value: 1e-14


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


.. py:class:: Hierachy(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, sys_ket_end: tenso.state.pureframe.End, sys_bra_end: tenso.state.pureframe.End, bath_ends: list[tenso.state.pureframe.End], sys_dim: int, bath_dims: list[int], bases: tenso.libs.utils.Optional[dict[tenso.state.pureframe.End, tenso.basis.dvr.DiscreteVariationalRepresentation]] = None)

   .. py:attribute:: sys_ket_end


   .. py:attribute:: sys_bra_end


   .. py:attribute:: bath_ends


   .. py:attribute:: dims
      :type:  dict[tenso.state.pureframe.End, int]


   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: _bases
      :type:  dict[tenso.state.pureframe.End, tenso.basis.dvr.DiscreteVariationalRepresentation]
      :value: None



   .. py:attribute:: _bathops


   .. py:attribute:: _terminators
      :type:  dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]


   .. py:attribute:: _terminate_visitor


   .. py:attribute:: _node_axes


   .. py:method:: lvn_list(sys_hamiltonian: tenso.libs.backend.ArrayLike) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: lindblad_list(sys_op: tenso.libs.backend.ArrayLike, lindblad_rate: float | None) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: i_heom_list(sys_op: tenso.libs.backend.ArrayLike, correlation: tenso.bath.correlation.Correlation, metric: Literal['re', 'abs'] | complex = 're') -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]

      Interaction picture of oscillating heom mode




   .. py:method:: heom_list(sys_op: tenso.libs.backend.ArrayLike, correlation: tenso.bath.correlation.Correlation, metric: Literal['re', 'abs'] | complex = 're') -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: _adm_factor(k: int, c: tenso.bath.correlation.Correlation, metric: Literal['re', 'abs'] | complex = 're')
      :staticmethod:



   .. py:method:: initialize_state(rdo: tenso.libs.backend.ArrayLike, rank: int) -> tenso.state.puremodel.Model

      Assume Ends sys_i and sys_j are attached to the root node axes 0 and 1.



   .. py:method:: _init_number_basis(k_end: tenso.state.pureframe.End)


   .. py:method:: _init_dvr_basis(state: tenso.state.puremodel.Model, k_end: tenso.state.pureframe.End, basis: tenso.basis.dvr.DiscreteVariationalRepresentation)


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


   .. py:attribute:: bath_ends
      :type:  list[tenso.state.pureframe.End]


   .. py:attribute:: _node_counter
      :type:  int
      :value: 0



   .. py:method:: _new_node() -> tenso.state.pureframe.Node


   .. py:method:: naive() -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: tree(bath_importances: None | list[int] = None, n_ary: int = 2) -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


   .. py:method:: train() -> tuple[tenso.state.pureframe.Frame, tenso.state.pureframe.Node]


