# [Monday Item Parser](https://github.com/avivatedgi/monday-item-parser)

[![Tests](https://github.com/avivatedgi/monday-item-parser/actions/workflows/tests.yml/badge.svg)](https://github.com/avivatedgi/monday-item-parser/actions/workflows/tests.yml) [![PyPI version](https://badge.fury.io/py/monday-item-parser.svg)](https://badge.fury.io/py/monday-item-parser)

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

* 0.2.0 (2021-01-14) - Updated the item's field value set method to be explicit (without calling `.value`)
* 0.1.2 (2021-01-13) - Fixed a small bug in the `Item::__init__` function
* 0.1.1 (2021-01-13) - Still first release, but got some problems with PyPI and Github Workflows
* 0.1.0 (2021-01-13) - First release

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

item = ItemExample()

# Setting the values of an item
item.item_name = "Aviv Atedgi"
item.status_example = "Working on it"
item.date_example = datetime.now()
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
```

## Special Thanks

* [Hydration](https://github.com/shustinm/hydration) ([Michael Shustin](https://github.com/shustinm/)) For the idea of the items metaclass
* [Monday](https://github.com/ProdPerfect/monday) ([ProdPerfect](https://github.com/ProdPerfect)) For the Monday client use in the library