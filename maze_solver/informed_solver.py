from operator import itemgetter
from typing import List, Union, Tuple
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
        # Check possible actions for node to expand
        for action_name in self.ACTIONS:
            jump_points.extend(self._get_jump_points(node, action_name))
        return jump_points

    def _get_jump_points(self, node: Node, action_name: str) -> Union[List[Node], List[None]]:
        """
        Get jump points of a node.

        :param node: origin node
        :param action_name: action name for new node
        :return: jump points of new node
        """

        jump_points = []
        row, column = self._calc_row_and_column(node, action_name)
        width, height = self._maze.get_maze_shape()
        if (0 < row < height-1) and (0 < column < width-1):
            new_node = Node(data=(row, column), action=action_name, parent=node, cost=self._calc_cost(node, action_name))
            current_position = self._maze.processed_maze()[row][column]
            # Define base case for recursion
            if current_position == 'B':
                jump_points.append(new_node)
            elif current_position == 1:
                # Define base case for recursion
                if self._is_jump_point(new_node, action_name):
                    jump_points.append(new_node)
                # Define recursion cases
                else:
                    # Recursion case for horizontal and vertical movements
                    if action_name in ['up', 'down', 'left', 'right']:
                        jump_points.extend(self._jump_orthogonal(new_node, action_name))
                    else:
                        # Recursion case for diagonal movements
                        jump_points.extend(self._jump_diagonal(new_node, action_name))
        return jump_points

    def _is_jump_point(self, node: Node, action_name: str) -> bool:
        """
        Check if node is jump point.

        :param node: node to check
        :param action_name: action name for new node
        :return: True - if node is jump point, False - otherwise
        """

        if action_name == 'up' or action_name == 'down':
            is_jump_point = self._check_vertical(node, action_name)
        elif action_name == 'right' or action_name == 'left':
            is_jump_point = self._check_horizontal(node, action_name)
        else:
            is_jump_point = self._check_diag(node, action_name)
        return is_jump_point

    def _calc_row_and_column(self, node: Node, action_name: str) -> Tuple[int, int]:
        current_row, current_column = self._get_row_and_column_from_node(node)
        action_row, action_column = self._get_row_and_column_from_action(action_name)
        row = current_row + action_row
        column = current_column + action_column
        return row, column

    def _get_row_and_column_from_node(self, node: Node) -> Tuple[int, int]:
        get_row, get_column = itemgetter(0), itemgetter(1)
        return get_row(node.data), get_column(node.data)

    def _get_row_and_column_from_action(self, action_name: str) -> Tuple[int, int]:
        get_row, get_column = itemgetter(0), itemgetter(1)
        return get_row(self.ACTIONS[action_name]), get_column(self.ACTIONS[action_name])

    def _calc_cost(self, node: Node, action_name: str) -> Union[int, float]:
        action_row, action_column = self._get_row_and_column_from_action(action_name)
        return node.cost + (action_row ** 2 + action_column ** 2) ** 0.5

    def _jump_orthogonal(self, node: Node, action_name: str) -> Union[List[Node], List[None]]:
        return self._get_jump_points(node, action_name)

    def _jump_diagonal(self, node: Node, action_name: str) -> Union[List[Node], List[None]]:
        jump_points = []
        possible_jumps = {
            'upper-right': ('up', 'right'),
            'upper-left': ('down', 'left'),
            'lower-right': ('down', 'right'),
            'lower-left': ('down', 'left'),
        }
        for possible_jump in possible_jumps[action_name]:
            jump_points.extend(self._get_jump_points(node, possible_jump))
        jump_points.extend(self._get_jump_points(node, 'upper-right'))
        return jump_points

    def _check_diag(self, node: Node, action_name: str) -> bool:
        actions_to_check = {
            'upper-right': {
                'row': 'down',
                'column': 'left',
            },
            'lower-right': {
                'row': 'up',
                'column': 'left',
            },
            'upper-left': {
                'row': 'down',
                'column': 'right',
            },
            'lower-left': {
                'row': 'up',
                'column': 'right',
            },
        }
        current_row, current_column = self._get_row_and_column_from_node(node)
        row_to_check, _ = self._calc_row_and_column(node, actions_to_check[action_name]['row'])
        _, column_to_check = self._calc_row_and_column(node, actions_to_check[action_name]['column'])
        width, height = self._maze.get_maze_shape()
        is_jump_point = False
        if (0 < row_to_check < height - 1) and (self._maze.processed_maze()[row_to_check][current_column] == 0):
            _, action_column = self._get_row_and_column_from_action(actions_to_check[action_name]['column'])
            new_column = current_column + action_column
            if (0 < new_column < width - 1) and (self._maze.processed_maze()[row_to_check][new_column] == 1):
                is_jump_point = True
        if (0 < column_to_check < width - 1) and (self._maze.processed_maze()[current_row][column_to_check] == 0):
            action_row, _ = self._get_row_and_column_from_action(actions_to_check[action_name]['row'])
            new_row = current_row + action_row
            if (0 < new_row < height - 1) and (self._maze.processed_maze()[new_row][column_to_check] == 1):
                is_jump_point = True
        return is_jump_point

    def _check_vertical(self, node: Node, action_name: str) -> bool:
        sides_to_check = ['right', 'left']
        is_jump_point = False
        current_row, current_column = self._get_row_and_column_from_node(node)
        width, height = self._maze.get_maze_shape()
        for side in sides_to_check:
            _, column_side = self._calc_row_and_column(node, side)
            if (0 < column_side < width - 1) and (self._maze.processed_maze()[current_row][column_side] == 0):
                row_diag_action, _ = self._get_row_and_column_from_action(action_name)
                _, column_side_action = self._get_row_and_column_from_action(side)
                row_diag = current_row + row_diag_action
                column_left_diag = current_column + column_side_action
                if (0 < row_diag < height-1) and (0 < column_left_diag < width-1) and (self._maze.processed_maze()[row_diag][column_left_diag] == 1):
                    is_jump_point = True
        return is_jump_point

    def _check_horizontal(self, node: Node, action_name: str) -> bool:
        sides_to_check = ['up', 'down']
        is_jump_point = False
        current_row, current_column = self._get_row_and_column_from_node(node)
        width, height = self._maze.get_maze_shape()
        for side in sides_to_check:
            row_side, _ = self._calc_row_and_column(node, side)
            if (0 < row_side < height - 1) and (self._maze.processed_maze()[row_side][current_column] == 0):
                _, column_side = self._get_row_and_column_from_action(action_name)
                row_side_action, _ = self._get_row_and_column_from_action(side)
                column_diag = current_column + column_side
                row_diag = current_row + row_side_action
                if (0 < column_diag < width - 1) and (0 < row_diag < height - 1) and (
                        self._maze.processed_maze()[row_diag][column_diag] == 1):
                    is_jump_point = True
        return is_jump_point