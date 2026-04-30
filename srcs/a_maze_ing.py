import sys
import random
from typing import List, Tuple, Optional, Set, Dict


class MazeGenerator:
    """
    Générateur de labyrinthe.
    Chaque cellule est un entier (0-15) représentant les murs (N, E, S, W).
    """
    def __init__(self, file_name: str) -> None:
        """
        Initialise le générateur de labyrinthe.
        """
        self._width: int = 0
        self._height: int = 0
        self._entry: Tuple[int, int] = (0, 0)
        self._exit: Tuple[int, int] = (0, 0)
        self._output_file: str = ""
        self._perfect: bool = False
        self._seed: Optional[int] = None
        self._maze: List[List[int]] = []
        self._DIRECTIONS = {
            "N": ((-1, 0), 1, 4),
            "E": ((0, 1), 2, 8),
            "S": ((1, 0), 4, 1),
            "W": ((0, -1), 8, 2)
        }
        self._path: List[Tuple[int, int]] = []
        self._path_str: str = ""
        self._REQUIRED_KEYS = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        }
        self.load_config()

    def load_config(self) -> None:
        """
        Charge la configuration depuis un fichier (config.txt).
        Remplit les attributs (voir fonction init)
        Initialise la matrice du labyrinthe à 0.
        """
        parameters = {}
        try:
            with open(sys.argv[1], "r") as f:
                contenu = f.read()
                for line in contenu.split():
                    if "=" in line:
                        key, value = line.split("=", 1)
                        parameters[key] = value
            missing = self._REQUIRED_KEYS - parameters.keys()
            if missing:
                raise ValueError(f"Missing parameters: {missing}")

            # Validate and set WIDTH
            try:
                self._width = int(parameters["WIDTH"])
            except ValueError as e:
                raise ValueError(f"Error: WIDTH must be an integer. {e}")

            # Validate and set HEIGHT
            try:
                self._height = int(parameters["HEIGHT"])
            except ValueError as e:
                raise ValueError(f"Error: HEIGHT must be an integer. {e}")

            # Validate and set ENTRY
            try:
                x, y = parameters["ENTRY"].split(",", 1)
                self._entry = (int(x), int(y))
            except ValueError as e:
                raise ValueError(
                    f"Error: ENTRY must be a tuple of two integers. {e}"
                )

            # Validate and set EXIT
            try:
                exit_parts = parameters["EXIT"].split(",")
                if len(exit_parts) != 2:
                    raise ValueError(
                        "EXIT must be two comma-separated integers"
                    )
                self._exit = (int(exit_parts[0]), int(exit_parts[1]))
            except ValueError as e:
                raise ValueError(
                    f"Error: EXIT must be a tuple of two integers. {e}"
                )

            # Validate and set OUTPUT_FILE
            self._output_file = parameters["OUTPUT_FILE"]
            if not self._output_file:
                raise ValueError(
                    "Error: OUTPUT_FILE must be a non-empty string"
                )

            # Validate and set PERFECT
            perfect_str = parameters["PERFECT"].lower()
            if perfect_str not in ["true", "false"]:
                raise ValueError("Error: PERFECT must be True or False")
            self._perfect = perfect_str == "true"

            # Optional parameters
            if "SEED" in parameters:
                try:
                    self._seed = int(parameters["SEED"])
                except ValueError:
                    self._seed = None

            # Initialize maze
            self._maze = [
                [15 for _ in range(self._width)] for _ in range(self._height)
            ]

        except FileNotFoundError:
            raise FileNotFoundError("Error: file not found")

    def _maze_generator(self) -> None:
        """
        Génère le labyrinthe par backtracking (DFS).
        """
        if self._seed is not None:
            random.seed(self._seed)

        stack: List[Tuple[int, int]] = [self._entry]
        visited: Set[Tuple[int, int]] = {self._entry}

        while stack:
            current_x, current_y = stack[-1]
            neighbors: List = []
            for (offsets, bit_current, bit_neighbor) in \
                    self._DIRECTIONS.values():
                dx, dy = offsets
                nx, ny = current_x + dx, current_y + dy

                if 0 <= nx < self._height and 0 <= ny < self._width:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny, bit_current, bit_neighbor))
            if neighbors:
                nx, ny, b_curr, b_next = random.choice(neighbors)
                self._maze[current_x][current_y] &= ~b_curr
                self._maze[nx][ny] &= ~b_next
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self._perfect:
            self._make_imperfect()

    def _make_imperfect(self, chance: float = 0.05) -> None:
        """
        Supprime aléatoirement des murs pour créer des cycles.
        """
        for r in range(self._height):
            for c in range(self._width):
                if c < self._width - 1 and (self._maze[r][c] & 2):
                    if random.random() < chance:
                        self._maze[r][c] &= ~2
                        self._maze[r][c + 1] &= ~8
                if r < self._height - 1 and (self._maze[r][c] & 4):
                    if random.random() < chance:
                        self._maze[r][c] &= ~4
                        self._maze[r + 1][c] &= ~1

    def _solve_maze(self) -> None:
        """
        Résout le labyrinthe en trouvant le chemin le plus court.
        """
        queue: List[Tuple[int, int]] = [self._entry]
        visited: Set[Tuple[int, int]] = {self._entry}
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            self._entry: None
        }

        while queue:
            current_x, current_y = queue.pop(0)
            if (current_x, current_y) == self._exit:
                break
            for (offsets, bit_current, bit_neighbor) in \
                    self._DIRECTIONS.values():
                dx, dy = offsets
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < self._height and 0 <= ny < self._width:
                    if not (self._maze[current_x][current_y] & bit_current) \
                            and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (current_x, current_y)
                        queue.append((nx, ny))

        if self._exit not in parent:
            print("No path found.")
            self._path = []
            return

        path: List[Tuple[int, int]] = []
        step: Optional[Tuple[int, int]] = self._exit
        while step is not None:
            path.append(step)
            step = parent.get(step)
        self._path = path[::-1]

    def convert(self) -> None:
        """
        Converti le chemin en chaine de caractere
        """
        if not self._path:
            self._path_str = ""
            return

        dirs: List[str] = []
        for i, (r, c) in enumerate(self._path):
            if i == 0:
                continue
            pr, pc = self._path[i - 1]
            dr, dc = r - pr, c - pc
            if (dr, dc) == (-1, 0):
                dirs.append("N")
            elif (dr, dc) == (1, 0):
                dirs.append("S")
            elif (dr, dc) == (0, 1):
                dirs.append("E")
            elif (dr, dc) == (0, -1):
                dirs.append("W")
            else:
                raise ValueError(f"Invalid move from {(pr, pc)} to {(r, c)}")
        self._path_str = "".join(dirs)

    def _output_data(self, file_name: str = "output.txt") -> None:
        """
        Cette fonction
        a pour but de sauvegarder les données dans le fichier de sortie
        """
        try:
            with open(file_name, "w", encoding="utf-8") as file_handle:
                for line in self._maze:
                    line_hex = [format(i, "X") for i in line]
                    file_handle.write("".join(line_hex) + "\n")
                file_handle.write("\n")
                file_handle.write(",".join(str(x) for x in self._entry) + "\n")
                file_handle.write(",".join(str(x) for x in self._exit) + "\n")
                file_handle.write(self._path_str)
        except OSError as err:
            print(err)


def main() -> None:
    try:
        maze_gen = MazeGenerator("config.txt")
        print("Configuration loaded successfully.")
        print(maze_gen.__dict__)
        maze_gen._maze_generator()
        print(maze_gen._maze)
        print("Solving maze...")
        maze_gen._solve_maze()
        print(maze_gen._path)
        maze_gen.convert()
        print(maze_gen._path_str)
        maze_gen._output_data()
    except (ValueError, FileNotFoundError) as e:
        print(e)
        return


if __name__ == "__main__":
    main()
