# Automates (automathwil.py)

Ce dépôt contient un ensemble de fonctions Python pour manipuler des automates finis (DFA/NFA), réaliser des opérations classiques (déterminisation, élimination d'epsilons, produit, concaténation, nettoyage, etc.) et proposer une interface de menu pour tester ces fonctions.

## Objectif du projet
Ce projet vise à fournir un ensemble d'outils pour manipuler, transformer et analyser des automates finis (déterministes et non-déterministes) en Python. Il est adapté pour l'apprentissage, la démonstration et l'expérimentation sur les automates.

## Fichier principal
- `automathwil.py` : implémente les structures et algorithmes pour travailler avec des automates. Il fournit :

### Principales fonctions et explications

#### 1. Affichage des transitions
- `afficheAutomate(matrice)` : Affiche les transitions d'un automate sous forme de matrice (DFA). Chaque ligne représente un état, chaque colonne un symbole. Les transitions sont affichées sous la forme `q<i> ---a<j>---> q<destination>`.
- `afficher_transitions_dict(transitions)` : Affiche les transitions d'un automate sous forme de dictionnaire (NFA ou epsilon). Les clés sont des tuples `(état, symbole)` et les valeurs des listes d'états cibles.

#### 2. Test d'acceptation
- `accepter(matrice, mot, finaux)` : Vérifie si un mot (liste d'entiers représentant les symboles) est accepté par un automate déterministe. Parcourt le mot symbole par symbole, suit les transitions, et vérifie si l'état final atteint est dans la liste des états finaux.

#### 3. Vérification et complétion
- `estComplet(automate)` : Vérifie si toutes les transitions sont définies (pas de `-1` dans la matrice). Retourne `True` si l'automate est complet.
- `Complet(automate)` : Rend l'automate complet en ajoutant un état poubelle et en redirigeant les transitions manquantes vers cet état.

#### 4. Déterminisation
- `determiniser(automate)` : Transforme un automate non-déterministe (NFA) en automate déterministe (DFA) en utilisant l'algorithme des ensembles d'états. Les nouveaux états sont des ensembles d'états originaux, renommés pour la lisibilité.

#### 5. Élimination des transitions epsilon
- `eliminer_transitions_epsilon(automate, epsilon_symbol="EPS")` : Supprime les transitions epsilon (EPS) en dupliquant les transitions sortantes et en recalculant les états finaux. Utilise la fermeture epsilon pour chaque état.

#### 6. Concaténation
- `concatenation(automate1, automate2)` : Crée un automate qui accepte la concaténation des langages des deux automates. Combine les matrices, décale les indices, et ajoute des transitions epsilon des états finaux du premier vers l'état initial du second.

#### 7. Nettoyage
- `nettoyer(automate)` : Supprime les états inutiles (inaccessibles ou ne menant à aucun état final). Conserve seulement les états accessibles depuis l'initial ET co-accessibles (pouvant atteindre un final).

#### 8. Produit cartésien
- `produit_automates(automate1, automate2)` : Calcule le produit de deux automates (intersection des langages). Les états du produit sont des paires d'états, et les transitions sont synchronisées sur l'alphabet commun.

#### 9. Lecture et sauvegarde
- `lire_automate(nom_fichier)` : Lit un automate depuis un fichier texte au format décrit ci-dessous.
- `sauvegarder_automate(automate, nom_fichier)` : Sauvegarde un automate dans un fichier texte.

#### 10. Menu interactif et démonstrations
- Plusieurs fonctions `use_case_*` illustrent chaque opération (affichage, test, déterminisation, etc.) et sont accessibles via un menu interactif dans le terminal.
- La fonction `main()` gère le menu, l'affichage des choix et l'exécution des démonstrations.

### Structure du menu
Le menu propose les opérations suivantes :
1. Afficher transitions
2. Fonction accepter
3. Vérifier si un automate est complet
4. Rendre un automate complet
5. Déterminiser
6. Éliminer epsilon
7. Lire/Sauvegarder automate
8. Nettoyer automate
9. Produit de deux automates
10. Concaténation de deux automates
0. Quitter

Chaque choix lance une démonstration ou une opération sur des exemples intégrés ou des fichiers présents dans le dossier.

## Prérequis
- Python 3.7+ (script écrit en Python pur, pas de dépendances externes).

## Utilisation
1. Ouvrir un terminal dans le dossier contenant `automathwil.py`.
2. Lancer le script :

```bash
python automathwil.py
```

3. Le script affiche un menu interactif. Choisissez un numéro pour exécuter une démonstration (ex. déterminisation, élimination d'epsilon, concaténation, etc.).

### Exemple d'exécution

```
Bienvenue dans Automate!
============================================================
MENU - Automate
============================================================
  1: Afficher transitions
  2: fonction accepter
  ...
  0: Quitter
============================================================
Entrez votre choix: 5
--- Déterminiser (format dict transitions) ---
Automate non-déterministe:
q0 --a--> [q0, q1]
q0 --b--> [q0]
...
Automate déterminisé:
q0 --a--> [q1]
...
États finaux déterminisés: ['q2']
État initial déterminisé: ['q0']
```

## Format attendu pour `lire_automate`
Le format texte attendu pour `lire_automate` (fichier) :
- Ligne 1 : nombre d'états (entier)
- Ligne 2 : nombre de symboles (entier)
- Lignes 3.. : matrice de transitions (une ligne par état, valeurs entières séparées par espaces, `-1` pour absence de transition)
- Avant-dernière ligne : liste des états finaux (séparés par espaces)
- Dernière ligne : état initial (entier)

Exemple minimal (fichier `automate_test.txt`) :

```
3
2
1 0
-1 2
2 -1
2
0
```

### Exemple de fichier automate1.txt
```
2
2
1 -1
-1 0
1
0
```

## Structure du code
- Fonctions utilitaires pour manipuler matrices et dictionnaires de transitions.
- Plusieurs wrappers `use_case_*` qui montrent comment appeler chaque opération.
- Menu principal `main()` pour tester interactivement.

### Organisation des fichiers
- `automathwil.py` : script principal, toutes les fonctions et le menu.
- `automate1.txt`, `automate2.txt` : exemples de fichiers d'automates pour les opérations de lecture, concaténation, etc.

## Extensibilité / Contributions
- Le code est organisé pour être lisible et modulaire : vous pouvez ajouter des fonctions (ex. minimisation) et les rattacher au menu en ajoutant un `use_case` et une entrée dans `MENU`.

### Ajouter une nouvelle opération
Pour ajouter une nouvelle fonctionnalité :
1. Créez une fonction Python (ex : `minimiser(automate)`).
2. Créez un wrapper `use_case_minimiser()` pour la démonstration.
3. Ajoutez une entrée dans le dictionnaire `MENU`.

## Remarques
- Certaines fonctions utilisent deux formats différents pour représenter un automate :
  - Matrice (liste de listes) pour DFA.
  - Dictionnaire de transitions (clé `(etat, symbole)` → liste d'états) pour NFA/epsilon.
- Le script inclut des démonstrations et des conversions entre ces représentations.

### Concepts clés
- **DFA (Automate déterministe)** : chaque état et symbole a une transition unique ou aucune (`-1`).
- **NFA (Automate non-déterministe)** : un état et symbole peuvent avoir plusieurs transitions (liste d'états).
- **Epsilon (EPS)** : transitions qui ne consomment aucun symbole, utilisées pour concaténation ou simplification.
- **Produit cartésien** : intersection des langages, utile pour opérations logiques sur automates.
- **Nettoyage** : suppression des états inutiles pour simplifier l'automate.
