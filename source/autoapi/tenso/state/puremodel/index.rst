tenso.state.puremodel
=====================

.. py:module:: tenso.state.puremodel


Classes
-------

.. autoapisummary::

   tenso.state.puremodel.Model


Functions
---------

.. autoapisummary::

   tenso.state.puremodel.triangular
   tenso.state.puremodel.zeros_model
   tenso.state.puremodel.eye_model


Module Contents
---------------

.. py:function:: triangular(n_list)

   A Generator yields the natural number in a triangular order.



.. py:class:: Model(valuation: dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray] | Iterable[tuple[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]])

   A Model is a Frame with valuation for each node.



   .. py:attribute:: _valuation
      :type:  dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]


   .. py:method:: __contains__(p: tenso.state.pureframe.Node) -> bool


   .. py:method:: __getitem__(p: tenso.state.pureframe.Node) -> tenso.libs.backend.OptArray


   .. py:method:: size() -> int

      Total number of numbers.



   .. py:method:: save(filename: str) -> None

      Save the model to a file.



   .. py:method:: load(filename: str) -> Model
      :classmethod:


      Load the model from a file.



   .. py:property:: nodes
      :type: set[tenso.state.pureframe.Node]



   .. py:method:: shape(p: tenso.state.pureframe.Node) -> list[int]


   .. py:method:: order(p: tenso.state.pureframe.Node) -> int


   .. py:method:: dimension(p: tenso.state.pureframe.Node, i: int) -> int


   .. py:method:: copy() -> Model

      A shallow copy of the model.



   .. py:method:: conjugate() -> Model

      Conjugate the model.



   .. py:method:: substitute(valuation: dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray] | Iterable[tuple[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]]) -> Model


   .. py:method:: update(valuation: dict[tenso.state.pureframe.Node, tenso.libs.backend.OptArray] | Iterable[tuple[tenso.state.pureframe.Node, tenso.libs.backend.OptArray]]) -> None

      Update the valuation of the model.



   .. py:method:: zero_like() -> Model


.. py:function:: zeros_model(shapes: dict[tenso.state.pureframe.Node, list[int]]) -> Model

   A model with proper shape arrays.
   Specify the dimension for each Edge in dims (default is 1).


.. py:function:: eye_model(frame: tenso.state.pureframe.Frame, root: tenso.state.pureframe.Node, shapes: dict[tenso.state.pureframe.Node, list[int]]) -> Model

