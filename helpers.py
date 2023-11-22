import simplejson as json
import requests
import sqlite3
from datetime import datetime
import logging

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Base api handling
def query_api(args):
    url = (
        f"https://api.foldingathome.org{args}"
    )
    return requests.get(url).json()

def lookup_user(user, save):
    """Lookup user's states"""
    # Make sure an argument was given
    if user is None:
        return None
    try:
        # Change to id if id is not given
        if not user.isnumeric():
            user_stats = query_api(f"/search/user?query={user}")
            user_id = user_stats[0]["id"]
        else:
            user_id = user
        # Get user data
        user_data = query_api(f"/uid/{user_id}")
    # If a web error happens return None
    except:
        return None
    # Check to make sure that user exists
    if not user_data:
        return None
    # Check when the last save took place
    # database = query_db('SELECT * FROM user WHERE user_id = ?', [str(user_id)])
    # date = datetime.utcnow()
    # formatted = date.strftime('%F %T')
    # diff = formatted - database[0]["date"]
    # logging.debug(diff)
    # Add the user's score to the database if told to save
    if save == 'checked':
        conn = get_db()
        conn.execute('INSERT INTO user (score, user_id) VALUES (?, ?)', (user_data["score"],user_id),)
        conn.commit()
        conn.close()
    # Query the database for the user
    database = query_db('SELECT * FROM user WHERE user_id = ?', [str(user_id)])
    database_dict = [dict(row) for row in database]
    # Render the username input form
    return database_dict

