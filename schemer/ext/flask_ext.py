from flask import request
from werkzeug.exceptions import UnprocessableEntity

from schemer.exceptions import SchemaValidationError
from schemer.validation_handler import ValidationHandler


class FlaskSchemaValidationError(UnprocessableEntity, SchemaValidationError):
    """
    Wraps a ValidationException in a format
    that returns something useful to the frontend
    """
    def __init__(self, exc, *args, **kwargs):
        self.validation_exception = exc
        super(FlaskSchemaValidationError, self).__init__(str(exc), *args, **kwargs)


class FlaskHandler(ValidationHandler):
    def __init__(self, get_json_options=None):
        self._get_json_options = get_json_options or {}

    def handle_validation_error(self, validation_error):
        raise FlaskSchemaValidationError(validation_error)

    def load_data(self, *args, **kwargs):
        return request.get_json(**self._get_json_options)
