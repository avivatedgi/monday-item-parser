import pytest

from datetime import datetime
from monday import MondayClient
from monday_item_parser import *

from .helpers import client, testing_board_id


def test_item_invalid_decleration():
    with pytest.raises(AttributeError):

        class InvalidItem(Item, monday_client=client, board_id=testing_board_id):
            field_that_doest_exists = NumberField


def test_item_invalid_decleration_ignored():
    class InvalidItem(
        Item,
        monday_client=client,
        board_id=testing_board_id,
        ignore_unused_fields=True,
    ):
        field_that_doest_exists = NumberField


class ItemExample(Item, monday_client=client, board_id=testing_board_id):
    status_example = StatusField
    date_example = DateField
    checkbox_example = CheckboxField
    country_example = CountryField
    email_example = EmailField
    link_example = LinkField
    numbers_example = NumberField
    people_example = PeopleField
    phone_example = PhoneField
    tags_example = TagsField
    text_example = TextField
    timeline_example = TimelineField


def test_change_item_attribute():
    item = ItemExample()
    with pytest.raises(AttributeError):
        item.status_example = StatusField()


def test_create_item_then_duplicate_it_and_update_it():
    item = ItemExample()
    item.item_name = "Aviv Atedgi"
    item.status_example.value = "Working on it"
    item.date_example.value = datetime.now()
    item.checkbox_example.value = True
    item.country_example.value = "IL"
    item.email_example.value = "aviv.atedgi2000@gmail.com"
    item.link_example.value = "https://www.github.com/avivatedgi"
    item.link_example.text = "My Github Profile"
    item.numbers_example.value = 192.4
    item.people_example.value = [Person(25200525)]
    item.phone_example.country_code = "IL"
    item.phone_example.value = "0501234567"
    item.tags_example.value = [12808387]
    item.text_example.value = "My Cool Text Example"
    item.timeline_example.value = [
        datetime.strptime("2000-05-01", "%Y-%m-%d"),
        datetime.now(),
    ]
    item.create_item("topics")

    new_item = item.duplicate_item()
    new_item.item_name = "Omri Siniver"
    new_item.status_example.value = 2
    new_item.date_example.value = datetime.now()
    new_item.checkbox_example.value = False
    new_item.country_example.value = "US"
    new_item.email_example.value = "omrisiniver@gmail.com"
    new_item.link_example.value = "https://www.google.com"
    new_item.link_example.text = "Google It"
    new_item.numbers_example.value = 154
    new_item.people_example.value = [Person(20106356)]
    new_item.phone_example.country_code = "US"
    new_item.phone_example.value = "12123123123"
    new_item.tags_example.value = [12808388]
    new_item.text_example.value = "YES"
    new_item.timeline_example.value = [
        datetime.strptime("2005-04-12", "%Y-%m-%d"),
        datetime.now(),
    ]
    new_item.update_item()


def test_fetch_items_and_delete():
    for item in ItemExample.fetch_items_from_board():
        item.delete_item()


def test_fetch_group_ids():
    for group_id in ItemExample.fetch_group_ids():
        assert group_id in ["topics", "group_title"]


def test_set_values_from_init():
    item = ItemExample(status_example=1, checkbox_example=True)
    assert item.status_example == 1
    assert item.checkbox_example == True
