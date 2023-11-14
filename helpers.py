import requests

def lookup_user(user):
    """Lookup user's states"""

    # Change username to id, then get data

    if not user.isnumeric():
        url = (
            f"https://api.foldingathome.org/search/user?query={user}"
        )

        user_data = (requests.get(url)).json()
        user_id = user_data[0]["id"]
    
    url = (
        f"https://api.foldingathome.org/uid/{user_id}"
    )
    user_info = requests.get(url).json()
    return user_info


        
    # Folding@home API
    url = ()

    # # Query API
    # try:
    #     response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
    #     response.raise_for_status()

    #     # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
    #     quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
    #     quotes.reverse()
    #     price = round(float(quotes[0]["Adj Close"]), 2)
    #     return {
    #         "name": symbol,
    #         "price": price,
    #         "symbol": symbol
    #     }
    # except (requests.RequestException, ValueError, KeyError, IndexError):
    #     return None