#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser()

# Permet à l'utilisateur d'intéragir directement avec le shell pour choisir les paramètres de l'analyse

# Arguments obligatoires : Sequence 1 et 2
parser.add_argument("s1", help="Sequence 1 au format fasta")
parser.add_argument("s2", help="Sequence 2 au format fasta")

# Arguments optionnels
parser.add_argument("-o", "--ouverture", default=-10, type=int,                 # Penalite ouverture de gap
                    help="Penalite d'ouverture de gap, par défaut de -10")
parser.add_argument("-e", "--extension", default=-1, type=int,                  # Penalite d'extension de gap
                    help="Penalite d'extension de gap, par défaut de -1")
parser.add_argument("-a", "--alignement", default="nucleique", choices=["nucleique", "proteique"],  # Type d'alignement
                    help="Type d'alignement : nucleique ou proteique")                        # nucleique / proteique
parser.add_argument("-m", "--matrice", default="None",                          # Matrice de substitution
                    help="Chemin vers un fichier contenant une matrice de substitution personalisé")
parser.add_argument("-l", "--local", action="store_true",                       # Alignement global ou local
                    help="Type d'alignement local")
parser.add_argument("-s", "--surprise", action="store_true",
                    help="Petite surprise")
parser.parse_args()

# WEBER Antonin p2003706 [L3 BISM]
