from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

# Creating an instance of class "Boggle"
boggle_game = Boggle()

BOGGLE_BOARD = "board"


# Root Route to display the Boggle Board
@app.route('/')
def homepage():
    """ 
    Display the Boogle Board from the Boggle class 
    By calling the "make_board()" method
    """

    # Calling the function which creates the Boggle Board
    board = boggle_game.make_board()

    # Storing that board into the SESSION
    session[BOGGLE_BOARD] = board

    # rendering a template "base.html"
    return render_template("base.html", board = board)

# This route is called from JS file where we make an AXIOS GET Request to this route and also by passing in the form data user entered as "params"
@app.route("/check-word")
def check_word():

    # Getting the word user entered from the form which was sent in AXIOS GET request
    word = request.args["word"]
    board = session[BOGGLE_BOARD]

    # Checking the word entered by user is a VALID WORD both in "words" dictionary and in the BOARD by calling the function "check_valid_word()" in Boggle class  
    response = boggle_game.check_valid_word(board, word)

    # The result we got back from the function "check_valid_word()" in Boggle class,
    # is sent to the JS file since we make an AJAX REQUEST, we respond it back as a JSON from this route using the jsonify function from Flask.
    return jsonify({'result': response})

# This route is called from JS ROUTE as a POST Request using AXIOS when the game TIMER ENDS
@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    # Since the data send from AXIOS POST is JSON, we cannot use "request.form" as we normally use for POST Request
    # Since its JSON we use "request.json" and retreive the "score" value we passes in POST Request
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    # Updating nplays and highscore in SESSION
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    # We respond back to JS from where we made POST Request with the "brokeRecord" value which holds the score value by comparing with the previous highscore value in SESSION and sends it ONLY when "score > highscore"
    return jsonify(brokeRecord = score > highscore)


