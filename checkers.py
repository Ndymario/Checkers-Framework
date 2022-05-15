############################################
# A "simple" game of checkers by Nolan Y.  #
############################################

from tabulate import tabulate
from math import floor

# Verbose will print any errors to the console, specifically for when a move is not legal
VERBOSE = True

'''
Trying to over-engineer this, the data for each checker is stored in this format:

KCXXXXYYYY

K: 0 for regular piece, 1 for kinged piece
C: 0 for red, 1 for black
X: Column the piece is on from 0 to 15 (in binary)
Y: Row the piece is on from 0 to 15 (in binary)
'''

class Checker():
    def __init__(self, king: bool, is_red: bool, x_pos: int, y_pos: int) -> None:
        # Make sure the width is in the range 0-15
        if x_pos > 15:
            x_pos = 15
        if x_pos < 0:
            x_pos = 0
        
        # Make sure the width is in the range 0-15
        if y_pos > 15:
            y_pos = 15
        if y_pos < 0:
            y_pos = 0
            
        self.data = (king<<9) | (is_red<<8) | (x_pos<<4) | (y_pos)
        
    def is_king(self):
        if ((self.data & 0b1000000000)>>9) == 1:
            return True
        else:
            return False
    
    def get_color(self):
        if ((self.data & 0b0100000000)>>8) == 1:
            return "Red"
        else:
            return "Black"
    
    def get_x_pos(self):
        return ((self.data & 0b0011110000)>>4)
    
    def get_y_pos(self):
        return (self.data & 0b0000001111)
        
    def __str__(self):
        return f"King: {self.is_king()} | Color: {self.get_color()} | X-Pos: {self.get_x_pos()} | Y-Pos: {self.get_y_pos()}"

# Standard size is 8x8, supports up to 16x16 if you really want a strange game of checkers
# Minimum size is 3x3 in order to actually be playable
class CheckerBoard():
    def __init__(self, width: int = 8, height: int = 8) -> None:
        # Make sure the width is in the range 3-16
        if width > 16:
            width = 16
        if width < 3:
            width = 3

        self.width = width
        
        # Make sure the height is in the range 3-16
        if height > 16:
            height = 16
        if height < 3:
            height = 3

        self.height = height
            
        self.pieces = []
        
        # Generate the game board to finalize initalization
        self.generate_board()
        
    # Function that generates the board based off of its width & height
    def generate_board(self):
        
        # Determine how many rows of checkers should be generated
        if self.height % 2 == 0:
            rows_to_generate = floor((self.height - 1)/2)
        else:
            rows_to_generate = floor(self.height/2)
            
        # Generate the pieces, don't place a piece on a "red" square
        current_row = 0
        while (current_row < rows_to_generate):
            for column in range (self.width):
                # First, the top half of the board
                if not self.red_check(current_row, column):
                    self.add_piece(Checker(False, False, column, current_row))
                    
                # Next, the bottom half of the board
                if not self.red_check((self.height - current_row - 1), column):
                    self.add_piece(Checker(False, True, column, (self.height - current_row - 1)))
                    
            current_row += 1

    def add_piece(self, piece: Checker):
        self.pieces.append(piece)

    def remove_piece(self, piece: Checker):
        self.pieces.remove(piece)
        
    def red_check(self, row: int, column: int):
        if (row + column) % 2 == 0:
            return False
        else:
            return True
        
    def get_number_of_pieces(self):
        return len(self.pieces)


'''
The rules of checkers:

1) Movement
    a. Checkers can only move to black squares
    b. Checkers can only move diagonally
    c. Checkers can only move forwards when it is not a king

2) Jumping
    a. Checkers can only jump forwards when it is not a king
    b. Checkers can only jump a piece if there is a square behind the piece being jumped
    c. Checkers can only jump a piece if the square behind it is not occupied
    d. Checkers must jump if a jump is available
    e. Checkers can not jump over a Checker of the same color

3) Kings
    a. Checkers are promoted to king when the checker reaches the other end of the board
    b. Kings are allowed to move in any direction
    c. Kings are allowed to jump in any direction if the jump is legal
    
4) Ending the Game
    a. When all of the opponent's pieces are captured you win
    b. If there are no legal moves available the game ends in a draw
'''

