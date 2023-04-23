from tictactoe import winner
from tictactoe import utility
from tictactoe import result

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

def test_winner():
    assert winner(board1) == X
    assert winner(board2) == O
    assert winner(board3) == None
    assert winner(board4) == O
    assert winner(board5) == None

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
    assert player(board1) == X