# Ibrahim Abou Zaidi 000541770 B1-INFO


import sys
import random
import os


def init_board(file_path= None):
    if file_path is None:
        return initial_board(7)
    else:
        return init_board_file(file_path)


def initial_board(n):
    board = []
    for i in range(2):  # boucle repete 2 fois car toujours 2 ligne pour chaque joueur
        res = []
        for j in range(n):
            res.append(2)
        board.append(res)
    for k in range(3, n-1):  # boucle vide repete n-4 fois
        res = []
        for l in range(n):
            res.append(0)
        board.append(res)
    for m in range(n-1, n+1):
        res = []
        for o in range(n):
            res.append(1)
        board.append(res)
    return board

def pions(ligne):
    pions = []
    for i in range(len(ligne)):
        a = ''
        if ligne[i].isalpha():
            a += ligne[i] + ligne[i+1]
            pions.append(a)
    return pions


def init_board_file(file_path):
    with open(file_path) as fichier:
        ligne_1 = repr(fichier.readline().split())
        ligne_2 = repr(fichier.readline().strip().split(','))
        ligne_3 = repr(fichier.readline().strip().split(','))
        board = []
        dimension =[]
        for i in ligne_1:
            if i.isnumeric():
                dimension.append(int(i))
        ligne, colonne = dimension
        pions_blancs = pions(ligne_2)
        pions_noirs = pions(ligne_3)
        for i in range(ligne):
            res = []
            for j in range(colonne):
                res.append(0)
            board.append(res)
        for j in pions_blancs:
            blanc = extract_pos(colonne, ligne ,j)
            x = blanc[0]
            y = blanc[1] 
            board[x][y] = 1
        for j in pions_noirs:
            noir = extract_pos(colonne, ligne ,j)
            x = noir[0]
            y = noir[1] 
            board[x][y] = 2
    return board

def extract_pos(colonne, ligne, str_pos):
    def pos_line(str_pos):
        int_pos = 0
        for i in str_pos:
            if i.isnumeric():
                int_pos += int(i)
        return int_pos
    board = [[0 for i in range(colonne)] for j in range(ligne)]
    int_lettre = ord(str_pos[0]) - 97
    int_pos = pos_line(str_pos)
    for nombre in range(ligne):
        for lettre in range(colonne):
            if nombre == ligne - int_pos and lettre == int_lettre:
                return (nombre, lettre)
    return None


def ai_select_peg(board, player):
    ligne_plus_proche = None
    for i in range(len(board)):
        if 2 in board[i]:
            ligne_plus_proche = i
    b = []
    for j in range(len(board[i])):
        if board[ligne_plus_proche][j] == 2:
            b.append(j)
    a = random.choice(b)
    return (ligne_plus_proche,a)


def ai_move(board, pos, player):
    if pos[1] != 0 and pos[1] != len(board[0])-1:
        if board[pos[0]+1][pos[1]] == 0:
            a = random.randint(-1,1)
            return (pos[0]+1,pos[1]+a)
        elif board[pos[0]+1][pos[1]] == 1:
            c = [-1,1]
            a = random.choice(c)
            return (pos[0]+1,pos[1]+a)
    elif pos[1] == 0:
        if board[pos[0]+1][pos[1]] == 0:
            a = random.randint(0,1)
            return(pos[0]+1,pos[1]+a)
        elif board[pos[0]+1][pos[1]] == 1:
            return(pos[0]+1,pos[1]+1)
    elif pos[1] == len(board[0])-1:
        if board[pos[0]+1][pos[1]] == 0:
            a = random.randint(-1,0)
            return(pos[0]+1,pos[1]+a)
        elif board[pos[0]+1][pos[1]] == 1:
            return(pos[0]+1,pos[1]-1)

def check_move(board, player, source, destination):
    if source is None or destination is None or destination == source:
        return False
    rang1, col1 = source
    rang2, col2 = destination
    if not is_in_board(len(board), len(board[0]), source) or not is_in_board(len(board), len(board[0]), destination):
        return False
    if board[rang1][col1] != player:
        return False
    elif destination == (rang1 + vertical_direction(player), col1):
        return board[rang2][col2] == 0
    elif destination == (rang1 + vertical_direction(player), col1 + 1) or\
            destination == (rang1 + vertical_direction(player), col1 - 1):
        return board[rang2][col2] != player
    return False

