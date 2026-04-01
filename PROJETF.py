
# Fonction principal

def afficheAutomate(matrice):
    """Affiche les transitions d'une matrice format """
    nbEtats = len(matrice)  # nombre d'états = nombre de lignes de la matrice
    nbSymbole = len(matrice[0])  # nombre de symboles = longueur d'une ligne (colonnes)
    print("LES TRANSITIONS")  # en-tête pour l'affichage des transitions
    for i in range(nbEtats):  # pour chaque état source i
        for j in range(nbSymbole):  # pour chaque symbole j
            if matrice[i][j] != -1:  # -1 signifie absence de transition
                # affiche la transition q<i> --a<j>--> q<destination>
                print("q" + str(i) + "---a" + str(j) + "--->q" + str(matrice[i][j]))

def accepter(matrice, mot, finaux):
    """Teste si un mot est accepté par une matrice """
    etat = 0
    i = 0
    while i < len(mot): ## parcours du mot
        symbole = mot[i] ## symbole courant
        print("i=" + str(symbole))## debug du symbole courant
        etat = matrice[etat][symbole] ## transition
        if etat == -1:
            return False
        i += 1
    return etat in finaux

def estComplet(automate):
    """Vérifie si un automate dict est complet"""
    matrice = automate["matrice"]  # récupère la matrice des transitions
    nbEtat = len(matrice)  # nombre d'états (lignes)
    nbSymbole = len(matrice[0])  # nombre de symboles (colonnes)
    for i in range(nbEtat):  # pour chaque état i
        for j in range(nbSymbole):  # pour chaque symbole j
            if matrice[i][j] == -1:  # si une transition manquante est trouvée
                return False  # l'automate n'est pas complet
    return True  # aucune transition manquante => complet

def Complet(automate):
    """Rend un automate complet en ajoutant un état poubelle"""
    if estComplet(automate):  # si déjà complet, ne rien faire
        return automate
    matrice = automate["matrice"]  # récupère la matrice existante
    nbEtat = len(matrice)  # nombre d'états avant d'ajouter l'état poubelle
    nbSymbole = len(matrice[0])  # nombre de symboles
    # Ajouter l'état poubelle: une nouvelle ligne pointant vers elle-même
    matrice.append([nbEtat] * nbSymbole)  # chaque symbole mène vers l'état poubelle (index = nbEtat)
    # Rediriger les transitions manquantes (-1) vers l'état poubelle
    for i in range(nbEtat):  # pour chaque ancien état
        for j in range(nbSymbole):  # pour chaque symbole
            if matrice[i][j] == -1:  # si transition manquante
                matrice[i][j] = nbEtat  # pointer vers l'état poubelle
    return automate  # retourne l'automate modifié

def determiniser(automate):
    """Déterminise un automate non-déterministe (format dict transitions)"""
    matriceND = automate["matrice"]
    finauxND = set(automate.get("finaux", []))
    initial_set = set(automate.get("initial", [0]))

    # Fonction pour transformer un ensemble en "{1,2}"
    def nommer(etat_set):
        if not etat_set:
            return "{}"
        lst = list(etat_set)
        lst.sort()  # trie pour garder un ordre constant
        s = "{"
        for i in range(len(lst)):
            s += str(lst[i])
            if i != len(lst)-1:
                s += ","
        s += "}"
        return s

    # Calcul du nombre de symboles
    nb_sym = 0
    for cle in matriceND:
        if cle[1] >= nb_sym:
            nb_sym = cle[1] + 1

    # Initialisation
    nouveaux = [initial_set]   # file à traiter
    deja_vus = [initial_set]   # pour ne pas traiter deux fois le même
    matriceDet = {}
    finauxDet = []
    initial_nom = nommer(initial_set)

    i = 0
    while i < len(nouveaux):
        ensemble = nouveaux[i]
        nom_source = nommer(ensemble)

        # Est-ce un état final ?
        for q in ensemble:
            if q in finauxND and nom_source not in finauxDet:
                finauxDet.append(nom_source)

        # Pour chaque symbole
        for s in range(nb_sym):
            dest = set()
            for q in ensemble:
                if (q, s) in matriceND:
                    for t in matriceND[(q, s)]:
                        dest.add(t)

            if dest:
                nom_dest = nommer(dest)
                matriceDet[(nom_source, s)] = [nom_dest]
                if dest not in deja_vus:
                    deja_vus.append(dest)
                    nouveaux.append(dest)
            else:
                matriceDet[(nom_source, s)] = []

        i += 1

    # Renommer les états en q0, q1, q2, ... pour meilleure lisibilité
    # L'état initial doit toujours être q0
    etats_renommes = sorted(matriceDet.keys(), key=lambda x: x[0])
    etats_uniques_set = set(e for (e, s) in etats_renommes) | set(finauxDet) | {initial_nom}
    etats_uniques_set.discard(initial_nom)
    etats_uniques = [initial_nom] + sorted(etats_uniques_set)
    mapping_etats = {ancien: f"q{idx}" for idx, ancien in enumerate(etats_uniques)}
    
    # Reconstruire avec les nouveaux noms
    matriceDet_renommee = {}
    for (etat, symbole), destinations in matriceDet.items():
        new_etat = mapping_etats[etat]
        new_dests = [mapping_etats[d] for d in destinations]
        matriceDet_renommee[(new_etat, symbole)] = new_dests
    
    finauxDet_renommes = [mapping_etats[f] for f in finauxDet]
    initial_nom_renomme = mapping_etats[initial_nom]

    return {
        "matrice": matriceDet_renommee,
        "finaux": finauxDet_renommes,
        "initial": [initial_nom_renomme]
    }
def afficher_transitions_dict(transitions):## affiche les transitions d'un dict de format (etat, symbole) -> [destinations]

    def format_state(state): ## formate un état pour l'affichage
        return f"q{state}" if isinstance(state, int) else str(state) ## si c'est un int, affiche qX, sinon affiche tel quel (pour les états nommés)
    def format_symbole(symbole): ## formate un symbole pour l'affichage
        if symbole == 0:
            return "a"
        if symbole == 1:
            return "b"
        return str(symbole)

    def cle_tri(cle):## clé de tri pour afficher d'abord par état, puis par symbole
        etat, symbole = cle
        if isinstance(symbole, int):
            return (etat, 0, symbole)
        return (etat, 1, str(symbole))

    for cle in sorted(transitions.keys(), key=cle_tri):# trier les clés pour un affichage ordonné
        etat, symbole = cle
        cibles = transitions[cle]
        if isinstance(cibles, (set, tuple)):
            cibles_iter = list(cibles)
        else:
            cibles_iter = cibles
        dest_formate = ", ".join(format_state(c) for c in cibles_iter)# formater les destinations pour l'affichage
        print(f"{format_state(etat)} --{format_symbole(symbole)}--> [{dest_formate}]")

