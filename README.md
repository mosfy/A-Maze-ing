*This project has been created as part of the 42 curriculum by nadoho, tfrances*

# A-MAZE-ING

## Description

A-Maze-ing est un générateur de labyrinthes en Python, avec résolution du plus court chemin et rendu visuel dans le terminal.

Le projet produit un fichier de sortie conforme au sujet:
- une grille hexadécimale (1 cellule = 1 caractère hexadécimal);
- puis une ligne vide;
- puis `ENTRY`, `EXIT` et le chemin solution (`N`, `E`, `S`, `W`).

## Features

- Génération aléatoire de labyrinthe (DFS itératif / recursive backtracking).
- Mode `PERFECT` (labyrinthe parfait) et mode imparfait (ajout de cycles contrôlés).
- Résolution en plus court chemin avec BFS.
- Encodage hexadécimal des murs par cellule.
- Rendu terminal avec interactions:
	- régénérer un labyrinthe,
	- afficher/masquer le chemin solution,
	- changer la palette de couleurs.

## Instructions

### Prérequis

- Python 3.10+ recommandé
- `uv` (ou `pip` si vous préférez)

### Installation

```bash
make install
```

### Exécution

```bash
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
make lint-strict
```

### Nettoyage

```bash
make clean
```

## Configuration file format (`config.txt`)

Clé/valeur au format `KEY=VALUE`, une par ligne.

### Clés obligatoires

- `WIDTH` : largeur du labyrinthe (int)
- `HEIGHT` : hauteur du labyrinthe (int)
- `ENTRY` : coordonnées `row,col`
- `EXIT` : coordonnées `row,col`
- `OUTPUT_FILE` : nom du fichier de sortie
- `PERFECT` : `TRUE` ou `FALSE`

### Clés optionnelles

- `SEED` : entier pour reproductibilité (support prévu dans la config)

### Exemple

```txt
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=5,9
OUTPUT_FILE=output.txt
PERFECT=TRUE
SEED=42
```

## Output encoding (walls)

Chaque cellule est encodée sur 4 bits selon l'ordre `N E S W`:

- bit 0 (`1`) = North
- bit 1 (`2`) = East
- bit 2 (`4`) = South
- bit 3 (`8`) = West

`1` = mur fermé, `0` = mur ouvert.

Exemples:
- `3` (`0011`) -> North + East fermés
- `A` (`1010`) -> East + West fermés

## Maze generation algorithm

Algorithme choisi: **Recursive Backtracking itératif (DFS avec pile)**.

Pourquoi ce choix:
- simple à implémenter et à maintenir;
- très bon pour générer des labyrinthes connectés;
- performant en pratique;
- facile à adapter en mode parfait/imparfait.

Pour la résolution, on utilise **BFS** afin d'obtenir un plus court chemin valide entre entrée et sortie.

## Reusable part

La partie réutilisable est la classe `MazeGenerator` dans `srcs/maze_generator.py`.

Elle permet:
- de charger une configuration,
- de générer la structure du labyrinthe,
- de résoudre le labyrinthe,
- de produire un chemin solution,
- d'exporter un fichier de sortie.

Exemple minimal:

```python
from srcs.maze_generator import MazeGenerator

maze = MazeGenerator()
maze._maze_generator()
maze._solve_maze()
maze.convert()
maze._output_data()
```

Note: le packaging dédié `mazegen-*` demandé par le sujet est préparé via `pyproject.toml`, et peut être finalisé/renommé selon la convention d'évaluation.

## Team & project management

### Roles

- `nadoho`: génération, résolution, export, intégration principale.
- `tfrances`: parsing/config, affichage terminal, interactions utilisateur, corrections visuelles.

### Planning (prévu vs réel)

- Le sprint initial en 7 jours a servi de base de suivi (voir `TODO.md`).
- Certaines tâches ont évolué en cours de route (corrections de génération, conformité lint, merge fixes).


### Tools used

- Git / GitHub
- Python 3
- uv
- flake8
- mypy

## Resources

- [Maze Generation — Recursive Backtracking](https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766)
- [Python Documentation](https://docs.python.org/3/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [flake8 Documentation](https://flake8.pycqa.org/)

## AI usage

L'IA a été utilisée comme assistant de développement pour:
- clarifier certaines exigences du sujet;
- proposer des corrections de structure (README/Makefile);
- accélérer la revue de conformité (lint, format de sortie, checklist d'évaluation).

Le design, les choix algorithmiques et l'intégration finale ont été validés et ajustés par l'équipe.
