from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)
            # test that you're getting a template

# test that json includes gameID, and that we a board
    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            # make a post request to /api/new-game

            resp = client.post("/api/new-game")
            data = resp.get_json()  # get the response body as json using .get_json()
            #change json variable name (data)
            self.assertIn(data.get("gameId"), games) # test that the game_id is in the dictionary of games (imported from app.py above)
            self.assertEqual(resp.is_json, True)
            self.assertEqual(isinstance(data.get("gameId"), str), True) # test that the game_id is a string
            self.assertEqual(isinstance(data.get("board"), list), True) # test that the board is a list
            #self.assertIsInstance
    def test_score_word(self):
        """Test if word is valid"""

        with app.test_client() as client:

            new_game_resp = client.post("/api/new-game") # make a post request to /api/new-game
            new_game_data = new_game_resp.get_json() # get the response body as json using .get_json()

            game_id = new_game_data.get('gameId')
            game = games.get(game_id) # find that game in the dictionary of games (imported from app.py above)


            game.board = [ # manually change the game board's rows so they are not random
                ['A', 'C', 'A', 'T', 'A'],
                ['A', 'A', 'A', 'A', 'A'],
                ['A', 'A', 'A', 'A', 'A'],
                ['A', 'A', 'A', 'A', 'A'],
                ['A', 'A', 'A', 'A', 'A'],
            ]

            score_word_resp_ok = client.post('/api/score-word', json={
                'gameId': game_id,
                'word': 'CAT'
            })
            data_ok = score_word_resp_ok.get_json()
            self.assertEqual(data_ok.get('result'), 'ok') # test to see that a valid word on the altered board returns {'result': 'ok'}

            score_word_resp_not_word = client.post('/api/score-word', json={
                'gameId': game_id,
                'word': 'KAUWKBUFW'
            })
            data_not_word = score_word_resp_not_word.get_json()
            self.assertEqual(data_not_word.get('result'), 'not-word') # test to see that an invalid word returns {'result': 'not-word'}

            score_word_resp_not_on_board = client.post('/api/score-word', json={
                'gameId': game_id,
                'word': 'DOG'
            })
            data_not_on_board = score_word_resp_not_on_board.get_json()
            self.assertEqual(data_not_on_board.get('result'), 'not-on-board') # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}

            score_word_resp_not_word_on_board = client.post('/api/score-word', json={
                'gameId': game_id,
                'word': 'AAAAA'
            })
            data_word_not_on_board = score_word_resp_not_word_on_board.get_json()
            self.assertEqual(data_word_not_on_board.get('result'), 'not-word')



