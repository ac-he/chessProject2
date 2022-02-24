from flask import Flask, render_template, request, url_for, redirect

import game
from game import *

app = Flask(__name__)

cur_turn = "white"

game_board = create_board()

select_message = " "


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", curTurn=cur_turn, board=game_board, selectedPiece=select_message)


@app.route("/", methods=["POST"])
def respond_to_click():
    #x = request.form["x"]
    #y = request.form["y"]
    s = request.form["selection"]
    select_message = "Moving piece " + s
    return render_template("index.html", curTurn=cur_turn, board=game_board, selectedPiece=select_message)


if __name__ == '__main__':
    app.run(debug=True)
