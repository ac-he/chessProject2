def make_tile(rank, file):
    ret_tile = {"rank": rank, "file" : file}
    if rank == 0 or rank == 9:
        if file == 0 or file == 9:
            ret_tile["tile class"] = "cornerLabel"
        else:
            ret_tile["tile class"] = "rankLabel"
        ret_tile["piece"] = get_rank_label_piece(file)
    elif file == 0 or file == 9:
        ret_tile["tile class"] = "fileLabel"
        ret_tile["piece"] = get_file_label_piece(rank)
    else:
        decide_color = (rank + file) % 2
        decide_color_str = ""
        if decide_color == 0:
            decide_color_str = "white"
            ret_tile["tile class"] = decide_color_str
        else:
            decide_color_str = "black"
            ret_tile["tile class"] = decide_color_str

        if rank == 1:
            ret_tile["piece"] = get_pawn('white')
        elif rank == 2:
            ret_tile["piece"] = get_piece_starting_at_file(file, 'white')
        elif rank == 7:
            ret_tile["piece"] = get_piece_starting_at_file(file, 'black')
        elif rank == 8:
            ret_tile["piece"] = get_pawn('black')
        else:
            ret_tile["piece"] = get_empty_piece()

    return ret_tile



def get_rank_label_piece(file):
    if file == 0 or file == 9:
        return {"label": "x"}
    return {"label": file}


def get_file_label_piece(rank):
    if rank == 0 or rank == 9:
        return {"label": "x"}
    return {"label": rank}


def get_empty_piece():
    return {"label": "_"}


def get_pawn(color):
    if color == "black":
        return {"name": "pawn", "label": "♟", "piece color": "black"}
    elif color == "white":
        return {"name": "pawn", "label": "♙", "piece color": "white"}

    return {"label": "?"}


def get_piece_starting_at_file(file, color):
    if color == "white":
        if file == 1 or file == 8:
            return {"name": "rook", "label": "♖", "piece color": color}
        elif file == 2 or file == 7:
            return {"name": "knight", "label": "♘", "piece color": color}
        elif file == 3 or file == 6:
            return {"name": "bishop", "label": "♗", "piece color": color}
        elif file == 4:
            return {"name": "king", "label": "♔", "piece color": color}
        elif file == 5:
            return {"name": "queen", "label": "♕", "piece color": color}
        else:
            return {"label": "w"}

    elif color == "black":
        if file == 1 or file == 8:
            return {"name": "rook", "label": "♜", "piece color": color}
        elif file == 2 or file == 7:
            return {"name": "knight", "label": "♞", "piece color": color}
        elif file == 3 or file == 6:
            return {"name": "bishop", "label": "♝", "piece color": color}
        elif file == 4:
            return {"name": "king", "label": "♚", "piece color": color}
        elif file == 5:
            return {"name": "queen", "label": "♛", "piece color": color}
        else:
            return {"label": "w"}

    else:
        return {"label": "?"}
    return {"label": " "}