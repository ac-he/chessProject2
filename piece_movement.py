import copy


def validate(move_from, move_to, board):
    """Validates a hypothetical movement of a specified piece between specified coordinates
    :param move_from: The tile being moved from
    :param move_to: The tile being moved to
    :return: True if the change in coordinates is valid for this piece, otherwise false
    """
    ret_bool = False

    # Get information about the given pieces
    name = move_from.get("piece").get("name")
    capturing = False
    if move_to.get("piece").get("label") != "_":
        capturing = True

    mf_rank = move_from.get("rank")
    mf_file = move_from.get("file")
    mt_rank = move_to.get("rank")
    mt_file = move_to.get("file")

    # Reverse if it's advancing from the black side of the board to simplify validation

    if name == "pawn":
        if move_from.get("piece").get("piece color") == "black":
            mf_rank = 9 - mf_rank
            mt_rank = 9 - mt_rank
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
    dif_rank = mt_rank - mf_rank  # I think rank == row and file == col
    dif_file = abs(mt_file - mf_file)

    if capturing:
        if dif_rank == 1 and dif_file == 1:
            ret_bool = True
    else:
        if dif_file == 0:
            if mf_rank == 2 and dif_rank <= 2:  # special first move pawn permissions
                ret_bool = True
            elif dif_rank == 1:  # normal pawn permissions
                ret_bool = True
    return ret_bool


def is_valid_rook_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    dif_rank = mt_rank - mf_rank
    dif_file = mt_file - mf_file
    # verticals
    if dif_file == 0:

        iterate_direction = 1
        if dif_rank < 0:
            iterate_direction = -1

        for i in range(iterate_direction, dif_rank, iterate_direction):
            checking = board[mf_rank + i][mf_file]
            if checking.get("piece").get("label") != "_":
                return False
        return True

    # horizontals
    if dif_rank == 0:

        iterate_direction = 1
        if dif_file < 0:
            iterate_direction = -1

        for i in range(iterate_direction, dif_rank, iterate_direction):
            checking = board[mf_rank][mf_file + i]
            if checking.get("piece").get("label") != "_":
                return False
        return True

    return False


def is_valid_knight_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    # move x right by 2
    # up or down 1
    if mt_file == (mf_file + 2) and 1 == abs(mt_rank - mf_rank):
        return True
    # move x left by 2
    # up or down 1
    if mt_file == (mf_file - 2) and 1 == abs(mt_rank - mf_rank):
        return True
    # move y up 2
    # left or right 1
    if mt_rank == (mf_rank + 2) and 1 == abs(mt_file - mf_file):
        return True
    # move y down 2
    # left or right 1
    if mt_rank == (mf_rank - 2) and 1 == abs(mt_file - mf_file):
        return True

    return False


def is_valid_bishop_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    dif_rank = mt_rank - mf_rank
    dif_file = mt_file - mf_file

    if abs(dif_rank) == abs(dif_file):
        # Assume working in up/right direction
        same_sign = True
        iterate_direction = 1
        if dif_rank < 0:  # if working in down direction
            iterate_direction = -1
            if dif_file > 0:  # if working in right direction
                same_sign = False
        elif dif_file < 0:  # if working in up/left direction
            same_sign = False

        for i in range(iterate_direction, dif_rank, iterate_direction):
            if same_sign:
                checking = board[mf_rank + i][mf_file + i]
            else:
                checking = board[mf_rank + i][mf_file - i]
            if checking.get("piece").get("label") != "_":
                return False
        return True

    return False


def is_valid_king_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    dif_rank = abs(mt_rank - mf_rank)
    dif_file = abs(mt_file - mf_file)

    if dif_rank == 1 and dif_file == 0:
        return True
    if dif_rank == 0 and dif_file == 1:
        return True
    if dif_rank == 1 and dif_file == 1:
        return True
    return False


def is_valid_queen_movement(board, mf_rank, mf_file, mt_rank, mt_file):
    ret_bool = is_valid_bishop_movement(board, mf_rank, mf_file, mt_rank, mt_file)
    if not ret_bool:
        ret_bool = is_valid_rook_movement(board, mf_rank, mf_file, mt_rank, mt_file)
    return ret_bool


def is_on_other_team(spot, color):
    # If the spot is empty
    if spot.get("piece").get("label") == "_":
        return False

    # If they are the same color
    if spot.get("piece").get("piece color") == color:
        return False

    # Otherwise return true
    return True


def pawn_can_kill(move_from, move_to):
    ret_bool = False

    # Get information about the given pieces
    name = move_from.get("piece").get("name")
    capturing = False
    if move_to.get("piece").get("label") != "_":
        capturing = True

    mf_rank = move_from.get("rank")
    mf_file = move_from.get("file")
    mt_rank = move_to.get("rank")
    mt_file = move_to.get("file")

    if move_from.get("piece").get("piece color") == "black":
        mf_rank = 9 - mf_rank
        mt_rank = 9 - mt_rank
    ret_bool = is_valid_pawn_movement(capturing, mf_rank, mf_file, mt_rank, mt_file)

    dif_rank = mt_rank - mf_rank  # I think rank == row and file == col
    dif_file = abs(mt_file - mf_file)
    if dif_rank == 1 and dif_file == 1:
        ret_bool = True

    return ret_bool


def can_kill_king(board, spot, king_x, king_y):
    # if spot is a pawn
    if spot.get("piece").get("name") == "pawn":
        # if pawn puts king in check
        if pawn_can_kill(spot, board[king_x][king_y]):
            return True

    # if this spot's piece puts king in check
    elif validate(spot, board[king_x][king_y], board):
        return True

    # this piece does not put king in check
    return False


def could_other_team_kill_king(board, k_rank, k_file, k_color):
    # scan the other teams pieces to see if they could kill our King
    for rank in range(1, 9):
        for file in range(1, 9):
            if is_on_other_team(board[rank][file], k_color):
                if can_kill_king(board, board[rank][file], k_rank, k_file):
                    print("can kill king from " + board[rank][file]["coord"])
                    return True
    return False


def putting_myself_in_check(board, mf_rank, mf_file, mt_rank, mt_file):
    hypothetical_board = copy.deepcopy(board)

    move_from = hypothetical_board[mf_rank][mf_file]
    cur_color = move_from["piece"]["piece color"]

    hypothetical_board[mt_rank][mt_file]["piece"] = move_from["piece"]
    hypothetical_board[mf_rank][mf_file]["piece"] = {"label": "_"}

    if is_king(board, mf_rank, mf_file):
        loc_king = (mt_rank, mt_file)
    else:
        loc_king = find_king(hypothetical_board, cur_color)

    result = could_other_team_kill_king(hypothetical_board, loc_king[0], loc_king[1], cur_color)
    return result


def is_king(board, rank, file):
    if board[rank][file]["piece"]["label"] != "_":
        if board[rank][file]["piece"]["name"] == "king":
            return True
    return False


def find_king(board, color):
    for rank in range(1, 9):
        for file in range(1, 9):
            if is_king(board, rank, file) and is_cur_color(board, rank, file, color):
                return rank, file


def is_cur_color(board, rank, file, color):
    if board[rank][file]["piece"]["label"] != "_":
        if board[rank][file]["piece"]["piece color"] == color:
            return True
