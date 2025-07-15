from hnefatal.game import Piece, Player, Coord, Game

def test_game_initialization():
    g = Game()
    assert hasattr(g, 'board')
    assert isinstance(g.board, list)
    assert hasattr(g, 'is_game_over')

def test_fill_board_13_by_13_content():
    g = Game()
    g.fill_board_13_by_13()
    assert len(g.board) == 13, "Expected board to have 13 rows"
    assert all(len(row) == 13 for row in g.board), "Expected each row to have 13 columns"
    # Check King position
    assert g.board[6][6] == Piece.KING, "Expected King to be at position (6, 6)"
    # Check that attackers and defenders are present
    attackers = sum(piece == Piece.ATTACKER for row in g.board for piece in row)
    defenders = sum(piece == Piece.DEFENDER for row in g.board for piece in row)
    assert attackers == 24, f"Expected 24 attackers on the board, got {attackers}"
    assert defenders == 12, f"Expected 12 defenders on the board, got {defenders}"

def test_print_board_runs():
    g = Game()
    g.fill_board_13_by_13()
    try:
        g.print_board()
    except Exception as e:
        assert False, f"print_board raised an exception: {e}"

def test_is_valid_move():
    g = Game()
    g.fill_board_13_by_13()

    # Valid horizontal move for defender
    from_pos = Coord(6, 4)
    to_pos = Coord(6, 2)
    assert g.is_valid_move(from_pos, to_pos) is True, "Expected valid horizontal move for defender"

    # Valid vertical move for defender
    from_pos.x, from_pos.y = 6, 4
    to_pos.x, to_pos.y = 10, 4
    assert g.is_valid_move(from_pos, to_pos) is True, "Expected valid vertical move for defender"

    # Invalid move: moving to same position
    from_pos.x, from_pos.y = 6, 5
    to_pos.x, to_pos.y = 6, 5
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected invalid move to same position"

    # Invalid move: moving diagonally
    from_pos.x, from_pos.y = 6, 4
    to_pos.x, to_pos.y = 5, 3
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected invalid diagonal move"

    # Invalid move: blocked by piece
    from_pos.x, from_pos.y = 6, 2
    to_pos.x, to_pos.y = 6, 8
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected invalid move due to blocking piece"

    # Invalid move: moving to occupied position
    from_pos.x, from_pos.y = 6, 4
    to_pos.x, to_pos.y = 6, 1
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected invalid move to occupied position"

    # Invalid move: obstructed by pieces
    from_pos.x, from_pos.y = 7,12
    to_pos.x, to_pos.y = 1,12
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected obstructed move from (7,12) to (1,12)"
    
    # Invalid move: obstructed by pieces
    from_pos.x, from_pos.y = 12, 5
    to_pos.x, to_pos.y = 12, 3
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected obstructed move from (12,5) to (12,3)"
    
    # Invalid move: obstructed by pieces
    from_pos.x, from_pos.y = 6, 6
    to_pos.x, to_pos.y = 6, 5
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected obstructed move from (12,5) to (12,3)"
    
    # Invalid move: obstructed by pieces
    from_pos.x, from_pos.y = 6, 6
    to_pos.x, to_pos.y = 6, 2
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected obstructed move from (12,5) to (12,3)"
    

    g.board[0][11] = Piece.KING
    from_pos.x, from_pos.y = 0, 11
    to_pos.x, to_pos.y = 0, 12
    assert g.is_valid_move(from_pos, to_pos) is True, "Expected valid move for Victory"

def test_attack_piece():
    g = Game()
    g.board[0][0] = Piece.DEFENDER
    g.board[0][1] = Piece.ATTACKER
    g.board[4][2] = Piece.DEFENDER
    from_pos = Coord(4, 2)
    to_pos = Coord(0, 2)
    
    # Move piece and attack
    g.move_piece_and_attack(from_pos, to_pos)
    
    # Check if the piece was moved
    assert g.piece_at(to_pos) == Piece.DEFENDER, "Expected piece to be moved to new position"
    assert g.piece_at(from_pos) == Piece.EMPTY, "Expected original position to be empty after move"
    
    # Check if an adjacent piece was attacked
    attacked_pos = Coord(0, 1)
    assert g.piece_at(attacked_pos) == Piece.EMPTY, "Expected attacked piece to be removed"

def test_move_piece():
    g = Game()
    g.fill_board_13_by_13()
    from_pos = Coord(6, 4)
    to_pos = Coord(6, 2)
    g.move_piece_and_attack(from_pos, to_pos)
    assert g.piece_at(to_pos) == Piece.DEFENDER, "Expected piece to be moved to new position"
    assert g.piece_at(from_pos) == Piece.EMPTY, "Expected original position to be empty after move"

def test_piece_equality():
    assert Piece.ATTACKER in Player.ATTACKER
    assert Piece.DEFENDER in Player.DEFENDER
    assert Piece.KING in Player.DEFENDER
    assert Piece.EMPTY not in Player.ATTACKER
    assert Piece.EMPTY not in Player.DEFENDER
    assert Piece.ATTACKER not in Player.DEFENDER

def run_all_tests():
    test_game_initialization()
    test_print_board_runs()
    test_fill_board_13_by_13_content()
    test_is_valid_move()
    test_move_piece()
    test_piece_equality()

    print("### All tests passed! ###")