import requests

"""
Gets raw data dump from the API for the user, note: Case sensitive
Returns None if the character is not found
"""
def get_raw_data_for_character(username):
    response = requests.get(f"https://query.idleclans.com/api/Player/profile/{username}")
    if response.status_code != 200:
        return None
    return response.json()

if __name__ == '__main__':
    print(get_raw_data_for_character("Talhalla"))