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
    if possible_moves:
        return possible_moves
    return None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try: 
        resultboard = copy.deepcopy(board)
        resultboard[action[0]][action[1]] = player(board)
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
    # our moves / maximizing
    for child in dad.children:
        if child.value == dad.target[dad.player]*100:
            return child.move

        # opponent moves / minimizing
        if child.children:
            for grandchild in child.children:              
                # our moves / maximizing
                if grandchild.children:                         
                    for minichild in grandchild.children:
                        # opponent moves / minimizing
                        if minichild.children:
                            minichild.value = minimaxhelper(minichild).value
                    grandchild.value = minimaxhelper(grandchild).value
            child.value = minimaxhelper(child).value
    return minimaxhelper(dad).move


def minimaxhelper(parent):
    """

    Args:
        dad (_Node_): takes a Node element representing a Game State that needs
        to have at least one possible Child

    Returns:
        the best rated child object for the incoming Node
    """
    if len(parent.children) == 0:
        return parent.value
    if parent.player == X:
        return max(parent.children, key=lambda c: c.value)
    else: 
        return min(parent.children, key=lambda c: c.value)



class Node:
    """
    Represents a possible game State 
    """
    def __init__(self, board, move = None):
        self.alpha = -1000
        self.beta = 1000
        self.value = 0
        self.terminal = terminal(board)
        self.board = board
        self.move = move
        self.children = []
        self.player = player(self.board)
        self.utility = utility(self.board)
        self.target = {X:1, O:-1}
        if move == None:
            self.tree()

        
    
    def tree(self):
        # our choices 
        for move in actions(self.board):
            child = Node(result(self.board,move), move)
            self.children.append(child)
            # opponent choices 
            if child.terminal:
                child.quality()
            else:
                for move in actions(child.board):
                    grandchild = Node(result(child.board, move), move)
                    child.children.append(grandchild)
                    # our choices 
                    if grandchild.terminal:
                        grandchild.quality()
                    else:
                        for move in actions(grandchild.board):
                            minichild = Node(result(grandchild.board, move), move)
                            grandchild.children.append(minichild)
                            # opponent choices 
                            if minichild.terminal:
                                minichild.quality()
                            else:
                                for i, move in enumerate(actions(minichild.board)):
                                    superchild = Node(result(minichild.board, move), move)
                                    minichild.children.append(superchild)
                                    superchild.quality()
                                    
                                    if grandchild.player == X:
                                        if superchild.value <= grandchild.beta:
                                            grandchild.beta = superchild.value
                                        else:
                                            break
                                    else:
                                        if superchild.value >= grandchild.alpha:
                                            grandchild.beta = superchild.value
                                        else:
                                            break

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
