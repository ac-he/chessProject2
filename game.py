import copy
import move
import pieces
from piece_movement import is_enemy_in_checkmate


# ----------- Board -----------


def create_board():
    """Creates a blank board and makes each individual tile
    :returns created board"""

    board = []
    rows, cols = (10, 10)
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(pieces.make_tile(i, j))
        board.append(col)

    return board


# create global board variable
board = create_board()


def get_game_board():
    """Getter method for the game board
    :returns current state of the board"""
    return board


# ----------- Turns -----------


def get_opposite_color(string: str) -> str:
    """Finds the color opposite of the one provided
    'white' -> 'black', 'black' -> 'white', 'anything else' -> ' '
    """
    return_color = " "
    if string == "white":
        return_color = "black"
    elif string == "black":
        return_color = "white"
    return return_color


def switch_turns() -> str:
    """Switches to the turn 'opposite' of the current turn
    :returns the turn that was switched to"""
    global turn
    turn = get_opposite_color(turn)
    return turn


turn = ""  # create global variable to track the current player/whose turn it is


def create_turn() -> str:
    """Sets up the initial turn"""
    global turn
    turn = "white"
    return turn


def get_cur_turn() -> str:
    """Getter method to return the current turn"""
    global turn
    return turn


def clear_click() -> dict:
    """Returns a cleared tile with no class, coordinates, or location"""
    return {"tile class": "none", "coord": "none", "rank": -1, "file": -1}


# ----------- Game ending -----------


is_over = False  # create global variable to track if the game is over


def get_is_over() -> bool:
    """Returns true if the game is over, false if game is in progress"""
    global is_over
    return is_over


def set_is_over(over: bool) -> bool:
    global is_over
    is_over = over
    return is_over


# ----------- Styling the selected tile -----------


selected = "background-color: #ff7"  # Define selected style as an html string
unselected = "" # No style for a tile which is unselected


def unselect(tile: dict) -> dict:
    """Change a provided tile's 'selected class' attribute to be unselected, then return the updated tile"""
    tile["selected class"] = unselected
    print(str(tile))
    return tile


def select(tile):
    """Change a provided tile's 'selected class' attribute to be selected, then return the updated tile"""
    tile["selected class"] = selected
    print(str(tile))
    return tile


# ----------- Interpreting a click on the board -----------


# create global variables to track the most recently clicked tiles
move_from = clear_click()
move_to = clear_click()


def react_to(rank: int, file: int) -> str:
    """Handle input from a specified (rank, file) location and change global game state variables accordingly
    :returns string with feedback for the player with a summary of their most recent move and its impact"""

    global move_to, move_from, board

    # Find the tile at the specified location
    clicked_tile = board[rank][file]
    clicked_tile_is_empty = clicked_tile.get("piece").get("label") == "_"

    # Create return string to be filled in later
    ret_str = ""

    if move_from == clicked_tile:  # Same tile clicked: cleared
        move_from = clear_click()
        ret_str = "Move cleared."
        board[rank][file] = unselect(clicked_tile)

    # If team tries to go when not their turn
    elif pieces.if_selected_piece_has_color(clicked_tile) and clicked_tile.get("piece").get("piece color") \
            != get_cur_turn() and move_from == clear_click():
        move_from = clear_click()
        ret_str = "It's not your turn!"

    # If user tries to select an empty space
    elif clicked_tile_is_empty and move_from == clear_click():
        move_from = clear_click()
        ret_str = "Cannot select an empty space!"

    # Select a piece!
    elif move_from.get("tile class") == "none":
        move_from = clicked_tile
        ret_str = "Selected " + move.get_tile_formatted_text(move_from) + "."
        board[rank][file] = select(clicked_tile)

    # Try to move!
    else:
        # The clicked tile is the tile being moved to
        move_to = clicked_tile
        move_from_rank = move_from.get("rank")
        move_from_file = move_from.get("file")

        # Try this movement to see if it worked
        move.new_move(move_from, move_to, board)
        can_move = move.get_most_recent_move_successful()

        if can_move:  # move is successful
            # If this somehow managed to capture the king, the game is over
            # Note: this should not happen with checkmate stuff currently in place
            if not clicked_tile_is_empty:
                is_king = board[rank][file]["piece"]["name"] == "king"
                if is_king:
                    set_is_over(True)

            # if after a successful move, check if the other team is in checkmate
            hypothetical_board = copy.deepcopy(board)
            hypothetical_board[rank][file]["piece"] = move_from.get("piece")
            hypothetical_board[move_from_rank][move_from_file]["piece"] = pieces.get_empty_piece()

            if is_enemy_in_checkmate(hypothetical_board, get_opposite_color(get_cur_turn())):
                set_is_over(True)

            # Figure out if this move allows a pawn to be promoted and trigger promotion actions if necessary
            to_promotable_space = (get_cur_turn() == "black" and rank == 1) or (get_cur_turn() == "white" and rank == 8)

            if move_from.get("piece").get("name") == "pawn" and to_promotable_space:
                ret_str = " It must now be promoted."  # Will be added after the normal part of the return string
                set_promotion_happening(True)

                # Select the new location
                board[rank][file] = select(move_to)

            # Clear and unselect the old location, regardless of promotion actions
            board[rank][file]["piece"] = move_from.get("piece")
            board[move_from_rank][move_from_file]["piece"] = pieces.get_empty_piece()
            board[move_from_rank][move_from_file] = unselect(move_from)
            move_from = clear_click()

            # Switch turns if not promoting
            if not promotion_happening:
                switch_turns()

        else:  # if move is not successful

            # Clear whatever move was tried since it did not work
            board[move_from_rank][move_from_file] = unselect(move_from)
            move_from = clear_click()

        # Clear whatever move was tried, unless it is still needed for promotion
        if not promotion_happening:
            move_to = clear_click()

        # update the return string
        ret_str = move.get_most_recent_feedback() + ret_str

    # return, used by every branch of the if statement
    return ret_str


# ----------- Promotion -----------


promotion_happening = False  # create global variable to track if the game is in a state requiring promotion


def set_promotion_happening(value: bool) -> bool:
    """Set to true if entering a promotion state, false if leaving a promotion state"""
    global promotion_happening
    promotion_happening = value
    return promotion_happening


def get_promotion_info():
    """Returns a tuple with promotion information.
    First element is a bool, true if promotion is happening, otherwise false
    Second element is an array, populated with promotion options unless promotion is not happening"""
    global promotion_happening
    if promotion_happening:
        promotion_options = copy.deepcopy(pieces.get_promotion_options(get_cur_turn()))
    else:
        promotion_options = []
    return promotion_happening, promotion_options


def promote_to(name: str) -> str:
    """Promotes piece move_to to a specified type of piece"""
    global move_to
    pieces.promote_at_tile(move_to, name)
    ret_str = "Pawn was moved to " + move_to.get('coord') + " and was promoted to " + name + "."

    # Stop promotion
    set_promotion_happening(False)

    # Unselect everything and clear out turn data, then switch turns
    board[move_to["rank"]][move_to["file"]] = unselect(move_to)
    move_to = clear_click()
    switch_turns()

    return ret_str


# ----------- Reset or Initialize -----------


def reset_game():
    """Set all the global variables in game.py to their starting values to start or re-start a game"""
    global move_to, move_from, board
    move_to = clear_click()
    move_from = clear_click()
    board = create_board()
    create_turn()
    set_promotion_happening(False)
    set_is_over(False)
    return
