from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setup(self):
        self.client = app.test_client()
        app.config['Testing'] = True

    def test_home(self):
        with  self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('plays'))
            self.assertIn(b'<p>High Score:' , response.data)
            self.assertIn(b'Score:' , response.data)
            self.assertIn(b'Time left:', response.data)

    def test_validWord(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')
    
    def test_invalid_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'] , 'not-on-board')

    