class CheckerEngine():
    def __init__(self, width:int = 8, height:int = 8) -> None:
        self.board = self.create_game(width, height)
        self.turn = 0

    def create_game(self, width: int, height: int):
        return CheckerBoard(width, height)
    
    '''
    Function that returns a tuple: (L, J, P)
        (bool) L - Is the passed move legal from the given piece
        (bool) J - Is the passed move a jump from the given piece
        (Checker) P - Piece that would be jumped if the jump was legal. None if the move was not a jump or if the piece that would be jumped is the same color as the piece performing the jump.
    
    move is the x-pos & y-pos, in the form XXXXYYYY of the move attempting to be made.
    
    Note that king promotions are handled in this function
    '''
    def movement_check(self, moving_piece: Checker, move: int):
        global VERBOSE
        move_is_jump = False
        jumped_piece = None
        
        # First, make sure the move passed is a valid move to parse
        if (move < 0) or (move > 255):
            if VERBOSE:
                print("Invalid move parameter")
            return (False, move_is_jump, jumped_piece)
        
        '''
        Basic Movement Logic
        '''
        # Now, make sure the move is on the board
            # Checking X
        if ((move >> 4) >= self.board.width):
            if VERBOSE:
                print("Illegal move: Move is not on the grid")
            return (False, move_is_jump, jumped_piece)
            
            # Checking Y
        if ((move & 0b00001111) >= self.board.height):
            if VERBOSE:
                print("Illegal move: Move is not on the grid")
            return (False, move_is_jump, jumped_piece)
        
        # Now, make sure the move is not to a red square
        if self.board.red_check((move & 0b00001111), (move >> 4)):
            if VERBOSE:
                print("Illegal move: Checkers can only move to Black Squares")
            return (False, move_is_jump, jumped_piece)
        
        # Now, check if the move is diagonal
        if (moving_piece.get_x_pos() == (move >> 4)) or (moving_piece.get_y_pos() == (move & 0b00001111)):
            if VERBOSE:
                print("Illegal move: Checkers can only move Diagonally")
            return (False, move_is_jump, jumped_piece)
        
        # Now, check if the move is going backwards for a Black piece
        if (moving_piece.get_y_pos() >= (move & 0b00001111)) and (moving_piece.is_king() == False) and (moving_piece.get_color() == "Black"):
            if VERBOSE:
                print("Illegal move: Checkers that have not been promoted to King can not move backwards")
            return (False, move_is_jump, jumped_piece)
        
        # Now, check if the move is going backwards for a Red piece
        if (moving_piece.get_y_pos() <= (move & 0b00001111)) and (moving_piece.is_king() == False) and (moving_piece.get_color() == "Red"):
            if VERBOSE:
                print("Illegal move: Checkers that have not been promoted to King can not move backwards")
            return (False, move_is_jump, jumped_piece)
        
        # Now, check if the square is occupied
        for piece in self.board.pieces:
            if (piece.get_x_pos() == (move >> 4)) and (piece.get_y_pos() == (move & 0b00001111)):
                if VERBOSE:
                    print("Illegal move: Checkers can not move to an occupied square")
                return (False, move_is_jump, jumped_piece)
        
        '''
        Jumping Logic
        '''
        # Determine if the move is attempting to be a jump
        if (moving_piece.get_x_pos() > ((move >> 4) + 1)) or (moving_piece.get_x_pos() < ((move >> 4) - 1)):
            move_is_jump = True
            
        if move_is_jump:
            
            # Now, check if the jump is going backwards for a Black piece
            if (moving_piece.get_y_pos() >= (move & 0b00001111)) and (moving_piece.is_king() == False) and (moving_piece.get_color() == "Black"):
                if VERBOSE:
                    print("Illegal move: Checkers that have not been promoted to King can not jump backwards")
                return (False, move_is_jump, jumped_piece)
            
            # Now, check if the move is going backwards for a Red piece
            if (moving_piece.get_y_pos() <= (move & 0b00001111)) and (moving_piece.is_king() == False) and (moving_piece.get_color() == "Red"):
                if VERBOSE:
                    print("Illegal move: Checkers that have not been promoted to King can not jump backwards")
                return (False, move_is_jump, jumped_piece)
            
            # Now, check if the piece being jumped over is the same color of the piece making the jump
            for piece in self.board.pieces:
                if (piece.get_x_pos() == ((move >> 4) + 1)) and (piece.get_y_pos() == ((move & 0b00001111) + 1)):
                    if piece.get_color() == moving_piece.get_color():
                        if VERBOSE:
                            print("Illegal move: Checkers can not jump oveer Checkers of their own color")
                        return (False, move_is_jump, jumped_piece)
                        
                    else:
                        jumped_piece = piece
                    
                if (piece.get_x_pos() == ((move >> 4) - 1)) and (piece.get_y_pos() == ((move & 0b00001111) - 1)):
                    if piece.get_color() == moving_piece.get_color():
                        if VERBOSE:
                            print("Illegal move: Checkers can not jump oveer Checkers of their own color")
                        return (False, move_is_jump, jumped_piece)
                    
                    else:
                        jumped_piece = piece
        
        '''
        King Logic
        '''
        # Promote the piece if it reaches the other end of the board
        if moving_piece.get_color() == "Red":
            if (move & 0b00001111) == 0:
                moving_piece.data = (moving_piece.data | 0b1000000000)
        
        else:
            if ((move & 0b00001111) == (self.board.height - 1)):
                moving_piece.data = (moving_piece.data | 0b1000000000)
            
        # If this step is reached, the move should be valid!
        return (True, move_is_jump, jumped_piece)
            
    def move(self, moving_piece: Checker, move: int):
        (was_legal, was_jump, jumped_piece) = self.movement_check(moving_piece, move)
        
        # If the move was legal, update the piece's information accordingly
        if was_legal:
            # We only care about updating the pos, so we preserve the king status and color
            temp_data = moving_piece.data >> 8
            final_data = (temp_data << 8) | (move)
            moving_piece.data = final_data
            
        if was_jump and (jumped_piece != None):
            self.board.pieces.remove(jumped_piece)
            
        return f"Was Legal: {was_legal}\t\t\tWas Jump: {was_jump}\t\t\tJumped Piece:\n\n{jumped_piece}\n"
    
# Function that generates a visual representation of what the passed board looks like
def render_board(board: CheckerBoard):
    tabulate_array = []
    
    # Append a new list for every row
    for i in range(board.height):
        tabulate_array.append([])
        # Append a new string for each column
        for j in range(board.width):
            tabulate_array[i].append("")
    
    for piece in board.pieces:
        checker = ""
        if piece.get_color() == "Black":
            checker = "B"
        
        if piece.get_color() == "Red":
            checker = "R"
        
        if piece.is_king():
            checker = "K" + checker
            
        tabulate_array[piece.get_y_pos()][piece.get_x_pos()] = tabulate_array[piece.get_y_pos()][piece.get_x_pos()] + " " + checker
        
    return tabulate(tabulate_array, tablefmt="grid")

debug = CheckerEngine(3, 3)

print(render_board(debug.board))