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

        if action_name in ['up', 'down', 'right', 'left']:
            is_jump_point = self._check_orthogonal(node, action_name)
        else:
            is_jump_point = self._check_diagonal(node, action_name)
        return is_jump_point

    def _calc_row_and_column(self, node: Node, action_name: str) -> Tuple[int, int]:
        """
        Calculate row and column of a new node.

        :param node: origin node
        :param action_name: action to do
        :return: row and column of new node
        """

        current_row, current_column = self._get_row_and_column_from_node(node)
        action_row, action_column = self._get_row_and_column_from_action(action_name)
        row = current_row + action_row
        column = current_column + action_column
        return row, column

    def _get_row_and_column_from_node(self, node: Node) -> Tuple[int, int]:
        """
        Get row and column of node.

        :param node: origin node
        :return: row and column of node
        """

        get_row, get_column = itemgetter(0), itemgetter(1)
        return get_row(node.data), get_column(node.data)

    def _get_row_and_column_from_action(self, action_name: str) -> Tuple[int, int]:
        """
        Get row and column of action.

        :param action_name: action
        :return: row and column of action
        """

        get_row, get_column = itemgetter(0), itemgetter(1)
        return get_row(self.ACTIONS[action_name]), get_column(self.ACTIONS[action_name])

    def _calc_cost(self, node: Node, action_name: str) -> Union[int, float]:
        """
        Calculate cost of new node.

        :param node: origin node
        :param action_name: action to do
        :return: cost of new node
        """

        action_row, action_column = self._get_row_and_column_from_action(action_name)
        return node.cost + (action_row ** 2 + action_column ** 2) ** 0.5

    def _jump_orthogonal(self, node: Node, action_name: str) -> Union[List[Node], List[None]]:
        """
        Jump in orthogonal direction.

        :param node: node to jump from
        :param action_name: orthogonal action
        :return: jump points if found
        """

        return self._get_jump_points(node, action_name)

    def _jump_diagonal(self, node: Node, action_name: str) -> Union[List[Node], List[None]]:
        """
        Jump in diagonal direction.

        :param node: node to jump from
        :param action_name: diagonal action
        :return: jump points if found
        """

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

    def _check_diagonal(self, node: Node, action_name: str) -> bool:
        """
        Check if node in diagonal movement direction is a jump point.

        :param node: origin node
        :param action_name: diagonal movement direction
        :return: True - if node in diagonal direction is jump point, False - otherwise
        """

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
        # Get node row and column where the wall may be
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

    def _check_orthogonal(self, node: Node, action_name: str) -> bool:
        """
        Check if node in orthogonal movement direction is a jump point.

        :param node: origin node
        :param action_name: orthogonal movement direction
        :return: True - if node in orthogonal direction is jump point, False - otherwise
        """

        sides = {
            'horizontal': ['right', 'left'],
            'vertical': ['up', 'down'],
        }
        is_jump_point = False
        current_row, current_column = self._get_row_and_column_from_node(node)
        # Which orthogonal side to check
        side_to_check = 'horizontal' if action_name in ['up', 'down'] else 'vertical'
        width, height = self._maze.get_maze_shape()
        for side in sides[side_to_check]:
            # Get node row and column where the wall may be
            row_side, column_side = self._calc_row_and_column(node, side)
            row = current_row if side_to_check == 'horizontal' else row_side
            column = column_side if side_to_check == 'horizontal' else current_column
            index_to_check = column if side_to_check == 'horizontal' else row
            border = width if side_to_check == 'horizontal' else height
            # Check if node is the wall
            if (0 < index_to_check < border - 1) and (self._maze.processed_maze()[row][column] == 0):
                row_action, column_action = self._get_row_and_column_from_action(action_name)
                row_side, column_side = self._get_row_and_column_from_action(side)
                column_move = column_side if side_to_check == 'horizontal' else column_action
                row_move =  row_action if side_to_check == 'horizontal' else row_side
                column_diag = current_column + column_move
                row_diag = current_row + row_move
                # Check if there is potential node passage
                if (0 < column_diag < width - 1) and (0 < row_diag < height - 1) and (
                        self._maze.processed_maze()[row_diag][column_diag] == 1):
                    is_jump_point = True
        return is_jump_point