def eliminer_transitions_epsilon(automate, epsilon_symbol="EPS"): 
    """Supprime les transitions epsilon en dupliquant les transitions sortantes"""
    transitions = automate.get("matrice", {})  # dict des transitions (clé=(etat,symbole))
    finaux = set(automate.get("finaux", []))  # ensemble des états finaux

    def ajouter_transition(source, symbole, arrivee):
        """Ajoute une transition source--symbole-->arrivee sans doublon"""
        arrivees = transitions.setdefault((source, symbole), [])  # cette partie est responsable de la création de la liste si absente
        if arrivee not in arrivees:  # évite les doublons
            arrivees.append(arrivee)

    etats = set(finaux)  # initialiser l'ensemble d'états avec les finaux
    for (etat, symbole), arrivees in transitions.items():  # découvrir tous les états du dict
        etats.add(etat)  # ajouter l'état source
        for arrivee in arrivees: 
            etats.add(arrivee)  # ajouter les états cibles

    epstransitions = {}  # liste d'états accessibles par EPS
    sorties = {}  #  list de (symbole, [arrivees]) pour symboles non-eps
    for (etat, symbole), arrivees in transitions.items():
        if symbole == epsilon_symbol:  # si la transition est une epsilon-transition
            epstransitions[etat] = list(arrivees)  # stocker les voisins epsilon
            continue
        # pour les autres symboles, stocker comme sorties de l'état
        sorties.setdefault(etat, []).append((symbole, list(arrivees)))

    def epsilon_closure(etat): 
        """Calcule la fermeture epsilon (ensemble d'états atteignables par EPS)"""
        fermeture = {etat}  # commence par l'état lui-même
        pile = [etat]  # pile 
        while pile:
            courant = pile.pop()
            for voisin in epstransitions.get(courant, []):  # voisins par EPS
                if voisin not in fermeture:
                    fermeture.add(voisin)  # ajouter nouvel état
                    pile.append(voisin)  # l'explorer aussi
        return fermeture

    fermetures = {etat: epsilon_closure(etat) for etat in etats}  # pré-calculer toutes les fermetures

    for etat, fermeture in fermetures.items():
        if fermeture.intersection(finaux):  # si la fermeture contient un final
            finaux.add(etat)  # alors l'état courant devient final
        for etat_ferme in fermeture:  # pour chaque état dans la fermeture
            for symbole, arrivees in sorties.get(etat_ferme, []):  # reproduire ses sorties non-eps
                for arrivee in arrivees:
                    for a in fermetures[arrivee]:  # inclure la fermeture de la cible
                        ajouter_transition(etat, symbole, a)  # ajouter transition équivalente

    cles_eps = [cle for cle in transitions if cle[1] == epsilon_symbol]  # trouver toutes les clés EPS
    for cle in cles_eps:
        transitions.pop(cle, None)  # supprimer les transitions epsilon originales

    automate["finaux"] = sorted(finaux)  # mettre à jour la liste triée des finaux
    return automate  # retourner l'automate modifié sans EPS


def concatenation(automate1, automate2):

    matrice1 = automate1["matrice"] 
    matrice2 = automate2["matrice"]
    finaux1 = set(automate1["finaux"])
    finaux2 = automate2["finaux"]
    initial1 = automate1["initial"][0] if isinstance(automate1["initial"], list) else automate1["initial"]
    initial2 = automate2["initial"][0] if isinstance(automate2["initial"], list) else automate2["initial"]
    
    # Nombre d'états dans a1
    n1 = len(matrice1)
    nbSymbole = len(matrice1[0])
    
    # Construire les transitions au format dict
    transitions = {}
    
    # Ajouter les transitions de a1
    for i in range(len(matrice1)):
        for j in range(nbSymbole):
            if matrice1[i][j] != -1:
                transitions[(i, j)] = [matrice1[i][j]]
    
    # Ajouter les transitions de a2 (avec décalage des indices de n1)
    for i in range(len(matrice2)):
        for j in range(nbSymbole):
            if matrice2[i][j] != -1:
                transitions[(i + n1, j)] = [matrice2[i][j] + n1]
    
    # Ajouter les transitions epsilon des états finaux de a1 vers l'état initial (décalé) de a2
    for etat_final in finaux1:
        transitions[(etat_final, "EPS")] = [initial2 + n1]
    
    # Mettre à jour les états finaux (renommer les indices de a2)
    nouveaux_finaux = [f + n1 for f in finaux2]
    
    return {
        "matrice": transitions,
        "finaux": nouveaux_finaux,
        "initial": [initial1]
    }

def nettoyer(automate): 
    """Supprime les états inutiles d'un automate
    
    Conserve seulement les états accessibles depuis l'état initial
    ET co-accessibles (pouvant atteindre un état final)
    """
    matrice = automate["matrice"]
    initial = automate["initial"]
    if isinstance(initial, list): # gérer le cas où initial est une liste
        initial = initial[0]
    finaux = set(automate["finaux"])

    # États accessibles depuis l'état initial
    accessibles = {initial}
    pile = [initial]

    while pile: 
        e = pile.pop()
        for j in range(len(matrice[e])):
            s = matrice[e][j]  # Correction: utiliser j au lieu de s
            if s != -1 and s not in accessibles:
                accessibles.add(s)
                pile.append(s)

    # États co-accessibles (pouvant atteindre un état final)
    co_accessibles = set(finaux)
    piles = list(finaux)

    while piles:
        t = piles.pop()
        for u in range(len(matrice)):
            if t in matrice[u] and u not in co_accessibles:
                co_accessibles.add(u)
                piles.append(u)

    # États utiles = intersection
    utiles = accessibles & co_accessibles
    utiles_tri = sorted(utiles)
    
    # Créer un mapping des anciens états vers les nouveaux indices
    mapping = {ancien: nouveau for nouveau, ancien in enumerate(utiles_tri)}
    
    # Reconstruire la matrice avec les états utiles
    nouvelle_matrice = []
    for ancien_idx in utiles_tri:
        nouvelle_ligne = []
        for j in range(len(matrice[ancien_idx])):
            ancien_etat_suiv = matrice[ancien_idx][j]
            if ancien_etat_suiv == -1 or ancien_etat_suiv not in mapping:
                nouvelle_ligne.append(-1)
            else:
                nouvelle_ligne.append(mapping[ancien_etat_suiv])
        nouvelle_matrice.append(nouvelle_ligne)
    
    # Mettre à jour les états finaux
    nouveaux_finaux = [mapping[f] for f in finaux if f in mapping]
    
    # Mettre à jour l'état initial
    nouvel_initial = mapping[initial]

    automate["matrice"] = nouvelle_matrice
    automate["finaux"] = nouveaux_finaux
    automate["initial"] = [nouvel_initial]

    return automate

