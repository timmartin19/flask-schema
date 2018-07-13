from enum import Enum


class SchemaLoad(Enum):
    """
    An Enum that indicates when the jsonschema should be loaded
    """
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        self_name = self.__class__.__name__
        other_name = other.__class__.__name__
        raise NotImplementedError(
            'Cannot compare {0} '
            'to {1}'.format(self_name, other_name))

    def __gt__(self, other):
        return not self.__lt__(other) and not self == other

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return self.__lt__(other) or self == other

    ALWAYS_RELOAD = 0
    ON_FIRST_USE = 1
    ON_INIT = 2
    ON_DECORATE = 3
