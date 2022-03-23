from flask import Flask, render_template, request, url_for, redirect
from game import *

app = Flask(__name__)


# Set up the initial game state
select_message = "Welcome"
reset_game()

# Set up variables this class will use to update the display
cur_turn = get_cur_turn()
game_board = get_game_board()
is_over = get_is_over()
can_promote = get_promotion_info()[0]
promote_options = get_promotion_info()[1]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message)


@app.route("/", methods=["POST"])
def respond_to_click():
    global cur_turn, game_board, select_message, is_over, can_promote, promote_options

    # If the 'new game' button was pressed
    if request.form.keys().__contains__("new game"):
        reset_game()
        cur_turn = get_cur_turn()
        game_board = get_game_board()
        is_over = get_is_over()
        select_message = "New game started."

    # If expecting a promotion button to be clicked
    elif can_promote:
        if request.form.keys().__contains__("rook"):  # Promote to rook
            select_message = promote_to("rook")
        elif request.form.keys().__contains__("knight"):  # Promote to knight
            select_message = promote_to("knight")
        elif request.form.keys().__contains__("bishop"):  # Promote to bishop
            select_message = promote_to("bishop")
        elif request.form.keys().__contains__("queen"):  # Promote to queen
            select_message = promote_to("queen")
        else:  # A different button was pressed, tell user about mistake
            select_message = "You must promote this pawn to one of the options shown below the board."

    # Otherwise, it must have been a click on the board
    else:
        # Loop through all (non-label) buttons
        for rank in range(1, 9):
            for file in range(1, 9):
                cur_coord = pieces.get_coord_str(rank, file)  # Figure out the coords are
                r = request.form.keys().__contains__(cur_coord)  # Check if they match the coords of the clicked button

                if r:  # This is the button that was clicked
                    new_select_message = react_to(rank, file)  # Update the game state and get the new message

                    if not new_select_message == "":  # Update the message if a new one was provided
                        select_message = new_select_message

                    is_over = get_is_over()  # Check if game is over
                    break  # Stop searching for buttons

        if is_over:  # Switch to game over screen and announce the winner
            winner = switch_turns()
            return render_template("winner.html", winner=winner)

    # Update all of the variables to prepare to update the display
    cur_turn = get_cur_turn()
    game_board = get_game_board()

    promoting = get_promotion_info()
    can_promote = promoting[0]
    promote_options = promoting[1]

    # Update the display
    return render_template("index.html", curTurn=cur_turn, board=game_board, feedbackMessage=select_message,
                           can_promote=can_promote, promote_options=promote_options)


if __name__ == '__main__':
    app.run(debug=True)