def produit_automates(automate1, automate2):
   
    
    # Vérifier que les alphabets sont identiques
    if automate1["alphabet"] != automate2["alphabet"]:
        raise ValueError("Les alphabets des deux automates doivent être identiques")  # validation d'usage
    
    alphabet = automate1["alphabet"]  # alphabet commun

    # Convertir les matrices list[list] en dict si nécessaire
    def convertir_si_matrice(auto):
        mat = auto.get("transitions", auto.get("matrice", {}))
        if isinstance(mat, list):
            # Convertir list[list] en dict avec indices entiers comme symboles
            d = {}
            for i in range(len(mat)):
                for j in range(len(mat[i])):
                    if mat[i][j] != -1:
                        d[(i, j)] = [mat[i][j]]
            return d
        return mat

    trans1 = convertir_si_matrice(automate1)
    trans2 = convertir_si_matrice(automate2)

    finaux1 = set(automate1["finaux"])  # ensemble des états finaux du 1
    finaux2 = set(automate2["finaux"])  # ensemble des états finaux du 2
    
    # Déterminer l'état initial (peut être int ou list)
    init1 = automate1["initial"]
    if isinstance(init1, list):
        init1 = init1[0]
    init2 = automate2["initial"]
    if isinstance(init2, list):
        init2 = init2[0]

    # État initial du produit = paire (initial1, initial2)
    initial_produit = (init1, init2) 
    
    
    etats_produit = [initial_produit]  # file à traiter
    visites = {initial_produit}  # ensemble des états déjà vus
    transitions_produit = {}  # dictionnaire des transitions du produit
    
    i = 0
    while i < len(etats_produit):
        etat_courant = etats_produit[i]  # état courant de la forme (q1,q2)
        q1, q2 = etat_courant
        
        # Pour chaque symbole de l'alphabet
        for idx, symbole in enumerate(alphabet):
            # Utiliser l'index ou le symbole selon le format des clés
            cle_sym = idx if (q1, idx) in trans1 or (q2, idx) in trans2 else symbole
            
            # Appliquer la transition dans automate1 (format tuple-clé)
            if (q1, cle_sym) in trans1 and trans1[(q1, cle_sym)]:
                q1_suiv = trans1[(q1, cle_sym)][0]  # prendre la première cible
            else:
                q1_suiv = None  # pas de transition définie
            
            # Appliquer la transition dans automate2 (format tuple-clé)
            if (q2, cle_sym) in trans2 and trans2[(q2, cle_sym)]:
                q2_suiv = trans2[(q2, cle_sym)][0]
            else:
                q2_suiv = None
            
            # Si les deux transitions existent, créer l'état du produit
            if q1_suiv is not None and q2_suiv is not None:
                etat_suiv = (q1_suiv, q2_suiv)  # nouvel état produit
                transitions_produit[(etat_courant, symbole)] = [etat_suiv]  # enregistrer la transition
                
                # Ajouter le nouvel état s'il n'a pas été visité
                if etat_suiv not in visites:
                    visites.add(etat_suiv)
                    etats_produit.append(etat_suiv)  # l'enfiler pour exploration
        
        i += 1  # passer au prochain état produit
    
    # États finaux: intersection (un état est final si ses deux composantes sont finales)
    finaux_produit = []
    for etat in etats_produit:
        q1, q2 = etat
        if q1 in finaux1 and q2 in finaux2:  # condition d'être final dans le produit
            finaux_produit.append(etat)
    
    return {
        "alphabet": alphabet,  # alphabet du produit
        "initial": initial_produit,  # état initial du produit
        "finaux": finaux_produit,  # liste des états finaux du produit
        "transitions": transitions_produit  # dictionnaire des transitions du produit
    }

def lire_automate(nom_fichier):
    """Lit un automate depuis un fichier"""
    with open(nom_fichier, 'r') as f: ## ouvrez le fichier en lecture
        lines = f.readlines() ## lire toutes les lignes
    
    nbEtats = int(lines[0].strip()) ## nombre d'états
    nbSymboles = int(lines[1].strip()) ## nombre de symboles
    
    matrice = []
    for i in range(2, 2 + nbEtats): ## lire la matrice
        ligne = list(map(int, lines[i].strip().split())) ## convertir en liste d'entiers
        matrice.append(ligne) ## ajouter à la matrice
    
    finaux = list(map(int, lines[2 + nbEtats].strip().split())) ## lire les états finaux
    initial = int(lines[2 + nbEtats + 1].strip())   ## lire l'état initial
    
    return {
        "matrice": matrice,
        "finaux": finaux,
        "initial": initial
    }

def sauvegarder_automate(automate, nom_fichier):
    """Sauvegarde un automate dans un fichier"""
    matrice = automate["matrice"]
    finaux = automate["finaux"]
    initial = automate.get("initial", 0)
    
    with open(nom_fichier, 'w') as f:
        f.write(str(len(matrice)) + "\n")
        f.write(str(len(matrice[0])) + "\n")
        
        for ligne in matrice:
            f.write(" ".join(map(str, ligne)) + "\n")
        
        f.write(" ".join(map(str, finaux)) + "\n")
        f.write(str(initial) + "\n")

def save_automates(fichier, automates_dict, fusionner=False):
    """
    Enregistre un dictionnaire d'automates (nom -> automate) dans un fichier.
    Format du fichier : nom|matrice|finaux|initial|alphabet;
    Crée le fichier s'il n'existe pas.

    Args:
        fichier: Chemin du fichier
        automates_dict: Dictionnaire nom -> automate ou liste d'automates
        fusionner: Si True, fusionne avec les automates existants. Si False, remplace tout.
    """
    import os

    # Créer le répertoire si nécessaire
    dossier = os.path.dirname(fichier)
    if dossier and not os.path.exists(dossier):
        os.makedirs(dossier)

    # Si automates_dict est une liste, la convertir en dictionnaire avec des noms par défaut
    if isinstance(automates_dict, list):
        automates_dict = {f"automate_{i}": automate for i, automate in enumerate(automates_dict)}

    # Si fusionner, charger les automates existants
    automates_a_sauvegarder = {}
    if fusionner and os.path.exists(fichier):
        automates_a_sauvegarder = load_automates(fichier)

    # Ajouter ou remplacer les nouveaux automates
    automates_a_sauvegarder.update(automates_dict)

    # Écrire dans le fichier
    with open(fichier, "w", encoding="utf-8") as f:
        for nom, automate in automates_a_sauvegarder.items():
            mat = automate.get('matrice', automate.get('transitions', {}))
            ligne = f"{nom}|{mat}|{automate['finaux']}|{automate['initial']}|{automate.get('alphabet', [])};\n"
            f.write(ligne)

