tenso.operator.sparse
=====================

.. py:module:: tenso.operator.sparse


Classes
-------

.. autoapisummary::

   tenso.operator.sparse.SparseSPO
   tenso.operator.sparse.SPOKet
   tenso.operator.sparse.ListModelInnerProduct
   tenso.operator.sparse.SparseSandwich
   tenso.operator.sparse._ComplexSingleTerm
   tenso.operator.sparse._SVDInfoCache
   tenso.operator.sparse._ProdEOM
   tenso.operator.sparse._DirectProdEOM
   tenso.operator.sparse.SparsePropagator
   tenso.operator.sparse.DynamicalSparsePropagator


Functions
---------

.. autoapisummary::

   tenso.operator.sparse._stack_orth
   tenso.operator.sparse._truncate
   tenso.operator.sparse._find_truncate_index
   tenso.operator.sparse._one_site_split
   tenso.operator.sparse._one_site_merge
   tenso.operator.sparse._two_site_merge
   tenso.operator.sparse._partitions
   tenso.operator.sparse._adaptive_two_site_split
   tenso.operator.sparse._modify_frame
   tenso.operator.sparse._two_site_split


Module Contents
---------------

.. py:function:: _stack_orth(tensor1: tenso.libs.backend.OptArray, tensor2: tenso.libs.backend.OptArray, axis: int, _dummy=True) -> tenso.libs.backend.OptArray

   Stack the tensor1 and tensor2 along axis.


.. py:function:: _truncate(tensor: tenso.libs.backend.OptArray, rank: int, axis: int)

   Truncate the tensor along axis.


.. py:function:: _find_truncate_index(s: tenso.libs.backend.OptArray, atol: float) -> int

.. py:function:: _one_site_split(array: tenso.libs.backend.OptArray, i: int) -> tuple[tenso.libs.backend.OptArray, tenso.libs.backend.OptArray]

.. py:function:: _one_site_merge(array: tenso.libs.backend.OptArray, j: int, from_: tenso.libs.backend.OptArray) -> tenso.libs.backend.OptArray

.. py:function:: _two_site_merge(state: tenso.state.puremodel.Model, p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int) -> tenso.libs.backend.OptArray

.. py:function:: _partitions(lst: list[int], order: int) -> list[tuple[list[int], list[int]]]

.. py:function:: _adaptive_two_site_split(state: tenso.state.puremodel.Model, p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int, from_: tenso.libs.backend.OptArray, target_rank: None | int = None, atol: None | float = None) -> tuple[tenso.libs.backend.OptArray, list[int], tenso.libs.backend.OptArray, list[int]]

.. py:function:: _modify_frame(frame: tenso.state.pureframe.Frame, p, p_axes, q, q_axes) -> tenso.state.pureframe.Frame

   Modify the frame to include the new axes for p and q.


.. py:function:: _two_site_split(state: tenso.state.puremodel.Model, p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int, from_: tenso.libs.backend.OptArray, target_rank: None | int = None, atol: None | float = None, ratio: None | float = None) -> tuple[tenso.libs.backend.OptArray, tenso.libs.backend.OptArray]

.. py:class:: SparseSPO(op_list: list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]], f_list: None | Callable[[float], list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]] = None, initial_time: float = 0.0)

   .. py:attribute:: n_ti


   .. py:attribute:: op_list


   .. py:attribute:: n_td
      :value: 0



   .. py:attribute:: f_list
      :value: None



   .. py:attribute:: dims
      :type:  dict[tenso.state.pureframe.End, int]


   .. py:method:: __add__(other: SparseSPO) -> SparseSPO


   .. py:method:: get_ti_terms() -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:method:: get_td_terms(t: float) -> list[dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]]


   .. py:property:: ends
      :type: set[tenso.state.pureframe.End]



.. py:class:: SPOKet(op: SparseSPO, state: tenso.state.puremodel.Model, frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, time=0.0)

   Intermediate class for the sparse operations in the model.


   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: _node_link_visitor


   .. py:attribute:: op_list


   .. py:attribute:: is_time_dependent


   .. py:attribute:: original_state


   .. py:attribute:: state_list


   .. py:method:: _operate() -> list[tenso.state.puremodel.Model]


   .. py:method:: canonicalize() -> None

      Canonicalize the state.



   .. py:method:: _move(state: tenso.state.puremodel.Model, p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int) -> None


   .. py:method:: close_with_bra(bra: tenso.state.puremodel.Model | None = None) -> complex

      Calculate the inner product.



   .. py:method:: close_with_conj(bras: SPOKet) -> complex

      Calculate the inner product.



