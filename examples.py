from maze_solver import InformedSolver, UninformedSolver, JPS

if __name__ == '__main__':
    maze = UninformedSolver('maze_samples/maze5.txt')
    solution = maze.solve(alg_name='dfs', show_explored=True)
    solution = maze.solve(alg_name='bfs', show_explored=True)

    maze = InformedSolver('maze_samples/maze5.txt')
    solution = maze.solve(heuristic_method='manhattan', show_explored=True)
    solution = maze.solve(heuristic_method='euclid', show_explored=True)

    maze = JPS('maze_samples/maze5.txt')
    solution = maze.solve()