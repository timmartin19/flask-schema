import unittest2
import os
from enum import Enum

from flask import Flask
from jsonschema import Draft3Validator, Draft4Validator, SchemaError

from scheming_flask import FlaskSchema, SchemaLoad


_TEST_SCHEMA = os.path.join(os.path.dirname(__file__), '..', 'schemas')


class TestSchemaDirProperty(unittest2.TestCase):
    def test_when_default(self):
        fs = FlaskSchema()
        self.assertEqual(fs.schema_dir, '.')

    def test_when_callable(self):
        fs = FlaskSchema(schema_dir=lambda: 'blah')
        self.assertEqual(fs.schema_dir, 'blah')

    def test_when_not_default_not_callable(self):
        fs = FlaskSchema(schema_dir='blah')
        self.assertEqual(fs.schema_dir, 'blah')


class TestInitApp(unittest2.TestCase):
    def test_when_empty(self):
        fs = FlaskSchema()
        fs.init_app()
        self.assertDictEqual({}, fs._schemas)

    def test_when_not_on_init_app(self):
        fs = FlaskSchema()
        fs.validate('blah', load_on=SchemaLoad.ON_FIRST_USE)
        fs.validate('blah2', load_on=SchemaLoad.ALWAYS_RELOAD)
        fs.init_app()
        self.assertDictEqual(fs._schemas, {})

    def test_when_valid__loads_schema(self):
        fs = FlaskSchema(_TEST_SCHEMA)
        fs.validate('blah.json', load_on=SchemaLoad.ON_INIT)
        fs.init_app()
        self.assertEqual(len(fs._schemas), 1)
        fs._schemas['blah.json'].validate('blah')


class TestValidate(unittest2.TestCase):
    def test_when_on_decorate__immediately_loads_schema(self):
        fs = FlaskSchema(_TEST_SCHEMA)
        fs.validate('blah.json', load_on=SchemaLoad.ON_DECORATE)
        self.assertEqual(len(fs._schemas), 1)

    def test_when_on_first_run(self):
        with Flask('blah').test_request_context(data='"blah"', content_type='application/json'):
            fs = FlaskSchema(_TEST_SCHEMA)
            decorator = fs.validate('blah.json', load_on=SchemaLoad.ON_FIRST_USE)
            self.assertEqual(len(fs._schemas), 0)
            blah = lambda: 'blah'
            blah = decorator(blah)
            self.assertEqual(len(fs._schemas), 0)
            blah()
            self.assertEqual(len(fs._schemas), 1)
            temp = fs._schemas['blah.json']
            # make sure it doesn't run again
            blah()
            self.assertIs(temp, fs._schemas['blah.json'])

    def test_when_always_reload(self):
        with Flask('blah').test_request_context(data='"blah"', content_type='application/json'):
            fs = FlaskSchema(_TEST_SCHEMA)
            decorator = fs.validate('blah.json', load_on=SchemaLoad.ALWAYS_RELOAD)
            self.assertEqual(len(fs._schemas), 0)
            blah = lambda: 'blah'
            blah = decorator(blah)
            self.assertEqual(len(fs._schemas), 0)
            blah()
            self.assertEqual(len(fs._schemas), 1)
            temp = fs._schemas['blah.json']
            # make sure it doesn't run again
            blah()
            self.assertIsNot(temp, fs._schemas['blah.json'])

    def test_when_on_init_and_not_initted(self):
        with Flask('blah').test_request_context(data='"blah"', content_type='application/json'):
            fs = FlaskSchema(_TEST_SCHEMA)
            decorator = fs.validate('blah.json', load_on=SchemaLoad.ON_INIT)
            self.assertEqual(len(fs._schemas), 0)
            blah = lambda: 'blah'
            blah = decorator(blah)
            self.assertEqual(len(fs._schemas), 0)
            blah()
            self.assertEqual(len(fs._schemas), 1)
            temp = fs._schemas['blah.json']
            # make sure it doesn't run again
            blah()
            self.assertIs(temp, fs._schemas['blah.json'])

    def test_when_load_on_not_set(self):
        fs = FlaskSchema(load_on=SchemaLoad.ALWAYS_RELOAD)
        fs.validate('blah.json')
        self.assertDictEqual(fs._schema_load_ons, {'blah.json': SchemaLoad.ALWAYS_RELOAD})

    def test_when_validator_set(self):
        fs = FlaskSchema(_TEST_SCHEMA)
        fs.validate('blah.json', load_on=SchemaLoad.ON_DECORATE)
        self.assertIsInstance(fs._schemas['blah.json'], Draft4Validator)
        fs.validate('blah.json', load_on=SchemaLoad.ON_DECORATE, validator=Draft3Validator)
        self.assertIsInstance(fs._schemas['blah.json'], Draft3Validator)


class TestBuildSchema(unittest2.TestCase):
    def test_when_file_exists(self):
        fs = FlaskSchema(_TEST_SCHEMA)
        schema = fs._build_schema('blah.json', Draft4Validator)
        self.assertIsNotNone(schema)

    def test_when_file_not_exists(self):
        fs = FlaskSchema()
        self.assertRaises(IOError, fs._build_schema, 'not-real', Draft4Validator)

    def test_when_schema_invalid(self):
        fs = FlaskSchema(_TEST_SCHEMA)
        self.assertRaises(SchemaError, fs._build_schema, 'invalid-schema.json', Draft4Validator)


class TestSchemaLoadEnum(unittest2.TestCase):
    def test_lt_when_compared_with_same_class(self):
        self.assertTrue(SchemaLoad.ALWAYS_RELOAD < SchemaLoad.ON_DECORATE)

    def test_lt_when_compared_with_different_class(self):
        class Blah(Enum):
            ANOTHER = 1
        self.assertRaises(NotImplementedError, lambda: SchemaLoad.ON_DECORATE < Blah.ANOTHER)
