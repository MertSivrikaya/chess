import copy
from sys import exit
"""

Coding Project | Started on 13.09.2022, Tuesday

Theme: Create a 'Chess' game


Notes:

if square in possible_moves():
    move()

Her hamle başı vezire şah çekilip çekilmediği (+) ve mat olup olmadığı kontrol edilmeli.
Bir taş hareket ettiğinde mevcut durumda şahı korumasız bırakıyorsa bu hamle yapılamaz. (+)
2. bir idealize board yapılabilir, taş buraya gitmişçesine ve buradaki hamleler değerlendirilir. (+)
Bir karenin tehdit altında olup olmadığını bulan fonksiyon. (+)
Piyon en uca gelince vezir olacak.
Şah ve matları hamle sonları değil hamle başları kontrol et.
Not: Bir şaha aynı anda en fazla bir taş tarafından şah çekilebilir.
check_mate_in_start_of_the_current_turn fonksiyonuna bak, aynı satırda mı sütünde mı çaprazda mı kontrol edilebilir.

"""


display_icons = {

    "white king" : "♔",
    "white queen" : "♕",
    "white rook" : "♖",
    "white bishop" : "♗",
    "white knight" : "♘",
    "white pawn" : "♙",

    "black king" : "♚",
    "black queen" : "♛",
    "black rook" : "♜",
    "black bishop" : "♝",
    "black knight" : "♞",
    "black pawn" : "♟︎",
}

