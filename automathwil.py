notDefined = -1
automate=[[3,1],
          [1,2],
          [-1, -1],
          [3,-1]]

m =[[0,1,-1],
     [2,-1,-1],
     [-1,-1,2]]

finaux= [2,3]


def afficheAutomate(matrice):
        nbEtats= len(matrice)
        nbSymbole= len(matrice[0])
        print("LES TRANSITIONS")
        for i in range(nbEtats):
            for j in range(nbSymbole):
                if matrice[i][j]!=-1:
                    print("q"+str(i)+"---a"+str(j)+"--->q"+str(matrice[i][j]))
                    
afficheAutomate(automate)
print("-------------------------")

def accepter(matrice, mot, finaux):
    etat= 0
    i=0
    while i<len(mot):
        symbole= mot[i]
        print("i="+str(symbole))
        etat= matrice[etat][symbole]
        if etat==-1:
            return False
        i+=1
    return etat in finaux

print(accepter(m,[0,0,1,0,2,2,2,2],finaux))
print("-------------------------")
    
def afficheAutomate1(matrice):
        nbEtat= len(matrice)
        nbSymbole= len(matrice[0])
        print("LES TRANSITIONS")
        for i in range(nbEtat):
            for j in range(nbSymbole):
                if matrice[i][j]!=-1:
                    print("q"+str(i)+"---a"+str(j)+"--->q"+str(matrice[i][j]))
                    
afficheAutomate1(automate)
print("-------------------------")
   
matrice1 = [[0,1,1],[2,1,1],[1,1,2]]
etats_finaux=[2]
automate={"matrice":matrice1,
          "finaux":[2]}
def estComplet(automate):
    matrice= automate["matrice"]
    nbEtat = len(matrice)
    nbSymbole = len(matrice[0])
    for i in range(nbEtat):
        for j in range(nbSymbole):
            if matrice[i][j] == -1:
                return False
    return True

##print(estComplet(automate))
##print("-------------------------")
    

def Complet(automate):
    if estComplet(automate):
        return automate
    nbEtat = len(matrice)
    nbSymbole = len(matrice[0])
    matrice.append([nbEtat, nbEtat, nbEtat])
    for i in range(nbEtat):
        for j in range(nbSymbole):
            if matrice[i][j] == -1:
                matrice[i][j]=nbEtat
    return automate

##print(Complet(automate))
##print("-------------------------")

def Complementaire(automate):
    if estComplet(automate)==True:
        Cautomate={}
        Cautomate["matrice"]=automate["matrice"]
        Cautomate["finaux"]=[]
        nbEtat=len(Cautomate["matrice"])
        for i in range(nbEtat):
            if i not in automate["finaux"]:
                Cautomate["finaux"].append(i)
        return Cautomate
    else:
        automate= Complet(automate)
        return Complementaire(automate)
    
##print(Complementaire(automate))
##print("-------------------------")
 
def determiniser(automate):
    matriceND = automate["matrice"]
    finauxND = automate.get("finaux", [])
    notDefined = -1

    nbSymbole = len(matriceND[0])

    # nouveaux états du DFA : chaque état = frozenset d'états NFA
    nouveauxEtats = [frozenset([0])]      # état initial {0}
    etat_index = {nouveauxEtats[0]: 0}

    matriceDet = []
    finauxDet = []

    i = 0
    while i < len(nouveauxEtats):
        ensemble = nouveauxEtats[i]
        ligne = []

        for s in range(nbSymbole):
            dest = set()
            for q in ensemble:
                cible = matriceND[q][s]
                if isinstance(cible, list):
                    for x in cible:
                        if x != notDefined:
                            dest.add(x)
                else:
                    if cible != notDefined:
                        dest.add(cible)

            if not dest:
                ligne.append(notDefined)
            else:
                dest_f = frozenset(dest)
                if dest_f not in etat_index:
                    etat_index[dest_f] = len(nouveauxEtats)
                    nouveauxEtats.append(dest_f)
                ligne.append(etat_index[dest_f])

        matriceDet.append(ligne)

        # si l'ensemble contient un état final du NFA, marquer final
        for q in ensemble:
            if q in finauxND:
                finauxDet.append(i)
                break

        i += 1

    return {"matrice": matriceDet, "finaux": finauxDet, "initial": [0]}

