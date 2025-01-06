from typing import List

from maze_solver.data_structure.node import GraphNode, BinaryTreeNode

class PriorityQueue:
    def __init__(self):
        # Initialize binary heap
        self._binary_heap: List[BinaryTreeNode] = list()
        self._content = dict()
        self._vertices_count = 0

    def __contains__(self, data: GraphNode):
        return data.data in self._content

    def put(self, data: GraphNode, key: int) -> None:
        """
        Put GraphNode with key to priority queue.

        :param data: GraphNode
        :param key: GraphNode key
        """

        # Create and add new node to the last layer in the most right position of binary heap
        new_node = BinaryTreeNode(data=data, key=key)
        self._binary_heap.append(new_node)
        if data.data not in self._content:
            self._content[data.data] = 1
        else:
            self._content[data.data] += 1
        self._vertices_count += 1
        # Check if new node bigger than parent node and move new node up
        self._siftup(self._vertices_count - 1)

    def pop(self) -> GraphNode:
        """
        Pop GraphNode with the smallest key from priority queue.

        :return: GraphNode with the smallest key
        """

        # Check if binary heap is empty
        if self.is_empty():
            raise IndexError('Pop from empty priority queue.')
        # Get root node to pop
        root_index = 0
        root = self._binary_heap[root_index]
        # if root.data.data in self._content:
        #     del self._content[root.data.data]
        if self._content[root.data.data] == 1:
            del self._content[root.data.data]
        else:
            self._content[root.data.data] -= 1
        # Get the last right node from the last layer and set as the root
        last_child = self._binary_heap.pop()
        self._vertices_count -= 1
        if not self.is_empty():
            self._binary_heap[root_index] = last_child
            # Check if new root node smaller than its children and move new root down
            self._siftdown(root_index)
        return root.data

    def show_tree(self):
        for node in self._binary_heap:
            print(node.key, end=' ')
        print()

    def is_empty(self) -> bool:
        return len(self._binary_heap) == 0

    def _get_parent_index(self, child_index: int) -> int:
        return (child_index - 1) // 2

    def _get_child_index(self, parent_index: int, which: 'str') -> int:
        child_index_from_child = {
            'right': lambda index: index * 2 + 2,
            'left': lambda index: index * 2 + 1,
        }
        return child_index_from_child[which](parent_index)

    def _siftup(self, child_index: int) -> None:
        """
        Moves the element at the given child index up the binary heap to maintain the heap property.

        :param child_index: child index
        """

        # Base case when child is root
        if child_index == 0:
            return
        child = self._binary_heap[child_index]
        # Get parent index and node
        parent_index = self._get_parent_index(child_index)
        parent = self._binary_heap[parent_index]
        # Base case when parent is not smaller than child
        if child.key >= parent.key:
            return
        else:
            # Recursive case otherwise
            self._binary_heap[child_index], self._binary_heap[parent_index] = self._binary_heap[parent_index], self._binary_heap[child_index]
            self._siftup(parent_index)

    def _siftdown(self, parent_index: int) -> None:
        """
        Moves the element at the given parent index down the binary heap to maintain the heap property.

        :param parent_index:
        """

        # Get right and left children indexes
        right_child_index = self._get_child_index(parent_index, 'right')
        left_child_index = self._get_child_index(parent_index, 'left')
        smallest = parent_index
        if (right_child_index <= self._vertices_count - 1) and (self._binary_heap[right_child_index].key < self._binary_heap[smallest].key):
            smallest = right_child_index
        if (left_child_index <= self._vertices_count - 1) and (self._binary_heap[left_child_index].key < self._binary_heap[smallest].key):
            smallest = left_child_index
        # Base case if parent is the biggest
        if parent_index == smallest:
            return
        else:
            # Recursive case otherwise
            self._binary_heap[parent_index], self._binary_heap[smallest] = self._binary_heap[smallest], self._binary_heap[parent_index]
            self._siftdown(smallest)