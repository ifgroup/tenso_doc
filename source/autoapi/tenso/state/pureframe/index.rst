tenso.state.pureframe
=====================

.. py:module:: tenso.state.pureframe

.. autoapi-nested-parse::

   Data structure for topology of tensors in a network



Classes
-------

.. autoapisummary::

   tenso.state.pureframe.Point
   tenso.state.pureframe.Node
   tenso.state.pureframe.End
   tenso.state.pureframe.Frame


Module Contents
---------------

.. py:class:: Point(name: Optional[str] = None)

   .. py:attribute:: __cache
      :type:  weakref.WeakValueDictionary[tuple[str, str], Point]


   .. py:attribute:: name
      :value: ''



.. py:class:: Node(name: Optional[str] = None)

   Bases: :py:obj:`Point`


   .. py:method:: __repr__() -> str


.. py:class:: End(name: Optional[str] = None)

   Bases: :py:obj:`Point`


   .. py:method:: __repr__() -> str


.. py:class:: Frame

   .. py:attribute:: _neighbor
      :type:  dict[Point, list[Point]]


   .. py:attribute:: _duality
      :type:  dict[tuple[Point, None | int], tuple[Point, None | int]]


   .. py:attribute:: _axes
      :type:  dict[tuple[Point, Point], tuple[None | int, None | int]]


   .. py:method:: __str__() -> str


   .. py:method:: __contains__(p: Point) -> bool


   .. py:method:: copy()


   .. py:method:: add_link(p: Point, q: Point) -> None

      Add a link between two points.
      End can only have one link. Node can have multiple links.



   .. py:property:: points
      :type: set[Point]



   .. py:property:: nodes
      :type: set[Node]



   .. py:property:: ends
      :type: set[End]



   .. py:method:: degree(p: Node)


   .. py:method:: dual(p: Point, i: None | int) -> tuple[Point, None | int]


   .. py:method:: axes(p: Point, q: Point) -> tuple[int, None | int]


   .. py:method:: near_points(key: Point) -> list[Point]


   .. py:method:: near_nodes(key: Node) -> list[Node]


   .. py:method:: node_link_visitor(start: Node) -> list[tuple[Node, int, Node, int]]


   .. py:method:: point_link_visitor(start: Point) -> list[tuple[Point, int, Point, int]]


   .. py:method:: node_visitor(start: Node, method: Literal['DFS', 'BFS'] = 'DFS') -> list[Node]


   .. py:method:: point_visitor(start: Node, method: Literal['DFS', 'BFS'] = 'DFS') -> list[Node]


   .. py:method:: get_node_depths(start: Node) -> dict[Node, int]


   .. py:method:: get_node_axes(start: Point) -> dict[Node, Optional[int]]


   .. py:method:: get_graph() -> dict[Node, list[Point]]


   .. py:method:: construct_from_graph(graph: dict[Node, list[Point]]) -> None


