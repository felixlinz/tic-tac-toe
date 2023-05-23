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
    print("#####################")
    return minimaxhelper(dad)

def minimaxhelper(dad):
    kiddos = []
    for child in dad.children:
        child.quality()
    dad.children.sort(key=lambda c: c.value, reverse=True)
    for child in dad.children:
        print("___________________")
        parent = child
        frontier = child.children
        for child in frontier:
            child.quality()
        frontier.sort(key=lambda c: c.value)
        while parent.terminal == False:
            print(parent.move, parent.opponent[parent.player])
            for child in parent.children:
                child.quality()
            parent.children.sort(key=lambda c: c.value)
            frontier.append(parent.children[-1])
            parent = frontier.pop()
        print(parent.move, parent.utility, "terminal")
        child.hypovalue = parent.utility
        kiddos.append(child)
        if child.hypovalue == dad.target[dad.player]:
            print("option1")
            return child.move
    backup = []
    kiddos.sort(key= lambda c: c.value, reverse=True)
    while len(kiddos) > 0:
        child = kiddos.pop(0)
        if child.hypovalue == dad.target[dad.player]:
            print("option2")
            return child.move
        elif child.hypovalue == child.target[child.player]:
            del child
        else:
            backup.append(child)
    print("option3")
    print(child.target[child.player], backup[0].hypovalue, backup[0].move)
    return backup[0].move


class Node:
    def __init__(self, board, parent = None, move = None):
        self.hypovalue = 0
        self.value = 0
        self.terminal = terminal(board)
        self.board = board
        self.move = move
        self.parent = parent
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
                    child = Node(moved_board, parent, move)
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
        self.these_grandchildren()  # collecting grandchildren for superdad
        if self.utility == self.target[self.opponent[self.player]]:
            self.value = 1000
        for _, depth in self.wins:
            self.value += (9/depth)*(9/depth)
        for _, depth in self.losses:
            self.value -= (9/depth)*(9/depth)

        """
        loosing_parents = set()     # making a set of moves that lead to a definite loss
        winning_parents = set()     # a set of opponent moves that enable us to win in the next move 
        for child in self.losses:
            loosing_parents.add(child.parent)
        for parent in loosing_parents: 
            parent.utility = -1     # giving utiity -1 to all parents that lead to definite losses

        for child in self.wins:
            winning_parents.add(child.parent)
        for parent in winning_parents:
            parent.theese_grandchildren()
            if len(parent.wins) == 0:
                parent.parent.utility = 1
        """
            


    
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
            elif child.terminal == True and child.utility == 0:
                self.grandchildren.append(child)
                self.ties.append((child, childdepth))
            else:
                self.allchildren.extend(child.children)



                
            


