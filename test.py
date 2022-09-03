from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text = True)

            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn("<h1> BOGGLE GAME </h1>", html)
            self.assertIn("<p>High Score:", html)
            self.assertIn('Score:', html)
            self.assertIn('Seconds Left:', html)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session and also checking the JSON RESPONSE """
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        res = self.client.get('/check-word?word=cat')
        self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary and not on board"""

        with self.client:
            self.client.get('/')
            response = self.client.get('/check-word?word=impossible')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if word is on the board but not in dictionary"""

        with self.client:
            self.client.get('/')
            response = self.client.get(
                '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
            self.assertEqual(response.json['result'], 'not-word')