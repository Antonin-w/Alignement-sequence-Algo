#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import popen  # Import de popen pour déterminer la taille de la fenêtre du shell


# Permet d'afficher correctement les dictionnaires
def print_dictionnaire(dictionnaire):
    for key, value in dictionnaire.items():
        print('\t', str(key), '\t', str(value))
    print("\n")


# Permet d'afficher correctement les matrices
def print_matrice(mat):
    print("\n".join([" ".join([str(i).ljust(4) for i in row]) for row in mat]))
    print("\n")


# Permet de lire une sequence en fichier fasta et la retourner en une chaine de caractère
def lecture_sequence(nom_du_fichier):
    fichier = open(nom_du_fichier)
    Sequence = ""
    for line in fichier:
        if line[0] != ">":
            Sequence += line.strip('\n')
    return Sequence


# Permet de renvoyer une sequence en majuscule et en remplacant les U par des T
def seq_maj_u_en_t(sequence):
    sequence = sequence.upper()
    sequence = sequence.replace("U", "T")
    return sequence


# Creation de la matrice de substitution
def matrice_de_substitution(match=2, missmatch_AG_CT=1, autre_missmatch=-1):
    matrice = {
        'A': {'A': match, 'C': autre_missmatch, 'G': missmatch_AG_CT, 'T': autre_missmatch},
        'C': {'A': autre_missmatch, 'C': match, 'G': autre_missmatch, 'T': missmatch_AG_CT},
        'G': {'A': missmatch_AG_CT, 'C': autre_missmatch, 'G': match, 'T': autre_missmatch},
        'T': {'A': autre_missmatch, 'C': missmatch_AG_CT, 'G': autre_missmatch, 'T': match},
    }
    return matrice


# Permet de creer une matrice vide à partir de la tailles des 2 séquences
def matrice_initialisation(Seq1, Seq2, gap_ouverture, gap_extension, type_de_matrice="score", type_ali="global"):
    long_s1 = len(Seq1) + 2
    long_s2 = len(Seq2) + 2
    matrice_v = []
    for i in range(long_s1):
        l = []
        for j in range(long_s2):
            if type_de_matrice == "score":  # Si c'est une matrice de score
                l.append(0)  # On complète la matrice par des 0
            else:  # Sinon c'est une matrice de traceback
                l.append("")  # On complète la matrice par des ""
        matrice_v.append(l)
    matrice_v[1][1] = 0
    if type_ali == "global":
        if gap_ouverture == 0:
            m = 1
        else:
            m = 2
        for k in range(2, long_s1):
            matrice_v[k][0] = Seq1[k - 2]  # On place les nucléotides de la séquence 1
            matrice_v[k][1] = gap_extension * (k - m) + gap_ouverture  # On place les penalites de gap
        for l in range(2, long_s2):
            matrice_v[0][l] = Seq2[l - 2]  # On place les nucléotides de la séquence 2
            matrice_v[1][l] = gap_extension * (l - m) + gap_ouverture  # On place les penalites de gap
    else:
        for m in range(2, long_s1):
            matrice_v[m][0] = Seq1[m - 2]  # On place la "legende", donc les nucleotides / AA en ordonnée
            matrice_v[m][1] = 0  # Dans le cas d'un alignement local, on place des 0 sur la première colonne
        for l in range(2, long_s2):
            matrice_v[0][l] = Seq2[l - 2]  # On fait pareil pour les abscisses, nucléotides
            matrice_v[1][l] = 0            # On remplit aussi de 0
    return matrice_v


# Permet de retourner un score à partir de la matrice de substitution
# a : premier nucleoide
# b : deuxième nucleotide
# matrice_sub : matrice de substitution nous indiquant les scores entre chaques nucleotides
def scoring(a, b, matrice_sub):
    return matrice_sub[a][b]


# Remplit 2 matrices, une avec les scores, une autre pour le traceback
def scoring_system(Seq1, Seq2, matrice_sub, gap_ouverture=-10, gap_extension=-1, alignement="nucleique",
                   type_ali="global"):
    if alignement == "nucleique":  # Si ce n'est pas une sequence proteique, on peut convertir les U en T
        Seq1 = seq_maj_u_en_t(Seq1)  # Conversion des sequences en majuscules et en remplacent les U par des T
        Seq2 = seq_maj_u_en_t(Seq2)
    # Creation de la matrice contrnant les scores
    matrice_score = matrice_initialisation(Seq1, Seq2, gap_ouverture, gap_extension, "score", type_ali)
    # Création de la matrice contenant le traceback
    matrice_fleche = matrice_initialisation(Seq1, Seq2, gap_ouverture, gap_extension, "fleche", type_ali)
    for m in range(1, len(matrice_fleche[0])):  # Remplissage de la "legende" de la matrice traceback
        matrice_fleche[1][m] = "←"
    for p in range(1, len(matrice_fleche)):
        matrice_fleche[p][1] = "↑"
    matrice_fleche[1][1] = "✘"
    for i in range(2, len(matrice_score)):
        for j in range(2, len(matrice_score[0])):  # Pour chaque case de la matrice (hors nucléotides / extensions gap)
            # Calcul du score entre les deux nucléotides
            sco = scoring(matrice_score[i][0], matrice_score[0][j], matrice_sub)
            diag = matrice_score[i - 1][j - 1] + sco  # Calcul du score en fonction de la diagonale
            top = matrice_score[i - 1][j]  # Initialisation valeur top avec la valeur de la case du haut
            left = matrice_score[i][j - 1]  # Initialisation valeur left avec la valeur de la case de gauche
            # Conditions permettant de savoir si c'est une extension de gap ou non
            if "↑" in matrice_fleche[i - 1][j]:  # Si dans la case du haut, il y a déja un gap (symbole "↑")
                top += gap_extension  # Alors on ajoute seulement une penalite d'extension
            else:
                top += gap_ouverture  # Sinon, on ajoute une penalite d'ouverture de gap
            # Conditions permettant de savoir si c'est une extension de gap ou non
            if "←" in matrice_fleche[i][j - 1]:  # Meme demarche que pour le score top, mais avec le left
                left += gap_extension
            else:
                left += gap_ouverture
            # On remplit la case de la matrice score avec le score le plus haut
            if type_ali == "global":
                matrice_score[i][j] = max(diag, left, top)
            else:
                matrice_score[i][j] = max(diag, left, top, 0)
            if matrice_score[i][j] == diag:  # Remplissage de la matrice traceback
                matrice_fleche[i][j] += "↖"
            if matrice_score[i][j] == top:
                matrice_fleche[i][j] += "↑"
            if matrice_score[i][j] == left:
                matrice_fleche[i][j] += "←"
    print("Matrice de scores :", "\n")
    print_matrice(matrice_score)  # Affichage matrice de scores a titre indicatif
    print("Matrice de traceback :", "\n")
    print_matrice(matrice_fleche)  # Affichage matrice traceback a titre indicatif
    return matrice_score, matrice_fleche  # Renvoie des deux matrices


