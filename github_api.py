import requests

BASE_DOMAIN = "https://api.github.com"


def get_user_info(username):
    url = f"{BASE_DOMAIN}/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
