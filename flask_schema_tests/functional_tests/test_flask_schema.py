import unittest2
import os

from flask import Flask, request
from jsonschema import ValidationError
from webtest import TestApp

from flask_schema import FlaskSchema


class TestFlaskIntegration(unittest2.TestCase):
    def setUp(self):
        _schema_dir = os.path.join(os.path.dirname(__file__), '..', 'schemas')
        app = Flask('blah')
        fs = FlaskSchema(_schema_dir)

        @app.route('/', methods=['POST'])
        @fs.validate('blah.json')
        def my_view():
            return 'whatever'

        fs.init_app()
        self.app = TestApp(app)

    def test_when_invalid_json(self):
        resp = self.app.post_json('/', params=1, expect_errors=True)
        self.assertEqual(422, resp.status_code)

    def test_when_valid_json(self):
        resp = self.app.post_json('/', params='blah')
        self.assertEqual(200, resp.status_code)
