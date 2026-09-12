import runner, maze
import ast
import argparse
import csv
from typing import Optional, Set, Tuple
import mazeprinter

def shortest_path(the_maze: list[list[list[int]]], starting: Optional[Tuple[int, int]] = None, goal: Optional[Tuple[int, int]] = None) -> list[Tuple[int, int]]:
    unrefined_path_without_movement: list[Tuple[int, int]]
    maze_dimensions = maze.get_dimensions(the_maze)

    if goal is None:
        goal = (maze_dimensions[0]-1, maze_dimensions[1]-1)

    if starting is None:
        starting = (0, 0)

    # Error handling for Target & Position
    if (goal[0] > maze_dimensions[0]-1) or (goal[1] > maze_dimensions[1]-1) or goal[0] < 0 or goal[1] < 0:
        raise ValueError("ERROR: Target was out of bounds...")

    if (starting[0] > maze_dimensions[0]-1) or (starting[1] > maze_dimensions[1]-1) or starting[0] < 0 or starting[1] < 0:
        raise ValueError("ERROR: Starting position was out of bounds...")

    # Create the runner at the starting position
    runner1 = runner.create_runner(starting[0], starting[1], "N")

    # Get an unrefined path from exploring the maze.
    string_unrefined_path = runner.explore(runner1, the_maze, goal)

    # Convert string path back to list of Tuples.
    unrefined_path: list[Tuple[int, int, str]
                         ] = ast.literal_eval(string_unrefined_path)

    csv_path = unrefined_path  # Contains log of exploration steps for csv file
    # Exploration_steps exclusive of final coord/destination
    exploration_steps = len(csv_path)-1

    # Create the array without movement details
    unrefined_path_without_movement = [
        (tup[0], int(tup[1])) for tup in unrefined_path]

    # Code for exploration.csv writing
    with open('exploration.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Step', 'x-coordinate', 'y-coordinate', 'Actions'])
        for i in range(0, exploration_steps):
            writer.writerow(
                [i+1, csv_path[i][0], csv_path[i][1], csv_path[i][2]])

    # Initialize the flag and a set for tracking visited coordinates
    flag = True
    temp_visited: Set[Tuple[int, int]] = set()

    while flag is True:

        # Set/Reset visited set to empty
        visited: Set[Tuple[int, int]] = set()
        for coord in unrefined_path:
            coord_Tuple = (int(coord[0]), int(coord[1]))
            if coord_Tuple in visited:

                # Find the first occurence of the repeated coordinate and the NEXT occurence
                first_occurence = unrefined_path_without_movement.index(
                    coord_Tuple)
                next_occurence = unrefined_path_without_movement.index(
                    coord_Tuple, first_occurence+1)

                # Delete the coordinates in between those two points - next occurence exclusive
                del unrefined_path[first_occurence:next_occurence]
                del unrefined_path_without_movement[first_occurence:next_occurence]

                # Because a deletion has taken place exit the for loop to perform another round
                break

            # Add visited coordinate to the set
            visited.add(coord_Tuple)

        # If all nodes can be visited without a break then the algorithm is complete, so set flag to False to exit.
        if visited == temp_visited:
            flag = False
        else:
            temp_visited = visited

    # Code for statistics writing Pt.2
    with open('statistics.txt', 'a') as file:
        score = ((exploration_steps) / 4) + len(unrefined_path)
        file.write("\n")
        file.write(str(score))
        file.write("\n")
        file.write(str(exploration_steps))
        file.write("\n")
        file.write(str(unrefined_path_without_movement))
        file.write("\n")
        file.write(str(len(unrefined_path_without_movement)))

    return unrefined_path_without_movement


def maze_reader(maze_file: str):

    # Handling file opening errors.
    try:
        maze_to_read = open(maze_file, "r")
    except:
        raise IOError("Invalid File Name")

    # Extracting file to 2d array and cleaning up.
    mazearr = maze_to_read.readlines()

    mazearr = [[s.rstrip() for s in row] for row in mazearr]
    mazearr = [[s for s in row if s != ''] for row in mazearr]

    # Checking the maze is in the correct format
    row_length = len(mazearr[0])
    for row in mazearr:
        length = len(row)
        if length != row_length:
            raise ValueError("Erroneous Maze Dimensions")

    if len(mazearr) % 2 == 0 or len(mazearr[0]) % 2 == 0:
        raise ValueError("Maze Constructed Incorrectly")

    for row in mazearr:
        for char in row:
            if char not in ('.', '#'):
                raise ValueError(
                    "Maze Constructed of Innapropriate Strings. Use '.' and '#' for path and walls respectively")

    width = int((len(mazearr[0]) - 1) / 2)
    height = int((len(mazearr) - 1) / 2)

    final_maze = maze.create_maze(width, height)

    h_wall_num = height
    y = height

    for j in range(1, len(mazearr)-1):
        horizontal_flag = False

        if j % 2 != 0:
            y = y - 1

        if j % 2 == 0:
            h_wall_num = h_wall_num-1
            horizontal_flag = True

        x = -1
        v_wall_num = 0

        for i in range(1, len(mazearr[0])-1):

            if i % 2 != 0:
                x = x + 1

            if i % 2 == 0 and j % 2 != 0:
                v_wall_num = v_wall_num + 1
                if mazearr[j][i] == "#":
                    final_maze = maze.add_vertical_wall(
                        final_maze, y, v_wall_num)

            if horizontal_flag is True and i % 2 != 0 and mazearr[j][i] == "#":
                final_maze = maze.add_horizontal_wall(
                    final_maze, x, h_wall_num)

    return final_maze


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="My implementation of the ECS Maze Runner - ******")
    parser.add_argument(
        'maze', type=str, help="The name of the maze file, e.g. the_maze.mz")
    parser.add_argument('--starting', type=str,
                        help='The starting position in format x, y e.g. 2, 6')
    parser.add_argument('--goal', type=str,
                        help='The goal position in format x, y e.g. 10, 5')
    args = parser.parse_args()

    with open("statistics.txt", "w") as file:
        file.write(args.maze)

    the_maze = maze_reader(args.maze)

    # Format exception handling for starting
    if args.starting is not None:
        try:
            starting: Optional[Tuple[int, int]] = None
            starting = ast.literal_eval(args.starting)
        except:
            raise IOError("Incorrect format for --starting. Use format x, y")

        if not isinstance(starting, tuple):
            raise IOError("Incorrect format for --goal. Use format x, y")
        elif len(starting) != 2:
            raise IOError("Incorrect format for --goal. Use format x, y")

    else:
        starting = None

    # Format exception handling for goal
    if args.goal is not None:
        try:
            goal: Optional[Tuple[int, int]] = None
            goal = ast.literal_eval(args.goal)
        except:
            raise IOError("Incorrect format for --goal. Use format x, y")

        if not isinstance(goal, tuple):
            raise IOError("Incorrect format for --goal. Use format x, y")
        elif len(goal) != 2:
            raise IOError("Incorrect format for --goal. Use format x, y")

    else:
        goal = None


    print("Finding the shortest path in the following maze:")
    mazeprinter.print_maze(the_maze)
    print(shortest_path(the_maze, starting, goal))
