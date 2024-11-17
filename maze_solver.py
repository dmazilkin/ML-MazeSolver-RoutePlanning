from operator import itemgetter
from queue import PriorityQueue
from PIL import Image, ImageDraw

from data_sctructures.base_maze import Maze
from data_sctructures.node import Node

class UninformedSolver:
    ALGORITHMS = {
        'dfs': -1,
        'bfs': 0,
    }

    def __init__(self, file_path):
        self._maze = Maze(file_path)
        self._file_name = file_path.split('/')[-1].split('.')[0]

    def solve(self, alg_name: str = 'dfs'):
        if alg_name not in self.ALGORITHMS:
            raise NameError('No such algorithm.')
        solution, explored = self._solve_maze(alg_name)
        self._save_solution_to_jpeg(explored, alg_name)

    def _save_solution_to_jpeg(self, explored, alg_name):
        rectangle_size = 25
        width, height = self._maze.get_maze_shape()
        img = Image.new('RGB', (25 * width, 25 * height), color='black')
        idraw = ImageDraw.Draw(img)
        for row in range(height):
            for column in range(width):
                symbol = self._maze.processed_maze()[row][column]
                if symbol == 0:
                    color = 'grey'
                else:
                    color = 'white'
                idraw.rectangle([(column * rectangle_size, row * rectangle_size),
                                 ((column + 1) * rectangle_size, (row + 1) * rectangle_size)], fill=color)

        for coords in explored:
            row = coords[0]
            column = coords[1]
            symbol = self._maze.processed_maze()[row][column]
            if symbol == 'A':
                color = 'red'
            elif symbol == 'B':
                color = 'yellow'
            else:
                color = 'green'
            idraw.rectangle([(column * rectangle_size, row * rectangle_size),
                             ((column + 1) * rectangle_size, (row + 1) * rectangle_size)], fill=color)

        img.save(f'./solutions/{self._file_name}_{alg_name}.jpeg')

    def _solve_maze(self, alg_name: str = 'dfs'):
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
        return found_node, explored

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
            if 0 <= row < height and 0 <= column < width:
                if self._maze.processed_maze()[row][column] != 0:
                    neighbors.append(Node(data=(row, column), action=action, parent=node, cost=node.cost+1))
        return neighbors

class InformedSolver:
    HEURISTIC_METHODS = ('manhattan', 'euclid')

    def __init__(self, file_path):
        self._maze = Maze(file_path)
        self._file_name = file_path.split('/')[-1].split('.')[0]

    def solve(self, heuristic_method: str = 'manhattan'):
        if heuristic_method not in self.HEURISTIC_METHODS:
            raise NameError('No such heuristic method.')
        solution, explored = self._solve_maze(method=heuristic_method)
        self._save_solution_to_jpeg(explored, heuristic_method)

    def _solve_maze(self, method: str = 'manhattan'):
        queue = PriorityQueue()
        explored = set()
        start_node = Node(data=self._maze.get_start())
        stop_node = self._maze.get_stop()
        found_node = None

        queue.put((self._get_heuristic(start_node, method=method), id(start_node), start_node))

        while not queue.empty():
            heuristic, _, node = queue.get()
            explored.add(node.data)
            if node.data == stop_node:
                found_node = node
                break
            else:
                neighbors = [neighbor for neighbor in self._expand_node(node) if neighbor.data not in explored]
                if len(neighbors) != 0:
                    for neighbor in neighbors:
                        queue.put((self._get_heuristic(neighbor, method=method), id(neighbor), neighbor))
        return found_node, explored

    def _save_solution_to_jpeg(self, explored, method):
        rectangle_size = 25
        width, height = self._maze.get_maze_shape()
        img = Image.new('RGB', (25 * width, 25 * height), color='black')
        idraw = ImageDraw.Draw(img)
        for row in range(height):
            for column in range(width):
                symbol = self._maze.processed_maze()[row][column]
                if symbol == 0:
                    color = 'grey'
                else:
                    color = 'white'
                idraw.rectangle([(column * rectangle_size, row * rectangle_size),
                                 ((column + 1) * rectangle_size, (row + 1) * rectangle_size)], fill=color)

        for coords in explored:
            row = coords[0]
            column = coords[1]
            symbol = self._maze.processed_maze()[row][column]
            if symbol == 'A':
                color = 'red'
            elif symbol == 'B':
                color = 'yellow'
            else:
                color = 'green'
            idraw.rectangle([(column * rectangle_size, row * rectangle_size),
                             ((column + 1) * rectangle_size, (row + 1) * rectangle_size)], fill=color)

        img.save(f'./solutions/{self._file_name}_{method}.jpeg')

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
            if 0 <= row < height and 0 <= column < width:
                if self._maze.processed_maze()[row][column] != 0:
                    neighbors.append(Node(data=(row, column), action=action, parent=node, cost=node.cost+1))
        return neighbors

    def _get_heuristic(self, node, method='manhattan'):
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


if __name__ == '__main__':
    maze = UninformedSolver('maze_samples/maze4.txt')
    solution = maze.solve(alg_name='dfs')
    solution = maze.solve(alg_name='bfs')

    maze = InformedSolver('maze_samples/maze4.txt')
    solution = maze.solve(heuristic_method='manhattan')
    solution = maze.solve(heuristic_method='euclid')