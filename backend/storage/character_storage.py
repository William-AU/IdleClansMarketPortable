import json
import logging
import os
from datetime import datetime
from difflib import unified_diff

from backend.api.character import get_raw_data_for_character
from backend.storage.storage_path_utils import get_or_create_directory_for_player
from backend.storage.character_storage_context import CharacterContext

logger = logging.getLogger(__name__)


def get_character_context(username):
    fetch_and_store_data_for_player(username)
    return CharacterContext(username)


def fetch_and_store_data_for_player(username):
    """
    Fetch character data from API, save it to disk, and log changes.
    """

    # Fetch new data
    new_data = get_raw_data_for_character(username)
    if new_data is None:
        logger.error("NO DATA FOUND")
        raise Exception("Character not found")

    character_path = get_or_create_directory_for_player(username)
    if not os.path.isfile(character_path + "original_data.json"):
        original_data_file = os.path.join(character_path, "original_data.json")
    else:
        original_data_file = None
    data_file = os.path.join(character_path, "raw_data.json")
    log_file = os.path.join(character_path, "raw_data.log")

    # Load old data if available
    old_data = None
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            old_data = json.load(f)

    # Write new data to file
    with open(data_file, "w") as f:
        json.dump(new_data, f, indent=4)

    # If this is the first time we get data, we save it again as original data, this data will never get overwritten
    if original_data_file is not None:
        with open(original_data_file, "w") as f:
            json.dump(new_data, f, indent=4)

    # Log changes
    log_changes(log_file, fetch_and_store_data_for_player.__name__, old_data, new_data)


def log_changes(log_file, caller_function, old_data, new_data):
    """
    Compare old vs new JSON data and append a structured log entry.
    """
    # Generate diff summary
    if old_data is None:
        changes_summary = "Initial data created."
    else:
        old_json_str = json.dumps(old_data, sort_keys=True, indent=4)
        new_json_str = json.dumps(new_data, sort_keys=True, indent=4)
        diff_lines = list(unified_diff(
            old_json_str.splitlines(),
            new_json_str.splitlines(),
            fromfile="old",
            tofile="new",
            lineterm=""
        ))
        changes_summary = "\n".join(diff_lines) if diff_lines else "No changes detected."

    # Build log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "accessed_from": caller_function,
        "changes": changes_summary
    }

    # Append log entry to file
    with open(log_file, "a") as log:
        log.write(json.dumps(log_entry, indent=4) + "\n\n")


if __name__ == '__main__':
    fetch_and_store_data_for_player("Talhalla")
