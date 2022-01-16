from __future__ import annotations

import copy
import inspect
import json

from bidict import bidict
from typing import Any, Dict, Iterable, Iterator, List, Optional
from monday import MondayClient

from .helpers import as_type, as_obj
from .fields import Field
from .exceptions import MondayClientError


class ItemMeta(type):
    __invalid_attribute_names__ = (
        # Attributes sets by the ItemMeta metaclass
        "_monday_client",
        "_field_names",
        "_board_id",
        "_monday_field_names",
        "_group_id",
        "_item_name",
        "_item_id",
        "_unsaved_item_name",
        # Properties from the Item class
        "fields",
        "board_id",
        "group_id",
        "item_name",
        "item_id",
    )

    def __new__(
        mcs,
        name,
        bases,
        attributes,
        monday_client: Optional[MondayClient] = None,
        board_id: Optional[int] = None,
        ignore_unused_fields: Optional[bool] = False,
    ):
        # Check if metaclass is running for class Item itself, in which case, it won't have any fields
        if not bases:
            return super().__new__(mcs, name, bases, attributes)

        # Validate that all of the attribute names are valid
        for field_name, field_obj in attributes.items():
            if field_name in ItemMeta.__invalid_attribute_names__:
                raise AttributeError(
                    f"Attribute name {field_name} is invalid for an Item derive!"
                )

        # If metaclass isn't running for the class `Item` itself
        # it must include `monday_client` and `board_id` as parameters
        if not monday_client:
            raise AttributeError(
                f"`monday_client` must be provided as parameter for Item derived class `{name}`"
            )

        if not board_id:
            raise AttributeError(
                f"`board_id` must be provided as parameter for Item derived class `{name}`"
            )

        attributes["_board_id"] = board_id
        attributes["_monday_client"] = monday_client
        attributes["_frozen"] = False

        # Save all of the fields under the `_field_names` attribute
        # and create a backup of them under the _backup_fields
        attributes["_field_names"] = []
        attributes["_backup_fields"] = {}

        for field_name, field_obj in attributes.items():
            # Ignore attributes that arent fields
            if not issubclass(as_type(field_obj), Field):
                continue

            # Convert to object (this is for non-instansiated Fields)
            field_obj = as_obj(field_obj)
            attributes["_field_names"].append(field_name)
            attributes["_backup_fields"][field_name] = copy.deepcopy(field_obj)
            attributes[field_name] = field_obj

        # Iterate over all of the fields in the monday board and save the field names
        # and id's in a bidict, the reason I use a bidict is so it will be easy
        # to get the monday field id from the column name and vice versa.
        attributes["_monday_field_names"] = bidict()

        board_data = monday_client.boards.fetch_boards_by_id([board_id])
        for field_data in board_data["data"]["boards"][0]["columns"]:
            # Replace the field name from the monday board to be lowercase
            # and replace spaces into underscores
            # (so "My Example Column" will become "my_example_column")
            field_name = field_data["title"].lower().replace(" ", "_")

            # If we didn't found this field in our attributes just don't add it
            if field_name not in attributes:
                continue

            # Validate that the field type is the same as the expected field type
            # declared in the item class
            actual_field_type = field_data["type"].lower()
            expcted_field_type = attributes[field_name].__monday_field_type__
            if actual_field_type != expcted_field_type:
                raise AttributeError(
                    f"'{name}::{field_name}' should be of type '{expcted_field_type}' but got '{actual_field_type}'"
                )

            # Save the field name & id
            attributes["_monday_field_names"][field_name] = field_data["id"]

        # Iterate again over the item fields and check if there are
        # fields that aren't in use
        if not ignore_unused_fields:
            for field_name in attributes["_field_names"]:
                if field_name not in attributes["_monday_field_names"]:
                    raise AttributeError(
                        f"'{name}::{field_name}' is declared but not used by the monday api"
                    )

        # Add some metadata for the monday fields to the attributes
        attributes["_item_name"] = None
        attributes["_item_id"] = None
        attributes["_group_id"] = None
        attributes["_unsaved_item_name"] = None
        attributes["_updated_fields"] = []

        return super().__new__(mcs, name, bases, attributes)


