import sys
import random
from pydantic import ValidationError
from srcs.maze_generator import MazeGenerator
from srcs.visualizer import Visualizer
from srcs.color_enum import Color
from srcs.config_validator import ConfigValidator
from typing import Any


colors = [(Color.black, Color.white, Color.green, Color.red, Color.yellow),
          (Color.yellow, Color.blue, Color.pink, Color.purple,
           Color.ultra_pink),
          (Color.dark_green, Color.brown, Color.gray_green, Color.dark_gray,
           Color.yellow),
          (Color.deep_black, Color.neon_pink, Color.ultra_pink,
           Color.ultra_pink, Color.yellow),
          (Color.dark_gray, Color.cigarette, Color.dark_brown,
           Color.dark_brown, Color.yellow)]


def print_maze(palette: Any, is_solved: bool, config: ConfigValidator) -> None:
    visualizer = Visualizer(palette, config)
    if is_solved:
        visualizer.print_maze_path()
    else:
        visualizer.print_maze()


def generate_print_maze(
    palette: Any, is_solved: bool, config: ConfigValidator
) -> None:
    maze = MazeGenerator(config)
    maze._maze_generator()
    maze._solve_maze()
    maze.convert()
    maze._output_data()
    print_maze(palette, is_solved, config)


def load_config() -> ConfigValidator | None:
    """Charge la config et affiche un message clair en cas d'erreur."""
    try:
        return ConfigValidator.from_argv()
    except (FileNotFoundError, ValueError, ValidationError) as err:
        print(f"Configuration error: {err}")
        return None


def main() -> None:
    # Valide et charge la configuration initiale
    config = load_config()
    if config is None:
        return

    random_palette = colors[0]
    is_solved = False
    generate_print_maze(random_palette, is_solved, config)
    try:
        while (True):
            print("===A-Maze-ing===")
            print("1. Re-generate a new maze")
            print("2. Show Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("choice? (1-4)")
            if choice == "1":
                new_config = load_config()
                if new_config is not None:
                    config = new_config
                    generate_print_maze(random_palette, is_solved, config)
            if choice == "2":
                if is_solved:
                    is_solved = False
                else:
                    is_solved = True
                print_maze(random_palette, is_solved, config)
            if choice == "3":
                random_palette = random.choice(colors)
                print_maze(random_palette, is_solved, config)
            if choice == "4":
                sys.exit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
