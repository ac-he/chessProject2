from flask import Flask, render_template, request, url_for, redirect

import game
from game import *

app = Flask(__name__)

cur_turn = create_turn()
game_board = create_board()
select_message = "Welcome"


@app.route("/", methods=["GET"])
def home():
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


if __name__ == '__main__':
    app.run(debug=True)
