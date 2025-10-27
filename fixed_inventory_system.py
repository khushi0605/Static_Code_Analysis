"""
A simple inventory management system script.

This module allows users to add, remove, and track items in an inventory.
The inventory data can be saved to and loaded from a JSON file.
"""

import json
from datetime import datetime

# Global variable
stock_data = {}


# FIX: (Pylint: invalid-name) Renamed from 'addItem' to 'add_item'
def add_item(item="default", qty=0, logs=None):
    """
    Adds a quantity of an item to the stock.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        print(f"Error: Invalid types for item ({type(item)}) "
              f"or qty ({type(qty)}). Skipping.")
        return

    if qty <= 0:
        print(f"Warning: Cannot add zero or negative quantity ({qty}) "
              f"for {item}. Skipping.")
        return

    if not item:
        print("Warning: Cannot add item with no name. Skipping.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


# FIX: (Pylint: invalid-name) Renamed from 'removeItem' to 'remove_item'
def remove_item(item, qty):
    """
    Removes a quantity of an item from the stock.
    """
    if not isinstance(item, str) or not isinstance(qty, int):
        print(f"Error: Invalid types for item ({type(item)}) "
              f"or qty ({type(qty)}). Skipping.")
        return

    if qty <= 0:
        print(f"Warning: Cannot remove zero or negative quantity ({qty}) "
              f"for {item}. Skipping.")
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Warning: Item '{item}' not found, cannot remove.")


# FIX: (Pylint: invalid-name) Renamed from 'getQty' to 'get_qty'
def get_qty(item):
    """
    Gets the quantity of a specific item.
    """
    return stock_data.get(item, 0)


# FIX: (Pylint: invalid-name) Renamed from 'loadData' to 'load_data'
def load_data(file="inventory.json"):
    """
    Loads inventory data from a JSON file.
    """
    # pylint: disable=global-statement
    # FIX: Disabling 'global-statement' warning.
    # This is necessary for this script's simple design.
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        print(f"Warning: {file} not found, starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        # FIX: (Pylint: line-too-long) Broke the long print statement
        print(f"Error: Could not decode {file}. File might be corrupt.")
        print("Starting with empty inventory.")
        stock_data = {}


# FIX: (Pylint: invalid-name) Renamed from 'saveData' to 'save_data'
def save_data(file="inventory.json"):
    """
    Saves the current inventory data to a JSON file.
    """
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data, indent=4))


# FIX: (Pylint: invalid-name) Renamed from 'printData' to 'print_data'
def print_data():
    """
    Prints a formatted report of all items in stock.
    """
    print("\n--- Items Report ---")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------\n")


# FIX: (Pylint: invalid-name) Renamed from 'checkLowItems' to 'check_low_items'
def check_low_items(threshold=5):
    """
    Returns a list of items with stock below the threshold.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """
    Main function to run the inventory system operations.
    """
    # FIX: Updated all function calls to use snake_case
    load_data()  # Load existing data first

    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")

    remove_item("apple", 3)
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    save_data()
    load_data()  # Reload to confirm save was successful
    print_data()

    print("eval used")


if __name__ == "__main__":
    main()

# FIX: (Pylint: missing-final-newline) This file now ends with a blank line.
# FIX: (Pylint: trailing-whitespace) All extra spaces at the end of lines are removed.