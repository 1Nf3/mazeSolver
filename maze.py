from typing import Tuple


def create_maze(width: int = 5, height: int = 5) -> list[list[list[int]]]:
    maze = [[[0, 0] for _ in range(height+1)]for _ in range(width + 1)]

    # maze[x][y][0] = horizontal wall above the cell at (x,y)
    # maze[x][y][1] = vertical wall to the left of the cell at (x,y,)
    for x in range(width+1):
        maze[x][0][0] = 1
        maze[x][height][0] = 1

    for y in range(height+1):
        maze[0][y][1] = 1
        maze[width][y][1] = 1

    return maze


def add_horizontal_wall(maze: list[list[list[int]]], x_coordinate: int, horizontal_line: int) -> list[list[list[int]]]:
    horizontal_lineval = get_dimensions(maze)[1]
    maze[x_coordinate][horizontal_lineval-horizontal_line][0] = 1
    return maze


def add_vertical_wall(maze: list[list[list[int]]], y_coordinate: int, vertical_line: int) -> list[list[list[int]]]:
    yval = get_dimensions(maze)[1] - 1
    maze[vertical_line][yval-y_coordinate][1] = 1
    return maze


def get_dimensions(maze: list[list[list[int]]]) -> Tuple[int, int]:
    width = len(maze) - 1
    height = len(maze[0]) - 1
    return (width, height)


# Is there a wall in North, East, South and West
def get_walls(maze: list[list[list[int]]], x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    directionsarr: list[bool] = [False, False, False, False]
    height = get_dimensions(maze)[1] - 1

    # Checking for North wall
    if maze[x_coordinate][height - y_coordinate][0] == 1:
        directionsarr[0] = True

    # Checking for West wall
    if maze[x_coordinate][height - y_coordinate][1] == 1:
        directionsarr[3] = True

    # Checking for East wall
    if maze[x_coordinate + 1][height - y_coordinate][1] == 1:
        directionsarr[1] = True

    # Checking for South wall
    if maze[x_coordinate][height - y_coordinate+1][0] == 1:
        directionsarr[2] = True

    # Convert the array to a Tuple
    directions = (directionsarr[0], directionsarr[1],
                  directionsarr[2], directionsarr[3])
    return directions
