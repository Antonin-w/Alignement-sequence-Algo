#!/usr/bin/python3
# -*- coding: utf-8 -*-

from FonctionsNW_WEBER_Antonin import *  # Import des fonctions dites "fonctionnelles" de l'algorithme
from Matrices_substitutions_de_base_WEBER_Antonin import *  # Import des matrices de substitutions de base
from argparse_WEBER_Antonin import *  # Import d'argparse permettant l'interaction directe avec le shell

args = parser.parse_args()

# Lit et copie les 2 séquences contenues dans les fichiers dans des variables (string)
Seq1 = lecture_sequence(args.s1)
Seq2 = lecture_sequence(args.s2)

print("Les paramètres que vous avez choisis sont :", "\n")
print("Sequence 1", "\t", Seq1)
print("Sequence 2", "\t", Seq2, "\n")

# Implémente dans des variables les paramètres de penalités de gaps indiquées par l'utilisateur, sinon les valeurs
# par défaut
gap_ouverture = args.ouverture
gap_extension = args.extension

print("Une ouverture de gap retire une penalite de", gap_ouverture)
print("Une extension de gap retire une penalite de", gap_extension, "\n")

# Rentre dans une variable le type d'alignement a effetuer (proteique / nucleique)
alignement_nucleique_ou_proteique = args.alignement
print("Alignement de sequences", alignement_nucleique_ou_proteique)

# Implémente la matrice de substitution de l'utilisateur, ou celles par défaut (en fonction du type d'alignement)
if args.matrice == "None":  # Si l'utilisateur ne rentre aucun matrice de substitution
    if alignement_nucleique_ou_proteique == 'nucleique':  # Dans le cas d'un alignement nucleique
        matrice_sub = matrice_substitution  # On utilisera la matrice de base avec les paramètres
        # Match = 2, missmatch purine/purine | pyrimidine/pyrimidine = 1
        # Autres missmatch = -1
    else:  # Dans le cas d'un alignement proteique
        matrice_sub = blosum62  # On utilisera la matrice Blosum62
else:  # Sinon, on utilise la matrice contenu dans le fichier indiqué
    exec(open(args.matrice).read())  # On importe les variables dans le fichier issus du chemin indiqué en option
    matrice_sub = matrice  # La matrice dans le fichier devra être nommée "matrice" !!

# Implemente une variable pour indiquer si c'est un alignement global ou local
if args.local:
    type_global_local = "local"
    print("Alignement local", "\n")
else:
    type_global_local = "global"
    print("Alignement global", "\n")


print("Matrice de substitution :", "\n")
print_dictionnaire(matrice_sub)  # Affiche la matrice de substitution


# Trouve, Affiche et retourne la matrice de score et la matrice de traceback
matricescore, matricefleche = scoring_system(Seq1, Seq2, matrice_sub, gap_ouverture, gap_extension,
                                             alignement_nucleique_ou_proteique, type_global_local)

# Affiche l'alignement et diverses informations supplémentaires
scores_totaux(matricefleche, matricescore, Seq1, Seq2, type_global_local)

# Fin main
# WEBER Antonin p2003706 [L3 BISM]










































































if args.surprise:
    import webbrowser
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
