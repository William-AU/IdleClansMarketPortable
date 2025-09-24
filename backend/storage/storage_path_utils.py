import os

"""
Looks for NAS storage if available, defaults to local storage otherwise
Specifically looks for the mounted drive /mnt/data/, otherwise defaults to the local_storage directory in the project directory
Returns a string path to the storage directory
"""
def get_base_path():
    if os.path.isdir("/mnt/data/"):
        return "/mnt/data/"
    return "local_storage/"

"""
Gets the string path to the cache location, creates the directory if it does not already exist
"""
def get_cache_path():
    base_path = get_base_path()
    cache_path = base_path + "cache/"
    if os.path.isdir(cache_path):
        return cache_path
    os.mkdir(cache_path)
    return cache_path

