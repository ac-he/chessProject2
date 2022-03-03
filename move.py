import pieces
import game
from piece_movement import validate

Move = {}
feedback = ""
success = False

# move_from move_to turn
def new_move(move_from, move_to, turn, Board):
    global Move
    Move = {"move from": move_from, "move to": move_to}
    mt_str = move_to.get("coord") + move_to.get("piece").get("label")
    mf_str = move_from.get("coord") + move_from.get("piece").get("label")

    set_was_unsuccessful()
    clear_feedback()
    # move not valid
    if not validate(move_from, move_to, Board):
        set_was_unsuccessful()
        set_feedback("Not a valid move!")
    # happy case
    else:
        set_was_successful()
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


def set_feedback(str):
    global feedback
    feedback = feedback + str
    return feedback


def clear_feedback():
    global feedback
    feedback = ""
    return feedback


def get_most_recent_feedback():
    global feedback
    return feedback