def load_automates(fichier):
    """
    Lit un fichier et renvoie un dictionnaire nom -> automate.
    Format attendu : nom|matrice|finaux|initial|alphabet;
    Crée le fichier vide s'il n'existe pas.
    """
    import os

    automates = {}

    # Si le fichier n'existe pas, le créer vide
    if not os.path.exists(fichier):
        with open(fichier, "w", encoding="utf-8") as f:
            pass
        return automates

    # Lire le fichier
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
        return automates

    # Parser le contenu
    for bloc in contenu.split(";"):
        if not bloc.strip():
            continue
        try:
            nom, matrice, finaux, initial, alphabet = bloc.strip().split("|")
            automate = {
                "matrice": eval(matrice),
                "finaux": eval(finaux),
                "initial": eval(initial),
                "alphabet": eval(alphabet)
            }
            automates[nom] = automate
        except ValueError as e:
            print(f"Erreur lors du parsing du bloc: {bloc}. Erreur: {e}")

    return automates

def matrice_vers_dict(automate):
    """Convertit un automate format matrice (list[list]) vers format dict {(état,symbole): [destinations]}"""
    matrice = automate["matrice"]
    finaux = automate.get("finaux", [])
    initial = automate.get("initial", 0)
    if isinstance(initial, list):
        initial = initial[0]
    transitions = {}
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            dest = matrice[i][j]
            if dest != -1:
                transitions[(i, j)] = [dest]
            else:
                transitions[(i, j)] = []
    return {
        "matrice": transitions,
        "finaux": finaux,
        "initial": [initial]
    }

def dict_vers_matrice(automate):
    """Convertit un automate format dict vers format matrice (list[list])"""
    transitions = automate["matrice"]
    finaux = automate.get("finaux", [])
    initial = automate.get("initial", [0])
    if isinstance(initial, list):
        initial = initial[0]
    # Trouver le nombre d'états et de symboles
    nb_etats = 0
    nb_symboles = 0
    for (etat, symbole), dests in transitions.items():
        if isinstance(etat, int):
            nb_etats = max(nb_etats, etat + 1)
        if isinstance(symbole, int):
            nb_symboles = max(nb_symboles, symbole + 1)
        for d in dests:
            if isinstance(d, int):
                nb_etats = max(nb_etats, d + 1)
    # Construire la matrice
    matrice = [[-1] * nb_symboles for _ in range(nb_etats)]
    for (etat, symbole), dests in transitions.items():
        if isinstance(etat, int) and isinstance(symbole, int) and dests:
            matrice[etat][symbole] = dests[0]
    return {
        "matrice": matrice,
        "finaux": finaux,
        "initial": initial
    }


def Complementaire(automate):  ## à partir d'un automate complet, créer son complémentaire
    """Crée l'automate complémentaire d'un automate complet."""
    automate_complet = Complet(automate) ## s'assurer que l'automate est complet
    Cautomate = {}
    Cautomate["matrice"] = [ligne[:] for ligne in automate_complet["matrice"]] ## copier la matrice
    Cautomate["finaux"] = [] ## les états finaux du complémentaire seront ceux qui ne sont pas finaux dans l'original
    nbEtats = len(Cautomate["matrice"])
    for i in range(nbEtats):## pour chaque état, s'il n'est pas dans les finaux de l'automate complet, alors il devient final dans le complémentaire
        if i not in automate_complet["finaux"]: ## si l'état i n'est pas final dans l'automate complet
            Cautomate["finaux"].append(i)
    if "initial" in automate_complet:
        Cautomate["initial"] = automate_complet["initial"]
    if "alphabet" in automate_complet:
        Cautomate["alphabet"] = automate_complet["alphabet"]
    return Cautomate


def analyser_mot_interactif(automate): ### analyse un mot avec l'automate, en demandant à l'utilisateur de saisir le mot à analyser, en gérant les cas où l'alphabet est défini ou non, et en affichant clairement le résultat de l'analyse.
    """Analyse un mot avec l'automate."""
    print("\n--- Analyse d'un mot ---")
    
    alphabet = automate.get("alphabet", [])
    matrice = automate["matrice"]
    
    if not alphabet:
        print("Aucun alphabet défini. Utilisez des indices numériques.")
        print(f"Nombre de symboles : {len(matrice[0]) if matrice else 0}")
        mot_input = input("Entrez les indices séparés par des virgules : ")
        try:
            mot = [int(x.strip()) for x in mot_input.split(",") if x.strip()]
        except ValueError:
            print("Erreur : entrée invalide.")
            return
    else:
        print(f"Alphabet : {alphabet}")
        mot_str = input("Entrez le mot (séparé par des espaces ou des virgules) : ")
        mot_list = [s.strip() for s in mot_str.replace(",", " ").split()]
        
        mot = []
        for symbole in mot_list:
            if symbole in alphabet:
                mot.append(alphabet.index(symbole))
            else:
                print(f"Symbole '{symbole}' non trouvé dans l'alphabet.")
                return
    
    resultat = Analyse_mot(automate, mot)
    if resultat:
        print(f"\n✓ Le mot est ACCEPTÉ par l'automate.")
    else:
        print(f"\n✗ Le mot est REFUSÉ par l'automate.")


def afficher_automate(automate, nom="Automate"):
    """Affiche un automate de manière lisible."""
    print(f"\n{'='*60}")
    print(f"{nom}")
    print(f"{'='*60}")
    matrice = automate["matrice"]
    print("Transitions:")
    if isinstance(matrice, dict):
        afficher_transitions_dict(matrice)
    else:
        for i, ligne in enumerate(matrice):
            print(f"  État {i}: {ligne}")
    print(f"États finaux : {automate.get('finaux', [])}")
    print(f"État initial : {automate.get('initial', 0)}")
    if "alphabet" in automate:
        print(f"Alphabet : {automate['alphabet']}")
    print(f"{'='*60}\n")


