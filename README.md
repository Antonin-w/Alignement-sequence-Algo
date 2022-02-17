                  Algorithme d'alignement de séquences - Needleman-Wunsch (1970)


Ce programme permet d'effectuer un alignement global de deux chaînes de caractères, pouvant être des séquences
de protéines ou de nucléotides.
Il fonctionne sur l'algorithme de Needleman-Wunsch expliqué içi :
    https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm

Dans ce README, CHEMIN est à remplacer par le chemin menant au fichier.

# I - Exécuter le programme et afficher l'aide

Afin d'utiliser ce programme, il faut exécuter le main.py
Pour cela, dans le terminal, entrez :
```bash
./CHEMIN/main.py
````
Si vous obtenez le message d'erreur suivant : -bash: ./main.py: Permission denied
C'est que vous n'avez pas autoriser l'exécution du fichier, pour cela, entrez la commande suivante :
     chmod +x CHEMIN/main.py

Pour obtenir de l'aide via le shell, exécuter le fichier en ajoutant l'option -h ou --help :
```bash
./CHEMIN/main.py --help
```
                usage: main.py [-h] [-o OUVERTURE] [-e EXTENSION] [-a {nucleique,proteique}]
                               [-m MATRICE] [-s]
                               s1 s2

                positional arguments:
                  s1                    Sequence 1 au format fasta
                  s2                    Sequence 2 au format fasta

                optional arguments:
                  -h, --help            show this help message and exit
                  -o OUVERTURE, --ouverture OUVERTURE
                                        Penalite d'ouverture de gap, par défaut de -10
                  -e EXTENSION, --extension EXTENSION
                                        Penalite d'extension de gap, par défaut de -1
                  -a {nucleique,proteique}, --alignement {nucleique,proteique}
                                        Type d'alignement : nucleique ou proteique
                  -m MATRICE, --matrice MATRICE
                                        Chemin vers un fichier contenant une matrice de
                                        substitution personalisé
                  -l, --local           Type d'alignement local
                  -s, --surprise        Petite surprise

L'aide permet d'indiquer les arguments obligatoires, optionnels, ainsi qu'une description de leur utilités.



# II- Utiliser le programme avec uniquement les paramètres obligatoires

Ce programme dispose de 2 arguments obligatoires : les 2 fichiers contenant chacun une séquence. Ils doivent être
au format FASTA.

Exemple d'un fichier format fasta :
     >Sequence1
     ATCuctacTACGTA

Exemple de commande pour exécuter le programme avec uniquement les 2 arguments obligatoires :
```bash
./CHEMIN/main.py CHEMIN/sequence1.fasta CHEMIN/sequence2.fasta
````


