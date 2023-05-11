"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None
childs = []


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
            if checker != None:
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
    rules = {X:1, O:-1}
    result = winner(board)
    return rules[result]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    global childs
    if not isinstance(board, Node):
        if actions(board):
            if len(actions(board)) == 9:
                childs = []
                return (1,1)
            elif len(actions(board)) == 8:
                childs = []
        if not childs:
            board = Node(board)
        else:
            for child in childs:
                if child.board == board:
                    board = child
    dad = board
    if len(dad.children) == 1:
        childs = []
        return dad.children[0].move
    elif terminal(dad.board) == True:
        childs = []
        return None
    for child in dad.children:
        child.quality()
    dad.children.sort(key=lambda c: c.value, reverse=True)
    return minimaxhelper(dad.children)
        
def minimaxhelper(children):
    """
    Returns a usseful child
    """
    for child in children: # moves done by us 
        legs = [child.children]
        board = child.board
        while not terminal(board):
            legs.extend(child.children)  # moves done by opponent 
            for kiddo in legs: 
                if kiddo.utility == kiddo.target[child.player]:
                    flag = True
            





class Node:
    def __init__(self, board, move = None):
        self.value = -100000
        self.terminal = terminal(board)
        self.board = board
        self.move = move
        self.maerial = 0
        self.children = []
        self.allchildren = []
        self.grandchildren = []
        self.wins = []
        self.losses = []
        self.ties = []
        self.opponent = {X:O, O:X}
        self.player = player(self.board)
        self.utility = utility(self.board)
        self.target = {X:1, O:-1}
        if move == None:
            self.tree()
    
    def tree(self):
        now = [self]
        while len(now) > 0:
            parent = now.pop(0)
            moves = actions(parent.board)
            if not terminal(parent.board):
                for move in moves:
                    moved_board = result(parent.board, move)
                    child = Node(moved_board, move)
                    now.append(child)
                    parent.children.append(child)

    """"
    def treecleaner(self):
        legs = [self]
        while len(legs) > 0:
            mom = legs.pop(0)
            for kiddo in mom.children:
                if kiddo.utility == kiddo.target[mom.player]:
                    mom.children = [kiddo]
                    legs.append(kiddo)
                    break
                for grandkiddo in kiddo.children:
                    if grandkiddo.utility == kiddo.target[kiddo.player]:
                        del kiddo
                        legs.extend(mom.children)
                        break
    """

    def depth(self):
        self._depth = 0
        for row in self.board:
            for cell in row: 
                if cell == EMPTY:
                    self._depth += 1
        return 9 - self._depth

    def quality(self):  
        self.these_grandchildren()
        for win, _ in self.wins:
            self.value += 1
        for loss, depth in self.losses:
            self.value -= (3/depth)*(3/depth)

    
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
                self.ties.append((child, childdepth))


                
            


