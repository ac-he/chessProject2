from flask import Flask, render_template, request, url_for, redirect
from game import *

app = Flask(__name__)

cur_turn = create_turn()
game_board = create_board()
select_message = "Welcome"
is_over = set_is_over(False)
can_promote = False
promote_options = []
reset_game()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message)


@app.route("/", methods=["POST"])
def respond_to_click():
    global cur_turn, game_board, select_message, is_over, can_promote, promote_options

    if request.form.keys().__contains__("new game"):
        reset_game()
        cur_turn = get_cur_turn()
        game_board = get_game_board()
        is_over = get_is_over()
        select_message = "New game started."

    elif can_promote:
        if request.form.keys().__contains__("rook"):
            select_message = promote_to("rook")
        elif request.form.keys().__contains__("knight"):
            select_message = promote_to("knight")
        elif request.form.keys().__contains__("bishop"):
            select_message = promote_to("bishop")
        elif request.form.keys().__contains__("queen"):
            select_message = promote_to("queen")
        else:
            select_message = "You must promote this pawn to one of the options shown below the board."

    else:
        for rank in range(1, 9):
            for file in range(1, 9):
                cur_coord = pieces.get_coord_str(rank, file)
                r = request.form.keys().__contains__(cur_coord)
                if r:
                    new_select_message = react_to(rank, file)
                    if not new_select_message == "":
                        select_message = new_select_message

                    is_over = get_is_over()

                    break
        if is_over:
            winner = switch_turns()
            return render_template("winner.html", winner=winner)

    cur_turn = get_cur_turn()
    game_board = get_game_board()

    promoting = get_promotion_info()
    can_promote = promoting[0]
    promote_options = promoting[1]

    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message, can_promote=can_promote, promote_options=promote_options)


if __name__ == '__main__':
    app.run(debug=True)
