import pieces


def print_board_chars(input_board):
    for rank in range(10):
        for file in range(10):
            print(input_board[rank][file]["piece"]["label"], end="")
        print()
    return


def create_board():
    board = []
    rows, cols = (10, 10)
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(pieces.make_tile(i, j))
        board.append(col)
    # print_board_chars(board)
    return board


Board = create_board()

def get_opposite_color(string):
    return_color = " "
    if string == "white":
        return_color = "black"
    elif string == "black":
        return_color = "white"

    return return_color


def switch_turns(cur_turn):
    cur_turn = get_opposite_color(cur_turn)
    return cur_turn


def get_cur_turn(cur_turn):
    return cur_turn

def react_to(rank, file):
    clicked_piece = Board[2][2].get("piece")
    ret_str = "Moving " + clicked_piece.get("name") + " to " + rank + "," + file
    return ret_str