def creer_automate_interactif():
    """Crée un automate via l'interface console."""
    print("\n--- Création d'un automate ---")
    
    try:
        nb_etats = int(input("Nombre d'états : "))
        if nb_etats <= 0:
            print("Erreur : le nombre d'états doit être positif.")
            return None
    except ValueError:
        print("Erreur : veuillez entrer un nombre entier.")
        return None
    
    print("\nAlphabet (séparé par des virgules, ou laissez vide) :")
    alpha_input = input("> ").strip()
    if alpha_input:
        alphabet = [s.strip() for s in alpha_input.split(",")]
    else:
        nb_symboles = int(input("Nombre de symboles dans l'alphabet : "))
        alphabet = [f"sym{i}" for i in range(nb_symboles)]
    
    nb_symboles = len(alphabet)
    
    print("\nSaisie de la matrice de transition :")
    print("(Entrez -1 pour aucune transition, ou plusieurs états séparés par des virgules pour un ND)")
    matrice = []
    est_nd = False
    for i in range(nb_etats):
        ligne = []
        for j, sym in enumerate(alphabet):
            try:
                val = input(f"  État {i}, symbole '{sym}' -> État(s) : ").strip()
                if val == "" or val == "-1":
                    ligne.append(-1)
                else:
                    parts = [p.strip() for p in val.split(",")]
                    if len(parts) > 1:
                        ligne.append([int(p) for p in parts])
                        est_nd = True
                    else:
                        ligne.append(int(parts[0]))
            except ValueError:
                ligne.append(-1)
        matrice.append(ligne)
    
    try:
        initial = int(input(f"\nÉtat initial (0-{nb_etats-1}) [0] : ").strip() or "0")
    except ValueError:
        initial = 0
    
    print("\nÉtats finaux (séparés par des virgules) :")
    finaux_input = input("> ").strip()
    if finaux_input:
        finaux = [int(f.strip()) for f in finaux_input.split(",")]
    else:
        finaux = []
    
    # Demander les transitions epsilon
    print("\nAjouter des transitions epsilon ? (o/n) [n] :")
    eps_input = input("> ").strip().lower()
    transitions_eps = {}
    if eps_input == "o":
        print("Pour chaque état, entrez les destinations epsilon (virgules), ou vide :")
        for i in range(nb_etats):
            eps_dest = input(f"  État {i} --ε--> État(s) : ").strip()
            if eps_dest:
                dests = [int(d.strip()) for d in eps_dest.split(",") if d.strip()]
                if dests:
                    transitions_eps[i] = dests

    if transitions_eps or est_nd:
        # Format dict pour supporter epsilon et/ou non-déterminisme
        dict_transitions = {}
        for i in range(nb_etats):
            for j in range(nb_symboles):
                dest = matrice[i][j]
                if dest == -1:
                    dict_transitions[(i, j)] = []
                elif isinstance(dest, list):
                    dict_transitions[(i, j)] = dest
                else:
                    dict_transitions[(i, j)] = [dest]
            if i in transitions_eps:
                dict_transitions[(i, "EPS")] = transitions_eps[i]
        automate = {
            "matrice": dict_transitions,
            "finaux": finaux,
            "initial": [initial],
            "alphabet": alphabet
        }
    else:
        automate = {
            "matrice": matrice,
            "finaux": finaux,
            "initial": initial,
            "alphabet": alphabet
        }

    print("\n✓ Automate créé avec succès !")
    afficher_automate(automate, "Nouvel automate")
    return automate


def modifier_automate_interactif(automate):
    """Modifie un automate de manière interactive."""
    print("\n--- Modification d'un automate ---")
    afficher_automate(automate, "Automate actuel")
    
    auto_modifie = {
        "matrice": [ligne[:] for ligne in automate["matrice"]],
        "finaux": automate["finaux"][:],
        "initial": automate.get("initial", 0),
        "alphabet": automate.get("alphabet", [])[:]
    }
    
    while True:
        print("\n--- Que voulez-vous modifier ? ---")
        print("1. Modifier une transition")
        print("2. Modifier l'état initial")
        print("3. Modifier les états finaux")
        print("4. Voir l'automate modifié")
        print("0. Terminer et enregistrer")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "0":
            return auto_modifie
        
        elif choix == "1":
            try:
                nb_etats = len(auto_modifie["matrice"])
                nb_symboles = len(auto_modifie["matrice"][0]) if auto_modifie["matrice"] else 0
                etat = int(input(f"État source (0-{nb_etats-1}) : "))
                symbole = int(input(f"Indice du symbole (0-{nb_symboles-1}) : "))
                nouvelle_val = input("Nouvelle destination (-1 pour aucune) : ").strip()
                if nouvelle_val == "" or nouvelle_val == "-1":
                    auto_modifie["matrice"][etat][symbole] = -1
                else:
                    auto_modifie["matrice"][etat][symbole] = int(nouvelle_val)
                print("✓ Transition modifiée.")
            except (ValueError, IndexError) as e:
                print(f"✗ Erreur : {e}")
        
        elif choix == "2":
            try:
                nb_etats = len(auto_modifie["matrice"])
                nouveau = int(input(f"Nouvel état initial (0-{nb_etats-1}) : "))
                auto_modifie["initial"] = nouveau
                print("✓ État initial modifié.")
            except ValueError:
                print("✗ Erreur de saisie.")
        
        elif choix == "3":
            finaux_input = input("Nouveaux états finaux (séparés par des virgules) : ").strip()
            if finaux_input:
                auto_modifie["finaux"] = [int(f.strip()) for f in finaux_input.split(",")]
                print("✓ États finaux modifiés.")
        
        elif choix == "4":
            afficher_automate(auto_modifie, "Automate modifié")
    
    return auto_modifie


def Analyse_mot(automate, mot, verbose=False):
    """
    Analyse un mot avec un automate (déterministe ou non-déterministe).
    """
    matrice = automate["matrice"]
    finaux = set(automate["finaux"])
    initial = automate.get("initial", 0)
    if isinstance(initial, list):
        initial = initial[0]

    if verbose:
        print("Analyse du mot", mot)

    if not mot:
        return initial in finaux

    etats_courants = {initial}

    for symbole_idx in mot:
        nouveaux_etats = set()
        for etat in etats_courants:
            if isinstance(matrice, dict):
                # Format dict: (etat, symbole) -> [destinations]
                dests = matrice.get((etat, symbole_idx), [])
                if isinstance(dests, list):
                    nouveaux_etats.update(dests)
                else:
                    nouveaux_etats.add(dests)
            else:
                # Format matrice: list[list]
                if 0 <= etat < len(matrice) and 0 <= symbole_idx < len(matrice[etat]):
                    transition = matrice[etat][symbole_idx]
                    if isinstance(transition, list):
                        nouveaux_etats.update(transition)
                    elif transition != -1:
                        nouveaux_etats.add(transition)
        etats_courants = nouveaux_etats

        if verbose:
            print(f"États après le symbole {symbole_idx}: {etats_courants}")

    return bool(etats_courants & finaux)


def estDeterministe(automate):
    """Vérifie si un automate est déterministe."""
    matrice = automate["matrice"]
    if isinstance(matrice, dict):
        for (etat, symbole), destinations in matrice.items():
            if symbole == "EPS":
                return False
            if isinstance(destinations, list) and len(destinations) > 1:
                return False
        return True
    for ligne in matrice:
        if any(isinstance(transition, list) for transition in ligne):
            return False
    return True


# MENU SYSTEM


