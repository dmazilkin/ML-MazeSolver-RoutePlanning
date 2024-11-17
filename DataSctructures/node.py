class Node:
    def __init__(self, data, parent: 'Node' = None, action = None, cost = 0):
        self._data = data
        self._parent = parent
        self._action = action
        self._cost = cost
    @property
    def data(self):
        return self._data
    @property
    def parent(self):
        return self._parent
    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, cost):
        self._cost = cost