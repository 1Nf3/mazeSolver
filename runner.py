import maze
from typing import Optional, Tuple


def create_runner(x: int = 0, y: int = 0, orientation: str = "N") -> Tuple[int, int, str]:
    xcoord = x
    ycoord = y
    orientation = orientation
    runner = (xcoord, ycoord, orientation)
    return runner


def get_x(runner: Tuple[int, int, str]) -> int:
    return runner[0]


def get_y(runner: Tuple[int, int, str]) -> int:
    return runner[1]


def get_orientation(runner: Tuple[int, int, str]) -> str:
    return runner[2]


def turn(runner: Tuple[int, int, str], direction: str) -> Tuple[int, int, str]:
    if direction == "Left" and runner[2] == "N":
        return (runner[0], runner[1], "W")
    elif direction == "Left" and runner[2] == "E":
        return (runner[0], runner[1], "N")
    elif direction == "Left" and runner[2] == "S":
        return (runner[0], runner[1], "E")
    elif direction == "Left" and runner[2] == "W":
        return (runner[0], runner[1], "S")
    elif direction == "Right" and runner[2] == "N":
        return (runner[0], runner[1], "E")
    elif direction == "Right" and runner[2] == "E":
        return (runner[0], runner[1], "S")
    elif direction == "Right" and runner[2] == "S":
        return (runner[0], runner[1], "W")
    elif direction == "Right" and runner[2] == "W":
        return (runner[0], runner[1], "N")
    else:
        raise ValueError


def forward(runner: Tuple[int, int, str]) -> Tuple[int, int, str]:
    if runner[2] == "N":
        return (runner[0], runner[1] + 1, runner[2])
    if runner[2] == "E":
        return (runner[0]+1, runner[1], runner[2])
    if runner[2] == "S":
        return (runner[0], runner[1] - 1, runner[2])
    if runner[2] == "W":
        return (runner[0] - 1, runner[1], runner[2])

    return runner


def sense_walls(runner: Tuple[int, int, str], maze1: list[list[list[int]]]) -> Tuple[bool, bool, bool]:  # Task 3 !!!
    x = runner[0]
    y = runner[1]
    orientation = runner[2]
    # returns a Tuple of bool[north,east,south,west]
    wallinfo = maze.get_walls(maze1, x, y)
    if orientation == "N":
        sensed = (wallinfo[3], wallinfo[0], wallinfo[1])
    elif orientation == "E":
        sensed = (wallinfo[0], wallinfo[1], wallinfo[2])
    elif orientation == "S":
        sensed = (wallinfo[1], wallinfo[2], wallinfo[3])
    elif orientation == "W":
        sensed = (wallinfo[2], wallinfo[3], wallinfo[0])
    else:
        raise ValueError

    return sensed


def go_straight(runner: Tuple[int, int, str], maze1: list[list[list[int]]]) -> Tuple[int, int, str]:
    if sense_walls(runner, maze1)[1] is False:
        runner = forward(runner)
        return runner
    else:
        raise ValueError


# Implementation of the left-hug algorithm to solve the maze #
def move(runner: Tuple[int, int, str], maze1: list[list[list[int]]]) -> Tuple[Tuple[int, int, str], str]:
    # Returns and stores a Tuple [left,front,right]
    current_sense = sense_walls(runner, maze1)
    movement = ""

    if current_sense[0] is False:
        runner = turn(runner, "Left")
        runner = forward(runner)
        movement = "LF"
    elif current_sense[1] is False:
        runner = forward(runner)
        movement = "F"
    elif current_sense[2] is False:
        runner = turn(runner, "Right")
        runner = forward(runner)
        movement = "RF"
    else:
        runner = turn(runner, "Right")
        runner = turn(runner, "Right")
        runner = forward(runner)
        movement = "RRF"

    move_output = (runner, movement)

    return move_output


def explore(runner: Tuple[int, int, str], maze1: list[list[list[int]]], goal: Optional[Tuple[int, int]] = None) -> str:

    movelist = [(runner[0], runner[1], "")]
    maze_dimensions = maze.get_dimensions(maze1)

    if goal is None:
        goal = (maze_dimensions[0]-1, maze_dimensions[1]-1)

    count = 0

    while (runner[0], runner[1]) != goal:
        move_output = move(runner, maze1)

        runner = move_output[0]
        movement = move_output[1]

        movelist.append((runner[0], runner[1], ""))
        movelist[count] = (movelist[count][0], movelist[count][1], movement)

        count = count + 1

    return str(movelist)
