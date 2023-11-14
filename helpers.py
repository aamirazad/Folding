import requests

def lookup_user(user):
    """Lookup user's states"""

    # Change username to id, then get data
    try:

        if not user.isnumeric():
            url = (
                f"https://api.foldingathome.org/search/user?query={user}"
            )

            user_data = (requests.get(url)).json()
            user_id = user_data[0]["id"]
        
        else:
            user_id = user

        url = (
            f"https://api.foldingathome.org/uid/{user_id}"
        )
        user_info = requests.get(url).json()
        return user_info

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

