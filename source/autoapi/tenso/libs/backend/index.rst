tenso.libs.backend
==================

.. py:module:: tenso.libs.backend

.. autoapi-nested-parse::

   Backend for accelerated array-operations.



Attributes
----------

.. autoapisummary::

   tenso.libs.backend.sundials_odeint
   tenso.libs.backend.MAX_EINSUM_AXES
   tenso.libs.backend.PI
   tenso.libs.backend.DOUBLE_PRECISION
   tenso.libs.backend.FORCE_CPU
   tenso.libs.backend.ON_DEVICE_EIGEN_SOLVER
   tenso.libs.backend.opt_device
   tenso.libs.backend.opt_dtype
   tenso.libs.backend.OptArray


Functions
---------

.. autoapisummary::

   tenso.libs.backend.opt_to_numpy
   tenso.libs.backend.opt_array
   tenso.libs.backend.opt_zeros
   tenso.libs.backend.opt_cat
   tenso.libs.backend.opt_stack
   tenso.libs.backend.opt_split
   tenso.libs.backend.opt_einsum
   tenso.libs.backend.opt_sum
   tenso.libs.backend.opt_tensordot
   tenso.libs.backend.opt_svd
   tenso.libs.backend.opt_odeint
   tenso.libs.backend.opt_pinv
   tenso.libs.backend.opt_inv
   tenso.libs.backend.opt_transform
   tenso.libs.backend.opt_multitransform
   tenso.libs.backend.opt_eye
   tenso.libs.backend.opt_trace
   tenso.libs.backend.opt_inner_product


Module Contents
---------------

.. py:data:: sundials_odeint
   :value: None


.. py:data:: MAX_EINSUM_AXES
   :value: 52


.. py:data:: PI
   :value: 3.141592653589793


.. py:data:: DOUBLE_PRECISION
   :value: True


.. py:data:: FORCE_CPU
   :value: True


.. py:data:: ON_DEVICE_EIGEN_SOLVER
   :value: False


.. py:data:: opt_device
   :value: 'cpu'


.. py:data:: opt_dtype

.. py:data:: OptArray

.. py:function:: opt_to_numpy(array: OptArray) -> numpy.typing.NDArray

.. py:function:: opt_array(array: numpy.typing.ArrayLike) -> OptArray

.. py:function:: opt_zeros(shape: list[int]) -> OptArray

.. py:function:: opt_cat(tensors: list[OptArray]) -> OptArray

.. py:function:: opt_stack(tensors: list[OptArray] | tuple[OptArray, Ellipsis]) -> OptArray

.. py:function:: opt_split(tensors: OptArray, size_list: list[int]) -> list[OptArray]

.. py:function:: opt_einsum(*args) -> OptArray

   Currently wrapper for torch.einsum without optimizing contraction order.


.. py:function:: opt_sum(array: OptArray, dim: int) -> OptArray

.. py:function:: opt_tensordot(a: OptArray, b: OptArray, axes: tuple[list[int], list[int]]) -> OptArray

.. py:function:: opt_svd(a: OptArray) -> tuple[OptArray, OptArray, OptArray]

   Perform singular value decomposition (SVD) on the input array without full matrices.

   :param a: The input array.
   :type a: OptArray

   :returns: A tuple containing the left singular vectors,
             singular values, and right singular vectors.
             Note that the singular values are of the real type.
   :rtype: tuple[OptArray, OptArray, OptArray]


.. py:function:: opt_odeint(func: Callable[[float, OptArray], OptArray], t0: float, y0: OptArray, dt: float, atol: float, rtol: float, method: str = 'dopri5') -> OptArray

   Avaliable method:
   - Home-made integrators:
       - `iterX` Taylor series up to `X`-th order.
       - `rk4` Fourth-order Runge-Kutta with 3/8 rule.
   - Adaptive-step from `torchdiffeq`:
       - `dopri8` Runge-Kutta 7(8) of Dormand-Prince-Shampine
       - `dopri5` Runge-Kutta 4(5) of Dormand-Prince.
       - `bosh3` Runge-Kutta 2(3) of Bogacki-Shampine
       - `adaptive_heun` Runge-Kutta 1(2)
   - Fixed-step `torchdiffeq`:
       - `euler` Euler method.
       - `midpoint` Midpoint method.
       - `explicit_adams` Explicit Adams.
       - `implicit_adams` Implicit Adams.
   - Scikit.odes/SUNDIALS compatable method (using numpy.array):
       - 'cvode' CVODE
       - 'bdf' Backward Differentiation Formula
       - 'admo' Adams-Moulton
       - 'rk8' Runge-Kutta 7(8)
       - 'rk5' Runge-Kutta 4(5)


.. py:function:: opt_pinv(a: OptArray, atol) -> OptArray

.. py:function:: opt_inv(a: OptArray) -> OptArray

.. py:function:: opt_transform(op: OptArray, tensor: OptArray, op_ax: int, tensor_ax: int)

.. py:function:: opt_multitransform(op_dict: dict[int, OptArray], tensor: OptArray) -> OptArray

.. py:function:: opt_eye(dim1: int, dim2: int | None = None) -> OptArray

.. py:function:: opt_trace(tensor1: OptArray, tensor2: OptArray, ax: int) -> OptArray

   Complex conjugate not included



.. py:function:: opt_inner_product(tensor1: OptArray, tensor2: OptArray) -> complex

