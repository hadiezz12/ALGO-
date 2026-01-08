 README – Manipulation et traitement d’automates finis en Python
 Présentation générale

Ce fichier Python implémente plusieurs opérations fondamentales sur les automates finis, aussi bien déterministes (AFD) que non déterministes (AFN), avec ou sans transitions epsilon (ε).

Il permet notamment de :

représenter un automate sous forme matricielle

afficher ses transitions

tester l’acceptation d’un mot

vérifier et rendre un automate complet

calculer le complémentaire d’un automate

déterminiser un automate non déterministe

supprimer les transitions epsilon

enchaîner ces transformations de manière robuste

Le code est structuré de façon progressive, avec des exemples d’exécution intégrés pour illustrer chaque concept 

automathwil

.

 Représentation des automates
 États et symboles

Les états sont représentés par des entiers : 0, 1, 2, ...

L’état initial est toujours l’état 0

Les symboles de l’alphabet sont représentés par leurs indices : 0, 1, 2, ...

 Valeur spéciale -1
notDefined = -1


Cette constante représente :

l’absence de transition

une transition impossible

une case vide dans la matrice de transition

 Structure d’un automate

Un automate est représenté par :

 Une matrice de transition
automate = [
    [3, 1],
    [1, 2],
    [-1, -1],
    [3, -1]
]


Chaque ligne = un état

Chaque colonne = un symbole

matrice[i][j] = k signifie :
depuis l’état qi, avec le symbole aj, on va vers l’état qk

 Une liste d’états finaux
finaux = [2, 3]

🖨️ Affichage des transitions
Fonction : afficheAutomate
def afficheAutomate(matrice):

 Objectif

Afficher toutes les transitions définies de l’automate sous forme lisible.

 Fonctionnement

Parcourt chaque état qi

Parcourt chaque symbole aj

Ignore les transitions -1

Affiche :

qi ---aj---> qk

 Exemple de sortie
q0---a0--->q3
q0---a1--->q1


Cette fonction est purement informative, sans effet sur l’automate.

 Test d’acceptation d’un mot
Fonction : accepter
def accepter(matrice, mot, finaux):

 Objectif

Déterminer si un mot est accepté par l’automate.

📥 Entrées

matrice : matrice de transitions

mot : liste de symboles (ex : [0,1,0,2])

finaux : états finaux

Algorithme

Démarre à l’état initial 0

Pour chaque symbole du mot :

suit la transition correspondante

si -1 → rejet immédiat

À la fin :

accepte si l’état final appartient à finaux

 Exemple
print(accepter(m,[0,0,1,0,2,2,2,2],finaux))


Retourne True ou False.

 Vérification de complétude
Fonction : estComplet
def estComplet(automate):

 Objectif

Vérifier si l’automate est complet, c’est-à-dire :

chaque état possède une transition définie pour chaque symbole

 Principe

Si une seule case vaut -1, l’automate n’est pas complet

Sinon → complet

 Complétion d’un automate
Fonction : Complet
def Complet(automate):

 Objectif

Transformer un automate incomplet en automate complet

 Méthode

Ajout d’un état poubelle

Toutes les transitions manquantes pointent vers cet état

L’état poubelle boucle sur lui-même

 Cette fonction modifie l’automate en place

 Automate complémentaire
Fonction : Complementaire
def Complementaire(automate):

 Objectif

Construire l’automate du langage complémentaire

 Règle fondamentale

Les états finaux deviennent non finaux

Les états non finaux deviennent finaux

 Précondition

L’automate doit être complet
 sinon il est complété automatiquement avant transformation

 Déterminisation (AFN → AFD)
Fonction : determiniser
def determiniser(automate):

 Objectif

Transformer un automate non déterministe en automate déterministe

 Principe théorique

Chaque état du DFA est un ensemble d’états du NFA

Représenté par un frozenset

On applique la construction par sous-ensembles

 Fonctionnement détaillé

État initial : {0}

Pour chaque ensemble d’états :

pour chaque symbole :

union des transitions possibles

Création dynamique de nouveaux états

Un état est final si au moins un état final du NFA est inclus

 Sortie
{
  "matrice": [...],
  "finaux": [...],
  "initial": [0]
}

ε Suppression des transitions epsilon
Fonction principale
supprimer_toutes_transitions_epsilon(automate, eps_index)

 Objectif

Éliminer toutes les transitions ε d’un automate non déterministe.

 Concepts clés
🔹 ε-transition

Transition qui ne consomme aucun symbole.

🔹 Fermeture ε

Ensemble de tous les états atteignables sans lire de symbole.

 Algorithme
Pour chaque état q :

Calcul de la fermeture ε

Copie de toutes les transitions sortantes non-ε

Mise à jour des états finaux

Suppression définitive des transitions ε

La suppression est répétée jusqu’à disparition totale.

 Bloc de démonstration (__main__)

Le fichier contient plusieurs tests automatiques :

 Suppression des ε-transitions
demo = {...}
supprimer_toutes_transitions_epsilon(demo, 2)

✔️ Déterminisation d’un automate non déterministe
print(determiniser(automateND))
