Simulating Circuits with A* Pathfinding
=======================================

This project simulates circuit-like pathways using the A* (A-star) algorithm
to find the shortest path through a grid-based maze.

Overview
--------

This is a Python-based simulation involving two main components:

- Maze generation: Creates a grid representing a circuit board or maze.
- A* pathfinding: Navigates the grid from a start to an end point using the
  A* algorithm, which is efficient and widely used in routing, games, and AI.

Together, they model how a connection can be intelligently routed through
obstacles in a simulated environment — similar to how circuits are laid out
on PCBs (Printed Circuit Boards) or how robots plan navigation paths.

How to Run
----------

Make sure you have Python 3 installed.

1. Clone the repository:
   git clone https://github.com/JiuChongZiYue/Simulating-Circuits-.git
   cd Simulating-Circuits-

2. Run the simulation:
   python Maze.py

The script will generate a maze and run the A* algorithm to solve it.

Dependencies
------------

No external libraries required — only standard Python libraries are used.

File Descriptions
-----------------

Maze.py
-------

- Builds a 2D grid (maze or circuit layout).
- Allows configuration of walls or obstacles to simulate realistic circuit paths.
- Defines start and end points.
- Displays the maze and the final path found by the algorithm.
- May include visualization using characters or symbols (e.g., "#" for walls, "*" for path).

Key Features:
- Customizable maze size.
- Random or manual obstacle placement.
- Visual output of the final path and grid state.

A-star.py
---------

- Implements the A* search algorithm:
    - Uses a priority queue to explore paths based on cost and distance.
    - Calculates `f(n) = g(n) + h(n)`, where:
        - g(n) is the cost to reach node n.
        - h(n) is the estimated cost from n to the goal (heuristic).
- Avoids obstacles and finds the optimal path.
- Returns the full path from start to goal.

Key Features:
    There are 2 modes in A-star.py, speed mode and demo mode. 

    Speed mode:  
        1. First it will automatically generate 50 mazes each of the is 101*101 by Maze class. 
        2. Then do Repeated_Forward Search, Repeated_Backward Search, Repeated_Forward Search which prefer small g value, 
           and Repeated_Forward with different h value calculation. 
        3. print how much time each Search took on all 50 mazes. 

    Demo mode: 
        1. Takes a input as how large you want the maze to be. 
        2. User can choose a way of search to use. 
        3. Choose if user want to run it automatically, or manully step by step. 
        4. Show how the agent find a path while discovering the whole environment. 


Example Output
--------------

Start point: (0, 0)
Goal point: (9, 9)
Obstacles placed: 20
Path found: Yes
Steps in path: 18

(Visual path shown in grid format in console)

Author
------

GitHub: @JiuChongZiYue