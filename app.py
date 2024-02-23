from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"


# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start new game and return JSON about game.

    Returns: JSON of {
       gameId: "...uuid-of-game...",
       board: [ [ 'A', 'B', ... ], ... ]
    }
    """

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    board = game.board

    game_data = {"gameId": game_id, "board": board}

    return jsonify(game_data)


@app.post("/api/score-word")
def score_word():
    """Recieves a word and determines whether that word is valid, not a word,
      or not on the game board

      Recieves: JSON of {
        gameId: "...uuid-of-game...",
        word: "str"
      }

      Returns: JSON of {
        result: "ok" or "not-word" or "not-on-board"
      }
      """

    word = request.json.get('word')
    game_id = request.json.get('gameId')
    curr_game = games.get(game_id)
    response = {}

    if not curr_game.is_word_in_word_list(word):
        response['result'] = "not-word"
    elif not curr_game.check_word_on_board(word):
        response['result'] = "not-on-board"
    else:
        response['result'] = 'ok'

    return jsonify(response)
