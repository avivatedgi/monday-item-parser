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

    def search_representation(self) -> str:
        """
        Returns the representation of the value as it should be when we want to search it
        by the items by column values query
        (Read more at https://api.developer.monday.com/docs/items-by-column-values-queries)

        Only classes that will implement this function can be used by the `Item::fetch_items_by_column_value` function.
        """

        raise AttributeError(
            "items_by_column_value is not supported for {}".format(
                self.__class__.__qualname__
            )
        )

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
