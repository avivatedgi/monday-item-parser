import pytest

from datetime import datetime
from monday import MondayClient
from monday_item_parser import *

from .helpers import client, testing_board_id, retry_in_case_of_budget_exhausted


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
    date_example = DateField(include_time=False)
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
    item.status_example = StatusField(7)
    assert item.status_example.value == 7


def test_add_attribute():
    item = ItemExample()

    with pytest.raises(AttributeError):
        item.new_attribute_should_fail = StatusField()


def test_item_update_hook():
    class ItemWithFieldHook(Item, monday_client=client, board_id=testing_board_id):
        status_example = StatusField

        @field_updated_hook(status_example)
        def status_example_hook(self):
            if self.status_example.value is not None:
                self.status_example.value += 1
            else:
                self.status_example.value = 0

    item = ItemWithFieldHook()
    item.status_example.value = 5
    assert item.status_example.value == 5
    item.status_example = 5
    assert item.status_example.value == 6


def test_set_values_from_init():
    item = ItemExample(status_example=1, checkbox_example=True)
    assert item.status_example.value == 1
    assert item.checkbox_example.value == True


def test_create_item_then_duplicate_it_and_update_it():
    item = ItemExample()
    item.item_name = "Aviv Atedgi"
    item.status_example = "Working on it"
    item.date_example = datetime.strptime("2000-05-01", "%Y-%m-%d")
    item.checkbox_example = True
    item.country_example = "IL"
    item.email_example = "aviv.atedgi2000@gmail.com"
    item.link_example.url = "https://www.github.com/avivatedgi"
    item.link_example.text = "My Github Profile"
    item.numbers_example = 192.4
    item.people_example = [Person(25200525)]
    item.phone_example.country_code = "IL"
    item.phone_example.phone = "0501234567"
    item.tags_example = [12808387]
    item.text_example = "My Cool Text Example"
    item.timeline_example.start = datetime.strptime("2000-05-01", "%Y-%m-%d")
    item.timeline_example.end = datetime.now()
    retry_in_case_of_budget_exhausted(lambda: item.create_item("topics"))

    new_item = item.duplicate_item()
    new_item.item_name = "Omri Siniver"
    new_item.status_example = 2
    new_item.date_example = datetime.now()
    new_item.checkbox_example = False
    new_item.country_example = "US"
    new_item.email_example = "omrisiniver@gmail.com"
    new_item.link_example = LinkField(url="https://www.google.com", text="Google It")
    new_item.numbers_example = 154
    new_item.people_example = [Person(20106356)]
    new_item.phone_example = PhoneField(phone="12123123123", country_code="US")
    new_item.tags_example = [12808388]
    new_item.text_example = "YES"
    new_item.timeline_example = TimelineField(
        start=datetime.strptime("2005-04-12", "%Y-%m-%d"),
        end=datetime.now(),
    )
    retry_in_case_of_budget_exhausted(new_item.update_item)


@pytest.mark.parametrize(
    "column_id,column_value",
    [
        ("status_example", "Stuck"),
        ("date_example", datetime.now()),
        # ("checkbox_example", None), # Unsupported field
        ("country_example", "US"),
        ("email_example", "omrisiniver@gmail.com"),
        ("link_example", Link(text="Google It")),
        ("numbers_example", 154),
        ("phone_example", Phone(phone="12123123123")),
        ("text_example", "YES"),
        (
            "timeline_example",
            Timeline(
                start=datetime.strptime("2005-04-12", "%Y-%m-%d"),
                end=datetime.now(),
            ),
        ),
    ],
)
def test_get_items_by_column_value(column_id, column_value):
    x = retry_in_case_of_budget_exhausted(
        lambda: ItemExample.fetch_items_by_column_value(**{column_id: column_value})
    )

    assert (
        retry_in_case_of_budget_exhausted(lambda: next(x)).item_name == "Omri Siniver"
    )
    with pytest.raises(StopIteration):
        retry_in_case_of_budget_exhausted(lambda: next(x))


def test_fetch_items_and_delete():
    for item in retry_in_case_of_budget_exhausted(ItemExample.fetch_items_from_board):
        retry_in_case_of_budget_exhausted(item.delete_item)


def test_fetch_group_ids():
    for group_id in retry_in_case_of_budget_exhausted(ItemExample.fetch_group_ids):
        assert group_id in ["topics", "group_title"]
