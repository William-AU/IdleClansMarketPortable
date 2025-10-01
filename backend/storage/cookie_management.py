import json
import logging
import os

from backend.storage.storage_path_utils import get_or_create_ajs_cache
logger = logging.getLogger(__name__)


def _get_all_cookies(ajs_id):
    logger.debug("Getting all cookies")
    path = get_or_create_ajs_cache(ajs_id)
    logger.debug("Found AJS cache path")
    if not os.path.isfile(path + "cookies.json"):
        logger.info(f"No json data file exists for id: {ajs_id}")
        return {}
    try:
        with open(path + "cookies.json", 'r') as file:
            json_data = json.load(file)
            if json_data is None:
                logger.info(f"No cookie data found for {ajs_id}, returning " + "{}")
                return {}
            logger.debug(f"Returning cookie data: {json_data}")
            return json_data
    except Exception as e:
        logger.error(f"Failed to get all cookies with error: {e}")
        return None

def save_cookie(ajs_id, cookie, value):
    logger.info(f"Saving cookie with ID: {ajs_id}, Cookie: {cookie}, Value: {value}")
    path = get_or_create_ajs_cache(ajs_id)
    logger.debug("Getting existing cookies")
    existing_cookies = _get_all_cookies(ajs_id)
    logger.debug(f"Setting new cookie: {cookie} in existing cookies: {existing_cookies}")
    existing_cookies[cookie] = value
    logger.debug("Success")
    try:
        logger.debug(f"Dumping json cookies: {existing_cookies}")
        with open(path + "cookies.json", 'w') as file:
            json.dump(existing_cookies, file)
        logger.debug("Success")
    except Exception as e:
        logger.debug(f"Failed to save cookie with error {e}")

    logger.debug("Cookie saved successfully")

def read_cookie(ajs_id, cookie):
    existing_cookies = _get_all_cookies(ajs_id)
    return existing_cookies[cookie]