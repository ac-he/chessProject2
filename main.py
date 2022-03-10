from flask import Flask, render_template, request, url_for, redirect
from game import *

app = Flask(__name__)

cur_turn = create_turn()
game_board = create_board()
select_message = "Welcome"
is_over = set_is_over(False)
promoting = True, [0, 0, 0, 0]
reset_game()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message)


@app.route("/", methods=["POST"])
def respond_to_click():
    global cur_turn, game_board, select_message, is_over, promoting

    if request.form.keys().__contains__("new game"):
        reset_game()
        cur_turn = get_cur_turn()
        game_board = get_game_board()
        is_over = get_is_over()
        select_message = "New game started."

    elif promoting:
        if request.form.keys().__contains__("rook"):
            promote_to("rook")
        elif request.form.keys().__contains__("knight"):
            promote_to("knight")
        elif request.form.keys().__contains__("bishop"):
            promote_to("bishop")
        elif request.form.keys().__contains__("queen"):
            promote_to("queen")

    else:
        for rank in range(1, 9):
            for file in range(1, 9):
                cur_coord = pieces.get_coord_str(rank, file)
                r = request.form.keys().__contains__(cur_coord)
                if r:
                    new_select_message = react_to(rank, file)
                    if not new_select_message == "":
                        select_message = new_select_message

                    cur_turn = get_cur_turn()
                    game_board = get_game_board()
                    is_over = get_is_over()
                    promoting = get_promotion_info()
                    break
        if is_over:
            print("RECIEVED OVER")
            winner = switch_turns()
            return render_template("winner.html", winner=winner)

    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message, promoting=promoting[0], promotingInfo=promoting[1])


if __name__ == '__main__':
    app.run(debug=True)
