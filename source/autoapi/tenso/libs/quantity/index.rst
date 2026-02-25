tenso.libs.quantity
===================

.. py:module:: tenso.libs.quantity

.. autoapi-nested-parse::

   Unit transformations.



Attributes
----------

.. autoapisummary::

   tenso.libs.quantity.atomic_unit_in
   tenso.libs.quantity.synonyms


Classes
-------

.. autoapisummary::

   tenso.libs.quantity.Quantity


Module Contents
---------------

.. py:data:: atomic_unit_in

.. py:data:: synonyms

.. py:class:: Quantity(value: float, unit: Optional[str] = None)

   Bases: :py:obj:`object`


   .. py:attribute:: value


   .. py:attribute:: unit
      :value: None



   .. py:method:: standardize(unit: Optional[str]) -> Optional[str]
      :staticmethod:



   .. py:property:: au
      :type: float



   .. py:method:: convert_to(unit: Optional[str] = None) -> Quantity


   .. py:method:: to(unit: Optional[str] = None) -> Quantity


   .. py:method:: __neg__() -> Quantity


   .. py:method:: __add__(other: Quantity) -> Quantity


   .. py:method:: __sub__(other: Quantity) -> Quantity


   .. py:method:: __mul__(other: float) -> Quantity


   .. py:method:: __truediv__(other: float) -> Quantity


   .. py:method:: __eq__(other: Quantity | Literal[0]) -> Quantity


   .. py:method:: __gt__(other: Quantity | Literal[0]) -> Quantity


   .. py:method:: __str__() -> str


   .. py:method:: __repr__() -> str


