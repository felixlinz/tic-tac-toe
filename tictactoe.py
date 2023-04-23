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
    if terminal(board):
        return None
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
    return possible_moves


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
        return True
    elif winner(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == None:
        return 0
    rules = {"X":1, "O":-1}
    result = winner(board)
    return rules[result]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if len(actions(board)) == 9:
        return (1,1)
    candidate = Node(board)
    candidate.value = -100000
    TicTacTree(candidate)
    for node in candidate.children:
        if (value := node.quality()) > candidate.value:
            candidate = node
            candidate.value = value
    return candidate.move


class TicTacTree:
    def __init__(self, node):
        self.now = [node]
        self.qualitytree = []
        self.treebuilder()
    
    def treebuilder(self):
        while len(self.now) != 0:
            parent = self.now.pop(0)
            moves = actions(parent.board)
            if moves:
                for move in moves:
                    node = Node(result(parent.board, move), move)
                    self.now.append(node)
                    self.qualitytree.append(node)
                    parent.children.append(node)
                

class Node:
    def __init__(self, board, move = None):
        self.terminal = terminal(board)
        self.board = board
        self.move = move
        self.children = []
        self.allchildren = []
        self.grandchildren = []
        self.wins = []
        self.losses = []
        self.player = player(self.board)
        self.utility = utility(self.board)
        self.target = {X:1, O:-1}
        self.opponent = {X:O, O:X}
        self.value = -100000

    def addchild(self, node):
        self.children.append(node)

    def quality(self):
        self.these_grandchildren()
        intital_value = 0
        maxdepth = 0
        mindepth = 100
        for child, depth in self.losses:
            if depth > maxdepth:
                maxdepth = depth
            elif depth < mindepth:
                mindepth = depth
        for child, depth in self.wins:
            intital_value = intital_value + int(maxdepth/depth)
        for child, depth in self.losses:
            intital_value = intital_value - int(math.pow((maxdepth/depth), 2))
        print("wins", len(self.wins))
        print("losses", len(self.losses))
        print("value", intital_value, "depth", mindepth, maxdepth)
        return intital_value
    
    def these_grandchildren(self):
        self.allchildren.extend(self.children)
        depth = 0
        while len(self.allchildren) > 0:
            depth += 1
            for child in self.allchildren:
                if child.utility == self.target[self.player]:
                    self.allchildren.remove(child)
                    self.wins.append((child, depth))
                elif child.utility == self.target[self.opponent[self.player]]:
                    self.allchildren.remove(child)
                    self.losses.append((child, depth))
                elif child.terminal == True:
                    self.allchildren.remove(child)
                else:
                    self.allchildren.extend(child.chhildren)


                
            


