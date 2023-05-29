"""
Tic Tac Toe Player
"""
import copy
import math
from functools import wraps
import time

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
    smart_moves = [{(0,0)},{(0,2)},{(2,0)},{(2,2)}]
    for i, line in enumerate(board):
        for e, cell in enumerate(line):
            if cell != X and cell != O:
                move = (i,e)
                possible_moves.add(move)
    """
    if len(possible_moves) > 7:
        if (1,1) not in possible_moves:
            possible_moves = random.choice(smart_moves)
            return possible_moves
        else: 
            return {(1,1)}
    """
    if possible_moves:
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
    checker = board[1][1]
    if board[0][0] == checker and board[2][2] == checker:
        return checker
    if board[0][2]==checker and board[2][0] == checker:
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
    dad = Node(board)
    if len(dad.children) == 1:
        return dad.children[0].move
    elif dad.terminal == True:
        return None
    # our moves
    for child in dad.children:
        # opponent moves
        if dad.children:
            for grandchild in child.children:
                # our moves
                if grandchild.children:
                    for minichild in grandchild.children:
                        # opponent moves
                        if minichild.children:
                            minichild.value = minimaxhelper(minichild).value
                    grandchild.value = minimaxhelper(grandchild).value
        if child.children:
            child.value = minimaxhelper(child).value
    print(minimaxhelper(dad).value)
    return minimaxhelper(dad).move

def minimaxhelper(dad):
    if dad.player == X:
        dad.children.sort(key=lambda c: c.value, reverse=True)
    else: 
        dad.children.sort(key=lambda c: c.value)
    return dad.children[0]


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
        self.quality()
        
    
    def tree(self):
        now = [self]
        for i in range(3):
            later = []
            while now:
                parent = now.pop(0)
                if not parent.terminal:
                    moves = actions(parent.board)
                    for move in moves:
                        moved_board = result(parent.board, move)
                        child = Node(moved_board, move)
                        parent.children.append(child)
                        later.append(child)
            now = later
        for node in now:
            rev = -1000
            if not node.terminal:
                    moves = actions(parent.board)
                    for move in moves:
                        moved_board = result(parent.board, move)
                        child = Node(moved_board, move)
                        if child.value > rev:
                            rev = child.value
                            parent.children.append(child)
                            later.append(child)
                        elif child.value < rev:
                            break

    def depth(self):
        self._depth = 0
        for row in self.board:
            for cell in row: 
                if cell == EMPTY:
                    self._depth += 1
        return 9 - self._depth

    def quality(self):  
        if not self.terminal:
            for row in self.board:
                self.evaluation(row)
            for i in range(3):
                column = [row[i] for row in self.board]
                self.evaluation(column)
            self.evaluation([self.board[0][0],self.board[1][1],self.board[2][2]])
            self.evaluation([self.board[0][2],self.board[1][1],self.board[2][0]])             
        else:
            self.value = self.utility * 100

    def evaluation(self, row):
        value = 0
        for cell in row:
            if cell != EMPTY:
                value += self.target[cell]
        if math.pow(value,2) == 4:
            self.value += value*5