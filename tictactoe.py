"""
Tic Tac Toe Player
"""
"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    other = 0
    for line in board:
        for cell in line:
            if cell == X:
                x += 1
            elif cell == O:
                o += 1
            else:
                other += 1
    if other == 0:
        return "papaya"
    elif x > o:
        return O
    else:
        return X      


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i, line in enumerate(board):
        for e, cell in enumerate(line):
            if cell != X and cell != O:
                move = (i,e)
                possible_moves.add(move)
    if possible_moves:
        return possible_moves
    return None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try: 
        fuckaround = copy.deepcopy(board)
        x,y = action
        operator = player(board)
        fuckaround[x][y] = operator
        return fuckaround
    except TypeError:
        raise Exception("not a valid move")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        checker = row[0]
        if row[1] == checker and row[2] == checker:
            return checker
    for i in range(3):
        checker = board[0][i]
        if board[1][i] == checker and board[2][i] == checker:
            return checker
    checker = board[0][0]
    if board[1][1] == checker and board[2][2] == checker:
        return checker
    checker = board[0][2]
    if board[1][1]==checker and board[2][0] == checker:
        return checker
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(list(actions(board))) == 0:
        print("hi")
        return True
    elif winner(board):
        return True
        print("hi")
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not winner(board):
        return 0
    rules = {"X":1, "O":-1}
    result = winner(board)
    return rules[result]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    spieler = player(board)
    opponent = {"X":O,"O":X}
    if terminal(board):
        return None
    c_board = copy.deepcopy(board)
    tree = []
    superparent = {"Board":c_board,"Move":None,"Parent":None, "Utility":utility(c_board)}
    parent = copy.deepcopy(superparent)
    now = copy.deepcopy(c_board)
    while winner(now) != opponent[spieler]:        
        tree_level = []
        if actions(now):
            options = actions(now)
        else:
            break
        for option in list(options):
            resultat = result(now, option)
            node = {"Board":resultat,"Move":option,"Parent":parent, "Utility":utility(resultat)}
            tree_level.append(node)
        tree.extend(tree_level)
        parent = tree.pop(0)
        now = parent["Board"]
    if spieler == X:
        for node in reversed(tree):
            if node["Utility"] == 1:
                while node["Parent"] != superparent:
                    node = node["Parent"]
                return node["Move"]
        for node in reversed(tree):
            if node["Utility"] == 0:
                while node["Parent"] != superparent:
                    node = node["Parent"] 
                return node["Move"]    
    elif spieler == O:
        for node in reversed(tree):
            if node["Utility"] == -1: 
                while node["Parent"] != superparent:
                    node = node["Parent"]
                return node["Move"]
        for node in reversed(tree):
            if node["Utility"] == 0:
                while node["Parent"] != superparent:
                    node = node["Parent"] 
                return node["Move"]