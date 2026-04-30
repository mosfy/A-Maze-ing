# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    visualizer.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tfrances <tfrances@student.42lehavre.fr>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/30 03:28:37 by tfrances          #+#    #+#              #
#    Updated: 2026/04/30 04:18:56 by tfrances         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from color_enum import Color


class Visualizer():
    def __init__(self):
        self.height = 5
        self.width = 5

        self.maze = []
        for x in range(0, self.height * 2 + 1):
            arrey = []
            for y in range(0, self.width * 2 + 1):
                arrey.append("1")
            self.maze.append(arrey)
                
        self.encoded_maze = []
        self.entry = ()
        self.exit = ()
        self.path = ""

        with open("../output.txt", "r") as f:
            content = f.read()
        number_n = 0
        res = ""
        for char in content:
            if char == "\n":
                number_n += 1
            else:
                number_n = 0
            if number_n == 2:
                break
            res += char

        self.encoded_maze = res.split("\n")
        self.encoded_maze.pop()
        print(self.encoded_maze)

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
        # self.maze[5][3] = "ntm"

    def print_maze(self):
        for x in range(0, self.width * 2+1):
            for y in range(0, self.height * 2+1):
                if self.maze[x][y] == "0":
                    print("█", end="")
                elif self.maze[x][y] == "1":
                    print(Color.black + "█" + Color.reset, end="")
            print()

if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.decode_output()
    visualizer.print_maze()
