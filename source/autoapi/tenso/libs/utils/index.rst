tenso.libs.utils
================

.. py:module:: tenso.libs.utils

.. autoapi-nested-parse::

   Metas.



Attributes
----------

.. autoapisummary::

   tenso.libs.utils.T


Functions
---------

.. autoapisummary::

   tenso.libs.utils.lazyproperty
   tenso.libs.utils.count_calls
   tenso.libs.utils.iter_round_visitor
   tenso.libs.utils.iter_visitor
   tenso.libs.utils.depths
   tenso.libs.utils.path
   tenso.libs.utils.huffman_tree
   tenso.libs.utils.unzip


Module Contents
---------------

.. py:data:: T

.. py:function:: lazyproperty(func: Callable[Ellipsis, T]) -> Callable[Ellipsis, T]

.. py:function:: count_calls(f: Callable[Ellipsis, T]) -> Callable[Ellipsis, T]

.. py:function:: iter_round_visitor(start: T, r: Callable[[T], list[T]]) -> Generator[tuple[T, bool], None, None]

   Iterative round-trip visitor. Only support 'DFS' (depth first) method.

   :param start: Initial object
   :param r: Relation function.


.. py:function:: iter_visitor(start: T, r: Callable[[T], list[T]], method: Literal['DFS', 'BFS'] = 'DFS') -> Generator[T, None, None]

   Iterative visitor.

   :param start: Initial object
   :param r: Relation function.
   :param method: in {'DFS', 'BFS'}. 'DFS': Depth first; 'BFS': Breadth first.


.. py:function:: depths(start: T, r: Callable[[T], list[T]]) -> dict[T, int]

   Iteratively geerate the depth of each component.

   :param start: Initial object
   :param r: Relation function.


.. py:function:: path(start: T, stop: T, r: Callable[[T], list[T]]) -> None | list[T]

   Iteratively generate the depth of each component.

   :param start: Initial object
   :param r: Relation function.


.. py:function:: huffman_tree(sources: list[T], new_obj: Callable[[], T], importances: Optional[list[int]] = None, n_ary: int = 2) -> tuple[collections.OrderedDict[T, list[T]], T]

   Generate a Tree for the soureces as leaves using Huffman coding method.



.. py:function:: unzip(iterable: Iterable) -> Iterable[Iterable]

   The same as zip(*iter) but returns iterators, instead
   of expand the iterator. Mostly used for large sequence.
   Reference: https://gist.github.com/andrix/1063340


