# CHATGPT INSPIRED
from typing import Optional
import maze_runner

def print_maze(maze: list[list[list[int]]], runner: Optional[tuple[int, int, str]] = None):
    if runner is None:
        runner = (0, 0, "E")

    width = len(maze) - 1
    height = len(maze[0]) - 1

    true_height = height - 1
    runner = (runner[0], true_height-runner[1], runner[2])
    if runner[2] == "N":
        symbol = "^"
    elif runner[2] == "E":
        symbol = ">"
    elif runner[2] == "S":
        symbol = "v"
    elif runner[2] == "W":
        symbol = "<"
    else:
        raise ValueError

    # Iterate through the maze to construct the visual representation
    for y in range(height):
        # Top walls for the row
        for x in range(width):
            print("+", end="")
            print("---" if maze[x][y][0] else "   ", end="")
        print("+")  # Right boundary for the row

        # Side walls for the row
        for x in range(width):
            print("|" if maze[x][y][1] else " ", end="")
            # Print runner or space
            if (x, y) == (runner[0], runner[1]):
                print(f" {symbol} ", end="")
            else:
                print("   ", end="")
        # Check for rightmost boundary for the row
        print("|" if maze[width][y][1] else " ")

    # Bottom walls (final row of horizontal walls)
    for x in range(width):
        print("+---", end="")
    print("+")  # Last corner of the maze


# x = maze_runner.maze_reader("mazes/maze1.mz")
# print_maze(x)