def vertical_direction(player):
    return 2 * player - 3

def is_in_board(n, m, pos):
    pos_a = pos[0]
    pos_b = pos[1]
    if 0 <= pos_a < n and 0 <= pos_b < m:
        return True
    else:
        return False

        
def ai_move(board, pos, player):
    possible_move = []
    for i in range(pos[1]-1,pos[1]+2):
        destination = (pos[0]+1, i)
        if check_move(board, player,  pos, destination):
            possible_move.append(destination)
    return (pos,random.choice(possible_move))

player = 1
board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 2, 0, 2, 0],
             [2, 0, 2, 2, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 0, 0],
             [1, 0, 0, 0, 1, 0],
             [0, 1, 0, 0, 0, 0]]

def pion_move(board, pos, player):
    possible_move = []
    for i in range(pos[1]-1,pos[1]+2):
        destination = (pos[0]-1, i)
        if check_move(board, player,  pos, destination):
            possible_move.append(destination)
    return possible_move


def input_select_peg(board, player):
    pion_selectionable = []
    for i in range(len(board)):
        pion_selectionable_ligne =  []
        for j in range(len(board[i])):
            pos_pion = (i,j)
            if board[i][j] == player and len(pion_move(board, pos_pion, player)) > 0:
                pion_selectionable_ligne.append(pos_pion)
        if len(pion_selectionable_ligne) > 0:
            pion_selectionable.append(pion_selectionable_ligne)
    joueur_selection = input("")
    horizontal = 0
    vertical = 0
    pion_selectionne = pion_selectionable[vertical][horizontal]
    while joueur_selection != 'y':
        if joueur_selection == 'l':
            horizontal += 1
            if horizontal == len(pion_selectionable[vertical]):
                horizontal = 0
            pion_selectionne = pion_selectionable[vertical][horizontal]
        elif joueur_selection == 'j':
            horizontal -= 1
            if horizontal == -1:
                horizontal = len(pion_selectionable[vertical]) - 1
            pion_selectionne = pion_selectionable[vertical][horizontal]
        elif joueur_selection == 'k':
                vertical += 1
                if vertical == len(pion_selectionable):
                    vertical = 0
                x = 100
                for indice, o in enumerate(pion_selectionable[vertical]):
                    distance = (abs(pion_selectionne[0] - o[0]) + abs(pion_selectionne[1] - o[1]))
                    if  distance < x:
                        x = distance
                        pion_selectionne = o
                        horizontal = indice
        elif joueur_selection == 'i':       
                vertical -= 1
                if vertical == len(pion_selectionable):
                    vertical = 0
                x = 100
                for indice, o in enumerate(pion_selectionable[vertical]):
                    distance = (abs(pion_selectionne[0] - o[0]) + abs(pion_selectionne[1] - o[1]))
                    if  distance < x:
                        x = distance
                        pion_selectionne = o
                        horizontal = indice
        joueur_selection = input("")
    
    return pion_selectionne
def print_vertical_border(n):
    print('     '+'— '*n)


def letter_of_player(player):
    if player == 2:
        letter = 'B'
    elif player == 1:
        letter = 'W'
    else:
        letter = '.'
    return letter

def print_interieur_board(board):
    j = len(board)
    for ligne in board:
        print(str(j).rjust(2), '|', end=' ')
        j -= 1
        for k in ligne:
            print(letter_of_player(k), end=' ')
        print('|', end='\n')


def print_noms_colones(board):
    alpha = 97
    print('     ', end='')
    for b in range(len(board[0])):
        print(chr(alpha), end=' ')
        alpha += 1


    

def print_board(board):
    print_vertical_border(len(board[0]))

    print_interieur_board(board)

    print_vertical_border(len(board[0]))
    print_noms_colones(board)
    
