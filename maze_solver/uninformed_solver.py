from operator import itemgetter
from PIL import Image, ImageDraw
from typing import Tuple, List, Set

from .data_structure import DoubleLinkedList
from .data_structure.base_maze import Maze
from .data_structure.node import GraphNode
from .helpers import *

class UninformedSolver:
    # Possible uninformed algorithms
    ALGORITHMS = {
        'dfs': -1,
        'bfs': 0,
    }

    # Rectangle size in pixels
    RECTANGLE_SIZE = 25

    def __init__(self, file_path: str):
        """
        Create uninformed maze solver object.

        :param file_path: path to text file with target maze
        """

        self._maze = Maze(file_path)
        self._file_name = file_path.split('/')[-1].split('.')[0]

    def solve(self, alg_name: str = 'dfs', show_explored: bool = False) -> None:
        """
        Solve maze with chosen uninformed algorithm.

        :param alg_name: uninformed algorithm name
        :param show_explored: show explored nodes
        """

        if alg_name not in self.ALGORITHMS:
            raise NameError('No such algorithm.')
        (solution, explored), time = self._solve_maze(alg_name)
        save_results(self._file_name, alg_name, len(solution), len(explored), time)
        self._save_solution_to_jpeg(solution, explored, alg_name, show_explored)

    def _save_solution_to_jpeg(self, solution: List[GraphNode], explored: List[GraphNode], alg_name: str, show_explored: bool) -> None:
        """
        Save maze picture with solution path.

        :param solution: solution nodes
        :param explored: explored nodes
        :param alg_name: algorithm name
        :param show_explored: True - show explored nodes, False - otherwise
        """

        width, height = self._maze.get_maze_shape()
        img = Image.new('RGB', (self.RECTANGLE_SIZE * width, self.RECTANGLE_SIZE * height), color='black')
        idraw = ImageDraw.Draw(img)
        for row in range(height):
            for column in range(width):
                coords = (row, column)
                if coords == self._maze.get_start():
                    color = (0, 100, 0)
                elif coords == self._maze.get_stop():
                    color = (255, 0, 0)
                elif coords in solution:
                    color = (0, 255, 0)
                elif show_explored and coords in explored:
                    color = (255, 160, 122)
                else:
                    symbol = self._maze.processed_maze()[row][column]
                    if symbol == 1:
                        color = 'white'
                    else:
                        color = 'grey'
                idraw.rectangle([(column * self.RECTANGLE_SIZE, row * self.RECTANGLE_SIZE),
                                 ((column + 1) * self.RECTANGLE_SIZE, (row + 1) * self.RECTANGLE_SIZE)], fill=color)
        img.save(f'./solutions/{self._file_name}_{alg_name}.jpeg')

    @measure_time
    def _solve_maze(self, alg_name) -> Tuple[Set[GraphNode], Set[GraphNode]]:
        """
        Solve maze with chosen uninformed algorithm.

        :param alg_name: algorithm name
        :return: solution and explored nodes
        """

        stack: DoubleLinkedList = DoubleLinkedList()
        explored: Set[GraphNode] = set()
        index = self.ALGORITHMS[alg_name]
        start_node = GraphNode(data=self._maze.get_start())
        stop_node = self._maze.get_stop()
        found_node = None

        stack.append(start_node)

        while not stack.is_empty():
            node = stack.remove(index)
            explored.add(node.data)
            if node.data == stop_node:
                found_node = node
                break
            else:
                neighbors = [neighbor for neighbor in self._expand_node(node) if neighbor.data not in explored and neighbor.data not in stack]
                for neighbor in neighbors:
                    stack.append(neighbor)

        if found_node is not None:
            solution = self._get_solution_path(found_node)
            return solution, explored
        else:
            raise ValueError('No solution found.')

    def _get_solution_path(self, target_node: GraphNode) -> Set[GraphNode]:
        """
        Get solution path nodes from target node.

        :param target_node: target node
        :return: solution path nodes
        """

        solution = set()
        node = target_node
        while node is not None:
            solution.add(node.data)
            node = node.prev
        return solution

    def _expand_node(self, node: GraphNode) -> List[GraphNode]:
        """
        Get possible node neighbors.

        :param node: node to expand
        :return: possible neighbors
        """

        actions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
        }
        get_row, get_column = itemgetter(0), itemgetter(1)
        neighbors = []

        for action in actions:
            row = get_row(actions[action]) + get_row(node.data)
            column = get_column(actions[action]) + get_column(node.data)
            width, height = self._maze.get_maze_shape()
            if 0 < row < height-1 and 0 < column < width-1:
                if self._maze.processed_maze()[row][column] != 0:
                    neighbors.append(GraphNode(data=(row, column), action=action, prev=node, cost=node.cost+1))
        return neighbors
