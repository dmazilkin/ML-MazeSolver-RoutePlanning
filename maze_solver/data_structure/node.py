from typing import Union

class GraphNode:
    def __init__(self, data, prev: 'GraphNode' = None, action = None, cost = 0):
        self._data = data
        self._prev = prev
        self._action = action
        self._cost = cost

    @property
    def data(self):
        return self._data

    @property
    def prev(self):
        return self._prev

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost):
        self._cost = cost

class ListNode:
    def __init__(self, data: GraphNode):
        self._data = data
        self._parent = None
        self._child = None

    @property
    def data(self):
        return self._data

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, child):
        self._child = child

class BinaryTreeNode:
    def __init__(self, data: GraphNode, key: Union[float, int]):
        self._data = data
        self._key = key

    @property
    def data(self):
        return self._data

    @property
    def key(self):
        return self._key