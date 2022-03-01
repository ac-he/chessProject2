def validate(move_from, move_to, board):
    """Validates a hypothetical movement between two specified tiles

    :param move_from: The tile being moved from
    :param move_to: The tile being moved to
    :param board: The board containing these tiles
    :return: True if the change in coordinates is valid for this piece, otherwise false
    """
    ret_bool = False

    # Get information about the given pieces
    name = move_from.get("piece").get("name")
    capturing = False
    if move_to.get("piece").get("label") != " ":
        capturing = True

    mf_rank = move_from.get("rank")
    mf_file = move_from.get("file")
    mt_rank = move_to.get("rank")
    mt_file = move_to.get("file")

    # Reverse if it's advancing from the black side of the board to simplify validation
    if move_from.get("piece").get("piece color") == "black":
        mf_rank = 9 - mf_rank
        mt_rank = 9 - mt_rank

    if name == "pawn":
        ret_bool = is_valid_pawn_movement(capturing, mf_rank, mf_file, mt_rank, mt_file)
    elif name == "rook":
        ret_bool = is_valid_rook_movement(board, mf_rank, mf_file, mt_rank, mt_file)
    elif name == "knight":
        ret_bool = is_valid_knight_movement(board, mf_rank, mf_file, mt_rank, mt_file)
    elif name == "bishop":
        ret_bool = is_valid_bishop_movement(board, mf_rank, mf_file, mt_rank, mt_file)
    elif name == "king":
        ret_bool = is_valid_king_movement(board, mf_rank, mf_file, mt_rank, mt_file)
    elif name == "queen":
        ret_bool = is_valid_queen_movement(board, mf_rank, mf_file, mt_rank, mt_file)

    return ret_bool


def is_valid_pawn_movement(capturing, mf_rank, mf_file, mt_rank, mt_file):
    ret_bool = False
    dif_rank = mt_rank - mf_rank
    dif_file = abs(mt_file - mf_file)

    if capturing:
        if dif_rank == 1 and dif_file == 1:
            ret_bool = True
    else:
        if dif_file == 0:
            if mf_rank == 2 and dif_rank <= 2:
                ret_bool = True
            elif dif_rank == 1:
                ret_bool = True

    return ret_bool


def is_valid_rook_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    return False


def is_valid_knight_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    return False


def is_valid_bishop_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    dif_rank = mt_rank - mf_rank
    dif_file = mt_file - mf_file
    if dif_rank == 0:
        return True
    elif dif_file == 0:
        return True
    else:
        return False
    return False


def is_valid_king_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    return False


def is_valid_queen_movement(capturing, mf_rank, mf_file, mt_rank, mt_file):
    return False