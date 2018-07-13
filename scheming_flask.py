"""
A tool for validating Flask requests using jsonschema
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from functools import wraps

from flask import request
from jsonschema import Draft4Validator, ValidationError

try:
    import ujson as json
except ImportError:
    import json

__author__ = 'Tim Martin'
__email__ = 'oss@timmartin.me'
__version__ = '0.1.2'


class FlaskSchema(object):
    """
    Used to wrap flask routes so that the
    incoming JSON is validated using jsonschema
    """
    def __init__(self,
                 schema_dir=None,
                 load_on=SchemaLoad.ON_INIT,
                 validator=Draft4Validator,
                 json_loader=json):
        """
        :param str schema_dir: The directory which contains
            the jsonschemas
        :param SchemaLoad load_on: When to load the schemas
            by default
        :param DraftV4Validator validator: The validator class
            to use.  DraftV3Validator is also a valid class.
            Any class with a classmethod `check_schema(json)`,
            and instance methods `validate(json)` and `__init__(json)`
        :param json_loader: By default ujson or json.  Any drop in
            replacement for `json` stdlib should work.
        """
        self._schema_dir = schema_dir or '.'
        self._schema_load = load_on
        self._validator_builder = validator
        self._schemas = {}
        self._schema_load_ons = {}
        self._json_loader = json_loader

    @property
    def schema_dir(self):
        """
        :return: The directory where the json schemas are stored
        """
        if callable(self._schema_dir):
            return self._schema_dir()
        return self._schema_dir

    def init_app(self, schema_dir=None):
        """
        Initialize all of the schemas where load_on is SchemaLoad.ON_INIT

        :param str schema_dir: Override the schema directory
        """
        self._schema_dir = schema_dir or self._schema_dir
        for schema_name, load_on in self._schema_load_ons.items():
            if load_on == SchemaLoad.ON_INIT:
                self._schemas[schema_name] = self._build_schema(
                    schema_name, self._validator_builder)

    def validate(self, schema_name, load_on=None, validator=None):
        """
        Returns a decorator for validating flask json requests

        ..code-block:: python

            app = Flask('my-app')
            validator = FlaskSchema('schema_dir/')


            @app.route('/')
            @validator.validate('my-schema.json')
            def my_view():
                # Everything has been validated at this point

        :param str schema_name: The name of the file in the schemas
            directory
        :param SchemaLoad load_on: When to load the schema
        :param validator:
        :return: A decorator
        """
        load_on = load_on or self._schema_load
        validator = validator or self._validator_builder
        self._schema_load_ons[schema_name] = load_on
        if load_on >= SchemaLoad.ON_DECORATE:
            self._schemas[schema_name] = self._build_schema(
                schema_name, validator)

        def _decorator(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                if load_on <= SchemaLoad.ALWAYS_RELOAD:
                    self._schemas[schema_name] = self._build_schema(
                        schema_name, validator)
                elif self._schemas.get(schema_name) is None:
                    self._schemas[schema_name] = self._build_schema(
                        schema_name, validator)
                schema = self._schemas[schema_name]
                try:
                    schema.validate(request.get_json())
                except ValidationError as exc:
                    raise SchemaValidationError(exc)
                return func(*args, **kwargs)
            return _wrapper
        return _decorator

    def _build_schema(self, schema_filename, validator):
        schema_path = os.path.join(self.schema_dir, schema_filename)
        with open(schema_path) as schema_file:
            schema_data = self._json_loader.load(schema_file)
        validator.check_schema(schema_data)
        return validator(schema_data)
