from typing import List, Tuple, Optional


class MazeGenerator:
    """
    Générateur de labyrinthe.
    Chaque cellule est un entier (0-15) représentant les murs (N, E, S, W).
    """
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: Optional[int] = None
    ) -> None:
        """
        Initialise le générateur de labyrinthe.
        :param width: largeur du labyrinthe
        :param height: hauteur du labyrinthe
        :param entry: coordonnées d'entrée (x, y)
        :param exit: coordonnées de sortie (x, y)
        :param output_file: nom du fichier de sortie
        :param perfect: True si le labyrinthe doit être parfait
        :param seed: graine aléatoire (optionnelle)
        """
        self._width: int = width
        self._height: int = height
        self._entry: Tuple[int, int] = entry
        self._exit: Tuple[int, int] = exit
        self._output_file: str = output_file
        self._perfect: bool = perfect
        self._seed: Optional[int] = seed
        # Matrice initialisée à 0 (tous murs ouverts)
        self._maze: List[List[int]] = [
            [0 for _ in range(width)] for _ in range(height)
        ]


def main() -> None:
    pass


if __name__ == "__main__":
    main()
