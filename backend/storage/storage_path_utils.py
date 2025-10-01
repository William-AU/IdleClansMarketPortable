import os
import platform

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


"""
Gets the directory containing information for a given player, created if it does not exist
"""


def get_or_create_directory_for_player(username):
    base_path = get_base_path()
    all_users_path = base_path + "players/"
    create_if_absent(all_users_path)
    player_path = all_users_path + username + "/"
    create_if_absent(player_path)
    return player_path


"""
Gets the directory used for storing session data
"""


def get_or_create_ajs_cache(ajs_id):
    base_path = get_base_path()
    session_cache_path = base_path + "session_cache/"
    create_if_absent(session_cache_path)
    ajs_id_path = session_cache_path + ajs_id + "/"
    create_if_absent(ajs_id_path)
    return ajs_id_path


"""
Dirty hack to get the log path, should only ever be called on the raspberry pie, as windows is only ever used for debugging (logging set to std.err) 
"""


def get_or_create_log_path():
    if platform.system() == "Windows":
        return None
    path = "~/IdleClans/IdleClansMarketPortable/logs/"
    create_if_absent(path)
    return path


def create_if_absent(path):
    if not os.path.isdir(path):
        os.mkdir(path)
