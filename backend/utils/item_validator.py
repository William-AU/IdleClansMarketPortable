import json
import logging

logger = logging.getLogger(__name__)

def validate(item_name, path="../data/item_ids.json"):
    if item_name == "NONE":
        return True
    with open(path, 'r') as file:
        data = json.load(file)
        for entry in data:
            if entry["name_id"] == item_name:
                return True
        return False


def verify_id(name, item_id):
    with open("../data/raw_data_dump", 'r') as file:
        for line in file:
            return f'"ItemId" : {item_id}, "Name" : "{name}"' in line
        return None


def verify_ids():
    with open("../data/item_ids.json", 'r') as file:
        data = json.load(file)
        for item in data:
            name = item["name_id"]
            item_id = item["itemId"]
            verify = verify_id(name, item_id)
            if not verify:
                logger.error(f"Failed to verify ({name}, {item_id})")
