from typing import Union

from .node import ListNode

class DoubleLinkedList:
    def __init__(self):
        self._head: Union[ListNode, None] = None
        self._tail: Union[ListNode, None] = None
        self._size: int = 0

    def __contains__(self, data):
        is_data = False
        current_node = self.head
        while current_node is not None:
            if current_node.data.data == data:
                is_data = True
                break
            current_node = current_node.child
        return is_data

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, node):
        self._head = node

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, node):
        self._tail = node

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    def append(self, data):
        new_node = ListNode(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.child = new_node
            new_node.parent = self.tail
            self.tail = new_node
        self.size += 1

    def remove(self, index):
        if abs(index) > self.size:
            raise ValueError("Index out of range.")
        if index < 0:
            index = self.size + index
        # Remove first node
        if index == 0:
            data = self.head.data
            if self.head.child is None:
                self.head = None
                self.tail = None
            else:
                child = self.head.child
                self.head = child
                child.parent = None
        elif index == self.size - 1:
            data = self.tail.data
            parent = self.tail.parent
            parent.child = None
            self.tail = parent
        else:
            i = 0
            current_node = self.head
            while i != index:
                current_node = current_node.child
                i += 1
            data = current_node.data
            parent = current_node.parent
            child = current_node.child
            parent.child = child
            child.parent = parent
        self.size -= 1
        return data

    def is_empty(self):
        return self.size == 0