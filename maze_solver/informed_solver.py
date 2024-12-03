from operator import itemgetter
from typing import List, Union
from queue import PriorityQueue

from .uninformed_solver import UninformedSolver
from .data_structure.node import Node

class InformedSolver(UninformedSolver):
    # Possible heuristic methods
    HEURISTIC_METHODS = (
        'manhattan',
        'euclid',
    )

    def __init__(self, file_path):
        """
        Create informed maze solver object.

        :param file_path: path to text file with target maze
        """

        super().__init__(file_path)

    def solve(self, heuristic_method: str = 'manhattan', show_explored: bool = False) -> None:
        """
        Solve maze with A* algorithm and chosen heuristic method.

        :param heuristic_method: heuristic method to use
        :param show_explored: show explored nodes
        """

        if heuristic_method not in self.HEURISTIC_METHODS:
            raise NameError('No such heuristic method.')
        solution, explored = self._solve_maze(method=heuristic_method)
        self._save_solution_to_jpeg(solution, explored, heuristic_method, show_explored)

    def _solve_maze(self, method):
        """
        Solve maze with chosen uninformed algorithm.

        :param alg_name: uninformed algorithm name
        :param show_explored: show explored nodes
        """
        queue = PriorityQueue()
        explored = set()
        start_node = Node(data=self._maze.get_start())
        stop_node = self._maze.get_stop()
        found_node = None

        queue.put((self._get_heuristic(start_node, method=method), id(start_node), start_node))

        while not queue.empty():
            _, _, node = queue.get()
            explored.add(node.data)
            if node.data == stop_node:
                found_node = node
                break
            else:
                neighbors = [neighbor for neighbor in self._expand_node(node) if neighbor.data not in explored]
                if len(neighbors) != 0:
                    for neighbor in neighbors:
                        queue.put((self._get_heuristic(neighbor, method=method), id(neighbor), neighbor))
        solution = self._get_solution_path(found_node)
        return solution, explored

    def _get_heuristic(self, node, method='manhattan') -> Union[int, float]:
        """
        Get heuristic value of a node.

        :param node: node to get heuristic for
        :param method: heuristic method to use
        :return: heuristic value of a node
        """
        get_row, get_column = itemgetter(0), itemgetter(1)
        stop_node = self._maze.get_stop()
        if method == 'manhattan':
            x = abs(get_row(stop_node) - get_row(node.data))
            y = abs(get_column(stop_node) - get_column(node.data))
            value = x + y
        elif method == 'euclid':
            x = (get_row(node.data) - get_row(stop_node))**2
            y = (get_column(node.data) - get_column(stop_node)) ** 2
            value = (x + y)**0.5
        else:
            raise NameError('No such method for heuristic function.')
        return value + node.cost

