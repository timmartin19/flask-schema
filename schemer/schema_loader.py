from abc import ABCMeta, abstractmethod
import json
import os

from jsonschema import Draft4Validator

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
    from urllib.request import Request


class SchemaLoader(metaclass=ABCMeta):
    @abstractmethod
    def load_schema(self, *args, **kwargs):
        raise NotImplementedError


class FileSchemaLoader(SchemaLoader):
    def __init__(self, schema_dir, json_loader=json, validator=Draft4Validator):
        self._schema_dir = schema_dir
        self._json_loader = json_loader
        self._validator = validator

    def load_schema(self, schema_filename):
        schema_path = os.path.join(self._schema_dir, schema_filename)
        with open(schema_path) as schema_file:
            schema_data = self._json_loader.load(schema_file)
        self._validator.check_schema(schema_data)
        return self._validator(schema_data)

