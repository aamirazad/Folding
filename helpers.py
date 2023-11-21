import simplejson as json
import requests
import sqlite3

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def lookup_user(user):
    """Lookup user's states"""
    # Make sure an argument was given
    if user is None:
        return None
    # Change username to id, then get data
    try:
        if not user.isnumeric():
            url = (
                f"https://api.foldingathome.org/search/user?query={user}"
            )

            user_stats = (requests.get(url)).json()
            user_id = user_stats[0]["id"]
        else:
            user_id = user
        url = (
            f"https://api.foldingathome.org/uid/{user_id}"
        )
        user_data = requests.get(url).json()
    # If a web error happens
    except:
        return None
    # Check to make sure that user exists
    if not user_data:
        return None
    # Add the user's score to the database
    conn = get_db()
    # conn.execute('INSERT INTO user (score, user_id) VALUES (?, ?)', (user_data["score"],user_data['id']),)
    conn.commit()
    conn.close()
    # Query the database for the user
    database = query_db('SELECT * FROM user WHERE user_id = ?', [user_data["id"]])
    database_dict = [dict(row) for row in database]
    # Render the username input form
    return database_dict