# III- Utiliser le programme avec des paramètres optionnels

    Pour simplifier l'écriture
    s1 = CHEMIN/sequence1.fasta
    s2 = CHEMIN/sequence2.fasta

    -h ou --help : Comme indiqué precedemment, permet d'afficher la page d'aide
        ./CHEMIN/main.py s1 s2 -h
    
    -o ou --ouverture : Permet de changer la penalite d'ouverture de gap (valeur par défaut = -10)
        ./CHEMIN/main.py s1 s2 -o -11   # Indique une penalite d'ouverture de gap de -11
    
    -e ou --extension : Permet de changer la penalite d'extension de gap (valeur par défaut = -1)
        ./CHEMIN/main.py s1 s2 -e -2    # Indique une penalite d'extension de gap de -2
    
    -a ou --alignement : Permet de renseigner le type de séquence à aligner
                         Il y a uniquement deux choix à entrer : nucleique ou proteique
                         Par défaut, le type de séquences à aligner est nucleique
        ./CHEMIN/main.py s1 s2 -a proteique     # Indique qu'il s'agit d'un alignement proteique, pas besoin de renseigner
                                                # dans le cas d'un alignement nucleique
    
    -m ou --matrice  : Permet de renseigner un le chemin d'un fichier contenant une matrice de substitution personalisée
                       La variable dans le fichier contenant la matrice de substitution doit impérativement
                       s'appeler "matrice". Elle doit être de la forme dictionnaire dans dictionnaire. Le fichier doit
                       être au format python.

    ./CHEMIN/main.py s1 s2 -m CHEMIN/FICHIER    # Remplacer FICHIER par le nom du fichier contenant la matrice

                   Par défaut, la matrice pour l'alignement des séquences nucléotidique est la suivante :
                   	 A 	 {'A': 2, 'C': -1, 'G': 1, 'T': -1}
                   	 C 	 {'A': -1, 'C': 2, 'G': -1, 'T': 1}
                   	 G 	 {'A': 1, 'C': -1, 'G': 2, 'T': -1}
                   	 T 	 {'A': -1, 'C': 1, 'G': -1, 'T': 2}

	               Par défaut, la matrice pour l'alignement des séquences protéique est BLOSUM62.
	               C'est l'une des plus adaptées pour detecter les plus faibles similaritées protéiques.
	               ftp://ftp.ncbi.nih.gov/blast/matrices/BLOSUM62

                   Exemple de matrice personalisée pour des séquences nucleiques :
                            matrice = {
                                'A': {'A': 1, 'C': -1, 'G': -1, 'T': -1},
                                'C': {'A': -1, 'C': 1, 'G': -1, 'T': -1},
                                'G': {'A': -1, 'C': -1, 'G': 1, 'T': -1},
                                'T': {'A': -1, 'C': -1, 'G': -1, 'T': 1},
                            }

                   Exemple de matrice personalisée pour des sequences proteiques :
                           matrice = {"A":  {"A": 1, "R": 1, "N": 1, "D": 1, "C": 1, "Q": 1, "E": -1, "G": 0, "H": -2, "I": -1, "L": -1, "K": -1, "M": -1, "F": -2, "P": -1, "S": 1, "T": 0, "W": -3, "Y": -2, "V": 0},
                    "R":  {"A": -1, "R": 5, "N": 0, "D": -2, "C": -3, "Q": 1, "E": 0, "G": -2, "H": 0, "I": -3, "L": -2, "K": 2, "M": -1, "F": -3, "P": -2, "S": -1, "T": -1, "W": -3, "Y": -2, "V": -3},
                    "N":  {"A": -2, "R": 0, "N": 6, "D": 1, "C": -3, "Q": 0, "E": 0, "G": 0, "H": 1, "I": -3, "L": -3, "K": 0, "M": -2, "F": -3, "P": -2, "S": 1, "T": 0, "W": -4, "Y": -2, "V": -3},
                    "D":  {"A": -2, "R": -2, "N": 1, "D": 6, "C": -3, "Q": 0, "E": 2, "G": -1, "H": -1, "I": -3, "L": -4, "K": -1, "M": -3, "F": -3, "P": -1, "S": 0, "T": -1, "W": -4, "Y": -3, "V": -3},
                    "C":  {"A": 0, "R": -3, "N": -3, "D": -3, "C": 9, "Q": -3, "E": -4, "G": -3, "H": -3, "I": -1, "L": -1, "K": -3, "M": -1, "F": -2, "P": -3, "S": -1, "T": -1, "W": -2, "Y": -2, "V": -1},
                    "Q":  {"A": -1, "R": 1, "N": 0, "D": 0, "C": -3, "Q": 5, "E": 2, "G": -2, "H": 0, "I": -3, "L": -2, "K": 1, "M": 0, "F": -3, "P": -1, "S": 0, "T": -1, "W": -2, "Y": -1, "V": -2},
                    "E":  {"A": -1, "R": 0, "N": 0, "D": 2, "C": -4, "Q": 2, "E": 5, "G": -2, "H": 0, "I": -3, "L": -3, "K": 1, "M": -2, "F": -3, "P": -1, "S": 0, "T": -1, "W": -3, "Y": -2, "V": -2},
                    "G":  {"A": 5, "R": -2, "N": 0, "D": -1, "C": -3, "Q": -4, "E": -2, "G": 6, "H": -2, "I": -4, "L": -4, "K": -2, "M": -3, "F": -3, "P": -2, "S": 0, "T": -2, "W": -2, "Y": -3, "V": -3},
                    "H":  {"A": 1, "R": 0, "N": 1, "D": -1, "C": -3, "Q": 0, "E": 0, "G": -2, "H": 8, "I": -3, "L": -3, "K": -1, "M": -2, "F": -1, "P": -2, "S": -1, "T": -2, "W": -2, "Y": 2, "V": -3},
                    "I":  {"A": -1, "R": -3, "N": -3, "D": -3, "C": -1, "Q": -3, "E": -3, "G": -4, "H": -3, "I": 4, "L": 2, "K": -3, "M": 1, "F": 0, "P": -3, "S": -2, "T": -1, "W": -3, "Y": -1, "V": 3},
                    "L":  {"A": -1, "R": -2, "N": -3, "D": -4, "C": -1, "Q": -2, "E": -3, "G": -4, "H": -3, "I": 2, "L": 4, "K": -2, "M": 2, "F": 0, "P": -3, "S": -2, "T": -1, "W": -2, "Y": -1, "V": 1},
                    "K":  {"A": -1, "R": 2, "N": 0, "D": -1, "C": -3, "Q": 1, "E": 1, "G": -2, "H": -1, "I": -3, "L": -2, "K": 5, "M": -1, "F": -3, "P": -1, "S": 0, "T": -1, "W": -3, "Y": -2, "V": -2},
                    "M":  {"A": -1, "R": -1, "N": -2, "D": -3, "C": 2, "Q": 0, "E": -2, "G": -3, "H": -2, "I": 1, "L": 2, "K": -1, "M": 5, "F": 0, "P": -2, "S": -1, "T": -1, "W": -1, "Y": -1, "V": 1},
                    "F":  {"A": -2, "R": -3, "N": -3, "D": -3, "C": -2, "Q": -3, "E": -3, "G": -3, "H": -1, "I": 0, "L": 0, "K": -3, "M": 0, "F": 6, "P": -4, "S": -2, "T": -2, "W": 1, "Y": 3, "V": -1},
                    "P":  {"A": -1, "R": -2, "N": -2, "D": -1, "C": -3, "Q": -1, "E": -1, "G": -2, "H": -2, "I": -3, "L": -3, "K": -1, "M": -2, "F": -4, "P": 7, "S": -1, "T": -1, "W": -4, "Y": -3, "V": -2},
                    "S":  {"A": -1, "R": -1, "N": 1, "D": 0, "C": -1, "Q": 0, "E": 0, "G": 0, "H": -1, "I": -2, "L": -2, "K": 0, "M": -1, "F": -2, "P": -1, "S": 4, "T": 1, "W": -3, "Y": -2, "V": -2},
                    "T":  {"A": 0, "R": -1, "N": 0, "D": -1, "C": -1, "Q": -1, "E": -1, "G": -2, "H": -2, "I": -1, "L": -1, "K": -1, "M": -1, "F": -2, "P": -1, "S": 1, "T": 5, "W": -2, "Y": -2, "V": 0},
                    "W":  {"A": -3, "R": -3, "N": -4, "D": -4, "C": -2, "Q": -2, "E": -3, "G": -2, "H": 9, "I": -3, "L": -2, "K": -3, "M": -1, "F": 1, "P": -4, "S": -3, "T": -2, "W": 11, "Y": 2, "V": -3},
                    "Y":  {"A": -2, "R": -2, "N": -2, "D": -3, "C": -2, "Q": -1, "E": -2, "G": -3, "H": 2, "I": -1, "L": -1, "K": -2, "M": -1, "F": 3, "P": -3, "S": -2, "T": -2, "W": 2, "Y": 7, "V": -1},
                    "V":  {"A": 0, "R": -1, "N": -3, "D": -3, "C": -1, "Q": 1, "E": -2, "G": -3, "H": -3, "I": 3, "L": 1, "K": -2, "M": 1, "F": -1, "P": -2, "S": -2, "T": 0, "W": -3, "Y": -1, "V": 4}}


    -l ou --local : En ajoutant ce paramètre, on peut obtenir un alignement local. Sans ce paramètre, par défaut ce sera
                    un alignement global.
        ./CHEMIN/main.py s1 s2 -l
    
    -s ou --suprise : Permet d'avoir une surprise, elle fonctionne comme le "--help", il suffit simplement de renseigner
                      "-s" ou "--surprise".
        ./CHEMIN/main.py s1 s2 -s