class ChessManager:
    def __init__(self):
        self.board = [[{"color": "None" , "piece": "None"} for z in range(8)] for i in range(8)] # None represents empty square.
        self.white_pieces = []
        self.black_pieces = []

    def is_a_valid_square(self, row, col):
        if row in range(8) and col in range(8): # It's a valid square.
            return True
        else:
            return False

    def is_move_valid(self, target_row, target_col, possible_moves): 
        
        if [target_row,target_col] in possible_moves:
            return True

        else:
            return False

    def is_a_opponent_piece(self, start_square_piece_color, target_square_piece_color):
        if start_square_piece_color == "white" and target_square_piece_color == "black":
            return True
        elif start_square_piece_color == "black" and target_square_piece_color == "white":
            return True
        else:
            return False

    def is_a_friendly_piece(self, start_square_piece_color, target_square_piece_color):
        if start_square_piece_color == target_square_piece_color and not start_square_piece_color == "None":
            return True
        else:
            return False

    def is_a_piece(self, target_row, target_col):
        if not chess_manager.board[target_row][target_col]["piece"] == "None":
            return True
        else:
            return False

    def get_piece_color(self, row, col):
        return self.board[row][col]["color"]

    def get_piece_type(self, row, col):
        return self.board[row][col]["piece"]
    
    def get_piece_display_symbol(self, row, col):
        return display_icons[self.get_piece_color(row,col) + " " + self.get_piece_type(row,col)]
        
    def empty_square(self, row, col):
        self.board[row][col]["color"] = "None"
        self.board[row][col]["piece"] = "None"

    def is_square_threatened(self, row, col, original_piece_color): # not opponents's piece
        square_to_check = [row,col]
        opponents_pieces = []

        if original_piece_color == "white": # opponent is 'black'.
            opponents_pieces = self.black_pieces
        else: # opponent is 'white'.
            opponents_pieces = self.white_pieces

        for opponent_piece in opponents_pieces:
            if square_to_check in opponent_piece.get_threatened_squares():
                return True

        return False

    def test_check_in_future_move(self, start_row, start_col, target_row, target_col):
        future_board = copy.deepcopy(self.board)
        future_white_pieces = copy.deepcopy(self.white_pieces)
        future_black_pieces = copy.deepcopy(self.black_pieces)

        color_of_moving_piece = self.get_piece_color(start_row, start_col)
        type_of_moving_piece = self.get_piece_type(start_row, start_col)

        if not future_board[target_row][target_col]["color"] == "None": # Capturing opponent's piece.
            deleted_piece_index = 0
            if color_of_moving_piece == "white": # we are capturing a black piece.
                for index, piece in enumerate(future_black_pieces):
                    if piece.position_on_the_board == [target_row, target_col]:
                        deleted_piece_index = index
                        break
                del future_black_pieces[deleted_piece_index]

            if color_of_moving_piece == "black": # we are capturing a white piece.
                for index, piece in enumerate(future_white_pieces):
                    if piece.position_on_the_board == [target_row, target_col]:
                        deleted_piece_index = index
                        break
                del future_white_pieces[deleted_piece_index]

            future_board[target_row][target_col]["color"] = "None"
            future_board[target_row][target_col]["piece"] = "None"
            
        
        future_board[start_row][start_col]["color"] = "None"
        future_board[start_row][start_col]["piece"] = "None" # Delete the old position and make it empty on the board.
        
        friendly_pieces = []
        if color_of_moving_piece == "white": 
            friendly_pieces = future_white_pieces
        else: 
            friendly_pieces = future_black_pieces

        start_index = -1
        for index, piece in enumerate(friendly_pieces):
            if piece.position_on_the_board == [start_row,start_col]:
                start_index = index

        if color_of_moving_piece == "white": 
            future_white_pieces[start_index].position_on_the_board = [target_row,target_col]
        else: 
            future_black_pieces[start_index].position_on_the_board = [target_row,target_col]

        future_board[target_row][target_col]["color"] = color_of_moving_piece
        future_board[target_row][target_col]["piece"] = type_of_moving_piece

        opponents_pieces = []
        if color_of_moving_piece == "white": # opponent is 'black'.
            opponents_pieces = future_black_pieces
        else: # opponent is 'white'.
            opponents_pieces = future_white_pieces

        kings_row = -1
        kings_col = -1

        for piece in friendly_pieces:
            if piece.piece_type == "king":
                kings_row, kings_col = piece.position_on_the_board[0], piece.position_on_the_board[1]
       
        square_to_check = [kings_row,kings_col]
        
        for opponent_piece in opponents_pieces:
            if square_to_check in opponent_piece.get_threatened_squares(): # gerçek konumuna göre, çalışmayabilir
                return True # it is a check

        return False

    def test_check_in_start_of_the_current_turn(self, color_to_check): # should also check mate
        pieces_to_check = []
        if color_to_check == "white":
            pieces_to_check = self.white_pieces
        else:
            pieces_to_check = self.black_pieces

        king_pos = []
        for piece in pieces_to_check:
            if piece.piece_type == "king":
                king_pos = piece.position_on_the_board

        if self.is_square_threatened(king_pos[0], king_pos[1], color_to_check):
            return True
        else:
            return False

    def check_mate_in_start_of_the_current_turn(self, color_to_check): # is being modified.
        pieces_to_check = []
        opponent_pieces = []
        if color_to_check == "white":
            pieces_to_check = self.white_pieces
            opponent_pieces = self.black_pieces
        else:
            pieces_to_check = self.black_pieces
            opponent_pieces = self.white_pieces

        king_pos = []
        king = None
        for piece in pieces_to_check:
            if piece.piece_type == "king":
                king_pos = piece.position_on_the_board
                king = piece
        
        if not len(king.get_possible_moves()) == 0: # king can move
            return False

        # check if there is another piece which can save the king.
        opponent_piece_which_is_threatening_king = None
        for piece in opponent_pieces:
            if king_pos in piece.get_threatened_squares():
                opponent_piece_which_is_threatening_king = piece

        if opponent_piece_which_is_threatening_king.piece_type == "pawn" or opponent_piece_which_is_threatening_king.piece_type == "knight" or opponent_piece_which_is_threatening_king.piece_type == "king":
            return True

        pass

        




    def print_board(self): 
        letters = ["A","B","C","D","E","F","G","H"]

        print("  ",end="")
        for letter in letters:
            print(" " + letter, end="")
        print()

        for index_for_row, row in enumerate(self.board):
            print(index_for_row + 1, end=" ")
            for index_for_col, col in enumerate(row):
                if not col["piece"] == "None":
                #    print("|" + col["color"][0] + col["piece"][0].upper(), end="")
                    print("|" + chess_manager.get_piece_display_symbol(index_for_row,index_for_col), end="")
                else:
                    print("| ", end="")
                    #print(" □", end="")
            print("|")

    def square_code_to_row_and_col(self, code_in_string): # e.g. A6
        row = int(code_in_string[1]) - 1
        col = -1
        letters = ["A","B","C","D","E","F","G","H"]

        for index, letter in enumerate(letters):
            if letter == code_in_string[0]:
                col = index

        return [row,col]

    def find_piece_by_position(self, row_to_look, col_to_look):
        all_pieces = self.white_pieces + self.black_pieces

        for piece in all_pieces:
            if piece.position_on_the_board == [row_to_look,col_to_look]:
                return piece

    def move_a_piece_by_code(self, start_code, end_code):
        start_square_pos = self.square_code_to_row_and_col(start_code)
        end_square_pos = self.square_code_to_row_and_col(end_code)

        piece_to_move = self.find_piece_by_position(start_square_pos[0], start_square_pos[1])

        piece_to_move.move(end_square_pos[0], end_square_pos[1])

    def start_the_game(self):
        turn = "white"
        while True:
            self.print_board()
            move = input(turn + "'s turn. Enter your move: ")
            if move[0] in ["A","B","C","D","E","F","G","H"] and int(move[1]) in range(1,9) and move[2] in ["A","B","C","D","E","F","G","H"] and int(move[3]) in range(1,9) and len(move) == 4:
                start_square, end_square = self.square_code_to_row_and_col(move[:2]), self.square_code_to_row_and_col(move[2:])
                piece = self.find_piece_by_position(start_square[0], start_square[1])
                try:
                    if piece.color == turn:
                        if end_square in piece.get_possible_moves():
                            piece.move(end_square[0],end_square[1])
                            if turn == "white":
                                turn = "black"
                            else:
                                turn = "white"
                        else:
                            print("Invalid move.")
                    else:
                        print("Invalid move.")
                except Exception as e:
                    print("Invalid move.")
                    print(e)

            else:
                print("Invalid move.")