def menu_gestion_automates(automates, nom_courant):
    """Menu pour gérer les automates (créer, charger, lister)."""
    while True:
        print("\n" + "="*60)
        print("  GESTION DES AUTOMATES")
        print("="*60)
        print("\n1. Créer un nouvel automate")
        print("2. Charger un automate depuis un fichier")
        print("3. Lister les automates dans un fichier")
        print("4. Lister les automates en mémoire")
        print("5. Sélectionner un automate en mémoire")
        print("6. Supprimer un automate de la mémoire")
        print("0. Retour au menu principal")
        print("-"*60)
        
        if nom_courant:
            print(f"\n[Automate courant : {nom_courant}]")
        print(f"[Automates en mémoire : {len(automates)}]")
        
        choix = input("\nVotre choix : ").strip()
        
        try:
            if choix == "0":
                return automates, nom_courant
            
            elif choix == "1":
                auto = creer_automate_interactif()
                if auto:
                    nom = input("\nDonnez un nom à cet automate : ").strip()
                    if not nom:
                        nom = f"automate_{len(automates)}"
                    automates[nom] = auto
                    nom_courant = nom
                    print(f"✓ Automate '{nom}' enregistré et sélectionné.")
                    input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "2":
                fichier = input("Nom du fichier [automates.txt] : ").strip() or "automates.txt"
                try:
                    autos_charges = load_automates(fichier)
                    if not autos_charges:
                        print(f"\n✗ Aucun automate trouvé dans '{fichier}'.")
                        input("\nAppuyez sur Entrée pour continuer...")
                        continue
                    
                    print(f"\n✓ {len(autos_charges)} automate(s) trouvé(s) dans '{fichier}'.")
                    for nom_fichier, auto in autos_charges.items():
                        print(f"\n--- Automate '{nom_fichier}' ---")
                        finaux = auto.get("finaux", [])
                        initial = auto.get("initial", 0)
                        print(f"  États finaux : {finaux}")
                        print(f"  État initial : {initial}")
                        mat = auto['matrice']
                        if isinstance(mat, dict):
                            nb = len(set(e for (e, s) in mat.keys()))
                        else:
                            nb = len(mat)
                        print(f"  Nombre d'états : {nb}")
                        
                        reponse = input(f"\nCharger cet automate '{nom_fichier}' ? (o/n) [o] : ").strip().lower()
                        if reponse == 'n':
                            continue
                        
                        nom = input(f"Nom pour cet automate [{nom_fichier}] : ").strip() or nom_fichier
                        automates[nom] = auto
                        print(f"  → '{nom}' ajouté en mémoire.")
                        if not nom_courant:
                            nom_courant = nom
                    input("\nAppuyez sur Entrée pour continuer...")
                except Exception as e:
                    print(f"\n✗ Erreur lors du chargement : {e}")
                    input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "3":
                fichier = input("Nom du fichier [automates.txt] : ").strip() or "automates.txt"
                try:
                    autos_charges = load_automates(fichier)
                    if not autos_charges:
                        print(f"\n✗ Aucun automate trouvé dans '{fichier}'.")
                    else:
                        print(f"\n--- {len(autos_charges)} automate(s) dans '{fichier}' ---")
                        for nom, auto in autos_charges.items():
                            print(f"\n[Automate : {nom}]")
                            print(f"  États finaux : {auto.get('finaux', [])}")
                            print(f"  État initial : {auto.get('initial', 0)}")
                            mat = auto['matrice']
                            if isinstance(mat, dict):
                                nb = len(set(e for (e, s) in mat.keys()))
                            else:
                                nb = len(mat)
                            print(f"  Nombre d'états : {nb}")
                    input("\nAppuyez sur Entrée pour continuer...")
                except Exception as e:
                    print(f"\n✗ Erreur : {e}")
                    input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                if not automates:
                    print("\n✗ Aucun automate enregistré en mémoire.")
                else:
                    print(f"\n--- Automates en mémoire ({len(automates)}) ---")
                    for nom in automates:
                        marqueur = " ← COURANT" if nom == nom_courant else ""
                        auto = automates[nom]
                        print(f"  • {nom}{marqueur}")
                        mat = auto['matrice']
                        if isinstance(mat, dict):
                            nb = len(set(e for (e, s) in mat.keys()))
                        else:
                            nb = len(mat)
                        print(f"      États finaux : {auto.get('finaux', [])}, Nb états : {nb}")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "5":
                if not automates:
                    print("\n✗ Aucun automate disponible en mémoire.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                print("\nAutomates disponibles :")
                for nom in automates:
                    print(f"  • {nom}")
                
                nom = input(f"\nNom de l'automate à sélectionner [{nom_courant}] : ").strip() or nom_courant
                if nom and nom in automates:
                    nom_courant = nom
                    print(f"✓ Automate '{nom}' sélectionné.")
                    afficher_automate(automates[nom], nom)
                else:
                    # Recherche partielle
                    correspondances = [n for n in automates if nom.lower() in n.lower()]
                    if len(correspondances) == 1:
                        nom_courant = correspondances[0]
                        print(f"✓ Automate '{nom_courant}' sélectionné.")
                        afficher_automate(automates[nom_courant], nom_courant)
                    elif len(correspondances) > 1:
                        print(f"Plusieurs automates correspondent à '{nom}' :")
                        for idx, c in enumerate(correspondances):
                            print(f"  {idx + 1}. {c}")
                        choix_num = input("Entrez le numéro : ").strip()
                        try:
                            idx = int(choix_num) - 1
                            if 0 <= idx < len(correspondances):
                                nom_courant = correspondances[idx]
                                print(f"✓ Automate '{nom_courant}' sélectionné.")
                                afficher_automate(automates[nom_courant], nom_courant)
                            else:
                                print("Numéro invalide.")
                        except ValueError:
                            print("Entrée invalide.")
                    else:
                        print(f"✗ Automate '{nom}' introuvable.")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                if not automates:
                    print("\n✗ Aucun automate à supprimer.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                print("\nAutomates disponibles :")
                for nom in automates:
                    print(f"  • {nom}")
                
                nom = input("\nNom de l'automate à supprimer : ").strip()
                if nom not in automates:
                    correspondances = [n for n in automates if nom.lower() in n.lower()]
                    if len(correspondances) == 1:
                        nom = correspondances[0]
                    elif len(correspondances) > 1:
                        print(f"Plusieurs automates correspondent à '{nom}' :")
                        for idx, c in enumerate(correspondances):
                            print(f"  {idx + 1}. {c}")
                        choix_num = input("Entrez le numéro : ").strip()
                        try:
                            idx = int(choix_num) - 1
                            if 0 <= idx < len(correspondances):
                                nom = correspondances[idx]
                            else:
                                print("Numéro invalide.")
                                input("\nAppuyez sur Entrée pour continuer...")
                                continue
                        except ValueError:
                            print("Entrée invalide.")
                            input("\nAppuyez sur Entrée pour continuer...")
                            continue
                    else:
                        print(f"✗ Automate '{nom}' introuvable.")
                        input("\nAppuyez sur Entrée pour continuer...")
                        continue
                reponse = input(f"Êtes-vous sûr de vouloir supprimer '{nom}' ? (o/n) [n] : ").strip().lower()
                if reponse == 'o':
                    del automates[nom]
                    if nom == nom_courant:
                        nom_courant = None
                    print(f"✓ Automate '{nom}' supprimé.")
                else:
                    print("Suppression annulée.")
                input("\nAppuyez sur Entrée pour continuer...")
            
            else:
                print("\n✗ Choix invalide. Veuillez choisir entre 0 et 6.")
        
        except KeyboardInterrupt: # Permet de revenir au menu principal avec Ctrl+C
            print("\n\nRetour au menu...")
            return automates, nom_courant
        except Exception as e:
            print(f"\n✗ Erreur : {e}")
            input("\nAppuyez sur Entrée pour continuer...")


def menu_operations(automates, nom_courant):
    """Menu pour les opérations sur les automates."""
    if not automates:
        print("\n✗ Aucun automate disponible. Veuillez d'abord créer ou charger un automate.")
        input("\nAppuyez sur Entrée pour continuer...")
        return automates, nom_courant
    
    if not nom_courant:
        print("\n⚠ Aucun automate sélectionné. Sélection d'un automate...")
        nom = input("Nom de l'automate : ").strip()
        if nom not in automates:
            print(f"✗ Automate '{nom}' introuvable.")
            input("\nAppuyez sur Entrée pour continuer...")
            return automates, nom_courant
        nom_courant = nom
    
    while True:
        print("\n" + "="*60)
        print("  OPÉRATIONS SUR LES AUTOMATES")
        print("="*60)
        print(f"\n[Automate courant : {nom_courant}]")
        print("-"*60)
        print("\n1.  Afficher l'automate courant")
        print("2.  Analyser un mot avec l'automate courant")
        print("3.  Vérifier si l'automate est complet")
        print("4.  Compléter l'automate")
        print("5.  Créer l'automate complémentaire")
        print("6.  Vérifier si l'automate est déterministe")
        print("7.  Déterminiser l'automate")
        print("8.  Supprimer les epsilon-transitions")
        print("9.  Enregistrer l'automate courant dans un fichier")
        print("10. Enregistrer tous les automates dans un fichier")
        print("11. Concaténer deux automates")
        print("12. Produit de deux automates")
        print("13. Nettoyer l'automate (supprimer les états inutiles)")
        print("14. Changer l'automate courant")
        print("15. Modifier l'automate courant")
        print("0.  Retour au menu principal")
        print("-"*60)
        
        choix = input("\nVotre choix : ").strip()
        
        try:
            if choix == "0":
                return automates, nom_courant
            
            elif choix == "1":
                afficher_automate(automates[nom_courant], nom_courant)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "2":
                analyser_mot_interactif(automates[nom_courant])
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "3":
                auto = automates[nom_courant]
                if estComplet(auto):
                    print("\n✓ L'automate est COMPLET.")
                else:
                    print("\n✗ L'automate n'est PAS complet.")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                auto = automates[nom_courant]
                auto_complet = Complet(auto.copy())
                nom = input("\nNom pour l'automate complété [auto_complet] : ").strip() or "auto_complet"
                automates[nom] = auto_complet
                print(f"✓ Automate complété sauvegardé sous le nom '{nom}'.")
                afficher_automate(auto_complet, nom)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "5":
                auto = automates[nom_courant]
                auto_comp = Complementaire(auto.copy())
                nom = input("\nNom pour l'automate complémentaire [auto_complementaire] : ").strip() or "auto_complementaire"
                automates[nom] = auto_comp
                print(f"✓ Automate complémentaire sauvegardé sous le nom '{nom}'.")
                afficher_automate(auto_comp, nom)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                auto = automates[nom_courant]
                if estDeterministe(auto):
                    print("\n✓ L'automate est DÉTERMINISTE.")
                else:
                    print("\n✗ L'automate est NON-DÉTERMINISTE.")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "7":
                auto = automates[nom_courant]
                # Convertir en format dict si nécessaire
                if isinstance(auto.get("matrice"), list):
                    auto_dict = matrice_vers_dict(auto)
                else:
                    auto_dict = {"matrice": dict(auto["matrice"]), "finaux": list(auto["finaux"]), "initial": list(auto.get("initial", [0]))}
                auto_det = determiniser(auto_dict)
                nom = input("\nNom pour l'automate déterminisé [auto_determinise] : ").strip() or "auto_determinise"
                automates[nom] = auto_det
                print(f"✓ Automate déterminisé sauvegardé sous le nom '{nom}'.")
                afficher_transitions_dict(auto_det["matrice"])
                print(f"États finaux : {auto_det['finaux']}")
                print(f"État initial : {auto_det['initial']}")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "8":
                auto = automates[nom_courant]
                # Convertir en format dict si nécessaire
                if isinstance(auto.get("matrice"), list):
                    auto_dict = matrice_vers_dict(auto)
                else:
                    auto_dict = {
                        "matrice": {k: list(v) for k, v in auto["matrice"].items()},
                        "finaux": list(auto.get("finaux", [])),
                        "initial": list(auto.get("initial", [0]))
                    }
                auto_no_eps = eliminer_transitions_epsilon(auto_dict)
                nom = input("\nNom pour l'automate sans epsilon [auto_sans_epsilon] : ").strip() or "auto_sans_epsilon"
                automates[nom] = auto_no_eps
                print(f"✓ Automate sans epsilon sauvegardé sous le nom '{nom}'.")
                afficher_transitions_dict(auto_no_eps["matrice"])
                print(f"États finaux : {auto_no_eps['finaux']}")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "9":
                fichier = input("Nom du fichier [automates.txt] : ").strip() or "automates.txt"
                try:
                    import os
                    fusionner = False
                    if os.path.exists(fichier):
                        reponse = input(f"Le fichier '{fichier}' existe. Fusionner ? (o/n) [o] : ").strip().lower()
                        fusionner = (reponse != 'n')
                    
                    save_automates(fichier, {nom_courant: automates[nom_courant]}, fusionner=fusionner)
                    action = "fusionné à" if fusionner else "sauvegardé dans"
                    print(f"✓ Automate '{nom_courant}' {action} '{fichier}'.")
                except Exception as e:
                    print(f"\n✗ Erreur lors de la sauvegarde : {e}")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "10":
                if not automates:
                    print("\n✗ Aucun automate à sauvegarder.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                fichier = input("Nom du fichier [automates.txt] : ").strip() or "automates.txt"
                try:
                    import os
                    fusionner = False
                    if os.path.exists(fichier):
                        reponse = input(f"Le fichier '{fichier}' existe. Fusionner ? (o/n) [o] : ").strip().lower()
                        fusionner = (reponse != 'n')
                    
                    save_automates(fichier, automates, fusionner=fusionner)
                    action = "fusionnés à" if fusionner else "sauvegardés dans"
                    print(f"✓ {len(automates)} automate(s) {action} '{fichier}'.")
                except Exception as e:
                    print(f"\n✗ Erreur lors de la sauvegarde : {e}")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "11":
                if len(automates) < 2:
                    print("\n✗ Vous avez besoin d'au moins 2 automates pour la concaténation.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                print("\nAutomates disponibles :")
                for nom in automates:
                    print(f"  • {nom}")
                
                print("\nSélection du premier automate :")
                nom1 = input(f"Nom [{nom_courant}] : ").strip() or nom_courant
                if nom1 not in automates:
                    print(f"✗ Automate '{nom1}' introuvable.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                print("\nSélection du deuxième automate :")
                nom2 = input("Nom : ").strip()
                if nom2 not in automates:
                    print(f"✗ Automate '{nom2}' introuvable.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                try:
                    auto_concat = concatenation(automates[nom1].copy(), automates[nom2].copy())
                    # Supprimer les epsilon-transitions pour obtenir un automate utilisable
                    auto_concat = eliminer_transitions_epsilon(auto_concat)
                    nom = input("\nNom pour l'automate concaténé [auto_concatenation] : ").strip() or "auto_concatenation"
                    automates[nom] = auto_concat
                    print(f"✓ Automate concaténé sauvegardé sous le nom '{nom}'.")
                    afficher_transitions_dict(auto_concat['matrice'])
                    print(f"États finaux : {auto_concat['finaux']}")
                    print(f"État initial : {auto_concat['initial']}")
                except Exception as e:
                    print(f"\n✗ Erreur : {e}")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "12":
                if len(automates) < 2:
                    print("\n✗ Vous avez besoin d'au moins 2 automates pour le produit.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                print("\nAutomates disponibles :")
                for nom in automates:
                    print(f"  • {nom}")
                
                print("\nSélection du premier automate :")
                nom1 = input(f"Nom [{nom_courant}] : ").strip() or nom_courant
                if nom1 not in automates:
                    print(f"✗ Automate '{nom1}' introuvable.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                print("\nSélection du deuxième automate :")
                nom2 = input("Nom : ").strip()
                if nom2 not in automates:
                    print(f"✗ Automate '{nom2}' introuvable.")
                    input("\nAppuyez sur Entrée pour continuer...")
                    continue
                
                try:
                    auto_produit = produit_automates(automates[nom1].copy(), automates[nom2].copy())
                    nom = input("\nNom pour l'automate produit [auto_produit] : ").strip() or "auto_produit"
                    automates[nom] = auto_produit
                    print(f"✓ Automate produit sauvegardé sous le nom '{nom}'.")
                    print(f"État initial : {auto_produit['initial']}")
                    print(f"États finaux : {auto_produit['finaux']}")
                    afficher_transitions_dict(auto_produit["transitions"])
                except Exception as e:
                    print(f"\n✗ Erreur : {e}")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "13":
                auto = automates[nom_courant]
                auto_nettoye = nettoyer(auto.copy())
                nom = input("\nNom pour l'automate nettoyé [auto_nettoye] : ").strip() or "auto_nettoye"
                automates[nom] = auto_nettoye
                print(f"✓ Automate nettoyé sauvegardé sous le nom '{nom}'.")
                print(f"  États avant : {len(auto['matrice'])}, États après : {len(auto_nettoye['matrice'])}")
                afficher_automate(auto_nettoye, nom)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "14":
                print("\nAutomates disponibles :")
                for nom in automates:
                    print(f"  • {nom}")
                
                nom = input(f"\nNom de l'automate à sélectionner [{nom_courant}] : ").strip() or nom_courant
                if nom and nom in automates:
                    nom_courant = nom
                    print(f"✓ Automate '{nom}' sélectionné.")
                else:
                    print(f"✗ Automate '{nom}' introuvable.")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "15":
                auto = automates[nom_courant]
                auto_modifie = modifier_automate_interactif(auto.copy())
                if auto_modifie is not None:
                    print("\nQue voulez-vous faire avec l'automate modifié ?")
                    print("1. Remplacer l'automate courant")
                    print("2. Enregistrer sous un nouveau nom")
                    action = input("Choix [1] : ").strip() or "1"
                    
                    if action == "1":
                        automates[nom_courant] = auto_modifie
                        print(f"✓ Automate '{nom_courant}' modifié.")
                    else:
                        nouveau_nom = input("Nouveau nom : ").strip() or f"{nom_courant}_modifie"
                        automates[nouveau_nom] = auto_modifie
                        print(f"✓ Automate modifié sauvegardé sous le nom '{nouveau_nom}'.")
                input("\nAppuyez sur Entrée pour continuer...")
            
            else:
                print("\n✗ Choix invalide. Veuillez choisir entre 0 et 15.")
        
        except KeyboardInterrupt:
            print("\n\nRetour au menu...")
            return automates, nom_courant
        except Exception as e:
            print(f"\n✗ Erreur : {e}")
            input("\nAppuyez sur Entrée pour continuer...")


def menu_principal():
    """Interface console principale avec menu logique en deux étapes."""
    automates = {}
    nom_courant = None
    
    while True:
        print("\n" + "="*60)
        print("  INTERFACE CONSOLE - GESTION D'AUTOMATES FINIS")
        print("="*60)
        print("\n1. Gérer les automates (créer, charger, lister)")
        print("2. Opérations sur les automates")
        print("0. Quitter")
        print("-"*60)
        
        if nom_courant:
            print(f"\n[Automate courant : {nom_courant}]")
        print(f"[Automates en mémoire : {len(automates)}]")
        
        choix = input("\nVotre choix : ").strip()
        
        try:
            if choix == "0":
                print("\nAu revoir !")
                break
            
            elif choix == "1":
                result = menu_gestion_automates(automates, nom_courant)
                if result is not None:
                    automates, nom_courant = result
            
            elif choix == "2":
                result = menu_operations(automates, nom_courant)
                if result is not None:
                    automates, nom_courant = result
            
            else:
                print("\n✗ Choix invalide. Veuillez choisir entre 0 et 2.")
        
        except KeyboardInterrupt:
            print("\n\nAu revoir !")
            break
        except Exception as e:
            print(f"\n✗ Erreur : {e}")
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    menu_principal()