## Exemples concrets :

Si vous souhaitez faire un alignement global avec un penalite d'ouverture de gap de -5, d'extension de -2, de sequences
protéiques avec la matrice de substitution Blosum62 :
```bash
./CHEMIN/main.py s1 s2 -o -5 -e -2 -a proteique
```
Si vous souhaitez faire un alignement global avec un penalite d'ouverture de gap de -8, d'extension de -1, de sequences
nucleiques avec une matrice de substitution personalisée et une surprise à la fin :
```bash
./CHEMIN/main.py s1 s2 -o -8 -m CHEMIN/FICHIER -s
```

Si vous souhaitez faire un alignement locale avec en penalite de gap de -1, d'extension de -1, de séquence nucléotidiques
avec la matrice de substitution de base :
```bash
./CHEMIN/main.py s1 s2 -o -1 -l
```

# IV - Interpretation des résultats

```bash
./main.py sequence1.fasta sequence2.fasta
```

Les premières lignes récapitulent les paramètres utilisés pour faire l'alignement :

Les paramètres que vous avez choisis sont :
Sequence 1       ATCuUCACTUCATtACTg                     # La première séquence
Sequence 2       tcgATCAGuuCAACTAC                      # La deuxième séquence

Une ouverture de gap retire une penalite de -10   # La penalite d'ouverture de gap
Une extension de gap retire une penalite de -1    # La penalite d'extension de gap

