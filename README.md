# Maze Solver

## Problem Description

This project solves the classic **pathfinding** problem. The maze is represented as a graph where:
- **Nodes** are valid positions in the maze.
- **Edges** are possible moves between nodes.

The goal of the algorithms is to find the shortest path from the start to the target, avoiding obstacles. This approach is used in games, robotics, and navigation systems.

## Implemented Search Algorithms

### Uninformed Algorithms
They use only data structures to decide the next node to expand:

- **DFS (Depth-First Search)**:
  - Uses a stack (LIFO).
  - Complete but not optimal.
  - Efficient in deep mazes but can waste time exploring dead ends.

- **BFS (Breadth-First Search)**:
  - Uses a queue (FIFO).
  - Complete and optimal (if all steps have equal cost).
  - Memory-intensive for large spaces.

### Informed Algorithms
They use heuristics to guide the search:

- **A\***:
  - Uses a priority queue (min-heap).
  - Evaluates nodes with the function:  
    \[
    f(x) = g(x) + h(x)
    \]
    where:
    - \(g(x)\) is the path cost from start to node \(x\),
    - \(h(x)\) is the heuristic estimate from \(x\) to the goal.
  - Complete and optimal if the heuristic is admissible.
  - On large open grids, it may waste time exploring equivalent paths.

- **JPS (Jump Point Search)**:
  - An optimized version of A\* for grids.
  - Skips unnecessary nodes and jumps directly to key points.
  - Significantly speeds up pathfinding on grids.

## Data Structures

### Maze
Stored as a 2D array with **O(1)** access time. Memory usage: **O(N × M)**, where N and M are maze dimensions.

### Stack and Queue
Implemented using a **Double-Linked List**:
- Provides quick access to both head and tail in **O(1)**.
- Suitable for both FIFO (queue) and LIFO (stack) buffers.

### Priority Queue
Implemented using a **min-binary heap**:
- A complete binary tree stored as an array.
- Insert and remove operations in **O(log n)**.
- Uses **sift-up** (insert) and **sift-down** (remove) operations to maintain heap order.

## Project Structure

- **`maze_solver/`** — main source code:
  - `uninformed_solver.py` — DFS and BFS implementations.
  - `informed_solver.py` — A\* and JPS implementations.
  - `data_structure/`:
    - `Maze.py` — maze processing and storage.
    - `DoubleLinkedList.py` — stack and queue.
    - `GraphNode.py` — search node representation.
    - `ListNode.py` — double-linked list node.
    - `BinaryTreeNode.py` — binary heap node.
    - `PriorityQueue.py` — priority queue.
  - `helpers/`:
    - Functions for measuring execution time and saving results.

- **`solutions/`** — stores algorithm results:
  - In **DataFrame** format and **JPEG** visualizations.

- **`examples/`** — usage examples for implemented algorithms.

## Installing Dependencies

```bash
poetry install
