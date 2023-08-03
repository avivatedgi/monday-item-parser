# [Monday Item Parser](https://github.com/avivatedgi/monday-item-parser)

[![Tests & Deploy to PyPI](https://github.com/avivatedgi/monday-item-parser/actions/workflows/deploy_pypi.yml/badge.svg)](https://github.com/avivatedgi/monday-item-parser/actions/workflows/deploy_pypi.yml) [![PyPI version](https://badge.fury.io/py/monday-item-parser.svg)](https://badge.fury.io/py/monday-item-parser)

## Introduction

[Monday Item Parser](https://github.com/avivatedgi/monday-item-parser) is a library used to define [Monday](www.monday.com) items structure in a specific board, and lets the user fetch, create, update and delete items from this board.

## Installation

```bash
pip install monday-item-parser
```

## Requirements

* Python >= 3.7
* [Monday library](https://github.com/ProdPerfect/monday) for the Mondayhttp client

## Changelog

* 0.2.13 (2023-08-03) - Added support for fetching group titles, and added the `group_title` to the `Item` class
* 0.2.12 (2023-08-03) - Added support for the Location field
* 0.2.10 (2022-09-08) - Added support for the Dropdown field and updated the monday library version
* 0.2.9 (2022-04-22) - Fixed a bug in Long Text field
* 0.2.8 (2022-04-22) - Added support for Long Text field
* 0.2.7 (2022-03-30) - Bumped version because of workflow problems (again :()
* 0.2.5 (2022-03-30) - Added mirror field to readme.
* 0.2.4 (2022-03-30) - Added support for mirror (lookup) fields.
* 0.2.3 (2021-01-16) - Same as 0.2.2, but got some problems with PyPI and Github Workflows again. :(
* 0.2.2 (2021-01-16) - Added support for [search items by column value](https://api.developer.monday.com/docs/items-by-column-values-queries)
* 0.2.1 (2021-01-16) - Added hooks for field values.
* 0.2.0 (2021-01-14) - Updated the item's field value set method to be explicit (without calling `.value`)
* 0.1.2 (2021-01-13) - Fixed a small bug in the `Item::__init__` function
* 0.1.1 (2021-01-13) - Still first release, but got some problems with PyPI and Github Workflows
* 0.1.0 (2021-01-13) - First release

## Todo List

* [ ] Create `fetch_groups` function to an item that returns the id along with the group title
* [ ] Add to the `create_item` function the option to add the item to a group by its title, not by id
* [ ] Add custom exceptions for common errors:
  * [ ] Budget Exhausted Error
  * [ ] Invalid Group Id (in item creation)

## How to use

### Items

Items are the full board item structure, built from fields.

```python
from monday import MondayClient
from monday_item_parser import Item, CheckboxField


board_id = 1234
monday_client = MondayClient("MONDAY_API_KEY_HERE")


class MyItem(Item, board_id=board_id, monday_client=monday_client):
    checkbox_example = CheckboxField()

    # Can be declared either as a type or as an instance, so this is good as well:
    checkbox_example = CheckboxField
```

**NOTE:** The variables in your item class must be named EXACTLY the same as in your monday board but in lower-case and replace spaces into underscore. For example a column in Monday with the name `My Nice Column` will must be defined in your item class `my_nice_column`.

#### Fetch items from board

```pycon
>>> for item in ExampleItem.fetch_items_from_board():
>>>     print(item)
```

![Items Preview](docs/images/items-print.png)

#### Fetch items by column value

You can fetch all of the items from board by a specific column value filter.

```python
# Let's filter all of the items with a Status column named "status_example" that holds the label "Done"
for item in ExampleItem.fetch_items_by_column_value(status_example="Done"):
    print(item)
```

More info about supported and unsupported fields you can search by [here](https://api.developer.monday.com/docs/items-by-column-values-queries).

| Field Type | Field Value to Search By |
| ---------- | ------------------------ |
| Text | `str` The text to search |
| Status | `str` The label to search |
| Numbers | Either `int` or `float`. The value to search |
| Date | `datetime.datetime` The date (year, month and day) to search by |
| Phone | `Phone` (internal library class) The phone number to search by |
| Country | `str` The country code to search by |
| Email | `str` The email to search by |
| Timeline | `Timeline` (internal library class) The start and end date to search by |
| Link | `Link` (internal library class) The display text (not the actual url link) to search by |
| Mirror | `str` The text to search |
| Long Text | `str` The text to search |

#### Create Item

**NOTE:** You can only create an item that isn't fetched from the board / already created using this exact function. If you want to create a new item that was fetched from the board you should use the `duplicate_item` function

```pycon
>>> item = MyItem(checkbox_example=True)
>>> item.name = "My First Example"
>>> item.create_item()
```

#### Duplicate Item

**NOTE:** You can only duplicate an item that was fetched from the board / created by the `create_item` function.

```pycon
>>> new_item = item.duplicate_item()
```

#### Update Item

**NOTE:** You can only update an item that was fetched from the board / created by the `create_item` function.

```pycon
>>> new_item.name = 'Updated Item'
>>> new_item.checkbox_example = False
>>> new_item.update_item()
```

#### Delete Item

**NOTE:** You can only delete an item that was fetched from the board / created by the `create_item` function.

```pycon
>>> new_item.delete_item()
```

#### Get Group Ids in Board

```pycon
>>> for group_id in ItemExample.fetch_group_ids():
>>>     print(group_id)
"topics"
"group_title"
```

#### Hook Field Values

A hook can be registered for whenever the value on a specific field is changed.

```python
from monday_item_parser import *

class ItemWithFieldHook(Item, monday_client=client, board_id=testing_board_id):
    status_example = StatusField
    checkbox_example = CheckboxField

    @field_updated_hook(status_example)
    def status_example_hook(self):
        if self.status_example.value is not None:
            # In the hook you must update the value with the
            # `.value` attribute if you don't want to trigger the hook again
            self.status_example.value += 1
        else:
            self.status_example.value = 0

item = ItemWithFieldHook()
# Trigger the hook by setting the value WITHOUT the `.value` attribute
item.status_example = 5
assert item.status_example.value == 6
```

### Fields

Field is actually an Monday board's item column. The currently supported types are:

| Monday Column Type | Library Class Name |
| ------------------ | ------------------ |
| Checkbox | `CheckboxField` |
| Country | `CountryField` |
| Date | `DateField` |
| Email | `EmailField` |
| Link | `LinkField` |
| Number | `NumberField` |
| People | `PeopleField` |
| Phone | `PhoneField` |
| Status | `StatusField` |
| Tags | `TagsField` |
| Text | `TextField` |
| Timeline | `TimelineField` |
| Mirror | `MirrorField` |
| Long Text | `LongTextField` |

#### Full Example

```python
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
	mirror_example = MirrorField
    long_text_example = LongTextField

item = ItemExample()

# Setting the values of an item
item.item_name = "Aviv Atedgi"
item.status_example = "Working on it"
item.date_example = datetime.now()
item.checkbox_example = True
item.country_example = "IL"
item.email_example = "aviv.atedgi2000@gmail.com"
item.link_example.value.url = "https://www.github.com/avivatedgi"
item.link_example.value.text = "My Github Profile"
item.link_example = LinkField(url="https://www.google.com", text="Google It")
item.numbers_example = 192.4
item.people_example = [Person(25200525)]
item.phone_example.value.country_code = "IL"
item.phone_example.value.phone = "0501234567"
item.phone_example = PhoneField(phone="12123123123", country_code="US")
item.tags_example = [12808387]
item.text_example = "My Cool Text Example"
item.timeline_example.value.start = datetime.strptime("2000-05-01", "%Y-%m-%d")
item.timeline_example.value.end = datetime.now()
item.timeline_example = TimelineField(
    start=datetime.strptime("2005-04-12", "%Y-%m-%d"),
    end=datetime.now(),
)
item.long_text_example = "Hello\nWorld"

# Getting the values of an item
print("Status Example =", item.status_example.value)
print("Date Example =", item.date_example.value)
print("Checkbox Example =", item.checkbox_example.value)
print("Country Example =", item.country_example.value)
print("Email Example =", item.email_example.value)
print("Link Example URL =", item.link_example.value.url)
print("Link Example Text =", item.link_example.value.text)
print("Numbers Example =", item.numbers_example.value)
print("People Example =", item.people_example.value)
print("Phone Example Country Code =", item.phone_example.value.country_code)
print("Phone Example Phone Number =", item.phone_example.value.phone)
print("Tags Example =", item.tags_example.value)
print("Text Example =", item.text_example.value)
print("Timeline Example Start Date =", item.timeline_example.value.start)
print("Timeline Example End Date =", item.timeline_example.value.end)
print("Mirror Example = ", item.mirror_example.value)
print("Long Text Example = ", item.long_text_example.value)
```

## Special Thanks

* [Hydration](https://github.com/shustinm/hydration) ([Michael Shustin](https://github.com/shustinm/)) For the idea of the items metaclass
* [Monday](https://github.com/ProdPerfect/monday) ([ProdPerfect](https://github.com/ProdPerfect)) For the Monday client use in the library