class Item(metaclass=ItemMeta):
    _field_names: List[str]
    _backup_fields: Dict[str, Field]
    _board_id: int
    _monday_client: MondayClient
    _monday_field_names: bidict
    _item_name: str
    _item_id: int
    _unsaved_item_name: str
    _group_id: str
    _frozen: bool

    @property
    def _changed_fields(self) -> Iterable[Field]:
        return (
            name
            for name in self._field_names
            if getattr(self, name).value != self._backup_fields[name].value
        )

    @property
    def _fields(self) -> Iterable[Field]:
        return (getattr(self, name) for name in self._field_names)

    @property
    def has_been_changed(self) -> bool:
        return any(self._changed_fields) or self._unsaved_item_name

    def __init__(self, *args, **kwargs):
        # Create a list of all the positional (required) arguments
        positional_args = []

        # if self is a subclass of Item (and not Item)
        if type(self) is not Item:
            for name, param in inspect.signature(self.__init__).parameters.items():
                # Check if the param is positional (required)
                if (
                    param.default == inspect.Parameter.empty
                    and param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                ):
                    positional_args.append(name)

        if len(args) != len(positional_args):
            raise ValueError(
                "Invalid arguments were passed to the superclass. "
                "Expected arguments: {} but {} given.".format(
                    positional_args, len(args)
                )
            )

        # Deepcopy the fields so different instances of Item have unique fields
        for name, field in self:
            setattr(self, name, copy.deepcopy(field))

        for k, v in kwargs.items():
            if k not in self._field_names:
                raise ValueError(
                    "Unexpected keyword argument given: {}={}".format(k, v)
                )

            setattr(self, k, v)

        # Make sure no one can update this item attributes after the instanciation
        self._frozen = True

        super().__init__()

    def __str__(self):
        x = [
            f"\x1b[32m{self.__class__.__qualname__}\x1b[0m "
            f"(\x1b[32mId:\x1b[0m {self._item_id} | \x1b[32mName:\x1b[0m {self._item_name} | \x1b[32mGroup Id:\x1b[0m {self._group_id}):"
        ]

        for name, field in self:
            if isinstance(field, Item):
                x.append("\t{} ({}):".format(name, field.__class__.__qualname__))
                x.extend(
                    "\t{}".format(field_str)
                    for field_str in str(field).splitlines()[1:]
                )
            else:
                name_and_id = "\t{} <\x1b[33m{}\x1b[0m>: ".format(
                    name, self._monday_field_names[name]
                )

                value = "\x1b[33m{}\x1b[0m({})".format(
                    field.__class__.__qualname__, str(field)
                )

                x.append("{}{}".format(name_and_id.ljust(48), value))

        return "\n".join(x)

    def __eq__(self, other) -> bool:
        return all(a.value == b.value for a, b in zip(self._fields, other._fields))

    def __ne__(self, other) -> bool:
        return not self == other

    def __iter__(self):
        """
        :return: Iterator of (name, field) tuples
        """
        return zip(self._field_names, self._fields)

    def __setattr__(self, key, value):
        """
        Only allows setting the field's values.
        :param key:     The name of the attribute to set
        :param value:   The value to set
        :return:        None
        """

        if key in self._field_names and not isinstance(value, Field):
            # Update the value of the field and invoke the hooks
            field = getattr(self, key)
            field.value = value
            self.invoke_field_update_hooks(field)
        elif key in self._field_names:
            # Overriding the field so we must save the hooks attribute and set them
            # after we update the field
            field = getattr(self, key)
            hooks = getattr(field, "_value_update_hooks", [])
            super().__setattr__(key, value)
            setattr(field, "_value_update_hooks", hooks)

            # Invoke the field hooks because the value has been changed
            self.invoke_field_update_hooks(field)
        elif hasattr(self, key) or not self._frozen:
            super().__setattr__(key, value)
        else:
            raise AttributeError(
                f"Monday fields attributes can not be changed! ({self.__class__.__qualname__}:{key})"
            )

    @property
    def item_id(self):
        return self._item_id

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, value: str):
        self._unsaved_item_name = value

    @property
    def group_id(self):
        return self._group_id

    def duplicate_item(self) -> Item:
        if not self._item_id:
            raise AttributeError(
                f"Can not duplicate item that wasn't fetched from the server"
            )

        item = copy.deepcopy(self)
        item._item_id = None
        item.create_item(self._group_id)
        return item

    def create_item(self, group_id: str):
        if self.item_id:
            raise AttributeError(f"The item already exists (id = {self._item_id})")

        # Get all the fields data
        column_values = {
            self._monday_field_names[field_name]: field.to_monday_dict()
            for field_name, field in self
            if field.to_monday_dict() is not None
        }

        # Create the item
        response = self._monday_client.items.create_item(
            self._board_id, group_id, self._unsaved_item_name, column_values
        )
        self.raise_monday_errors(response)

        # Validate that the creation succeed
        self._item_id = response["data"]["create_item"]["id"]

        # Update the backup so it will hold those values now
        for field_name, field in self:
            self._backup_fields[field_name] = copy.deepcopy(field)

        # Set the needed attributes after the create request
        self._item_name = self._unsaved_item_name
        self._unsaved_item_name = None
        self._group_id = group_id

    def update_item(self):
        if not self.item_id:
            raise AttributeError(
                "Can not update an item that wasn't fetch from the server. Did you mean `create_item`?"
            )

        if not self.has_been_changed:
            # No need to update anything if there are no changes
            return

        # Get all the changed fields data (we wan't to update only what we change, not everything)
        column_values = {
            self._monday_field_names[field_name]: getattr(
                self, field_name
            ).to_monday_dict()
            for field_name in self._changed_fields
            if getattr(self, field_name).to_monday_dict() is not None
        }

        if self._unsaved_item_name:
            column_values["name"] = self._unsaved_item_name

        # Update the item in the monday board
        data = self._monday_client.items.change_multiple_column_values(
            self._board_id, self.item_id, column_values
        )
        self.raise_monday_errors(data)

        # Update the name of the item
        if self._unsaved_item_name:
            self._item_name = self._unsaved_item_name
            self._unsaved_item_name = None

        # Update the backup items
        for field_name, field in self:
            self._backup_fields[field_name] = copy.deepcopy(field)

    def delete_item(self):
        if not self.item_id:
            raise AttributeError(
                "Can not update an item that wasn't fetch from the server. Did you mean `create_item`?"
            )

        data = self._monday_client.items.delete_item_by_id(self.item_id)
        self.raise_monday_errors(data)

        self._unsaved_item_name = None
        self._item_id = None

    @classmethod
    def from_monday_dictionary(cls, data: Dict[str, Any]):
        obj = cls()
        obj._item_id = int(data["id"])
        obj._item_name = data["name"]
        obj._unsaved_item_name = None
        obj._group_id = data["group"]["id"]

        for column_data in data["column_values"]:
            monday_id = column_data["id"]

            # Check if the monday id is in our item dictionary
            if monday_id not in obj._monday_field_names.inverse:
                continue

            attribute_name = obj._monday_field_names.inverse[monday_id]

            # Load the data from the monday dictionary
            column_value = (
                json.loads(column_data["value"]) if column_data["value"] else None
            )

            getattr(obj, attribute_name).from_monday_dict(column_value)

            # Create a backup so we will know what have been changed
            obj._backup_fields[attribute_name] = copy.deepcopy(
                getattr(obj, attribute_name)
            )

        return obj

    @classmethod
    def fetch_items_from_board(cls) -> Iterator[Item]:
        board_data = cls._monday_client.boards.fetch_items_by_board_id([cls._board_id])

        cls.raise_monday_errors(board_data)

        for item in board_data["data"]["boards"][0]["items"]:
            yield cls.from_monday_dictionary(item)

    @classmethod
    def fetch_items_by_column_value(cls, **kwargs):
        field_name, field_value = next(iter(kwargs.items()))

        if field_name not in cls._monday_field_names:
            raise AttributeError("Invalid field to search by {}".format(field_name))

        monday_id = cls._monday_field_names[field_name]
        field_copy = copy.deepcopy(getattr(cls, field_name))
        field_copy.value = field_value
        data = field_copy.search_representation()

        items_data = cls._monday_client.items.fetch_items_by_column_value(
            cls._board_id, monday_id, data
        )

        cls.raise_monday_errors(items_data)

        for item in items_data["data"]["items_by_column_values"]:
            yield cls.from_monday_dictionary(item)

    @staticmethod
    def raise_monday_errors(response):
        if isinstance(response, dict) and "errors" in response:
            errors = [
                error["message"] if "message" in error else error
                for error in response["errors"]
            ]

            raise MondayClientError("Got error from monday client", errors)

    @classmethod
    def fetch_group_ids(cls) -> Iterator[str]:
        groups_data = cls._monday_client.groups.get_groups_by_board([cls._board_id])
        for group in groups_data["data"]["boards"][0]["groups"]:
            yield group["id"]

    def invoke_field_update_hooks(self, field: Field):
        for f in getattr(field, "_value_update_hooks", ()):
            f(self)

    @classmethod
    def field_updated_hook(cls, field):
        def register_field_hook(func: callable):
            if hasattr(field, "_value_update_hooks"):
                field._value_update_hooks.append(func)
            else:
                field._value_update_hooks = [func]

            return func

        return register_field_hook
