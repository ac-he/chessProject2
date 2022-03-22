import pieces
import game
from piece_movement import validate, putting_myself_in_check, is_enemy_in_check, is_enemy_in_checkmate


Move = {}
feedback = ""
success = False
whiteInCheckmate = False
blackInCheckmate = False


def get_tile_formatted_text(tile):
    name = str(tile.get("piece").get("label"))
    ret_str = str(tile.get("coord"))
    if name != "_":
        ret_str = name + " at " + ret_str
    return ret_str


def new_move(move_from, move_to, board):
    global Move
    Move = {"move from": move_from, "move to": move_to}
    print(move_from)
    print(move_to)

    mt_str = get_tile_formatted_text(move_to)
    mf_str = get_tile_formatted_text(move_from)

    captured = False
    if move_to.get("piece").get("label") != "_":
        captured = True

    mt_rank = move_to.get("rank")
    mt_file = move_to.get("file")
    mf_rank = move_from.get("rank")

    mf_file = move_from.get("file")
    set_was_unsuccessful()
    clear_feedback()

    # Tried to capture another piece of the same color
    if move_from.get("piece").get("piece color") == move_to.get("piece").get("piece color"):
        set_was_unsuccessful()
        set_feedback("Cannot capture a piece you already own!")

    # Move not valid according to rules in piece_movement.py
    elif not validate(move_from, move_to, board):
        set_was_unsuccessful()
        set_feedback("Not a valid move!")

    # are you moving such that you would immediately be in check?
    elif putting_myself_in_check(board, mf_rank, mf_file, mt_rank, mt_file):
        set_was_unsuccessful()
        set_feedback("This move places your king in check!")
    else:
        set_was_successful()
        if captured:
            set_feedback("Captured " + mt_str + " with " + mf_str + ".")
        else:
            set_feedback("Moved " + mf_str + " to " + mt_str + ".")

    return get_most_recent_move_successful()


def get_most_recent_move_successful():
    global success
    return success


def set_was_successful():
    global success
    success = True
    return success


def set_was_unsuccessful():
    global success
    success = False
    return success


def set_feedback(fstr):
    global feedback
    feedback = feedback + fstr
    return feedback


def clear_feedback():
    global feedback
    feedback = ""
    return feedback


def get_most_recent_feedback():
    global feedback
    return feedback
