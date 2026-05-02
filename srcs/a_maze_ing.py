import sys
import random
from maze_generator import MazeGenerator
from visualizer import Visualizer
from color_enum import Color

colors = [(Color.black, Color.white, Color.green, Color.red, Color.yellow),
          (Color.yellow, Color.blue, Color.pink, Color.purple, Color.ultra_pink),
          (Color.dark_green, Color.brown, Color.gray_green, Color.dark_gray,
           Color.yellow),
          (Color.deep_black, Color.neon_pink, Color.ultra_pink,
           Color.ultra_pink, Color.yellow),
          (Color.dark_gray, Color.cigarette, Color.dark_brown,
           Color.dark_brown, Color.yellow)]


def print_maze(palette, is_solved):
    visualizer = Visualizer(palette)
    if is_solved:
        visualizer.print_maze_path()
    else:
        visualizer.print_maze()


def generate_print_maze(palette, is_solved):
    maze = MazeGenerator()
    maze._maze_generator()
    maze._solve_maze()
    maze.convert()
    maze._output_data()
    print_maze(palette, is_solved)


def main() -> None:
    random_palette = colors[0]
    is_solved = False
    generate_print_maze(random_palette, is_solved)
    try:
        while (True):
            print("===A-Maze-ing===")
            print("1. Re-generate a new maze")
            print("2. Show Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("choice? (1-4)")
            if choice == "1":
                generate_print_maze(random_palette, is_solved)
            if choice == "2":
                if is_solved:
                    is_solved = False
                else:
                    is_solved = True
                print_maze(random_palette, is_solved)
            if choice == "3":
                random_palette = random.choice(colors)
                print_maze(random_palette, is_solved)
            if choice == "4":
                sys.exit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
