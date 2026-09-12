# mazeSolver
A Left-Hug Algorithm Maze Solver written in Python for my first university coursework (COMP1312). 

Finds the shortest path from a start position to a goal position in a maze using the simple left-hug algorithm.

(Please be nice it was my first major software project :) )

# Usage

Run using `python3 maze_runner.py mazes/{maze}` or `python3 maze_runner.py mazes/{maze} --starting {x},{y} --goal {x},{y}`

Output will be in the form of a list of coordinate tuples, showcasing the shortest path.

Example mazes are located `mazes`

If a starting and target is not set the mazerunner will start in the bottom left corner and aim to reach the top right.

# Current Limitations

- Maze Printer will break on extremely large mazes and output garbage (doom.mz and above)
- Mazes with loops will break LH


