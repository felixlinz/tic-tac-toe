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
        i, j = action
        resultboard = copy.deepcopy(board)
        if resultboard[i][j] == EMPTY:
            resultboard[i][j] = player(board)
            return resultboard
        else:
            raise Exception("not a valid move")
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
    dad = Parent(board)
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
        takes a Node object representing a Game State that needs
        to have at least one possible Child

    Returns:
        the best rated child object for the incoming Node
    """
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
                  
class Parent(Node):
    """
    Parent Node of possible game tree
    Instances of this only on initial board fed to 
    minimax
    """
    def __init__(self, board):
        super().__init__(board)
        self.tree()

    def tree(self):
        """
        generates 4 levels of ancestors for the parent node
        if possible
        """
        # MAX PLAYER
        for e, move in enumerate(actions(self.board)):

            child = Child(result(self.board,move), move)
            self.children.append(child)
            # MIN PLAYER
            if child.terminal:
                child.quality()
            else:

                for move in actions(child.board):
                    
                    grandchild = Child(result(child.board, move), move)
                    child.children.append(grandchild)
                    # MAX PLAYER
                    if grandchild.terminal:
                        grandchild.quality()
                    else:
                        
                        for i, move in enumerate(actions(grandchild.board)):
                            minichild = Child(result(grandchild.board, move), move)
                            grandchild.children.append(minichild)
                            # MIN PLAYER
                            if minichild.terminal:
                                minichild.quality()
                            else:
                                
                                for move in actions(minichild.board):
                                    
                                    superchild = Child(result(minichild.board, move), move)
                                    minichild.children.append(superchild)
                                    superchild.quality()
                                    
                                    # alphabeta pruning                                
                                    if grandchild.player == X:
                                        if superchild.value < minichild.beta:
                                            minichild.beta = superchild.value  
                                            if minichild.beta > grandchild.alpha:
                                                grandchild.alpha = minichild.beta
                                            if superchild.value < grandchild.alpha and i != 0:
                                                break       
    
                                    else:
                                        if superchild.value > minichild.alpha:
                                            minichild.alpha = superchild.value  
                                            if minichild.alpha < grandchild.beta:
                                                grandchild.beta = minichild.alpha
                                            if superchild.value > grandchild.beta and i != 0:
                                                break    

class Child(Node):
    """
    Child of every other possible instance that 
    is generated by the parent node
    adds the quality() method that can be used 
    to evaluate how good a certain game state is
    """
    def __init__(self, board, move):
        super().__init__(board, move)
        

    def quality(self):  
        """
        figueres out a value for the node its called on
        
        """
        if not self.terminal:
            for row in self.board:
                # row evaluation
                self.row_evaluation(row)
            for i in range(3):
                # column evaluation
                self.row_evaluation([row[i] for row in self.board])
            # diagonal evaluation
            self.row_evaluation([self.board[0][0],self.board[1][1],self.board[2][2]])
            self.row_evaluation([self.board[0][2],self.board[1][1],self.board[2][0]])             
        else:
            # assigns a value of - 100 for loosing state, 100 for winner, 0 for draw
            self.value = self.utility * 100

    def row_evaluation(self, row):
        """
        edits the value of its node based on the
        usefullness of a single row 
        """
        value = 0
        for cell in row:
            if cell != EMPTY:
                value += self.target[cell]
        if math.pow(value,2) == 4:
            self.value += value*5