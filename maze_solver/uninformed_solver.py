from operator import itemgetter
from PIL import Image, ImageDraw
from typing import List, Union

from .data_structure.base_maze import Maze
from .data_structure.node import Node

class UninformedSolver:
    ALGORITHMS = {
        'dfs': -1,
        'bfs': 0,
    }

    RECTANGLE_SIZE = 25

    def __init__(self, file_path):
        self._maze = Maze(file_path)
        self._file_name = file_path.split('/')[-1].split('.')[0]

    def solve(self, alg_name: str = 'dfs', show_explored: bool = False):
        if alg_name not in self.ALGORITHMS:
            raise NameError('No such algorithm.')
        solution, explored = self._solve_maze(alg_name)
        print(len(explored))
        self._save_solution_to_jpeg(solution, explored, alg_name, show_explored)

    def _save_solution_to_jpeg(self, solution, explored, alg_name, show_explored: bool):
        width, height = self._maze.get_maze_shape()
        img = Image.new('RGB', (self.RECTANGLE_SIZE * width, self.RECTANGLE_SIZE * height), color='black')
        idraw = ImageDraw.Draw(img)
        for row in range(height):
            for column in range(width):
                coords = (row, column)
                if coords == self._maze.get_start():
                    color = 'yellow'
                elif coords == self._maze.get_stop():
                    color = 'blue'
                elif coords in solution:
                    color = 'green'
                elif show_explored and coords in explored:
                    color = 'red'
                else:
                    symbol = self._maze.processed_maze()[row][column]
                    if symbol == 1:
                        color = 'white'
                    else:
                        color = 'grey'
                idraw.rectangle([(column * self.RECTANGLE_SIZE, row * self.RECTANGLE_SIZE),
                                 ((column + 1) * self.RECTANGLE_SIZE, (row + 1) * self.RECTANGLE_SIZE)], fill=color)
        img.save(f'./solutions/{self._file_name}_{alg_name}.jpeg')

    def _solve_maze(self, alg_name):
        stack = []
        index = self.ALGORITHMS[alg_name]
        explored = set()
        start_node = Node(data=self._maze.get_start())
        stop_node = self._maze.get_stop()
        found_node = None

        stack.append(start_node)

        while len(stack) != 0:
            node = stack.pop(index)
            explored.add(node.data)
            if node.data == stop_node:
                found_node = node
                break
            else:
                neighbors = [neighbor for neighbor in self._expand_node(node) if neighbor.data not in explored]
                stack.extend(neighbors)

        solution = self._get_solution_path(found_node)
        return solution, explored

    def _get_solution_path(self, target_node):
        solution = set()
        node = target_node
        while node is not None:
            solution.add(node.data)
            node = node.parent
        return solution

    def _expand_node(self, node):
        actions = {
            'up': (1, 0),
            'down': (-1, 0),
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
                    neighbors.append(Node(data=(row, column), action=action, parent=node, cost=node.cost+1))
        return neighbors
