import simplejson as json
import requests
import sqlite3
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

def get_user(user):
    """Ping folding@home's api for user data"""
    # Make sure an argument was given
    if user is None:
        return None
    try:
        # Change to id if id is not given
        user_stats = query_api(f"/search/user?query={user}")
        # This would happen when 
        if user_stats == []:
            user_id = user
        else:
            user_id = user_stats[0]["id"]
        # Return user data
        user_data = query_api(f"/uid/{user_id}")
        return user_data, user_id
    # If a web error happens return None
    except:
        return None
    # Check to make sure that user exists
    if not user_data:
        return None
        
def save_user(user_id, score):
    """Save user data"""
    conn = get_db()
    conn.execute('INSERT INTO user (user_id,score) VALUES (?, ?)', (user_id,score),)
    conn.commit()
    conn.close()

def lookup_user(user, save):
    """Lookup user's states"""
    # Query api for user data
    # Make sure an argument was given
    if user is None:
        return None
    user_data, user_id = get_user(user)
    # Add the user's score to the database if told to save
    if save == 'checked':
        save_user(user_id,user_data["score"])
    # Query the database for the user
    database = query_db('SELECT * FROM user WHERE user_id = ?', [str(user_id)])
    database_dict = [dict(row) for row in database]
    # Render the username input form
    return database_dict

def auto_save():
    # Get list of user's setup to be auto saved
    logging.debug("autosave")
    users = query_db('SELECT user_id as user_id FROM saves')
    for user in users:
        logging.debug(f"USER ID {user['user_id']}")
        data = get_user(int(user['user_id']))
        logging.debug(data)
        save_user(user['user_id'], data[0]["score"])

def back_save():
    logging.debug("backsave")
    while True:
        auto_save()
        time.sleep(600)