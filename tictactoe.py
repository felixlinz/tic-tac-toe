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
    empty = 0
    for line in board:
        for cell in line:
            if cell not in [X,O]:
                empty += 1
    if (empty % 2) == 0:
        return O
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
    if len(possible_moves) != 0:
        return possible_moves
    return None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try: 
        resultboard = copy.deepcopy(board)
        y,x = action
        operator = player(board)
        resultboard[y][x] = operator
        return resultboard
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
    if not actions(board):
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
    elif len(actions(board)) == 1:
        return (actions(board)).pop()
    dad = Node(board)
    candidates = [dad.children[0]]
    for child in dad.children:
        child.these_grandchildren()
        if child.quality() > candidates[-1].quality():
            candidates.append(child)
    return candidates[-1].move

    
def treebuilder(node):
    now = [node]
    while len(now) > 0:
        parent = now.pop(0)
        moves = actions(parent.board)
        if not terminal(parent.board):
            for move in moves:
                moved_board = result(parent.board, move)
                node = Node(moved_board, move)
                now.append(node)
                parent.addchild(node)


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
        if move == None:
            treebuilder(self)

    def addchild(self, node):
        self.children.append(node)

    def depth(self):
        self._depth = 0
        for row in self.board:
            for cell in row: 
                if cell == EMPTY:
                    self._depth += 1
        return 9 - self._depth

    def quality(self):  
        value = 0
        if self.utility == self.target[self.player]:
            value += 100000
        for solution, depth in self.wins:
            value = value + int(10/depth)*int(10/depth)
            if depth == 2: 
                value += 100
        for solution, depth in self.losses:
            value = value - int(10/depth)*int(10/depth)
            if depth == 1: 
                value = value - 10000
            elif depth == 3: 
                value = value - 5000
        """
        for loss, depth in self.losses:
            if depth < 3:
                win = win - 20000
        """
        return len(self.wins) - len(self.losses) + value
    
    def these_grandchildren(self):
        self.allchildren.extend(self.children)
        depth = self.depth()
        while len(self.allchildren) > 0:
            child = self.allchildren.pop(0)
            childdepth = child.depth() - depth 
            if child.utility == self.target[self.opponent[self.player]]:
                self.wins.append((child, childdepth))
                self.grandchildren.append(child)
            elif child.utility == self.target[self.player]:
                self.losses.append((child, childdepth))
                self.grandchildren.append(child)
            else:
                self.allchildren.extend(child.children)






                
            


