import abc

from typing import Any, Dict


class Field(abc.ABC):
    # This field is used to what is the matching type according
    # to Monday API when fetching data from monday boards
    __monday_field_type__ = None

    @abc.abstractmethod
    def to_monday_dict(self) -> Dict[str, Any]:
        """
        Represent the item as a monday dictionary.
        This dictionary is the way that Monday API knows how to create/update an item
        """

        raise NotImplementedError

    @abc.abstractmethod
    def from_monday_dict(self, data: Any):
        """
        Change the item value from the monday dictionary (fetch the data from the monday api)
        """

        raise NotImplementedError

    @property
    def value(self) -> Any:
        """
        A property to get the current value of the field
        """

        return self._value

    @value.setter
    def value(self, value):
        """
        A property setter (set's the field value)
        """

        self._value = value

    def __str__(self) -> str:
        return str(self.value)
