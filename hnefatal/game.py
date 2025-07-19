from enum import Enum

class Piece(Enum):
    EMPTY = 0
    KING = 2
    DEFENDER = 1
    ATTACKER = -1

    def __str__(self):
        if self == Piece.EMPTY:
            return "."
        elif self == Piece.KING:
            return "K"
        elif self == Piece.ATTACKER:
            return "O"
        elif self == Piece.DEFENDER:
            return "X"
        else:
            raise ValueError("Invalid piece type")
        
    def get_player(self):
        if self == Piece.ATTACKER:
            return Player.ATTACKER
        elif self == Piece.DEFENDER or self == Piece.KING:
            return Player.DEFENDER
        else:
            return None
        
    def __int__(self):
        return self.value
        
    def __float__(self):
        return float(self.value)
        
class Player(Enum):
    ATTACKER = 1
    DEFENDER = 2

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.value == other.value
        return False

    def __str__(self):
        if self == Player.ATTACKER:
            return "Attacker"
        elif self == Player.DEFENDER:
            return "Defender"
        else:
            raise ValueError("Invalid player type")
        
    
    def __contains__(self, piece):
        if not isinstance(piece, Piece):
            return False
        
        if self == Player.DEFENDER:
            return piece == Piece.DEFENDER or piece == Piece.KING
        elif self == Player.ATTACKER:
            return piece == Piece.ATTACKER
        
        return False
        
class Coord():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coord):
            return self.x == other.x and self.y == other.y
        return False

class Move():
    def __init__(self, from_pos: Coord, to_pos: Coord):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def __str__(self):
        return f"Move from ({self.from_pos.x}, {self.from_pos.y}) to ({self.to_pos.x}, {self.to_pos.y})"