Alignement de sequences nucleique                 # Le type de sequences a aligner (acides nucleiques ou proteiques)
Alignement global                                 # Le type d'alignement : global ou local

La matrice de substitution utilisée

                   Matrice de substitution :
                   A   {'A': 2, 'C': -1, 'G': 1, 'T': -1}
                   C 	 {'A': -1, 'C': 2, 'G': -1, 'T': 1}
                   G 	 {'A': 1, 'C': -1, 'G': 2, 'T': -1}
                   T 	 {'A': -1, 'C': 1, 'G': -1, 'T': 2}

La matrice de score à partir des paramètres précedents, attention, pour les séquences nucléotidiques, toute la séquence en légende à été mise en majuscule, et les U transformés en T.

                   Matrice de scores :   

    0    0    T    C    G    A    T    C    A    G    T    T    C    A    A    C    T    A    C
    0    0    -10  -11  -12  -13  -14  -15  -16  -17  -18  -19  -20  -21  -22  -23  -24  -25  -26
    A    -10  -1   -2   -3   -4   -5   -6   -7   -8   -9   -10  -11  -12  -13  -14  -15  -16  -17
    T    -11  -2   0    -1   -2   -2   -3   -4   -5   -6   -7   -8   -9   -10  -11  -12  -13  -14
    C    -12  -3   0    -1   -2   -1   0    -1   -2   -3   -4   -5   -6   -7   -8   -9   -10  -11
    T    -13  -4   -1   -1   -2   0    0    -1   -2   0    -1   -2   -3   -4   -5   -6   -7   -8
    T    -14  -5   -2   -2   -2   0    1    0    -1   0    2    1    0    -1   -2   -3   -4   -5
    C    -15  -6   -3   -3   -3   -1   2    1    0    0    1    4    3    2    1    0    -1   -2
    A    -16  -7   -4   -2   -1   -4   -2   4    3    -1   -1   0    6    5    4    3    2    1
    C    -17  -8   -5   -3   -2   0    -2   -3   3    4    0    1    -1   5    7    6    5    4
    T    -18  -9   -6   -4   -3   0    1    -3   -4   5    6    1    0    -2   6    9    8    7
    T    -19  -10  -7   -5   -4   -1   1    0    -4   -2   7    7    0    -1   -1   8    8    9
    C    -20  -11  -8   -6   -5   -2   1    0    -1   -3   -1   9    6    -1   1    0    7    10
    A    -21  -12  -9   -7   -4   -6   -3   3    1    -2   -4   -1   11   8    -2   0    2    6
    T    -22  -13  -10  -8   -5   -2   -5   -4   2    3    0    -3   1    10   9    0    -1   3
    T    -23  -14  -11  -9   -6   -3   -1   -6   -5   4    5    1    -4   0    11   11   1    0
    A    -24  -15  -12  -10  -7   -4   -2   1    -5   -6   4    4    3    -2   1    10   13   3
    C    -25  -16  -13  -11  -8   -5   -2   -3   0    -4   -5   6    3    2    0    2    9    15
    T    -26  -17  -14  -12  -9   -6   -3   -3   -4   2    -2   -4   5    2    3    2    1    10
    G    -27  -18  -15  -12  -11  -10  -7   -2   -1   -5   1    -3   -3   6    1    2    3    0


