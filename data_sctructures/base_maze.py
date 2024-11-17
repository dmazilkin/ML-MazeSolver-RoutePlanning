class Maze:
    def __init__(self, file_path):
        self._maze = self._read_maze_from_file(file_path)
        self._maze_height = len(self._maze)
        self._maze_width = len(self._maze[0])
        self._start, self._stop = self._find_start_and_stop_coords()

    def processed_maze(self):
        return self._maze

    def get_maze_shape(self):
        '''

        :return: width, height
        '''
        return self._maze_width, self._maze_height

    def get_start(self):
        return self._start

    def get_stop(self):
        return self._stop

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