import pytest
from tictactoe import winner
from tictactoe import utility
from tictactoe import result
from tictactoe import player
from tictactoe import Node
from tictactoe import minimax
from tictactoe import initial_state

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

board7 = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [X, EMPTY, EMPTY]]

board6 = [[X, EMPTY, O],
          [O, X, O],
          [X, EMPTY, O]]


def test_initial_state():
    assert initial_state() == initial_board

def test_winner():
    assert winner(board1) == X
    assert winner(board2) == O
    assert winner(board3) == None
    assert winner(board4) == O
    assert winner(board5) == None
    assert winner(board6) == O

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
    with pytest.raises(Exception):
        result(board6, (0,0))
    with pytest.raises(Exception):
        result([000])
    with pytest.raises(Exception):
        result(initial_board, (0,0,0))

def test_player():
    assert player(initial_board) == X
    assert player(board3) == O

def test_minimax():
    assert minimax(initial_board) == (1,1)
    assert minimax(board2) == None
    assert minimax(board5) == (0,0)
    
test_node = Node(initial_board)
test_node2 = Node(board1)
test_node3 = Node(board2)
test_node4 = Node(board3)
test_node5 = Node(board5)
    
def test_quality():
    test_node.quality()
    assert test_node.value == 0
    test_node2.quality()
    assert test_node2.value == 100
    test_node3.quality()
    assert test_node3.value == -100
    test_node4.quality()
    assert test_node4.value == 0
    test_node5.quality()
    assert test_node5.value == -10
