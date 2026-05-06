"""mazegen
=======

Générateur de labyrinthe réutilisable pour un usage dans d'autres projets.

Ce module expose une seule classe publique : `MazeGenerator`.

Démarrage rapide
----------------

```python
from mazegen import MazeGenerator

    generator = MazeGenerator(width=10, height=8, seed=42, perfect=False)
maze = generator.maze              # grille 2D de bitmasks
solution = generator.solution      # liste de coordonnées (ligne, colonne)
path = generator.solution_directions
```

Paramètres personnalisés
------------------------

`MazeGenerator` accepte :

- `width` et `height` : dimensions du labyrinthe
- `entry` et `exit` : coordonnées optionnelles `(ligne, colonne)`
- `perfect` : mettre `False` pour ajouter des boucles
- `seed` : génération déterministe si fournie

Accès à la structure générée
----------------------------

- `maze` : grille où chaque cellule est un bitmask représentant les murs
- `entry` / `exit` : points d'entrée et de sortie sélectionnés
- `solution` : liste des coordonnées allant de l'entrée à la sortie
- `solution_directions` : chaîne avec les déplacements `N`, `E`, `S`, `W`

La structure est volontairement simple et peut être différente du format
utilisé dans les fichiers de sortie du reste du projet.
"""

from __future__ import annotations

from collections import deque
import random
from typing import Deque, Dict, List, Optional, Sequence, Set, Tuple

Cell = Tuple[int, int]
Grid = List[List[int]]