class Piece: # Chess Piece
    def __init__(self, placement_row, placement_col, color, piece_type):
        self.position_on_the_board = [placement_row, placement_col] # Shows the position of the piece on the board formatted as [row,column].
        self.piece_type = piece_type
        self.display_symbol = display_icons[color + " " + piece_type]

        chess_manager.board[placement_row][placement_col]["color"] = color
        chess_manager.board[placement_row][placement_col]["piece"] = self.piece_type
        self.color = color

    def set_position(self, new_row, new_col):
        chess_manager.board[self.position_on_the_board[0]][self.position_on_the_board[1]]["color"] = "None"
        chess_manager.board[self.position_on_the_board[0]][self.position_on_the_board[1]]["piece"] = "None" # Delete the old position and make it empty on the board.

        self.position_on_the_board = [new_row, new_col]
        chess_manager.board[new_row][new_col]["color"] = self.color
        chess_manager.board[new_row][new_col]["piece"] = self.piece_type

    def move(self, target_row, target_col):
        if not chess_manager.board[target_row][target_col]["color"] == "None": # Capturing opponent's piece.
            self.capture(target_row, target_col)
            
        self.set_position(target_row, target_col)
            
    def capture(self, target_row, target_col): # Empty the square we are moving and delete the piece we are capturing.
        deleted_piece_index = 0
        if self.color == "white": # we are capturing a black piece.
            for index, piece in enumerate(chess_manager.black_pieces):
                if piece.position_on_the_board == [target_row, target_col]:
                    deleted_piece_index = index
                    break
            del chess_manager.black_pieces[deleted_piece_index]

        if self.color == "black": # we are capturing a white piece.
            for index, piece in enumerate(chess_manager.white_pieces):
                if piece.position_on_the_board == [target_row, target_col]:
                    deleted_piece_index = index
                    break
            del chess_manager.white_pieces[deleted_piece_index]

        chess_manager.empty_square(target_row, target_col)
        
class Pawn(Piece): # Piyon 
    def __init__(self, placement_row, placement_col, color):
        super().__init__(placement_row, placement_col, color, "pawn")

    def get_threatened_squares(self): # Pawn's threating way and moving way is different so we need to check them separately.

        unchecked_threatened_squares = []
        threatened_squares = []
        
        if self.color == "white":
            unchecked_threatened_squares.append([self.position_on_the_board[0] - 1, self.position_on_the_board[1] - 1])
            unchecked_threatened_squares.append([self.position_on_the_board[0] - 1, self.position_on_the_board[1] + 1])

        elif self.color == "black":
            unchecked_threatened_squares.append([self.position_on_the_board[0] + 1, self.position_on_the_board[1] - 1])
            unchecked_threatened_squares.append([self.position_on_the_board[0] + 1, self.position_on_the_board[1] + 1])

        for square in unchecked_threatened_squares:
            if chess_manager.is_a_valid_square(square[0], square[1]):
                threatened_squares.append(square)

        return threatened_squares

    def get_possible_moves(self): # return all possible moves including the threatening squares

        unchecked_possible_moves = []
        possible_moves = []

        if self.color == "white":
            unchecked_possible_moves.append([self.position_on_the_board[0] - 1, self.position_on_the_board[1]])
            if self.position_on_the_board[0] == 6:
                unchecked_possible_moves.append([self.position_on_the_board[0] - 2, self.position_on_the_board[1]])

        elif self.color == "black":
            unchecked_possible_moves.append([self.position_on_the_board[0] + 1, self.position_on_the_board[1]])
            if self.position_on_the_board[0] == 1:
                unchecked_possible_moves.append([self.position_on_the_board[0] + 2, self.position_on_the_board[1]])

        for square in unchecked_possible_moves:
            if chess_manager.is_a_valid_square(square[0], square[1]):
                if chess_manager.board[square[0]][square[1]]["piece"] == "None":
                    if not chess_manager.test_check_in_future_move(self.position_on_the_board[0], self.position_on_the_board[1], square[0], square[1]):
                        possible_moves.append(square)

        for threatened_square in self.get_threatened_squares():
            if not chess_manager.board[threatened_square[0]][threatened_square[1]]["piece"] == "None":
                if not chess_manager.board[threatened_square[0]][threatened_square[1]]["color"] == self.color:
                    if not chess_manager.test_check_in_future_move(self.position_on_the_board[0], self.position_on_the_board[1], threatened_square[0], threatened_square[1]):
                        possible_moves.append(threatened_square) 

        return possible_moves
            