class JPS(InformedSolver):
    # Possible actions for JPS maze solver
    ACTIONS = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1),
        'upper-left': (-1, -1),
        'upper-right': (-1, 1),
        'lower-left': (1, -1),
        'lower-right': (1, 1),
    }

    def __init__(self, file_path: str):
        """
        Create JPS maze solver object.

        :param file_path: path to text file with target maze
        """

        super().__init__(file_path)

    def _expand_node(self, node: Node) -> List[Node]:
        """
        Find possible node neighbors to move to.

        :param node: node to expand
        :return: list of node possible neighbors
        """

        jump_points = []
        for action_name in self.ACTIONS:
            jump_point = self._get_jump_points(node, action_name)
            if jump_point is not None:
                jump_points.append(jump_point)
        return jump_points

    def _get_jump_points(self, node: Node, action_name: str) -> Union[Node, None]:
        """
        Get jump points of a node.

        :param node: origin node
        :param action_name: action name for new node
        :return: jump points of new node
        """

        jump_point = None
        get_row, get_column = itemgetter(0), itemgetter(1)
        current_row, current_column = get_row(node.data), get_column(node.data)
        cost_row, cost_column = get_row(self.ACTIONS[action_name]), get_column(self.ACTIONS[action_name])
        row = current_row + cost_row
        column = current_column + cost_column
        width, height = self._maze.get_maze_shape()
        if 0 < row < height-1 and 0 < column < width-1:
            new_node = Node(data=(row, column), action=action_name, parent=node, cost=node.cost + (cost_row**2 + cost_column**2)**0.5)
            current_position = self._maze.processed_maze()[row][column]
            if current_position == 1:
                if self._is_jump_point(new_node, action_name):
                    jump_point = new_node
                else:
                    if action_name in ['up', 'down', 'left', 'right']:
                        jump_point = self._get_jump_points(new_node, action_name)
                    elif action_name == 'upper-right':
                        jump_point = self._get_jump_points(new_node, 'up')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'right')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'upper-right')
                    elif action_name == 'upper-left':
                        jump_point = self._get_jump_points(new_node, 'up')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'left')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'upper-left')
                    elif action_name == 'lower-right':
                        jump_point = self._get_jump_points(new_node, 'down')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'right')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'lower-right')
                    elif action_name == 'lower-left':
                        jump_point = self._get_jump_points(new_node, 'down')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'left')
                        if jump_point is None:
                            jump_point = self._get_jump_points(new_node, 'lower-left')
            elif current_position == 'B':
                jump_point = new_node
        return jump_point

    def _is_jump_point(self, node: Node, action_name: str) -> bool:
        """
        Check if node is jump point.

        :param node: node to check
        :param action_name: action name for new node
        :return: True - if node is jump point, False - otherwise
        """

        is_jump_point = False
        get_row, get_column = itemgetter(0), itemgetter(1)
        current_row, current_column = get_row(node.data), get_column(node.data)
        width, height = self._maze.get_maze_shape()
        if action_name == 'up' or action_name == 'down':
            column_left = current_column + get_column(self.ACTIONS['left'])
            column_right = current_column + get_column(self.ACTIONS['right'])
            if (0 < column_left < width-1) and (self._maze.processed_maze()[current_row][column_left] == 0):
                is_jump_point = True
            if (0 < column_right < width-1) and (self._maze.processed_maze()[current_row][column_right] == 0):
                is_jump_point = True
        elif action_name == 'right' or action_name == 'left':
            row_up = current_row + get_row(self.ACTIONS['up'])
            row_down = current_row + get_row(self.ACTIONS['down'])
            if (0 < row_up < height-1) and (self._maze.processed_maze()[row_up][current_column] == 0):
                is_jump_point = True
            if (0 < row_down < height-1) and (self._maze.processed_maze()[row_down][current_column] == 0):
                is_jump_point = True
        elif action_name == 'upper-right':
            row_down = current_row + get_row(self.ACTIONS['down'])
            column_left = current_column + get_column(self.ACTIONS['left'])
            if (0 < row_down < height-1) and (self._maze.processed_maze()[row_down][current_column] == 0):
                is_jump_point = True
            if (0 < column_left < width-1) and (self._maze.processed_maze()[current_row][column_left] == 0):
                is_jump_point = True
        elif action_name == 'lower-right':
            row_up = current_row + get_row(self.ACTIONS['up'])
            column_left = current_column + get_column(self.ACTIONS['left'])
            if (0 < row_up < height-1) and (self._maze.processed_maze()[row_up][current_column] == 0):
                is_jump_point = True
            if (0 < column_left < width-1) and (self._maze.processed_maze()[current_row][column_left] == 0):
                is_jump_point = True
        elif action_name == 'upper-left':
            row_down = current_row + get_row(self.ACTIONS['down'])
            column_right = current_column + get_column(self.ACTIONS['right'])
            if (0 < row_down < height-1) and (self._maze.processed_maze()[row_down][current_column] == 0):
                is_jump_point = True
            if (0 < column_right <width-1) and (self._maze.processed_maze()[current_row][column_right] == 0):
                is_jump_point = True
        elif action_name == 'lower-left':
            row_up = current_row + get_row(self.ACTIONS['up'])
            column_right = current_column + get_column(self.ACTIONS['right'])
            if (0 < row_up < height-1) and (self._maze.processed_maze()[row_up][current_column] == 0):
                is_jump_point = True
            if (0 < column_right < width-1) and (self._maze.processed_maze()[current_row][column_right] == 0):
                is_jump_point = True
        return is_jump_point