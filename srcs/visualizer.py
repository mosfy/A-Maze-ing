from color_enum import Color


class Visualizer():
    def __init__(self, palette):
        self.height = 10
        self.width = 10

        self.maze = []
        for x in range(0, self.height * 2 + 1):
            array = []
            for y in range(0, self.width * 2 + 1):
                array.append("1")
            self.maze.append(array)

        self.encoded_maze = []
        self.entry = ()
        self.exit = ()
        self.path = ""
        self.color_wall = palette[0]
        self.color_path = palette[1]
        self.color_entry = palette[2]
        self.color_exit = palette[3]
        self.color_solve = palette[4]

        with open("output.txt", "r") as f:
            content = f.read().strip()

        parts = content.split("\n\n")

        # 1. Maze
        maze_part = parts[0]
        self.encoded_maze = maze_part.split("\n")

        # 2. Infos
        info_part = parts[1].split("\n")

        self.entry = tuple(map(int, info_part[0].split(",")))
        self.exit = tuple(map(int, info_part[1].split(",")))
        self.path = info_part[2]

        print("Entry:", self.entry)
        print("Exit:", self.exit)
        print("Path:", self.path)

    def decode_output(self):
        north = ["1", "3", "5", "7", "9", "B", "D", "F"]
        south = ["4", "5", "6", "7", "C", "D", "E", "F"]
        east = ["2", "3", "6", "7", "A", "B", "E", "F"]
        west = ["8", "9", "A", "B", "C", "D", "E", "F"]
        i = 0
        j = 0
        for x in range(1, self.width * 2, 2):
            for y in range(1, self.height * 2, 2):
                self.maze[y][x] = "0"
                # print(f"{j},{i}: {self.encoded_maze[i][j]}")
                if self.encoded_maze[i][j] not in north:
                    self.maze[y-1][x] = "0"
                if self.encoded_maze[i][j] not in south:
                    self.maze[y+1][x] = "0"
                if self.encoded_maze[i][j] not in east:
                    self.maze[y][x+1] = "0"
                if self.encoded_maze[i][j] not in west:
                    self.maze[y][x-1] = "0"
                # print(f"{x}, {y}")
                i += 1
            i = 0
            j += 1

    def print_maze(self):
        self.decode_output()
        x_entry, y_entry = self.entry
        x_exit, y_exit = self.exit
        x_entry = x_entry * 2 + 1
        y_entry = y_entry * 2 + 1
        x_exit = x_exit * 2 + 1
        y_exit = y_exit * 2 + 1
        for x in range(0, self.width * 2+1):
            for y in range(0, self.height * 2+1):
                if self.maze[x][y] == "0":
                    if x == x_entry and y == y_entry:
                        print(self.color_entry + "██" + Color.reset, end="")
                    elif x == x_exit and y == y_exit:
                        print(self.color_exit + "██" + Color.reset, end="")
                    else:
                        print(self.color_path + "██" + Color.reset, end="")
                elif self.maze[x][y] == "1":
                    print(self.color_wall + "██" + Color.reset, end="")
            print()

    def print_maze_path(self):
        self.decode_output()
        x_entry, y_entry = self.entry
        x_exit, y_exit = self.exit
        x_entry = x_entry * 2 + 1
        y_entry = y_entry * 2 + 1
        x_exit = x_exit * 2 + 1
        y_exit = y_exit * 2 + 1

        x = x_entry
        y = y_entry

        # Construire le chemin
        path_positions = [(y, x)]

        for direction in self.path:
            if direction == "N":
                path_positions.append((y - 1, x))
                y -= 2
                path_positions.append((y, x))

            elif direction == "S":
                path_positions.append((y + 1, x))
                y += 2
                path_positions.append((y, x))

            elif direction == "E":
                path_positions.append((y, x + 1))
                x += 2
                path_positions.append((y, x))

            elif direction == "W":
                path_positions.append((y, x - 1))
                x -= 2
                path_positions.append((y, x))

        print(path_positions)
        for x in range(0, self.width * 2+1):
            for y in range(0, self.height * 2+1):
                if self.maze[x][y] == "0":
                    if x == x_entry and y == y_entry:
                        print(self.color_entry + "█" + Color.reset, end="")
                    elif x == x_exit and y == y_exit:
                        print(self.color_exit + "█" + Color.reset, end="")
                    elif (x, y) in path_positions:
                        print(self.color_solve + "█" + Color.reset, end="")
                    else:
                        print(self.color_path + "█" + Color.reset, end="")
                elif self.maze[x][y] == "1":
                    print(self.color_wall + "█" + Color.reset, end="")
            print()
