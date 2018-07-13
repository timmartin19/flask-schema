from abc import ABCMeta, abstractmethod


class ValidationHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_validation_error(self, validation_error):
        raise NotImplementedError

    @abstractmethod
    def load_data(self, *args, **kwargs):
        raise NotImplementedError
