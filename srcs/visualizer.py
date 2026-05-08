from .color_enum import Color
from typing import List, Tuple


class Visualizer():
    def __init__(
            self,
            palette: List[str],
            width: int,
            height: int,
            file_name: str
                ) -> None:
        self.height = height
        self.width = width

        self.maze = []
        for x in range(0, self.height * 2 + 1):
            array = []
            for y in range(0, self.width * 2 + 1):
                array.append("1")
            self.maze.append(array)

        self.encoded_maze: List[str] = []
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.path: str = ""
        self.color_wall = palette[0]
        self.color_path = palette[1]
        self.color_entry = palette[2]
        self.color_exit = palette[3]
        self.color_solve = palette[4]

        with open(file_name, "r") as f:
            content = f.read().strip()

        parts = content.split("\n\n")

        # 1. Maze
        maze_part = parts[0]
        self.encoded_maze = maze_part.split("\n")

        # 2. Infos
        info_part = parts[1].split("\n")

        x_entry_str, y_entry_str = info_part[0].split(",")
        self.entry = (int(x_entry_str), int(y_entry_str))

        x_exit_str, y_exit_str = info_part[1].split(",")
        self.exit = (int(x_exit_str), int(y_exit_str))
        self.path = info_part[2]

        print("Entry:", self.entry)
        print("Exit:", self.exit)
        print("Path:", self.path)

    def decode_output(self) -> None:
        north = ["1", "3", "5", "7", "9", "B", "D", "F"]
        south = ["4", "5", "6", "7", "C", "D", "E", "F"]
        east = ["2", "3", "6", "7", "A", "B", "E", "F"]
        west = ["8", "9", "A", "B", "C", "D", "E", "F"]

        for j in range(0, self.width):
            for i in range(0, self.height):
                x = j * 2 + 1
                y = i * 2 + 1

                self.maze[y][x] = "0"

                if self.encoded_maze[i][j] not in north:
                    self.maze[y - 1][x] = "0"
                if self.encoded_maze[i][j] not in south:
                    self.maze[y + 1][x] = "0"
                if self.encoded_maze[i][j] not in east:
                    self.maze[y][x + 1] = "0"
                if self.encoded_maze[i][j] not in west:
                    self.maze[y][x - 1] = "0"

    def print_maze(self) -> None:
        self.decode_output()
        x_entry, y_entry = self.entry
        x_exit, y_exit = self.exit

        # Convertir les coordonnées logiques en coordonnées maze
        row_entry = x_entry * 2 + 1
        col_entry = y_entry * 2 + 1
        row_exit = x_exit * 2 + 1
        col_exit = y_exit * 2 + 1

        for row in range(0, self.height * 2 + 1):
            for col in range(0, self.width * 2 + 1):
                if self.maze[row][col] == "0":
                    if row == row_entry and col == col_entry:
                        print(self.color_entry + "██" + Color.reset, end="")
                    elif row == row_exit and col == col_exit:
                        print(self.color_exit + "██" + Color.reset, end="")
                    else:
                        print(self.color_path + "██" + Color.reset, end="")
                elif self.maze[row][col] == "1":
                    print(self.color_wall + "██" + Color.reset, end="")
            print()

    def print_maze_path(self) -> None:
        self.decode_output()
        x_entry, y_entry = self.entry
        x_exit, y_exit = self.exit

        # Convertir les coordonnées logiques en coordonnées maze
        row_entry = x_entry * 2 + 1
        col_entry = y_entry * 2 + 1
        row_exit = x_exit * 2 + 1
        col_exit = y_exit * 2 + 1

        col = col_entry
        row = row_entry

        # Construire le chemin
        path_positions = [(row, col)]

        for direction in self.path:
            if direction == "N":
                path_positions.append((row - 1, col))
                row -= 2
                path_positions.append((row, col))

            elif direction == "S":
                path_positions.append((row + 1, col))
                row += 2
                path_positions.append((row, col))

            elif direction == "E":
                path_positions.append((row, col + 1))
                col += 2
                path_positions.append((row, col))

            elif direction == "W":
                path_positions.append((row, col - 1))
                col -= 2
                path_positions.append((row, col))

        for row in range(0, self.height * 2 + 1):
            for col in range(0, self.width * 2 + 1):
                if self.maze[row][col] == "0":
                    if row == row_entry and col == col_entry:
                        print(self.color_entry + "██" + Color.reset, end="")
                    elif row == row_exit and col == col_exit:
                        print(self.color_exit + "██" + Color.reset, end="")
                    elif (row, col) in path_positions:
                        print(self.color_solve + "██" + Color.reset, end="")
                    else:
                        print(self.color_path + "██" + Color.reset, end="")
                elif self.maze[row][col] == "1":
                    print(self.color_wall + "██" + Color.reset, end="")
            print()
