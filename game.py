import move
import pieces


def create_board():
    board = []
    rows, cols = (10, 10)
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(pieces.make_tile(i, j))
        board.append(col)

    return board


board = create_board()


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
    return board


turn = ""
is_over = False


def create_turn():
    global turn
    turn = "white"
    return turn


def get_cur_turn():
    global turn
    return turn


def clear_click():
    return {"tile class": "none", "coord": "none", "rank": -1, "file": -1}


def get_is_over():
    global is_over
    return is_over


def set_is_over(over):
    global is_over
    is_over = over
    return is_over


move_to = clear_click()
move_from = clear_click()

selected = "background-color: #ff7"
unselected = ""


def react_to(rank, file):
    global move_to, move_from, board, selected, unselected
    clicked_tile = board[rank][file]
    clicked_tile_is_empty = clicked_tile.get("piece").get("label") == "_"
    ret_str = ""

    if move_from == clicked_tile:  # Same tile clicked: cleared
        move_from = clear_click()
        ret_str = "Move cleared."
        board[rank][file]["selected class"] = unselected
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
        board[rank][file]["selected class"] = selected

    # Try to move!
    else:
        move_to = clicked_tile
        move_from_rank = move_from.get("rank")
        move_from_file = move_from.get("file")

        move.new_move(move_from, move_to, board)

        can_move = move.get_most_recent_move_successful()
        if can_move:
            if not clicked_tile_is_empty:
                is_king = board[rank][file]["piece"]["name"] == "king"

                if is_king:
                    set_is_over(True)

            board[rank][file]["piece"] = move_from.get("piece")
            board[move_from_rank][move_from_file]["piece"] = pieces.get_empty_piece()

            move_from = clear_click()
            switch_turns()
        else:
            move_from = clear_click()

        board[move_from_rank][move_from_file]["selected class"] = unselected
        move_to = clear_click()
        ret_str = move.get_most_recent_feedback()

    return ret_str


def reset_game():
    global move_to, move_from, board
    move_to = clear_click()
    move_from = clear_click()
    board = create_board()
    create_turn()
    set_is_over(False)
    return
