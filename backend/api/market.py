import json
import time

import requests
from configuration import constants
from datetime import datetime
from backend.storage.storage_path_utils import get_cache_path


def is_cache_too_old(timestamp):
    time_obj = datetime.strptime(timestamp, constants.TIME_FORMAT_STRING)
    now = datetime.now()
    return (now - time_obj) > constants.CACHE_REFRESH_TIME


def check_if_cached(item_id, path_prefix=get_cache_path()):
    try:
        with open(f"{path_prefix}{item_id}", 'r') as f:
            data = json.load(f)
            if is_cache_too_old(data["timestamp"]):
                return None
            return data
    except FileNotFoundError:
        return None


def cache_data(item_id, data, path_prefix=get_cache_path()):
    data["timestamp"] = datetime.now().strftime(constants.TIME_FORMAT_STRING)
    with open(f"{path_prefix}{item_id}", 'w') as f:
        json.dump(data, f, indent=4)


def _fetch_and_cache(url, cache_id, cache_path_prefix):
    """
    Helper function to fetch data from URL, handle rate limiting,
    and cache the result.
    """
    cached_data = check_if_cached(cache_id, cache_path_prefix)
    if cached_data is not None:
        return cached_data

    response = requests.get(url)

    if response.status_code == 429:
        print("Rate limit reached, waiting 3 minutes to ensure new slot")
        time.sleep(60 * 3)
        return _fetch_and_cache(url, cache_id, cache_path_prefix)

    print(response)
    data = response.json()
    cache_data(cache_id, data, cache_path_prefix)
    return data


def get_info(item_id, cache_path_prefix=get_cache_path()):
    """
    Fetch basic item info with caching.
    """
    url = f"https://query.idleclans.com/api/PlayerMarket/items/prices/latest/{item_id}"
    return _fetch_and_cache(url, item_id, cache_path_prefix)


def get_detailed_info(item_id, cache_path_prefix=get_cache_path()):
    """
    Fetch comprehensive item info with caching.
    """
    cache_id = f"{item_id}_COMPREHENSIVE"
    url = f"https://query.idleclans.com/api/PlayerMarket/items/prices/latest/comprehensive/{item_id}"
    return _fetch_and_cache(url, cache_id, cache_path_prefix)
