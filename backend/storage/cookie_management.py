import json
import logging
import os

from backend.storage.storage_path_utils import get_or_create_ajs_cache
logger = logging.getLogger(__name__)


def _get_all_cookies(ajs_id):
    if ajs_id is None:
        logger.warning("_get_all_cookies called with empty ajs id")
        return None
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
    if ajs_id is None:
        logger.warning("save_cookie called with empty ajs id")
        return
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
        logger.error(f"Failed to save cookie with error {e}")

    logger.debug("Cookie saved successfully")

"""
Reads the value of a cookie, if the cookie is not found, return None
"""
def read_cookie(ajs_id, cookie):
    if ajs_id is None:
        logger.warning("read_cookie called with empty ajs id")
        return None
    existing_cookies = _get_all_cookies(ajs_id)
    if cookie not in existing_cookies:
        return None
    return existing_cookies[cookie]

def clear_cookies(ajs_id):
    if ajs_id is None:
        logger.warning("clear_cookies called with empty ajs id")
        return
    logger.info(f"Clearing cookies for {ajs_id}")
    path = get_or_create_ajs_cache(ajs_id)
    try:
        open(path + "cookies.json", 'w').close()
    except Exception as e:
        logger.error(f"Failed to clear cookies for: {ajs_id} with error: {e}")