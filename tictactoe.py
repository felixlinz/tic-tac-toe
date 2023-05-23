"""
Tic Tac Toe Player
"""
import copy
import math
import random
from functools import wraps
import time

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
    smart_moves = [{(0,0)},{(0,2)},{(2,0)},{(2,2)}]
    for i, line in enumerate(board):
        for e, cell in enumerate(line):
            if cell != X and cell != O:
                move = (i,e)
                possible_moves.add(move)
    if len(possible_moves) > 7:
        if (1,1) not in possible_moves:
            possible_moves = random.choice(smart_moves)
            return possible_moves
        else: 
            return {(1,1)}
    elif possible_moves:
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

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

@timeit
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    global childs
    if not isinstance(board, Node):
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
    return minimaxhelper(dad)

def minimaxhelper(dad):
    for child in dad.children:
        child.quality()
    dad.children.sort(key=lambda c: c.value, reverse=True)
    # first level children sorted by quality
    for child in dad.children:
        parent = child
        while parent.terminal == False:
            for kiddo in parent.children:
                kiddo.quality()
            parent.children.sort(key=lambda c: c.value)
            parent = parent.children[-1]
        child.hypovalue = parent.utility
        if child.hypovalue == dad.target[dad.player]:
            return child.move
    backup = []
    for child in dad.children:
        if child.hypovalue == dad.target[dad.player]:
            return child.move
        elif not child.hypovalue == child.target[child.player]:
            backup.append(child)
    return backup[0].move

class Node:
    def __init__(self, board, move = None):
        self.hypovalue = 0
        self.value = 0
        self.terminal = terminal(board)
        self.board = board
        self.move = move
        self.children = []
        self.wins = []
        self.losses = []
        self.opponent = {X:O, O:X}
        self.player = player(self.board)
        self.utility = utility(self.board)
        self.target = {X:1, O:-1}
        if move == None:
            self.tree()
    
    def tree(self):
        now = [self]
        while now:
            parent = now.pop(0)
            moves = actions(parent.board)
            if not parent.terminal:
                for move in moves:
                    moved_board = result(parent.board, move)
                    child = Node(moved_board, move)
                    now.append(child)
                    parent.children.append(child)

    def depth(self):
        self._depth = 0
        for row in self.board:
            for cell in row: 
                if cell == EMPTY:
                    self._depth += 1
        return 9 - self._depth

    def quality(self):  
        self.these_grandchildren()  # collecting grandchildren for superdad
        if self.utility == self.target[self.opponent[self.player]]:
            self.value += 1000
        elif self.utility == self.target[self.player]:
            self.value -= 1000
        for _, depth in self.wins:
            self.value += (9/depth)*(9/depth)
        for _, depth in self.losses:
            self.value -= (9/depth)*(9/depth)

    def these_grandchildren(self):
        self.allchildren = []
        self.allchildren.extend(self.children)
        depth = self.depth()
        while len(self.allchildren) > 0:
            child = self.allchildren.pop(0)
            childdepth = child.depth() - depth 
            if child.utility == self.target[self.opponent[self.player]]:
                self.wins.append((child, childdepth))
            elif child.utility == self.target[self.player]:
                self.losses.append((child, childdepth))
            else:
                self.allchildren.extend(child.children)