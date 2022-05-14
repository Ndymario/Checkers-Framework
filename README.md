# Ndy's Checkers Framework
The classic game of checkers, written entirely from scratch!

## Why checkers?
Checkers is a simple and fun game, meaning it's a good base for all sorts of things.

## Framework? What's that about?
Just a fancy way for me to say that this was programmed with flexibility in mind. 

- There are *no* mandatory external dependencies beyond the standard Python libraries.
  - The only external dependency that is in this program is tabulate, which is only for rendering the board in your terminal and is not needed for any core functionality.

## List of Classes
Here's a breakdown of what you'll find in this framework:

- Checker()
  - The playing piece of the game
  - Information is stored in the format "KCXXXXYYYY"
    - K: 0 for regular piece, 1 for king piece
    - C: 0 for red, 1 for black
    - X: Column the piece is on from 0 to 15 (in binary)
    - Y: Row the piece is on from 0 to 15 (in binary)
  - Methods
    - is_king(): Returns True if this piece is a King, returns False if not
    - get_color(): Returns a string describing what color the piece is; Red or Black
    - get_x_pos(): Returns the X-Position of the piece as an int
    - get_y_pos(): Returns the X-Position of the piece as an int

- CheckerBoard()
  - The playing area of the game, keeps track of the pieces
    - width: How wide the board is (range of 3-16), x_pos refers to the location horizontally
    - height: How tall the board is (range of 3-16), y-pos refers to the location vertically
      - Coordinates begin, or (0, 0), at the top left of the board
    - pieces: Array of all pieces on the board
  - Methods
    - generate_board(): Generate the starting layout based off of the size of the board
    - add_piece(): Takes a Checker as a parameter and adds it to the pieces array
    - remove_piece(): Takes a Checker as a parameter and removes it from the pieces array
    - red_check(): Takes in a row and column number as parameters and determines if that square is red
    - get_number_of_pieces(): Returns the number of pieces in the pieces array

- CheckerEngine()
  - The heart of the game, contains all game logic
    - board: The current game board
    - turn: The current turn, 0 for black's turn and 1 for red's 
      - [TODO] - Add logic to prevent players from going out of order
  - Methods
    - create_game(): Returns a CheckerBoard to initialize the engine with
    - movement_check(): Takes in a Checker and XXXXYYYY to determine if the passed move is legal
    - move(): Takes in a Checker and XXXXYYYY, if the move is legal the method will update the pieces accordingly
