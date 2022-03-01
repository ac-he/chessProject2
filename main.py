from flask import Flask, render_template, request, url_for, redirect

import piece_movement
import game
from game import *

app = Flask(__name__)

cur_turn = create_turn()
game_board = create_board()
select_message = "Welcome"


@app.route("/", methods=["GET"])
def home():
    validation_tests()
    return render_template("index.html", curTurn=cur_turn, board=game_board, selectedPiece=select_message)


@app.route("/", methods=["POST"])
def respond_to_click():
    global cur_turn, game_board, select_message
    select_message = " "

    for rank in range(1, 9):
        for file in range(1, 9):
            cur_coord = pieces.get_coord_str(rank, file)
            r = request.form.keys().__contains__(cur_coord)
            if r:
                select_message = react_to(rank, file)
                cur_turn = get_cur_turn()
                game_board = get_game_board()
                break

    return render_template("index.html", curTurn=cur_turn, board=game_board, selectedPiece=select_message)


def validation_tests():
    test_board = create_board()
    test_board[4][4]["piece"] = {"name": "bishop", "piece color": "white"}
    test_d4 = test_board[4][4]
    test_h4 = test_board[4][8]
    test_a4 = test_board[4][1]
    test_d2 = test_board[2][4]
    test_d6 = test_board[2][6]
    test_f1 = test_board[1][6]

    print("Should Evaluate True")
    print("01. " + str(piece_movement.validate(test_d4, test_a4, test_board)))  # Move left
    print("02. " + str(piece_movement.validate(test_d4, test_h4, test_board)))  # Move right
    print("03. " + str(piece_movement.validate(test_d4, test_d2, test_board)))  # Move up
    print("04. " + str(piece_movement.validate(test_d4, test_d6, test_board)))  # Move down

    print("\nShould Evaluate False")
    print("05. " + str(piece_movement.validate(test_d2, test_d6, test_board)))  # Pawn is at d2
    print("06. " + str(piece_movement.validate(test_d6, test_d4, test_board)))  # Empty
    print("07. " + str(piece_movement.validate(test_f1, test_a4, test_board)))  # Not in trajectory
    print("08. " + str(piece_movement.validate(test_f1, test_h4, test_board)))  # Not in trajectory
    return


if __name__ == '__main__':
    app.run(debug=True)