class Game:
    board = []

    def __init__(self):
        self.board = [[Piece.EMPTY for _ in range(13)] for _ in range(13)]
        
    def fill_board_13_by_13(self):
        self.board = [[Piece.EMPTY for _ in range(13)] for _ in range(13)]
        # Place King at center
        self.board[6][6] = Piece.KING
        # Place defenders around the King
        defender_positions = [
            (6, 5), (6, 7), (5, 6), (7, 6),
            (6, 4), (6, 8), (4, 6), (8, 6),
            (5, 5), (5, 7), (7, 5), (7, 7)
        ]
        for x, y in defender_positions:
            self.board[x][y] = Piece.DEFENDER
        # Place attackers (example positions, adjust as needed for your rules)
        attacker_positions = [
            # Top row
            (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 6),
            # Bottom row
            (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (11, 6),
            # Left column
            (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (6, 1),
            # Right column
            (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (6, 11),
        ]
        for x, y in attacker_positions:
            self.board[x][y] = Piece.ATTACKER

    def print_board(self):
        for row in self.board:
            print(" ".join(str(piece) for piece in row))
        print()

    def find_king_position(self):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece == Piece.KING:
                    return Coord(i, j)
        return None

    def is_king_in_corner(self):
        king_pos = self.find_king_position()

        assert king_pos is not None, "King position not found on the board"

        x, y = king_pos.x, king_pos.y

        # Check if king is in a corner
        if (x, y) in [(0, 0), (0, 12), (12, 0), (12, 12)]:
            return True

    def is_king_surrounded(self):
        king_pos = self.find_king_position()

        assert king_pos is not None, "King position not found on the board"

        x, y = king_pos.x, king_pos.y

        # Directions: up, down, left, right
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        attacker_count = 0
        wall_count = 0

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 13 and 0 <= ny < 13:
                if self.board[nx][ny] == Piece.ATTACKER:
                    attacker_count += 1
            else:
                wall_count += 1

        # Surrounded by attackers on all four sides
        if attacker_count == 4:
            return True

        # Back against wall and surrounded by 3 attackers
        if wall_count == 1 and attacker_count == 3:
            return True

        return False
    
    # Returns None if game is still ongoing or returns the player whom won
    def is_game_over(self):
        # Check if the king is in a corner
        if self.is_king_in_corner():
            return Player.DEFENDER
        
        # Check if the king is surrounded
        if self.is_king_surrounded():
            return Player.ATTACKER
        
        # Check if all pieces of one player are captured
        attacker_pieces = sum(piece == Piece.ATTACKER for row in self.board for piece in row)
        defender_pieces = sum(piece == Piece.DEFENDER for row in self.board for piece in row) # If no defenders but the king is alive, attackers win

        if attacker_pieces == 0:
            return Player.DEFENDER
        elif defender_pieces == 0:
            return Player.ATTACKER
        
        return None
    
    def piece_at(self, pos: Coord):
        return self.board[pos.x][pos.y]
    
    # Check if a move is valid. Any piece can move to an empty space in the same row or column, as long as there are no pieces in between.
    # Any piece cannot occupy a corner or the middle of the board, besides the king.
    def is_valid_move(self, from_pos: Coord, to_pos: Coord):
        assert all(0 <= element < 13 for element in [from_pos.x, from_pos.y, to_pos.x, to_pos.y]), "Coordinates must be between 0 and 12"

        if from_pos == to_pos:
            return False 
        
        piece = self.piece_at(from_pos)
        if piece == Piece.EMPTY:
            return False
        
        if self.piece_at(to_pos) != Piece.EMPTY:
            return False
        
        if piece != Piece.KING:
            if to_pos.x in [0, 12] and to_pos.y in [0, 12]:
                return False
            if to_pos == Coord(6, 6):
                return False

        if from_pos.x == to_pos.x:
            row = self.board[from_pos.x]

            if from_pos.y < to_pos.y:
                leftmost = from_pos.y + 1
                rightmost = to_pos.y
            else:
                leftmost = to_pos.y
                # rightmost = from_pos.y - 1
                rightmost = from_pos.y 

            for piece in row[leftmost:rightmost]:
                if piece != Piece.EMPTY:
                    return False                                                                                                                                                                                              
        
        elif from_pos.y == to_pos.y:
            
            if from_pos.x < to_pos.x:
                leftmost = from_pos.x + 1
                rightmost = to_pos.x
            else:
                leftmost = to_pos.x
                # rightmost = from_pos.x - 1
                rightmost = from_pos.x

            for column in self.board[leftmost:rightmost]:
                if column[from_pos.y] != Piece.EMPTY:
                    return False   
        else:
            # Invalid move, not in the same row or column
            return False
        
        return True
    
    # Move a piece from one position to another.
    # Attack adjacent pieces if it's an opponent and they are sandwiched either against an allied piece or a corner, or the center.
    def move_piece_and_attack(self, from_pos: Coord, to_pos: Coord):
        piece = self.piece_at(from_pos)
        player = piece.get_player()
        self.board[to_pos.x][to_pos.y] = piece
        self.board[from_pos.x][from_pos.y] = Piece.EMPTY

        # check for adjacent pieces to attack
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if abs(dx) + abs(dy) != 1: continue
                nx, ny = to_pos.x + dx, to_pos.y + dy
                if nx > 12 or nx < 0: continue
                if ny > 12 or ny < 0: continue

                other_piece = self.piece_at(Coord(nx, ny))
                if other_piece == Piece.EMPTY or other_piece in player or other_piece == Piece.KING:
                    continue

                nnx = to_pos.x + 2*dx
                nny = to_pos.y + 2*dy
                against_corner_wall = (nnx == 0 or nnx == 12) and (nny == 0 or nny == 12)
                if not against_corner_wall:
                    if nnx > 12 or nnx < 0: continue
                    if nny > 12 or nny < 0: continue

                against_center_wall = nnx == 6 and nny == 6

                allied_piece_between = self.piece_at(Coord(nnx, nny)) in player

                if allied_piece_between or against_corner_wall or against_center_wall:
                    # We attacked a piece
                    # print(f"Attacking piece at ({nx}, {ny})")
                    self.board[nx][ny] = Piece.EMPTY