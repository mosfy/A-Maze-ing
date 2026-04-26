from typing import List, Tuple, Optional, IO


class MazeGenerator:
    """
    Générateur de labyrinthe.
    Chaque cellule est un entier (0-15) représentant les murs (N, E, S, W).
    """
    def __init__(self, file_name: IO[str]) -> None:
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
        self._REQUIRED_KEYS = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        }
        self.load_config(file_name)

    def load_config(self, file_name: IO[str]) -> None:
        """
        Charge la configuration depuis un fichier (config.txt).
        Remplit les attributs (voir fonction init)
        Initialise la matrice du labyrinthe à 0.
        """
        parameters = {}
        try:
            with open(file_name, "r") as f:
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
                [0 for _ in range(self._width)] for _ in range(self._height)
            ]

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: {file_name} file not found")


def main() -> None:
    try:
        maze_gen = MazeGenerator("config.txt")
        print("Configuration loaded successfully.")
        print(maze_gen.__dict__)
    except (ValueError, FileNotFoundError) as e:
        print(e)
        return


if __name__ == "__main__":
    main()
