import pieces


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


def isOnOtherTeam(spot, king_color):
    # if the king's piece color is not the same as the spots team color
    # then its on the opposite team
    if king_color == spot.get("piece").get("piece color"):
        return False
    return True


def canPawnKillMe(move_from, move_to, board):
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


def canKillKing(board, spot, king_x, king_y, king_color):
    # killing works a lil different for a pawn, they kill sideways not by norm move
    # if spot is a pawn
    if spot.get("piece").get("name") == "pawn":
        if canPawnKillMe(spot, board[king_x][king_y], board):
            return True
    else:
        # if spot curPosition is valid to move to King cur position, return True
        if validate(spot, board[king_x][king_y], board):
            return True
    return False


def am_I_putting_myself_in_check(board, mf_rank, mf_file, mt_rank, mt_file):
    if board[mf_file][mf_rank].get("piece").get("name") != "king":
        board[mf_rank][mf_file].get("piece").get("name")
        # print("here")
        return False
    # let's assume the King moved to see if he would be in danger there
    king_x = mt_file
    king_y = mt_rank
    king_color = board[mf_file][mf_rank].get("piece").get("piece color")
    # y is 1   x is 4
    # scan the other teams pieces to see if they could kill our King
    for row in board:
        for spot in row:
            if isOnOtherTeam(spot, king_color):
                if canKillKing(board, spot, king_x, king_y, king_color):
                    return True
    # print("passed fforr")
    return False


def am_I_putting_my_king_in_check(board, move_from, move_to):
    print(str(move_to))
    # rank is x
    # file is y
    y = move_from.get("rank")
    x = move_from.get("file")
    cur_color = move_from.get("piece").get("piece color")
    # print(cur_color)

    if board[x][y].get("piece").get("name") == "king":
        return False

    hypothetical_board = board
    move_to["piece"] = move_from["piece"]
    move_to["piece"] = pieces.get_empty_piece()

    # find the current king
    for rank in range(1, 9):
        for file in range(1, 9):
            if hypothetical_board[rank][file]["piece"]["label"] != "_":
                if hypothetical_board[rank][file]["piece"]["name"] == "king" and \
                        hypothetical_board[rank][file]["piece"]["piece color"] == cur_color:
                    king_rank = rank
                    king_file = file
                    # print(king_rank)
                    # print(king_file)
                    check = am_I_putting_myself_in_check(hypothetical_board, king_rank, king_file, king_rank, king_file)
                    # print(check)
                    return check
    print(str(move_to))
    return False
