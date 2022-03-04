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
    #validation_tests()
    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message)


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

    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message)


#def validation_tests():
#    test_a2 = {"rank": 2, "file": 1, "piece": {"piece color": "white", "name": "pawn"}}
#    test_a3 = {"rank": 3, "file": 1, "piece": {"label": " "}}
#    test_a4 = {"rank": 4, "file": 1, "piece": {"label": " "}}
#    test_f7 = {"rank": 7, "file": 7, "piece": {"piece color": "black", "name": "pawn"}}
#    test_f6 = {"rank": 6, "file": 7, "piece": {"label": " "}}
#    test_f5 = {"rank": 5, "file": 7, "piece": {"label": " "}}
#    test_e6 = {"rank": 6, "file": 6, "piece": {"piece color": "white", "name": "pawn"}}
#    test_e7 = {"rank": 7, "file": 6, "piece": {"piece color": "black", "name": "pawn"}}
#    test_f4 = {"rank": 4, "file": 7, "piece": {"piece color": "white", "name": "pawn"}}#

    #print("Should Evaluate True")
    #print("01. " + str(piece_movement.validate(test_a2, test_a3)))  # Move one ahead from r2
    #print("02. " + str(piece_movement.validate(test_a2, test_a4)))  # Move two ahead from r2
    #print("03. " + str(piece_movement.validate(test_f7, test_f6)))  # Move one ahead from r7
    #print("04. " + str(piece_movement.validate(test_f7, test_f5)))  # Move two ahead from r7
    #print("05. " + str(piece_movement.validate(test_f7, test_e6)))  # Capture
    #print("06. " + str(piece_movement.validate(test_e6, test_f7)))  # Capture
    #print("07. " + str(piece_movement.validate(test_f4, test_f5)))  # Move one ahead from r4

    #print("\nShould Evaluate False")
    #print("08. " + str(piece_movement.validate(test_a3, test_a2)))  # Move backwards
    #print("09. " + str(piece_movement.validate(test_a2, test_f6)))  # Move across board
    #print("10. " + str(piece_movement.validate(test_f7, test_a3)))  # Move across board
    #print("11. " + str(piece_movement.validate(test_f5, test_f7)))  # Move backwards
    #print("12. " + str(piece_movement.validate(test_e7, test_f7)))  # Move sideways
    #print("13. " + str(piece_movement.validate(test_e6, test_f6)))  # Move sideways
    #print("14. " + str(piece_movement.validate(test_f4, test_f6)))  # Move two ahead from r4

    #return


if __name__ == '__main__':
    app.run(debug=True)
