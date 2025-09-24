from utils.item_validator import validate
import json


def lookup_item(item_name, item_ids_path="data/item_ids.json"):
    if item_name == "NONE":
        return -1
    if not validate(item_name, item_ids_path):
        raise Exception(f"Unknown item name {item_name}")
    with open(item_ids_path, "r") as file:
        data = json.load(file)
        for entry in data:
            if entry["name_id"] == item_name:
                return entry["itemId"]
        raise Exception(f"Unable to find id for known item name {item_name}")