import json

import requests
from jsonschema import Draft4Validator

from schemer.schema_loader import SchemaLoader

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class URLSchemaLoader(SchemaLoader):
    def __init__(self, schema_url_root, json_loader=json, validator=Draft4Validator):
        self._json_loader = json_loader
        self._validator = validator
        self._host = schema_url_root

    def load_schema(self, url_path, method, **extra_requests_args):
        full_url = urljoin(self._host, url_path)
        resp = requests.request(method, full_url, **extra_requests_args)
        schema = self._json_loader.loads(resp.content)
        self._validator.check_schema(schema)
        return self._validator(schema)