class MazeGenerator:
    """Génère et résout un labyrinthe.

    Paramètres
    ----------
    width:
        Nombre de colonnes du labyrinthe.
    height:
        Nombre de lignes du labyrinthe.
    entry:
        Cellule de départ optionnelle sous la forme `(ligne, colonne)`.
        Par défaut : `(0, 0)`.
    exit:
        Cellule d'arrivée optionnelle sous la forme `(ligne, colonne)`.
        Par défaut : le coin inférieur droit.
    perfect:
        Si `True`, le labyrinthe est parfait (un seul chemin possible entre
        deux cellules). Si `False`, des passages supplémentaires sont ouverts
        pour créer des boucles via `_open_extra_passages()`.
    seed:
        Graine aléatoire optionnelle pour une génération reproductible.
    """

    _DIRECTIONS: Dict[str, Tuple[Tuple[int, int], int, int]] = {
        "N": ((-1, 0), 1, 4),
        "E": ((0, 1), 2, 8),
        "S": ((1, 0), 4, 1),
        "W": ((0, -1), 8, 2),
    }

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        entry: Optional[Cell] = None,
        exit: Optional[Cell] = None,
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry if entry is not None else (0, 0)
        self.exit = exit if exit is not None else (height - 1, width - 1)
        self.perfect = perfect
        self.seed = seed
        self._rng = random.Random(seed)
        self._maze: Grid = []
        self._solution: List[Cell] = []
        self._solution_directions: str = ""

        self._validate()
        self.generate(perfect=perfect)
        self.solve()

    def _validate(self) -> None:
        if self.width < 2 or self.height < 2:
            raise ValueError("width and height must be at least 2")
        for label, cell in (("entry", self.entry), ("exit", self.exit)):
            row, col = cell
            if not (0 <= row < self.height and 0 <= col < self.width):
                raise ValueError(f"{label} {cell} is outside the maze bounds")
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different")

    @property
    def maze(self) -> Grid:
        """Retourne la grille du labyrinthe sous forme de bitmasks."""

        return self._maze

    @property
    def solution(self) -> List[Cell]:
        """Retourne le plus court chemin entre l'entrée et la sortie."""

        return self._solution

    @property
    def solution_directions(self) -> str:
        """Retourne la solution encodée avec les déplacements
        `N`, `E`, `S`, `W`."""

        return self._solution_directions

    def generate(self, *, perfect: Optional[bool] = None) -> Grid:
        """Génère un nouveau labyrinthe et le retourne.

        Si `perfect` est fourni, il remplace temporairement le mode courant.
        """

        if perfect is not None:
            self.perfect = perfect

        self._maze = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]

        stack: List[Cell] = [self.entry]
        visited: Set[Cell] = {self.entry}

        while stack:
            row, col = stack[-1]
            neighbors: List[Tuple[int, int, int, int]] = []

            for offsets, current_bit, next_bit in self._DIRECTIONS.values():
                d_row, d_col = offsets
                next_row = row + d_row
                next_col = col + d_col
                if 0 <= next_row < self.height and 0 <= next_col < self.width:
                    if (next_row, next_col) not in visited:
                        neighbors.append(
                            (next_row, next_col, current_bit, next_bit)
                        )

            if neighbors:
                next_row, next_col, current_bit, next_bit = (
                    self._rng.choice(neighbors)
                )
                self._maze[row][col] &= ~current_bit
                self._maze[next_row][next_col] &= ~next_bit
                visited.add((next_row, next_col))
                stack.append((next_row, next_col))
            else:
                stack.pop()

        if not self.perfect:
            self._open_extra_passages()

        return self._maze

    def _open_extra_passages(self, chance: float = 0.05) -> None:
        """Ouvre quelques murs supplémentaires pour créer des boucles."""

        for row in range(self.height):
            for col in range(self.width):
                if col < self.width - 1 and self._maze[row][col] & 2:
                    if self._rng.random() < chance:
                        self._maze[row][col] &= ~2
                        self._maze[row][col + 1] &= ~8

                if row < self.height - 1 and self._maze[row][col] & 4:
                    if self._rng.random() < chance:
                        self._maze[row][col] &= ~4
                        self._maze[row + 1][col] &= ~1

    def solve(self) -> List[Cell]:
        """Résout le labyrinthe et retourne le plus court chemin."""

        queue: Deque[Cell] = deque([self.entry])
        visited: Set[Cell] = {self.entry}
        parent: Dict[Cell, Optional[Cell]] = {self.entry: None}

        while queue:
            row, col = queue.popleft()
            if (row, col) == self.exit:
                break

            for offsets, current_bit, _next_bit in self._DIRECTIONS.values():
                d_row, d_col = offsets
                next_row = row + d_row
                next_col = col + d_col
                if 0 <= next_row < self.height and 0 <= next_col < self.width:
                    if not (self._maze[row][col] & current_bit) and (
                        next_row,
                        next_col,
                    ) not in visited:
                        visited.add((next_row, next_col))
                        parent[(next_row, next_col)] = (row, col)
                        queue.append((next_row, next_col))

        if self.exit not in parent:
            self._solution = []
            self._solution_directions = ""
            return self._solution

        path: List[Cell] = []
        step: Optional[Cell] = self.exit
        while step is not None:
            path.append(step)
            step = parent.get(step)

        self._solution = path[::-1]
        self._solution_directions = self._path_to_directions(self._solution)
        return self._solution

    def _path_to_directions(self, path: Sequence[Cell]) -> str:
        directions: List[str] = []
        for index, (row, col) in enumerate(path):
            if index == 0:
                continue
            prev_row, prev_col = path[index - 1]
            delta = (row - prev_row, col - prev_col)
            if delta == (-1, 0):
                directions.append("N")
            elif delta == (1, 0):
                directions.append("S")
            elif delta == (0, 1):
                directions.append("E")
            elif delta == (0, -1):
                directions.append("W")
            else:
                raise ValueError(
                    f"Invalid move from {(prev_row, prev_col)} to {(row, col)}"
                )
        return "".join(directions)

    def regenerate(
        self,
        *,
        seed: Optional[int] = None,
        perfect: Optional[bool] = None,
    ) -> Grid:
        """Régénère le labyrinthe, avec éventuellement une nouvelle graine
        ou un nouveau mode `perfect`.
        """

        if seed is not None:
            self.seed = seed
            self._rng = random.Random(seed)
        self.generate(perfect=perfect)
        self.solve()
        return self._maze


__all__ = ["MazeGenerator"]
