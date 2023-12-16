import simplejson as json
import requests
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging
import datetime
import time

# Setup logging
if os.getenv('LOGGING') == True:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)

load_dotenv()

def get_db():
    engine = create_engine(
        f"mysql+pymysql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE')}",
        echo=os.getenv('LOGGING') == 'True',
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
    result = db.execute(text(query), args)
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

        
def save_user(user_id, score, day=False):
    """Save user data"""
    if day == True:
        query_db('INSERT INTO user (user_id, score, day) VALUES (:user_id, :score, True)', {'user_id': user_id, 'score': score})
    else:
        query_db('INSERT INTO user (user_id, score) VALUES (:user_id, :score)', {'user_id': user_id, 'score': score})
    return

def lookup_user(user, save=False):
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
    if save is True:
        save_user(user_id,user_data["score"])
    # Query the database for the user
    database = query_db('SELECT * FROM user WHERE user_id = :user_id', {'user_id': user_id}, one=True)
    # Replace datetime with the actual date
    formatted_database = []
    for row in database:
        formatted_row = []
        for value in row:
            if isinstance(value, datetime.datetime):
                formatted_row.append(value.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                formatted_row.append(value)
        formatted_database.append(formatted_row)
    return formatted_database

def calculate_daily(user):
    # Get user_id and error check
    if user is None:
        return None
    result = get_user(user)
    if result is None:
        return None
    user_data, user_id = result
    # Query the database for all of the daily saves for the user
    database = query_db('SELECT * FROM user WHERE user_id = :user_id AND day=True', {'user_id': user_id}, one=True)
    # Calculate the difference between every two days
    start_score = None
    daily_stats = []
    daily_days = []
    for item in database:
        if start_score is None:
            start_score = item[2]
        else:
            difference = item[2] - start_score
            start_score = None
            daily_stats.append(difference)
            daily_days.append(item[1].strftime('%Y-%m-%d %H:%M:%S'))
    dictionary = dict(zip(daily_days,daily_stats))
    return dictionary

def auto_save(day=False):
    # Get list of user's setup to be auto saved
    users = query_db('SELECT user_id FROM saves', one=True)
    for user in users:
        time.sleep(10)
        data = get_user(user[0])
        if data is not None:
            save_user(user[0], data[0]['score'])

def daily_save():
    users = query_db('SELECT user_id FROM saves', one=True)
    for user in users:
        time.sleep(10)
        data = get_user(user[0])
        if data is not None:
            # Mark the save as a day save
            save_user(user[0], data[0]['score'], day=True)