# Renvoie des informations sur l'un des meilleurs alignements
def scores_totaux(matrice_fleche, matrice_score, Seq1, Seq2, type_ali="global"):
    seq1_aligne = ""
    seq2_aligne = ""
    symbole = ""
    nombre_match = 0
    nombre_missmatch = 0
    nombre_gaps = 0
    if type_ali == "local":  # Dans le cas d'un alignement local
        x = 0
        for a in range(2, len(matrice_score)):
            for b in range(2, len(matrice_score[0])):
                if matrice_score[a][b] > x:
                    x = matrice_score[a][b]
                    i = a  # On conserve la position de la case ou la valeur est la plus élevée
                    j = b
        matrice = matrice_score  # On utilisera la matrice de score pour savoir ou s'arreter
        cond = 0  # Quand il y aura une case égale à 0
        score_total = matrice_score[i][j]  # Le score total correspond à la case de départ, avec la plus grande valeur
    else:
        i = len(Seq1) + 1  # Dans le cas d'un alignement global, le début sera les coordonnées de la dernière case
        j = len(Seq2) + 1
        cond = "✘"  # Notre signal d'arrêt sera au début de la matrice, la ou nous avons placé une croix
        matrice = matrice_fleche  # Dans ce cas, nous utilisons la matrice de fleche
        score_total = matrice_score[-1][-1]  # Le score de l'alignement correspondra à la dernière cellule de la matrice
    while matrice[i][j] != cond:
        if "↖" in matrice_fleche[i][j]:  # Si il y a presence d'une fleche diagonale,
            seq1_aligne += Seq1[i - 2]  # alors on copie simplement le nuceotide dans la séquence,
            seq2_aligne += Seq2[j - 2]  # on fait cela pour les deux séquences
            if seq1_aligne[-1] == seq2_aligne[-1]:  # Si les nucléotides sont identiques
                nombre_match += 1  # c'est un match
                symbole += "|"
            else:  # sinon c'est un missmatch
                nombre_missmatch += 1
                symbole += "."
            i -= 1
            j -= 1
        elif "↑" in matrice_fleche[i][j]:  # Dans le cas d'une fleche verticale, il y a presence d'un gap
            seq1_aligne += Seq1[i - 2]  # sur la sequence 2
            seq2_aligne += "-"  # On ajoute donc le nucleotide de la sequence 1 à la sequence
            nombre_gaps += 1  # Mais on ajoute un gap '-' à la séquence 2
            symbole += " "
            i -= 1  # On n'itère pas j à cause du gap
        elif "←" in matrice_fleche[i][j]:  # Même démarche que pour la fleche vers le haut
            seq1_aligne += "-"  # Sauf que dans ce cas, c'est la séquence 1 qui à la présence
            seq2_aligne += Seq2[j - 2]  # d'un gap, on n'itère donc pas i cette fois-ci
            nombre_gaps += 1
            symbole += " "
            j -= 1

    print("Alignement :", "\n")
    seq1_aligne = seq1_aligne[::-1]  # Nous avons suivi la matrice d'en bas à droite pour aller jusqu'a
    seq2_aligne = seq2_aligne[::-1]  # en haut à gauche, par conséquent, les séquences ont été recopiées
    symbole = symbole[::-1]  # à l'envers, on reverse simplement les deux chaines de caractères
    columns = int(popen('stty size', 'r').read().split()[1]) - 1
    a = len(seq1_aligne)
    i = 0
    while a > columns:
        print()
        print(seq1_aligne[i:columns + i])
        print(symbole[i:i + columns])
        print(seq2_aligne[i:i + columns])
        i += columns
        a -= columns
    print()
    print(seq1_aligne[i:])
    print(symbole[i:])
    print(seq2_aligne[i:])
    print("\n", "Legende :", "\n", "| match ", "\n",  # Affichage de l'alignement et des diverses
          ". missmatch", "\n", "- gap", "\n")  # informations obtenus via la fonction
    print("Le nombre de match est de :", nombre_match)
    print("Le nombre de missmatch est de :", nombre_missmatch)
    print("Le nombre de gaps est de :", nombre_gaps)
    print("Le score total cet alignement est de :", score_total)
    # Le score total est censé être identique au score de la dernière case de la matrice de score