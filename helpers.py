import simplejson as json
import requests
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

def get_db():
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE')}",
        connect_args={
            'ssl': {
                'ca': os.getenv('CERT', '/etc/ssl/cert.pem'),
            },
        }
    )
    db = scoped_session(sessionmaker(bind=engine))
    return db

def query_db(query, args=(), one=False):
    db = get_db()
    result = db.execute(text(query), args).fetchall()
    db.close()
    return result

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
        # If no user data is returned (invalid user) return None
        if not user_data:
            return None
        return user_data, user_id
    # If a web error happens return None
    except:
        return None

        
def save_user(user_id, score):
    """Save user data"""
    db = get_db().bind.raw_connection()
    cursor = db.cursor()
    cursor.execute('INSERT INTO user (user_id, score) VALUES (%s, %s)', (user_id, score))
    db.commit()
    cursor.close()
    db.close()
    return user_id

def lookup_user(user, save):
    """Lookup user's states"""
    # Query api for user data
    # Make sure an argument was given
    if user is None:
        return None
    result = get_user(user)
    if result is None:
        return None
    user_data, user_id = result
    # Add the user's score to the database if told to save
    if save == 'checked':
        save_user(user_id,user_data["score"])
    # Query the database for the user
    database = query_db('SELECT * FROM user WHERE user_id = :user_id', {'user_id': user_id}, one=True)
    formatted_database = []
    for row in database:
        formatted_row = []
        for value in row:
            if isinstance(value, datetime.datetime):
                formatted_row.append(value.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                formatted_row.append(value)
        formatted_database.append(formatted_row)
    logging.debug(formatted_database)
    auto_save()
    return formatted_database

def auto_save():
    # Get list of user's setup to be auto saved
    users = query_db('SELECT user_id FROM saves', one=True)
    for user in users:
        data = get_user(int(user['user_id']))

        if data is not None:
            save_user(user['user_id'], data[0]["score"])
