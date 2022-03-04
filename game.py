import move
import pieces
from piece_movement import validate


def create_board():
    """

    :return:
    """
    board = []
    rows, cols = (10, 10)
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(pieces.make_tile(i, j))
        board.append(col)

    return board


Board = create_board()


def get_opposite_color(string):
    return_color = " "
    if string == "white":
        return_color = "black"
    elif string == "black":
        return_color = "white"
    return return_color


def switch_turns():
    global turn
    turn = get_opposite_color(turn)
    return turn


def get_game_board():
    # for r in Board:
        # for f in r:
            # print(f["coord"], end="")
            # if f["tile class"] == "whiteSelected" or f["tile class"] == "blackSelected":
            #    print("s", end="")
            # print(f["piece"]["label"], end=" ")
        # print()
    return Board


def get_tile_formatted_text(tile):
    name = str(tile.get("piece").get("label"))
    ret_str = str(tile.get("coord"))
    if name != "_":
        ret_str = name + " at " + ret_str
    return ret_str


turn = ""


def create_turn():
    global turn
    turn = "white"
    return turn


def get_cur_turn():
    return turn


def clear_click():
    return {"tile class": "none", "coord": "none", "rank": -1, "file": -1}


move_to = clear_click()
move_from = clear_click()

selected = "background-color: #990"
unselected = ""


def react_to(rank, file):
    global move_to, move_from, Board, selected, unselected
    clicked_tile = Board[rank][file]
    ret_str = ""

    if move_from == clicked_tile: #Same tile clicked: cleared
        move_from = clear_click()
        ret_str = "Move cleared."
        Board[rank][file]["selected color"] = unselected
    # If team tries to go when not their turn
    elif pieces.if_selected_piece_has_color(clicked_tile) and clicked_tile.get("piece").get("piece color") \
            != get_cur_turn() and move_from == clear_click():
        move_from = clear_click()
        ret_str = "It's not your turn!"
        # If user tries to select an empty space
    elif clicked_tile.get("piece").get("label") == "_" and move_from == clear_click():
        move_from = clear_click()
        ret_str = "Cannot select an empty space!"
    # Select a piece!
    elif move_from.get("tile class") == "none":
        move_from = clicked_tile
        ret_str = "Selected " + move_from.get("piece").get("label") + " at " + pieces.get_coord_str(rank, file) + "."
        Board[rank][file]["selected color"] = selected
    # Try to move!
    else:
        move_to = clicked_tile
        move_from_rank = move_from.get("rank")
        move_from_file = move_from.get("file")

        move.new_move(move_from, move_to, Board)

        if move.get_most_recent_move_successful():
            Board[rank][file]["piece"] = move_from.get("piece")
            Board[move_from_rank][move_from_file]["piece"] = pieces.get_empty_piece()

            move_from = clear_click()
            switch_turns()
        else:
            move_from = clear_click()

        Board[rank][file]["selected color"] = unselected
        move_to = clear_click()
        ret_str = move.get_most_recent_feedback()

    return ret_str 

