# PROJETF - Gestionnaire d'Automates Finis

Un outil interactif en Python pour créer, manipuler et transformer des **automates finis** (déterministes et non-déterministes). Ce projet couvre l'ensemble des opérations classiques de la théorie des automates : déterminisation, complétion, complémentaire, élimination des epsilon-transitions, concaténation, produit cartésien et nettoyage.

---

## Table des matières

1. [Objectif du projet](#objectif-du-projet)
2. [Concepts théoriques](#concepts-théoriques)
3. [Prérequis](#prérequis)
4. [Lancement](#lancement)
5. [Structure du menu interactif](#structure-du-menu-interactif)
6. [Représentation des automates](#représentation-des-automates)
7. [Fonctions principales et algorithmes](#fonctions-principales-et-algorithmes)
8. [Formats de fichier](#formats-de-fichier)
9. [Exemple d'utilisation pas à pas](#exemple-dutilisation-pas-à-pas)
10. [Organisation du code](#organisation-du-code)
11. [Ajouter une nouvelle opération](#ajouter-une-nouvelle-opération)

---

## Objectif du projet

Ce projet fournit une boîte à outils complète pour :

- **Créer** des automates finis via une interface console interactive (DFA, NFA, NFA-epsilon)
- **Transformer** des automates : déterminisation, complétion, élimination d'epsilon, complémentaire
- **Combiner** des automates : concaténation de langages, produit cartésien (intersection)
- **Analyser** des automates : test d'acceptation de mots, vérification de propriétés (complet, déterministe)
- **Nettoyer** des automates : suppression des états inaccessibles et non co-accessibles
- **Sauvegarder et charger** des automates depuis/vers des fichiers

Il est conçu pour l'apprentissage et la mise en pratique de la théorie des langages formels et des automates.

---

## Concepts théoriques

| Concept | Description |
|---|---|
| **DFA** (Automate Fini Déterministe) | Pour chaque couple (état, symbole), il existe **au plus une** transition. Pas de transition epsilon. |
| **NFA** (Automate Fini Non-Déterministe) | Pour chaque couple (état, symbole), il peut exister **plusieurs** transitions simultanées. |
| **Epsilon-transition (EPS)** | Transition qui ne consomme aucun symbole d'entrée. Permet de passer d'un état à un autre "gratuitement". |
| **État poubelle** | État ajouté lors de la complétion : toutes les transitions manquantes pointent vers cet état, qui boucle sur lui-même. |
| **Fermeture epsilon** | Ensemble de tous les états atteignables depuis un état donné en suivant uniquement des epsilon-transitions. |
| **Complémentaire** | Automate qui accepte exactement les mots que l'automate original rejette (nécessite un automate complet). |
| **Produit cartésien** | Construction d'un automate dont le langage est l'**intersection** des langages de deux automates. |
| **Nettoyage** | Suppression des états **inaccessibles** (non atteignables depuis l'initial) et **non co-accessibles** (ne pouvant atteindre aucun état final). |

---
## Lancement

```bash
cd h:\Documents\TD
python PROJETF.py
```

Le programme démarre une interface console interactive avec un système de menus.

---

## Structure du menu interactif

Le programme s'organise en **deux niveaux de menus** :

### Menu principal
```
============================================================
  INTERFACE CONSOLE - GESTION D'AUTOMATES FINIS
============================================================

1. Gérer les automates (créer, charger, lister)
2. Opérations sur les automates
0. Quitter
```

### Menu "Gestion des automates"
| Option | Action |
|--------|--------|
| 1 | Créer un nouvel automate via l'interface interactive |
| 2 | Charger des automates depuis un fichier |
| 3 | Lister les automates contenus dans un fichier |
| 4 | Lister les automates actuellement en mémoire |
| 5 | Sélectionner un automate en mémoire comme "automate courant" |
| 6 | Supprimer un automate de la mémoire |

### Menu "Opérations sur les automates"
| Option | Opération |
|--------|-----------|
| 1 | Afficher l'automate courant (transitions, états finaux, initial) |
| 2 | Analyser un mot (tester si un mot est accepté ou refusé) |
| 3 | Vérifier si l'automate est complet |
| 4 | Compléter l'automate (ajout d'un état poubelle) |
| 5 | Créer l'automate complémentaire |
| 6 | Vérifier si l'automate est déterministe |
| 7 | Déterminiser l'automate (NFA → DFA) |
| 8 | Supprimer les epsilon-transitions |
| 9 | Enregistrer l'automate courant dans un fichier |
| 10 | Enregistrer tous les automates dans un fichier |
| 11 | Concaténer deux automates |
| 12 | Produit de deux automates (intersection des langages) |
| 13 | Nettoyer l'automate (supprimer les états inutiles) |
| 14 | Changer l'automate courant |
| 15 | Modifier l'automate courant (transitions, initial, finaux) |

---

## Représentation des automates

Le projet utilise **deux formats internes** pour représenter un automate, selon le contexte :

### Format matrice (`list[list[int]]`) — pour les DFA

Chaque automate est un dictionnaire Python :

```python
automate = {
    "matrice": [
        [1, -1, 2],   # État 0 : symbole 0 → état 1, symbole 1 → aucun, symbole 2 → état 2
        [-1, 2, -1],   # État 1 : symbole 1 → état 2
        [3, -1, 0],    # État 2 : symbole 0 → état 3, symbole 2 → état 0
        [-1, 1, -1]    # État 3 : symbole 1 → état 1
    ],
    "finaux": [2],          # Liste des états finaux
    "initial": 0,           # État initial
    "alphabet": ["a", "b", "c"]  # (optionnel) Noms des symboles
}
```

- Chaque **ligne** correspond à un état (indice = numéro de l'état).
- Chaque **colonne** correspond à un symbole de l'alphabet (indice = numéro du symbole).
- La valeur `-1` indique l'**absence de transition**.

### Format dictionnaire (`dict`) — pour les NFA et NFA-epsilon

```python
automate = {
    "matrice": {
        (0, 0): [1, 2],     # État 0, symbole 0 → états 1 ET 2 (non-déterministe)
        (0, 1): [0],        # État 0, symbole 1 → état 0
        (1, "EPS"): [2],    # État 1, epsilon → état 2 (epsilon-transition)
        (2, 0): [2],        # État 2, symbole 0 → état 2
    },
    "finaux": [2],
    "initial": [0],
    "alphabet": ["a", "b"]
}
```

- Les **clés** sont des tuples `(état, symbole)` où le symbole est un entier ou la chaîne `"EPS"` pour epsilon.
- Les **valeurs** sont des listes d'états de destination (permet le non-déterminisme).

### Conversion entre formats

Deux fonctions utilitaires permettent de passer d'un format à l'autre :
- `matrice_vers_dict(automate)` : matrice → dictionnaire
- `dict_vers_matrice(automate)` : dictionnaire → matrice

---

## Fonctions principales et algorithmes

### Affichage

| Fonction | Description |
|----------|-------------|
| `afficheAutomate(matrice)` | Affiche les transitions d'un automate au format matrice : `q0 ---a0---> q1` |
| `afficher_transitions_dict(transitions)` | Affiche les transitions d'un automate au format dictionnaire : `q0 --a--> [q1, q2]` |
| `afficher_automate(automate, nom)` | Affichage complet et lisible d'un automate (transitions + finaux + initial + alphabet) |

### Test d'acceptation

| Fonction | Description |
|----------|-------------|
| `accepter(matrice, mot, finaux)` | Teste si un mot (liste d'indices de symboles) est accepté par un DFA. Parcourt le mot symbole par symbole en suivant les transitions. |
| `Analyse_mot(automate, mot)` | Version plus robuste qui gère à la fois les DFA et NFA. Maintient un ensemble d'états courants et explore toutes les branches possibles. |
| `analyser_mot_interactif(automate)` | Interface interactive pour saisir un mot et tester son acceptation. |

### Vérification et transformation

| Fonction | Algorithme | Description |
|----------|------------|-------------|
| `estComplet(automate)` | Parcours de la matrice | Retourne `True` si toutes les transitions sont définies (aucun `-1`). |
| `Complet(automate)` | Ajout d'état poubelle | Ajoute un état qui boucle sur lui-même et redirige toutes les transitions manquantes vers celui-ci. |
| `estDeterministe(automate)` | Inspection des transitions | Retourne `False` si une transition mène à plusieurs états ou s'il existe des epsilon-transitions. |
| `Complementaire(automate)` | Inversion des finaux | Complète d'abord l'automate, puis inverse les états finaux et non-finaux. |

### Déterminisation (NFA → DFA)

`determiniser(automate)` implémente l'**algorithme de construction par sous-ensembles** :

1. L'état initial du DFA est l'ensemble `{initial}` du NFA.
2. Pour chaque ensemble d'états et chaque symbole, on calcule l'union des destinations.
3. Les nouveaux ensembles d'états sont explorés récursivement jusqu'à stabilisation.
4. Un ensemble est final s'il contient au moins un état final du NFA.
5. Les états sont renommés en `q0, q1, q2...` pour la lisibilité.

### Élimination des epsilon-transitions

`eliminer_transitions_epsilon(automate)` utilise la **fermeture epsilon** :

1. Pour chaque état, calcule sa fermeture epsilon (tous les états atteignables par des chaînes de transitions epsilon).
2. Si la fermeture d'un état contient un état final, cet état devient lui aussi final.
3. Pour chaque état, duplique les transitions non-epsilon de tous les états dans sa fermeture.
4. Supprime toutes les transitions epsilon du dictionnaire.

### Concaténation

`concatenation(automate1, automate2)` construit l'automate du langage $L_1 \cdot L_2$ :

1. Les états du deuxième automate sont **décalés** (indices += nombre d'états du premier).
2. Des **epsilon-transitions** sont ajoutées depuis chaque état final du premier automate vers l'état initial du second.
3. Les états finaux du résultat sont ceux du second automate (décalés).
4. L'état initial est celui du premier automate.

### Produit cartésien (intersection)

`produit_automates(automate1, automate2)` construit un automate pour $L_1 \cap L_2$ :

1. Chaque état du produit est une **paire** `(q1, q2)` d'états des deux automates.
2. L'état initial est `(initial1, initial2)`.
3. Pour chaque symbole, la transition suit simultanément les deux automates.
4. Un état `(q1, q2)` est final si `q1` est final dans le premier **ET** `q2` est final dans le second.

### Nettoyage

`nettoyer(automate)` conserve uniquement les **états utiles** :

1. **Accessibles** : parcours en profondeur depuis l'état initial.
2. **Co-accessibles** : parcours inverse depuis les états finaux.
3. **Utiles** = accessibles ∩ co-accessibles.
4. La matrice est reconstruite avec une renumérotation des états conservés.

### Lecture et sauvegarde

| Fonction | Description |
|----------|-------------|
| `lire_automate(fichier)` | Lit un automate depuis un fichier texte (format simple, voir ci-dessous). |
| `sauvegarder_automate(automate, fichier)` | Écrit un automate dans un fichier texte. |
| `save_automates(fichier, automates_dict, fusionner)` | Sauvegarde un dictionnaire d'automates dans un fichier (format `nom\|matrice\|finaux\|initial\|alphabet;`). Peut fusionner avec un fichier existant. |
| `load_automates(fichier)` | Charge un dictionnaire d'automates depuis un fichier. Crée le fichier s'il n'existe pas. |

---

## Formats de fichier

### Format simple (pour `lire_automate` / `sauvegarder_automate`)

```
<nombre d'états>
<nombre de symboles>
<matrice de transitions : une ligne par état, valeurs séparées par des espaces, -1 = pas de transition>
<états finaux séparés par des espaces>
<état initial>
```

**Exemple** (3 états, 2 symboles) :

```
3
2
1 0
-1 2
2 -1
2
0
```

Cela décrit :
- État 0 : symbole 0 → état 1, symbole 1 → état 0
- État 1 : symbole 0 → aucun, symbole 1 → état 2
- État 2 : symbole 0 → état 2, symbole 1 → aucun
- État final : 2
- État initial : 0

### Format multi-automates (pour `save_automates` / `load_automates`)

```
nom|matrice|finaux|initial|alphabet;
```

Chaque automate est sérialisé sur une ligne, séparé par des `|`, terminé par `;`. Les champs matrice, finaux, initial et alphabet sont des représentations Python évaluables.

---

## Exemple d'utilisation pas à pas

### 1. Lancer le programme

```bash
python PROJETF.py
```

### 2. Créer un automate

```
Choisissez 1 → Gérer les automates
Choisissez 1 → Créer un nouvel automate

Nombre d'états : 3
Alphabet : a, b
  État 0, symbole 'a' → 1
  État 0, symbole 'b' → 0
  État 1, symbole 'a' → -1
  État 1, symbole 'b' → 2
  État 2, symbole 'a' → 2
  État 2, symbole 'b' → 2
État initial : 0
États finaux : 2
Nom : mon_automate
```

### 3. Tester un mot

```
Retour → Menu principal → 2 (Opérations)
Choisissez 2 → Analyser un mot
Alphabet : ['a', 'b']
Entrez le mot : a b

✓ Le mot est ACCEPTÉ par l'automate.
```

### 4. Sauvegarder

```
Choisissez 9 → Enregistrer dans un fichier
Nom du fichier : mes_automates.txt
✓ Automate 'mon_automate' sauvegardé dans 'mes_automates.txt'.
```

---

## Organisation du code

Le fichier `PROJETF.py` est structuré en sections logiques :

| Section | Contenu |
|---------|---------|
| **Données d'exemple** | Matrices et configurations d'automates pré-définies pour les tests |
| **Fonctions d'affichage** | `afficheAutomate`, `afficher_transitions_dict`, `afficher_automate` |
| **Fonctions d'analyse** | `accepter`, `Analyse_mot`, `analyser_mot_interactif` |
| **Fonctions de vérification** | `estComplet`, `estDeterministe` |
| **Fonctions de transformation** | `Complet`, `determiniser`, `eliminer_transitions_epsilon`, `Complementaire`, `nettoyer` |
| **Fonctions de combinaison** | `concatenation`, `produit_automates` |
| **Fonctions de conversion** | `matrice_vers_dict`, `dict_vers_matrice` |
| **Fonctions de fichier** | `lire_automate`, `sauvegarder_automate`, `save_automates`, `load_automates` |
| **Interface interactive** | `creer_automate_interactif`, `modifier_automate_interactif` |
| **Système de menus** | `menu_principal`, `menu_gestion_automates`, `menu_operations` |

---

## Ajouter une nouvelle opération

Pour étendre le projet avec une nouvelle fonctionnalité (par exemple la **minimisation**) :

1. **Implémenter la fonction** :
   ```python
   def minimiser(automate):
       # votre algorithme ici
       return automate_minimise
   ```

2. **Ajouter une option dans `menu_operations`** : ajouter un `elif choix == "16":` qui appelle votre nouvelle fonction.

3. **Mettre à jour l'affichage du menu** : ajouter `print("16. Minimiser l'automate")` dans le bloc d'affichage du menu.


