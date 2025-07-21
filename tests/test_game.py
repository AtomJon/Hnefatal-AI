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

    # Invalid move: center position
    g.board[6][6] = Piece.EMPTY  # Clear center for this test
    g.board[5][6] = Piece.DEFENDER
    from_pos.x, from_pos.y = 5, 6
    from_pos.x, from_pos.y = 6, 6
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected invalid move to center (6,6)"

    # Invalid move: corner position
    g.board[0][0] = Piece.EMPTY  # Clear center for this test
    g.board[0][1] = Piece.DEFENDER
    from_pos.x, from_pos.y = 0, 1
    from_pos.x, from_pos.y = 0, 0
    assert g.is_valid_move(from_pos, to_pos) is False, "Expected invalid move to corner (0,0)"

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

    # Attack a piece against a corner
    g.board[0][1] = Piece.ATTACKER
    g.board[0][2] = Piece.EMPTY
    g.board[0][3] = Piece.DEFENDER
    from_pos = Coord(0, 3)
    to_pos = Coord(0, 2)
    g.move_piece_and_attack(from_pos, to_pos)
    assert g.piece_at(Coord(0, 1)) == Piece.EMPTY, "Expected piece to be removed"
    assert g.piece_at(to_pos) == Piece.DEFENDER, "Expected piece to remain"

    # Attack a piece against the center
    g.board[6][5] = Piece.ATTACKER
    g.board[6][4] = Piece.EMPTY
    g.board[6][3] = Piece.DEFENDER
    from_pos = Coord(6, 3)
    to_pos = Coord(6, 4)
    g.move_piece_and_attack(from_pos, to_pos)
    assert g.piece_at(Coord(6, 5)) == Piece.EMPTY, "Expected piece to be removed"
    assert g.piece_at(to_pos) == Piece.DEFENDER, "Expected piece to remain"

    # INVALID ATTACK: Attack a piece against a wall
    g.board[0][2] = Piece.ATTACKER
    g.board[0][3] = Piece.EMPTY
    g.board[0][4] = Piece.DEFENDER
    from_pos = Coord(0, 4)
    to_pos = Coord(0, 3)
    g.move_piece_and_attack(from_pos, to_pos)
    assert g.piece_at(to_pos) == Piece.DEFENDER, "Expected piece to remain"
    assert g.piece_at(Coord(0,2)) == Piece.ATTACKER, "Expected piece to remain"

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

def test_game_over():
    g = Game()
    g.board[6][5] = Piece.DEFENDER
    g.board[6][4] = Piece.ATTACKER
    g.board[0][0] = Piece.KING
    assert g.is_game_over() == Player.DEFENDER, "Expected king in corner to be defender"
    g.board[0][0] = Piece.EMPTY
    g.board[12][0] = Piece.KING
    assert g.is_game_over() == Player.DEFENDER, "Expected king in corner to be defender"
    g.board[12][0] = Piece.EMPTY
    g.board[0][12] = Piece.KING
    assert g.is_game_over() == Player.DEFENDER, "Expected king in corner to be defender"
    g.board[0][12] = Piece.EMPTY
    g.board[12][12] = Piece.KING
    assert g.is_game_over() == Player.DEFENDER, "Expected king in corner to be defender"

    g = Game()
    g.board[6][6] = Piece.KING
    g.board[6][5] = Piece.ATTACKER
    assert g.is_game_over() == Player.ATTACKER, "Expected no remaining defenders to be attacker"
    g.board[6][5] = Piece.DEFENDER
    assert g.is_game_over() == Player.DEFENDER, "Expected no remaining attackers to be defender"

    g.board[6][6] = Piece.KING
    g.board[4][4] = Piece.DEFENDER
    g.board[6][7] = Piece.ATTACKER
    g.board[5][6] = Piece.ATTACKER
    g.board[7][6] = Piece.ATTACKER
    g.board[6][5] = Piece.ATTACKER
    assert g.is_game_over() == Player.ATTACKER, "Expected surrounded king to be attacker"

    g = Game()
    g.board[6][6] = Piece.DEFENDER

    g.board[0][6] = Piece.KING
    g.board[0][7] = Piece.ATTACKER
    g.board[0][5] = Piece.ATTACKER
    g.board[1][6] = Piece.ATTACKER
    assert g.is_game_over() == Player.ATTACKER, "Expected surrounded king to be attacker"

    g.fill_board_13_by_13()
    assert g.is_game_over() == None, "Expected ongoing game"

def run_all_tests():
    test_game_initialization()
    test_print_board_runs()
    test_fill_board_13_by_13_content()
    test_is_valid_move()
    test_move_piece()
    test_piece_equality()
    test_game_over()

    print("### All tests passed! ###")