from curses.textpad import rectangle
from operator import itemgetter

from DataSctructures.node import Node

from PIL import Image, ImageDraw

class MazeSolverUninformed:
    def __init__(self, file_path):
        self._maze = self._read_maze_from_file(file_path)
        self._maze_height = len(self._maze)
        self._maze_width = len(self._maze[0])
        self._start, self._stop = self._find_start_and_stop_coords()
        self._target = None

    def _read_maze_from_file(self, file_path):
        content = []
        with open(file_path, 'r') as file:
            for line in file:
                line = [self._process_symbol(symbol) for symbol in list(line.rstrip())]
                content.append(line)
        return content

    def _process_symbol(self, symbol):
        if symbol == '#':
            return 0
        elif symbol == ' ':
            return 1
        else:
            return symbol

    def _find_start_and_stop_coords(self):
        start, stop = None, None
        for row in range(self._maze_height):
            for column in range(self._maze_width):
                if self._maze[row][column] == 'A':
                    start = (row, column)
                if self._maze[row][column] == 'B':
                    stop = (row, column)
        return start, stop

    def solve_maze(self):
        stack = []
        explored = set()
        start_node = Node(data=self._start)
        found_node = None

        stack.append(start_node)

        while len(stack) > 0:
            node = stack.pop(0)
            explored.add(node.data)
            if node.data == self._stop:
                found_node = node
                stack = []
            else:
                neighbors = [neighbor for neighbor in self._expand_node(node) if neighbor.data not in explored]
                stack.extend(neighbors)
        self._target = found_node
        return self._target, explored

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
            if 0 <= row < self._maze_height and 0 <= column < self._maze_width:
                if self._maze[row][column] != 0:
                    neighbors.append(Node(data=(row, column), action=action, parent=node, cost=node.cost+1))
        return neighbors


if __name__ == '__main__':
    rectangle_size = 25
    maze = MazeSolverUninformed('maze_samples/maze4.txt')
    img = Image.new('RGB', (25*maze._maze_width, 25*maze._maze_height), color='black')
    idraw = ImageDraw.Draw(img)
    for row in range(maze._maze_height):
        for column in range(maze._maze_width):
            symbol = maze._maze[row][column]
            if symbol == 0:
                color = 'grey'
            else:
                color = 'white'
            idraw.rectangle([(column*rectangle_size, row*rectangle_size), ((column+1)*rectangle_size, (row+1)*rectangle_size)], fill=color)
    # img.show()

    solution, explored = maze.solve_maze()
    print(solution.cost, print(len(explored)))

    # node = solution
    # while node is not None:
    #     row = node.data[0]
    #     column = node.data[1]
    #     symbol = maze._maze[row][column]
    #     if symbol == 'A':
    #         color = 'red'
    #     elif symbol == 'B':
    #         color = 'yellow'
    #     else:
    #         color = 'green'
    #     idraw.rectangle([(column * rectangle_size, row * rectangle_size),
    #                      ((column + 1) * rectangle_size, (row + 1) * rectangle_size)], fill=color)
    #     node = node.parent

    for coords in explored:
        row = coords[0]
        column = coords[1]
        symbol = maze._maze[row][column]
        if symbol == 'A':
            color = 'red'
        elif symbol == 'B':
            color = 'yellow'
        else:
            color = 'green'
        idraw.rectangle([(column * rectangle_size, row * rectangle_size),
                         ((column + 1) * rectangle_size, (row + 1) * rectangle_size)], fill=color)
    img.show()