class Bishop(Piece): # Fil 
    def __init__(self, placement_row, placement_col, color):
        super().__init__(placement_row, placement_col, color, "bishop")

    def get_threatened_squares(self):
        threatened_squares = []

        for i in range(4):
            for change_in_row in range(1,8):
                if i % 2 == 0:
                    change_in_col = change_in_row
                else:
                    change_in_col = -change_in_row

                if i >= 2:
                    change_in_row *= -1

                target_row = self.position_on_the_board[0] + change_in_row
                target_col = self.position_on_the_board[1] + change_in_col

                if chess_manager.is_a_valid_square(target_row, target_col):
                    threatened_squares.append([target_row, target_col])

                    if chess_manager.is_a_piece(target_row, target_col):
                        break
        
        return threatened_squares

    def get_possible_moves(self):
        possible_moves = []

        for square in self.get_threatened_squares():
            if not chess_manager.is_a_friendly_piece(self.color, chess_manager.get_piece_color(square[0], square[1])):
                if not chess_manager.test_check_in_future_move(self.position_on_the_board[0], self.position_on_the_board[1], square[0], square[1]):
                    possible_moves.append(square)

        return possible_moves
            
class Knight(Piece): # At 
    def __init__(self, placement_row, placement_col, color):
        super().__init__(placement_row, placement_col, color, "knight",)

    def get_threatened_squares(self):
        threatened_squares = []
        change_in_row = -2
        change_in_col = -1

        for i in range(8):
            if i % 2 == 0:
                change_in_row *= -1
            change_in_col *= -1

            if i == 4:
                change_in_row, change_in_col = change_in_col, change_in_row
                
            target_row = self.position_on_the_board[0] + change_in_row
            target_col = self.position_on_the_board[1] + change_in_col

            if chess_manager.is_a_valid_square(target_row, target_col):
                threatened_squares.append([target_row, target_col])
                

        return threatened_squares

    def get_possible_moves(self):
        possible_moves = []

        for square in self.get_threatened_squares():
            if not chess_manager.is_a_friendly_piece(self.color, chess_manager.get_piece_color(square[0], square[1])):
                if not chess_manager.test_check_in_future_move(self.position_on_the_board[0], self.position_on_the_board[1], square[0], square[1]):
                    possible_moves.append(square)

        return possible_moves

class Rook(Piece): # Kale 
    def __init__(self, placement_row, placement_col, color):
        super().__init__(placement_row, placement_col, color, "rook")

    def get_threatened_squares(self):
        threatened_squares = []
    
        for i in range(4):
            for change_in_row in range(1,8):
                if not i % 2 == 0:
                    change_in_row *= -1

                if i <= 1:
                    target_row = self.position_on_the_board[0]
                    target_col = self.position_on_the_board[1] + change_in_row
                else:
                    target_row = self.position_on_the_board[0] + change_in_row
                    target_col = self.position_on_the_board[1]

                if chess_manager.is_a_valid_square(target_row, target_col):
                    threatened_squares.append([target_row, target_col])

                    if chess_manager.is_a_piece(target_row, target_col):
                        break
        
        return threatened_squares
                
    def get_possible_moves(self):
        possible_moves = []

        for square in self.get_threatened_squares():
            if not chess_manager.is_a_friendly_piece(self.color, chess_manager.get_piece_color(square[0], square[1])):
                if not chess_manager.test_check_in_future_move(self.position_on_the_board[0], self.position_on_the_board[1], square[0], square[1]):
                    possible_moves.append(square)

        return possible_moves