La matrice de traceback à partir des paramètres précedents, même indications que pour la matrice de score du dessus pour les matrices nucléotidiques.

                   Matrice de traceback : 
          T    C    G    A    T    C    A    G    T    T    C    A    A    C    T    A    C
     ✘    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←
    A    ↑    ↖    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←    ←
    T    ↑    ↑    ↖    ←    ←    ↖    ←    ←    ←    ↖←   ↖←   ←    ←    ←    ←    ↖←   ←    ←
    C    ↑    ↑    ↖    ↖←   ↖←   ↖    ↖    ←    ←    ←    ←    ↖←   ←    ←    ↖←   ←    ←    ↖←
    T    ↑    ↑    ↑    ↖    ↖←   ↖    ↖    ↖←   ↖←   ↖    ↖←   ←    ←    ←    ←    ↖←   ←    ←
    T    ↑    ↑    ↑    ↖↑   ↖    ↖    ↖    ←    ←    ↖    ↖    ←    ←    ←    ←    ↖←   ←    ←
    C    ↑    ↑    ↖↑   ↖↑   ↖↑   ↖↑   ↖    ←    ←    ↖    ↖    ↖    ←    ←    ↖←   ←    ←    ↖←
    A    ↑    ↑    ↑    ↖    ↖    ↖    ↖    ↖    ←    ↖    ↖    ↖    ↖    ↖←   ←    ←    ↖←   ←
    C    ↑    ↑    ↖↑   ↑    ↑    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ←    ←    ↖←
    T    ↑    ↑    ↑    ↑    ↑    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ←    ←
    T    ↑    ↑    ↑    ↑    ↑    ↖↑   ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖
    C    ↑    ↑    ↖↑   ↑    ↑    ↑    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖
    A    ↑    ↑    ↑    ↖↑   ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↑    ↖    ↖    ↖←   ↖    ↖    ↖
    T    ↑    ↑    ↑    ↑    ↑    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↑    ↖    ↖←   ↖    ↖    ↖
    T    ↑    ↑    ↑    ↑    ↑    ↖↑   ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖↑   ↖    ↖    ←    ↖
    A    ↑    ↑    ↑    ↖↑   ↖↑   ↑    ↑    ↖    ↖    ↖↑   ↑    ↖    ↖    ↖    ↑    ↖↑   ↖    ←
    C    ↑    ↑    ↖↑   ↑    ↑    ↑    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖
    T    ↑    ↑    ↑    ↑    ↑    ↖↑   ↑    ↖    ↖    ↖    ↖    ↖↑   ↖    ↖    ↖    ↖    ↖    ↖
    G    ↑    ↑    ↑    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖    ↖↑


Alignement : Schéma représentant l'alignement

        ATCuUCACTUCATtACTg
        .....||...||.. ...
        tcgATCAGuuCAAC-TAC

 Legende :
 
       | match
       . missmatch
       - gap

Indications sur le nombre de match/missmatch/gaps ainsi que le score total de l'alignement


Le nombre de match est de : 4


Le nombre de missmatch est de : 13


Le nombre de gaps est de : 1


Le score total cet alignement est de : 0

# V - Explication des principales fonctions utilisées (plus de details dans les commentaires du code)

print_dictionnaire(dictionnaire) : Permet d'afficher des dictionnaires.


print_matrice(mat) : Permet d'afficher des matrices.


lecture_sequence(nom_du_fichier) : Permet de lire une séquence dans un fichier fasta pour la retourner en format str.


scoring(a, b, matrice_sub) : Calcul le score entre 2 nucléotides (ou acides aminés) à l'aide d'une matrice de substitution.


scoring_system(Seq1, Seq2, matrice_sub, gap_ouverture=-10, gap_extension=-1, alignement="nucleique") : Affiche et
renvoie une matrice de score, et une matrice de traceback.


sscores_totaux(matrice_fleche, Seq1, Seq2, matrice_sub, gap_ouverture, gap_extension, alignement="nucleique") : Affiche
une représentation visuelle de l'alignement, accompagnée de diverses informations (nombre de match/missmatch/gaps, score
total de l'alignement)



Ce programme à été réalisé dans le cadre d'un travail de bioinformatique à l'Université Claude-Bernard Lyon1.
WEBER Antonin Etudiant L3 Bioinformatique, Statistique et Modélisation, Université Claude-Bernard, Lyon1.






















