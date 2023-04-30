from tictactoe import winner
from tictactoe import utility
from tictactoe import result
from tictactoe import player
from tictactoe import Node

X = "X"
O = "O"
EMPTY = None

initial_board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

board1 =  [[X, X, X],
            [EMPTY, O, EMPTY],
            [O, EMPTY, O]]

board2 = [[O, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [X, X, O]]

board3 = [[O, EMPTY, X],
            [EMPTY, O, EMPTY],
            [X, X, EMPTY]]

board4 = [[O, EMPTY, EMPTY],
            [O, X, EMPTY],
            [O, X, X]]

board5 = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [X, X, O]]

board5 = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [X, EMPTY, EMPTY]]

board6 = [[X, EMPTY, O],
          [O, X, O],
          [X, EMPTY, O]]

board7 = [[EMPTY, X, O],
          [EMPTY, X, O],
          [EMPTY, X, EMPTY]]

def test_winner():
    assert winner(board1) == X
    assert winner(board2) == O
    assert winner(board3) == None
    assert winner(board4) == O
    assert winner(board5) == None
    assert winner(board6) == O
    assert winner(board7) == X

def test_utility():
    assert utility(board1) == 1
    assert utility(board2) == -1
    assert utility(board3) == 0
    assert utility(board4) == -1
    assert utility(board5) == 0
    assert utility(board5) == 0

def test_result():
    assert result(initial_board, (1,0)) == [[EMPTY, EMPTY, EMPTY],
            [X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    assert result(initial_board, (1,1)) == [[EMPTY, EMPTY, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    assert result(initial_board, (2,2)) == [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, X]]

def test_player():
    assert player(initial_board) == X
    assert player(board3) == O

def test_depth():
    d1board = Node(board1)
    assert d1board.depth() == 6
    d2board = Node(board2)
    assert d2board.depth() == 5
    d3board = Node(board3)
    assert d3board.depth() == 5

