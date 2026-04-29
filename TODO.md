# A-Maze-ing Project — Sprint 7 Jours


## Jour 1 : Setup & Architecture
- [*] **[Global]** Initialisation du repo Git et du `.gitignore` (Python, Bytecode, venv)
- [*] **[nadoho]** Définir la classe `MazeGenerator` et la structure de données (ex: matrice d'entiers)
- [*] **[tfrances]** Créer le parseur pour `config.txt` (gestion des clés WIDTH, HEIGHT, etc.)
- [*] **[tfrances]** Gérer les erreurs de configuration (valeurs invalides, fichier manquant)

## Jour 2 : Cœur de la Génération
- [ ] **[nadoho]** Implémenter le Recursive Backtracker itératif (avec une stack pour éviter les RecursionError)
- [ ] **[nadoho]** Intégrer le système de seed pour la reproductibilité
- [ ] **[tfrances]** Premier rendu ASCII simple dans le terminal pour visualiser la grille
- [ ] **[tfrances]** Système de navigation de base (boucle d'entrée utilisateur)

## Jour 3 : Algorithmes Spécifiques & Motif 42
- [ ] **[nadoho]** Algorithme de résolution (BFS ou Dijkstra) pour trouver le chemin le plus court
- [ ] **[tfrances]** Implémenter le motif "42" (marquer les cellules comme bloquées avant la génération)
- [ ] **[tfrances]** Vérifier la contrainte "pas de zone ouverte 3x3"
- [ ] **[nadoho]** Conversion du chemin trouvé en format textuel (N, E, S, W)

## Jour 4 : Export & Normes de Code
- [ ] **[nadoho]** Exporter le labyrinthe au format hexadécimal (Bitwise 0-F)
- [ ] **[nadoho]** Écrire le fichier de sortie conforme au sujet
- [ ] **[tfrances]** Mise aux normes du code : type hints partout et conformité flake8 / mypy
- [ ] **[tfrances]** Créer le Makefile (règles install, run, lint, clean)

## Jour 5 : Packaging & Documentation
- [ ] **[nadoho]** Créer les fichiers de packaging (`setup.py` ou `pyproject.toml`) pour générer le `.whl`
- [ ] **[nadoho]** Tester l'installation du module `mazegen-*` dans un environnement vierge
- [ ] **[tfrances]** Rédiger le `README.md`

## Jour 6 : Interactivité & Bonus
- A voir