class Queen(Piece): # Vezir 
    def __init__(self, placement_row, placement_col, color):
        super().__init__(placement_row, placement_col, color, "queen")

    def get_threatened_squares(self):
        threatened_squares = []
    
        for i in range(4):
            for change_in_row in range(1,8):
                if not i % 2 == 0:
                    change_in_row *= -1

                if i <= 1:
                    target_row = self.position_on_the_board[0]
                    target_col = self.position_on_the_board[1] + change_in_row
                else:
                    target_row = self.position_on_the_board[0] + change_in_row
                    target_col = self.position_on_the_board[1]

                if chess_manager.is_a_valid_square(target_row, target_col):
                    threatened_squares.append([target_row, target_col])

                    if chess_manager.is_a_piece(target_row, target_col):
                        break

        for i in range(4):
            for change_in_row in range(1,8):
                if i % 2 == 0:
                    change_in_col = change_in_row
                else:
                    change_in_col = -change_in_row

                if i >= 2:
                    change_in_row *= -1

                target_row = self.position_on_the_board[0] + change_in_row
                target_col = self.position_on_the_board[1] + change_in_col

                if chess_manager.is_a_valid_square(target_row, target_col):
                    threatened_squares.append([target_row, target_col])

                    if chess_manager.is_a_piece(target_row, target_col):
                        break
        
        return threatened_squares

    def get_possible_moves(self):
        possible_moves = []

        for square in self.get_threatened_squares():
            if not chess_manager.is_a_friendly_piece(self.color, chess_manager.get_piece_color(square[0], square[1])):
                if not chess_manager.test_check_in_future_move(self.position_on_the_board[0], self.position_on_the_board[1], square[0], square[1]):
                    possible_moves.append(square)

        return possible_moves

class King(Piece): # Şah 
    def __init__(self, placement_row, placement_col, color):
        super().__init__(placement_row, placement_col, color, "king")

    def get_threatened_squares(self):
        threatened_squares = []
        for change_in_row in range(-1,2):
            for change_in_col in range(-1,2):
                if not change_in_row == 0 and not change_in_col == 0:
                    
                    target_row = self.position_on_the_board[0] + change_in_row
                    target_col = self.position_on_the_board[1] + change_in_col
                    
                    if chess_manager.is_a_valid_square(target_row, target_col):
                        threatened_squares.append([target_row, target_col])

        return threatened_squares

    def get_possible_moves(self): 
        possible_moves = []

        for square in self.get_threatened_squares():
            if not chess_manager.is_a_friendly_piece(self.color, chess_manager.get_piece_color(square[0], square[1])):
                if not chess_manager.is_square_threatened(square[0], square[1], self.color): # Hamle yaptığı kare tehdit altında mı kontrol edilmeli, şaha özel durum.
                    possible_moves.append(square)

        return possible_moves

chess_manager = ChessManager()

for col in range(8): # Defining pawns of both sides.
    chess_manager.white_pieces.append(Pawn(6, col, "white"))
    chess_manager.black_pieces.append(Pawn(1, col, "black"))

# Defining bishops of both sides.
chess_manager.white_pieces.append(Bishop(7, 2, "white"))
chess_manager.white_pieces.append(Bishop(7, 5, "white"))
chess_manager.black_pieces.append(Bishop(0, 2, "black"))
chess_manager.black_pieces.append(Bishop(0, 5, "black"))

# Defining knights of both sides.
chess_manager.white_pieces.append(Knight(7, 1, "white"))
chess_manager.white_pieces.append(Knight(7, 6, "white"))
chess_manager.black_pieces.append(Knight(0, 1, "black"))
chess_manager.black_pieces.append(Knight(0, 6, "black"))

# Defining rooks of both sides.
chess_manager.white_pieces.append(Rook(7, 0, "white"))
chess_manager.white_pieces.append(Rook(7, 7, "white"))
chess_manager.black_pieces.append(Rook(0, 0, "black"))
chess_manager.black_pieces.append(Rook(0, 7, "black"))

# Defining queens of both sides.
chess_manager.white_pieces.append(Queen(7, 3, "white"))
chess_manager.black_pieces.append(Queen(0, 3, "black"))

# Defining kings of both sides.
chess_manager.white_pieces.append(King(7, 4, "white"))
chess_manager.black_pieces.append(King(0, 4, "black"))

chess_manager.start_the_game() # black pieces on the top, white pieces on the bottom by default