print("FIN")
print("-------------------------")


def supprimer_transitions_epsilon(automate, eps_index):
    """Supprime les epsilon-transitions d'un automate en une seule passe."""
    matrice = automate["matrice"]
    finaux = automate.get("finaux", [])
    nbEtat = len(matrice)
    nbSymbole = len(matrice[0])

    def _cibles(entree):
        """Retourne un set d'entiers cibles pour une cellule de la matrice."""
        if entree == notDefined:
            return set()
        if isinstance(entree, (list, set, tuple)):
            return set(x for x in entree if x != notDefined)
        return {entree}

    def _ecrire_entree(q, sym, ensemble_cibles):
        """Écrit `ensemble_cibles` dans matrice[q][sym] en forme compacte."""
        if not ensemble_cibles:
            matrice[q][sym] = notDefined
        elif len(ensemble_cibles) == 1:
            matrice[q][sym] = next(iter(ensemble_cibles))
        else:
            matrice[q][sym] = sorted(list(ensemble_cibles))

    def fermeture_epsilon(depart):
        fermeture = {depart}
        pile = [depart]
        while pile:
            s = pile.pop()
            for t in _cibles(matrice[s][eps_index]):
                if t not in fermeture:
                    fermeture.add(t)
                    pile.append(t)
        return fermeture

    for q in range(nbEtat):
        fermeture = fermeture_epsilon(q)

        # Si un état de la fermeture est final, q devient final
        for s in fermeture:
            if s in finaux and q not in finaux:
                finaux.append(q)

        # Recopier les transitions sortantes (sauf eps) depuis tous les états de la fermeture
        for s in fermeture:
            for sym in range(nbSymbole):
                if sym == eps_index:
                    continue
                cibles_s = _cibles(matrice[s][sym])
                if not cibles_s:
                    continue
                actuel = _cibles(matrice[q][sym])
                union = actuel.union(cibles_s)
                _ecrire_entree(q, sym, union)

        # Supprimer les transitions epsilon de q
        _ecrire_entree(q, eps_index, set()) 

    automate["finaux"] = finaux
    return automate


def contient_epsilon(automate, eps_index):#Elle sert donc de test de condition pour savoir si l’automate contient encore des transitions spontanées (ε).
    matrice = automate["matrice"]
    for row in matrice:
        if row[eps_index] != notDefined:
            return True
    return False


def supprimer_toutes_transitions_epsilon(automate, eps_index):
    """Répète la suppression des epsilon-transitions jusqu'à disparition totale."""
    iteration = 0
    while contient_epsilon(automate, eps_index):
        iteration += 1
        supprimer_transitions_epsilon(automate, eps_index)
        
    return automate


if __name__ == "__main__":
    # Démonstration : automate avec epsilon = indice de symbole 2
    demo = {
        "matrice": [
            [1, -1, 2],  # q0: a0->q1, a2(eps)->q2
            [-1, 2, -1], # q1: a1->q2
            [-1, -1, -1] # q2: pas de transitions sortantes
        ],
        "finaux": [2]
    }
    print("Avant suppression des epsilon-transitions :")
    print(demo)
    supprimer_toutes_transitions_epsilon(demo, 2)
    print("Après suppression des epsilon-transitions :")
    print(demo)


# Exemple : automate non-déterministe
automateND = {
    
    "matrice": [
        [[1,2], [0]],   
        [[2], [0,2]], 
        [[2], notDefined]  
    ],
    "finaux": [2]
}

print("DETERMINISATION de 'automateND' (non-déterministe):")
print(automateND)
print(determiniser(automateND))
print("-------------------------")


