from boggle import Boggle
from flask import Flask, request, render_template,jsonify,session

app = Flask(__name__)
app.config["Secret_Key"] = "abcdefghijklmnop"

boggle_game = Boggle()

@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    plays = session.get('plays', 0)

    return render_template("index.html", board = board , highscore = highscore , plays = plays)

@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board,word)

    return jsonify({'result':response})

@app.route("/score" , methods = ["POST"])
def score():
    score = request.args["score"]
    highscore = session.get("highscore",0)
    plays = session.get("plays",0)

    session['plays'] = plays + 1 
    session['highscore'] = max(score,highscore)

    return jsonify(newRecord = score > highscore)