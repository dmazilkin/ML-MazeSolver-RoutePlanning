from time import time
from os import path
import pandas as pd

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        func_output = func(*args, **kwargs)
        stop = time()
        return func_output, stop - start
    return wrapper

def save_results(maze_name: str, alg_name: str, solution: int, explored: int, time: float):
    if not path.isfile('solutions/results.csv'):
        df = pd.DataFrame(data={'Maze name': maze_name, 'Algorithm name': alg_name, 'Solution': solution, 'Explored': explored, 'Time': time}, index=[0])
        df = df.set_index('Maze name')
        df.to_csv('solutions/results.csv')
    else:
        results = pd.read_csv('solutions/results.csv', index_col=0)
        df = pd.DataFrame(data={'Maze name': maze_name, 'Algorithm name': alg_name, 'Solution': solution, 'Explored': explored, 'Time': time}, index=[0])
        df = df.set_index('Maze name')
        updated_results = pd.concat([results, df], join='inner')
        updated_results.to_csv('solutions/results.csv', mode='w')