.. py:class:: ListModelInnerProduct(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, ket_states: list[tenso.state.puremodel.Model], bra_states: list[tenso.state.puremodel.Model] | None = None)

   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: ket_states


   .. py:method:: forward() -> complex

      Actuall calculate the inner product.



.. py:class:: SparseSandwich(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, ket_state: tenso.state.puremodel.Model, bra_state: tenso.state.puremodel.Model | None = None, op: SparseSPO | None = None, time=0.0)

   .. py:attribute:: op
      :value: None



   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: ket


   .. py:attribute:: bra


   .. py:attribute:: n_terms


   .. py:attribute:: _td_eoms
      :type:  list[_ComplexSingleTerm]


   .. py:method:: forward() -> complex

      Calculate the inner product.



.. py:class:: _ComplexSingleTerm(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, bra_state: tenso.state.puremodel.Model, op: dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray], ket_state: tenso.state.puremodel.Model)

   Calculate the matrix element value of a single term.
   < bra_state | [op] | ket_state >


   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: ket_state


   .. py:attribute:: bra_state


   .. py:attribute:: mean_fields
      :type:  dict[tuple[tenso.state.pureframe.Node, int], None | tenso.libs.backend.OptArray]


   .. py:attribute:: densities
      :type:  dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]


   .. py:attribute:: expectation_value
      :value: None



   .. py:attribute:: node_axes
      :type:  dict[tenso.state.pureframe.Node, None | int]


   .. py:attribute:: _dual


   .. py:attribute:: _node_visitor
      :type:  list[tenso.state.pureframe.Node]


   .. py:attribute:: _point_visitor
      :type:  list[tenso.state.pureframe.Point]


   .. py:method:: update_primitive_mean_fields(op: dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]) -> None

      Update the mean fields of the primitive operator.

      :param op: The operator dictionary containing the mean fields.
      :type op: dict[End, OptArray]

      :returns: None



   .. py:method:: get_node_mean_field(bra_a: tenso.libs.backend.OptArray, ket_a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> None | tenso.libs.backend.OptArray

      Calculate the mean field with a specific node.

      :param a: The array for which the mean field is calculated.
      :type a: OptArray
      :param p: The node for which the mean field is calculated.
      :type p: Node
      :param i: The index of the node to be excluded from the mean field calculation.
      :type i: int

      :returns: The calculated mean field if there are other nodes in the mean field calculation,
                otherwise None.
      :rtype: None or OptArray



   .. py:method:: update_mean_fields() -> None

      From leaves to the root.



   .. py:method:: get_mean_holes() -> None

      From leaves to the root.



   .. py:method:: get_density() -> None

      Calculate the density matrix.



.. py:class:: _SVDInfoCache(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node)

   SVD infos for shifted root.


   .. py:attribute:: frame


   .. py:attribute:: u
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray | None]


   .. py:attribute:: s
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray | None]


   .. py:attribute:: vh
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray | None]


   .. py:attribute:: _dual


   .. py:attribute:: _node_axes
      :type:  dict[tenso.state.pureframe.Node, None | int]


   .. py:attribute:: _node_visitor
      :type:  list[tenso.state.pureframe.Node]


   .. py:method:: _print_keys()


   .. py:method:: _get_node_svd(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> tuple[tenso.libs.backend.OptArray, tenso.libs.backend.OptArray, tenso.libs.backend.OptArray]


   .. py:method:: update(state: tenso.state.puremodel.Model) -> None

      From root to leaves.



.. py:class:: _ProdEOM(op: dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray], frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, reg_atol: float | None = None, reg_method: Literal['truncate', 'extend'] = 'extend', reg_type: Literal['mf', 'mf2', 'ip'] = 'ip')

   Solve the equation wrt Product operator:
   d/dt |state> = [op] |state>


   .. py:attribute:: frame


   .. py:attribute:: reg_method
      :value: 'extend'



   .. py:attribute:: reg_type
      :value: 'ip'



   .. py:attribute:: reg_atol
      :value: None



   .. py:attribute:: mean_fields
      :type:  dict[tuple[tenso.state.pureframe.Node, int], None | tenso.libs.backend.OptArray]


   .. py:attribute:: _reg_mean_fields
      :type:  dict[tenso.state.pureframe.Node, None | tenso.libs.backend.OptArray]


   .. py:attribute:: _reg_inner_products
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]


   .. py:attribute:: node_axes
      :type:  dict[tenso.state.pureframe.Node, None | int]


   .. py:attribute:: _dual


   .. py:attribute:: _node_visitor
      :type:  list[tenso.state.pureframe.Node]


   .. py:attribute:: _order


   .. py:method:: update_primitive_mean_fields(op: dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]) -> None

      Update the mean fields of the primitive operator.

      :param op: The operator dictionary containing the mean fields.
      :type op: dict[End, OptArray]

      :returns: None



   .. py:method:: node_eom(node: tenso.state.pureframe.Node, array: tenso.libs.backend.OptArray, s: None | tenso.libs.backend.OptArray = None, vh: None | tenso.libs.backend.OptArray = None) -> tenso.libs.backend.OptArray

      Calculate the equation of motion for a given node.

      :param node: The node for which to calculate the equation of motion.
      :type node: Node
      :param a: The array of the node.
      :type a: OptArray
      :param s: The array of the adjoint singular values
      :type s: OptArray
      :param vh: The array of the adjoint basis
      :type vh: OptArray

      :returns: The result of the equation of motion calculation.
      :rtype: OptArray



   .. py:method:: get_krylov(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int, power: int = 1) -> tenso.libs.backend.OptArray


   .. py:method:: get_node_mean_field(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> None | tenso.libs.backend.OptArray

      Calculate the mean field with a specific node.

      :param a: The array for which the mean field is calculated.
      :type a: OptArray
      :param p: The node for which the mean field is calculated.
      :type p: Node
      :param i: The index of the node to be excluded from the mean field calculation.
      :type i: int

      :returns: The calculated mean field if there are other nodes in the mean field calculation,
                otherwise None.
      :rtype: None or OptArray

      .. note:: a is assumed to be semi-unitary along i axis.



   .. py:method:: update_mean_fields(state: tenso.state.puremodel.Model) -> None

      From leaves to the root.



   .. py:method:: _get_node_reg_mf(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> None | tenso.libs.backend.OptArray

      Calculate the mean field with a specific node using the SVD information
      such that the root is pretend to at (p, i).

      :param a: The array U from the SVD associated to node `p`.
      :type a: OptArray
      :param p: The node for which the mean field is calculated.
      :type p: Node
      :param i: The index of the node to be excluded from the mean field calculation.
      :type i: int

      :returns: The calculated mean field if there are other nodes in the mean field calculation,
                otherwise None.
      :rtype: None or OptArray

      .. note:: a is assumed to be semi-unitary along i axis.



   .. py:method:: _update_reg_mfs(svd_info: _SVDInfoCache) -> None

      From root to leaves.



   .. py:method:: _get_node_reg_ip(a: tenso.libs.backend.OptArray, u: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> tenso.libs.backend.OptArray


   .. py:method:: _update_reg_ips(state: tenso.state.puremodel.Model, svd_info: _SVDInfoCache) -> None

      From root to leaves.



   .. py:method:: update_adjointness(state: tenso.state.puremodel.Model, svd_info: _SVDInfoCache) -> None

      From root to leaves.



   .. py:method:: get_node_adjointness(node: tenso.state.pureframe.Node, s: tenso.libs.backend.OptArray, vh: tenso.libs.backend.OptArray) -> None | tenso.libs.backend.OptArray


.. py:class:: _DirectProdEOM(op: dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray], frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, reg_atol: float | None = None, reg_method: Literal['truncate', 'extend'] = 'extend', reg_type: Literal['mf', 'mf2', 'ip'] = 'ip')

   Solve the equation wrt Product operator:
   d/dt |state> = [op] |state>


   .. py:attribute:: frame


   .. py:attribute:: reg_method
      :value: 'extend'



   .. py:attribute:: reg_type
      :value: 'ip'



   .. py:attribute:: reg_atol
      :value: None



   .. py:attribute:: mean_fields
      :type:  dict[tuple[tenso.state.pureframe.Node, int], None | tenso.libs.backend.OptArray]


   .. py:attribute:: _reg_mean_fields
      :type:  dict[tenso.state.pureframe.Node, None | tenso.libs.backend.OptArray]


   .. py:attribute:: _reg_inner_products
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]


   .. py:attribute:: _reg_s
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]


   .. py:attribute:: _reg_v
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]


   .. py:attribute:: node_axes
      :type:  dict[tenso.state.pureframe.Node, None | int]


   .. py:attribute:: _dual


   .. py:attribute:: _node_visitor
      :type:  list[tenso.state.pureframe.Node]


   .. py:attribute:: _order


   .. py:method:: update_primitive_mean_fields(op: dict[tenso.state.pureframe.End, tenso.libs.backend.OptArray]) -> None

      Update the mean fields of the primitive operator.

      :param op: The operator dictionary containing the mean fields.
      :type op: dict[End, OptArray]

      :returns: None



   .. py:method:: node_eom(node: tenso.state.pureframe.Node, array: tenso.libs.backend.OptArray) -> tenso.libs.backend.OptArray

      Calculate the equation of motion for a given node.

      :param node: The node for which to calculate the equation of motion.
      :type node: Node
      :param a: The arry of the node.
      :type a: OptArray

      :returns: The result of the equation of motion calculation.
      :rtype: OptArray



   .. py:method:: get_node_adjointness(node: tenso.state.pureframe.Node) -> None | tenso.libs.backend.OptArray


   .. py:method:: get_krylov(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int, power: int = 1) -> tenso.libs.backend.OptArray


   .. py:method:: get_node_mean_field(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> None | tenso.libs.backend.OptArray

      Calculate the mean field with a specific node.

      :param a: The array for which the mean field is calculated.
      :type a: OptArray
      :param p: The node for which the mean field is calculated.
      :type p: Node
      :param i: The index of the node to be excluded from the mean field calculation.
      :type i: int

      :returns: The calculated mean field if there are other nodes in the mean field calculation,
                otherwise None.
      :rtype: None or OptArray

      .. note:: a is assumed to be semi-unitary along i axis.



   .. py:method:: update_mean_fields(state: tenso.state.puremodel.Model) -> None

      From leaves to the root.



   .. py:method:: _get_node_svd(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> tuple[tenso.libs.backend.OptArray, tenso.libs.backend.OptArray, tenso.libs.backend.OptArray]


   .. py:method:: _get_node_reg_mf(a: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> None | tenso.libs.backend.OptArray

      Calculate the mean field with a specific node using the SVD information
      such that the root is pretend to at (p, i).

      :param a: The array U from the SVD associated to node `p`.
      :type a: OptArray
      :param p: The node for which the mean field is calculated.
      :type p: Node
      :param i: The index of the node to be excluded from the mean field calculation.
      :type i: int

      :returns: The calculated mean field if there are other nodes in the mean field calculation,
                otherwise None.
      :rtype: None or OptArray

      .. note:: a is assumed to be semi-unitary along i axis.



   .. py:method:: _get_csadj_reg_mf(state: tenso.state.puremodel.Model) -> None

      From root to leaves.



   .. py:method:: _get_node_reg_ip(a: tenso.libs.backend.OptArray, u: tenso.libs.backend.OptArray, p: tenso.state.pureframe.Node, i: int) -> tenso.libs.backend.OptArray


   .. py:method:: _get_csadj_reg_ip(state: tenso.state.puremodel.Model) -> None

      From root to leaves.



   .. py:method:: update_adjointness(state: tenso.state.puremodel.Model) -> None

      From root to leaves.



.. py:class:: SparsePropagator(op: SparseSPO, state: tenso.state.puremodel.Model, frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, renormalize_root=False, init_time=0.0)

   .. py:attribute:: keyword_settings
      :value: ['vmf_atol', 'ps2_atol', 'ps2_ratio', 'ode_method', 'ode_atol', 'ode_rtol', 'vmf_reg_method',...



   .. py:attribute:: vmf_atol
      :type:  float | None
      :value: 1e-07



   .. py:attribute:: ps2_atol
      :type:  float | None
      :value: 1e-07



   .. py:attribute:: ps2_ratio
      :type:  float | None
      :value: 2.0



   .. py:attribute:: ode_atol
      :type:  float
      :value: 1e-05



   .. py:attribute:: ode_rtol
      :type:  float
      :value: 1e-07



   .. py:attribute:: vmf_reg_method
      :type:  Literal['extend', 'truncate']
      :value: 'extend'



   .. py:attribute:: vmf_reg_type
      :type:  Literal['ip', 'mf', 'mf2']
      :value: 'ip'



   .. py:attribute:: ode_method
      :type:  Literal['rk4', 'bosh3', 'dopri5', 'dopri8']
      :value: 'dopri5'



   .. py:attribute:: cache_svd_info
      :type:  bool
      :value: True



   .. py:method:: info()
      :classmethod:



   .. py:method:: update_settings(**kwargs)
      :classmethod:



   .. py:attribute:: ops


   .. py:attribute:: state


   .. py:attribute:: frame


   .. py:attribute:: root


   .. py:attribute:: time
      :value: 0.0



   .. py:attribute:: _node_visitor


   .. py:attribute:: _node_link_visitor


   .. py:attribute:: _depths


   .. py:attribute:: _shape_list
      :value: []



   .. py:attribute:: _size_list
      :value: []



   .. py:attribute:: n_terms


   .. py:attribute:: _ti_eoms
      :type:  list[_DirectProdEOM | _ProdEOM]


   .. py:attribute:: is_time_dependent


   .. py:attribute:: _td_eoms
      :type:  list[_DirectProdEOM | _ProdEOM]


   .. py:attribute:: ode_step_counter
      :type:  int
      :value: 0



   .. py:method:: renormalize_root()


   .. py:method:: update_size_list()


   .. py:method:: update_td_terms(time: float) -> None


   .. py:method:: propagate(end: float, dt: float, ps_method: Literal['vmf', 'ps1', 'ps2'] = 'vmf') -> Generator[tuple[float, tenso.state.puremodel.Model], None, None]


   .. py:method:: adaptive_propagate(end: float, fixed_dt: float, fixed_ps_method: Literal['ps1', 'vmf'] = 'vmf', fixed_steps: int = 1, adaptive_dt: float | None = None, adaptive_ps_steps: int = 1) -> Generator[tuple[float, tenso.state.puremodel.Model], None, None]


   .. py:method:: mixed_propagate(end: float, dt: float, ending_ps_method: Literal['ps2', 'ps1', 'vmf'] = 'ps1', starting_dt: float | None = None, starting_ps_method: Literal['ps1', 'ps2'] = 'ps2', max_starting_rank: int | None = None, max_starting_steps: int | None = None) -> Generator[tuple[float, tenso.state.puremodel.Model], None, None]


   .. py:method:: vmf_step(dt: float) -> None


   .. py:method:: ps1_step(dt: float) -> None


   .. py:method:: ps2_step(dt: float) -> None


   .. py:method:: _vectorize(tensors: None | list[tenso.libs.backend.OptArray] = None) -> tenso.libs.backend.OptArray


   .. py:method:: _update_state_from_vector(vec: tenso.libs.backend.OptArray) -> None


   .. py:method:: _node_step(p: tenso.state.pureframe.Node, dt: float) -> None


   .. py:method:: _one_site_move(p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int, dt: None | float) -> None


   .. py:method:: _krylov_one_site_move(p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int, dt: None | float) -> None
      :abstractmethod:


      Experimental method for adaptive PS1 step.
      Extend the _one_site_move method to include the adaptive rank on edge p-q.
      This is done by extending the column space of p and q according to the
      First order krylov space {p, F_p} and {q, F_q} when the cannonical center is
      at the edge p-q.



   .. py:method:: _two_site_move(p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int, dt: float) -> None


   .. py:method:: _ps1_forward_step(dt: float) -> None


   .. py:method:: _ps1_backward_step(dt: float) -> None


   .. py:method:: _ps2_forward_step(dt: float) -> None


   .. py:method:: _ps2_backward_step(dt: float) -> None


   .. py:method:: _get_vmf_func()


   .. py:method:: _get_vmf_func_direct()


   .. py:method:: _get_cmf_func()


   .. py:method:: _odeint(func: Callable[[float, tenso.libs.backend.OptArray], tenso.libs.backend.OptArray], y0: tenso.libs.backend.OptArray, dt: float, tuple_complex: bool = True) -> tenso.libs.backend.OptArray


.. py:class:: DynamicalSparsePropagator(op: SparseSPO, state: tenso.state.puremodel.Model, frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, renormalize_root=False, init_time=0.0)

   Bases: :py:obj:`SparsePropagator`


   .. py:attribute:: _get_vmf_func


   .. py:method:: _adaptive_two_site_move(p: tenso.state.pureframe.Node, i: int, q: tenso.state.pureframe.Node, j: int, dt: float) -> None
      :abstractmethod:


      Experimental method for adaptive PS2 step.
      Extend the _two_site_move method to include the adaptive connectivity between the neighbors of p and q.



