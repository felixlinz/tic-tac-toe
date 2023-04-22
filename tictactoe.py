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
        return True
    elif winner(board):
        return True
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
    candidate = Node(board)
    candidate.value = -100000
    TicTacTree(candidate)
    for node in candidate.children:
        if node.quality() > candidate.value:
            candidate = node
            candidate.value = candidate.quality()
    return candidate.move



class TicTacTree:
    def __init__(self, node):
        self.now = [node]
        self.treebuilder()
    
    def treebuilder(self):
        while len(self.now) != 0:
            level = self.now.pop(0)
            moves = actions(level.board)
            tree = []
            if moves != None:
                for move in moves:
                    moved_board = result(level.board, move)
                    node = Node(moved_board, move)
                    self.now.append(node)
                    level.addchild(node)
        return tree


class Node:
    def __init__(self, board, move = None):
        self.board = board
        self.move = move
        self.children = []
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
        grandchildren = self.grandchildren()
        for child, depth in grandchildren:
            if child.utility == self.target[self.player]:
                self.wins.append((child ,depth))
            elif child.utility == self.target[self.opponent[self.player]]:
                self.losses.append((child, depth))
        intital_value = 0
        for child, depth in self.wins:
            intital_value = intital_value + (10-depth)
        for child, depth in self.losses:
            intital_value = intital_value - (depth)
        return intital_value
    
    def grandchildren(self):
        grandchildren = []
        children = self.children
        depth = 0
        nextround = []
        while len(children) != 0:
            depth += 1
            for child in children:
                if len(child.children) == 0:
                    grandchildren.append((child, depth))
                    children.remove(child)
                else:
                    nextround.extend(child.children)
                    children.remove(child)
            children = nextround
        print("Depth: ", depth)
        return grandchildren

                
            


