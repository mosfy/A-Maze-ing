from typing import List, Tuple, Optional, IO


class MazeGenerator:
    """
    Générateur de labyrinthe.
    Chaque cellule est un entier (0-15) représentant les murs (N, E, S, W).
    """
    def __init__(self) -> None:
        """
        Initialise le générateur de labyrinthe (attributs vides, à remplir via load_config).
        """
        self._width: int = 0
        self._height: int = 0
        self._entry: Tuple[int, int] = (0, 0)
        self._exit: Tuple[int, int] = (0, 0)
        self._output_file: str = ""
        self._perfect: bool = False
        self._seed: Optional[int] = None
        self._maze: List[List[int]] = []

    def load_config(self, file: IO[str]) -> None:
        """
        Charge la configuration depuis un fichier ouvert (config.txt).
        Remplit les attributs width, height, entry, exit, output_file, perfect, seed.
        Initialise la matrice du labyrinthe à 0.
        """
        pass


def main() -> None:
    pass


if __name__ == "__main__":
    main()
