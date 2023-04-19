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
    if terminal(board):
        return False
    possible_moves = set()
    for i, line in enumerate(board):
        for e, cell in enumerate(line):
            if cell != X and cell != O:
                move = (i,e)
                possible_moves.add(move)
    if possible_moves:
        print(possible_moves)
        return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try: 
        fuckaround = copy.deepcopy(board)
        x,y = action
        operator = player(board)
        if not winner(board):
            fuckaround[x][y] = operator
        print(fuckaround)
        return fuckaround
    except TypeError:
        raise Exception("not a valid move")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        checker = [row[0]]
        for cell in row:
            if cell == checker[0]:
                checker.append(cell)
        if len(checker) == 4:
            return checker[0]
    for i in range(3):
        checker = [row[i]]
        for row in board:
            if row[i] == checker[0]:
                checker.append(row[i])
        if len(checker) == 4:
            return checker[0]
    checker = [board[0][0]]
    for i, row in enumerate(board[1:]):
        if row[i] == checker[0]:
            checker.append(row[i])
    if len(checker) == 3:
            return checker[0]
    position = 2
    checker = [board[0][position]]
    for row in board:
        position -= 1
        if row[position] == checker[0]:
            checker.append(row[position])
            checker.append(row[position])
    if len(checker) == 4:
        return checker[0]
    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    i = 0
    for row in board:
        for cell in row:
            if cell not in [X,O]:
                i += 1
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not winner(board):
        return 0
    rules = {"X":1, "O":-1}
    result = winner(board)
    print(rules[result])
    return rules[result]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    spieler = player(board)
    if terminal(board):
        return None
    c_board = board.copy()
    tree = []
    parent = {"Board":c_board,"Move":None,"Parent":None, "Utility":utility(c_board)}
    now = copy.deepcopy(c_board)
    while terminal(now) == False:
        if not terminal(now):         
            options = actions(now)
            tree_level = []
            for option in list(options):
                resultat = result(now, option)
                node = {"Board":result,"Move":option,"Parent":parent, "Utility":utility(resultat)}
                tree_level.append(node)
            now = resultat
            tree.append(tree_level)
    if spieler == X:
        for node in tree[-1]:
            if node["Utility"] == 1: 
                while node["Parent"] is not None:
                    node = node["Parent"]
                return node["Move"]
        for node in tree[-1]:
            if node["Utility"] == 0: 
                while node["Parent"] is not None:
                    node = node["Parent"]
                return node["Move"]
        
    elif spieler == O:
        for node in tree[-1]:
            if node["Utility"] == -1: 
                while node["Parent"] is not None:
                    node = node["Parent"]
                return node["Move"]
    for node in tree[-1]:
            if node["Utility"] == 0: 
                while node["Parent"] is not None:
                    node = node["Parent"]
                return node["Move"]