import sqlite3
import requests
from datetime import datetime

class UserNotFoundError(Exception):
    pass

def init_db():
    """
    Initializes db (if needed)
    """

    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    uid INTEGER
                );
            ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS message_counts (
            user_id INTEGER,
            year INTEGER,
            message_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, year),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    ''')


    conn.commit()
    conn.close()

def link_user(user_id, wb_uid):
    """
    Links a WB uid to a Discord uid
    """
    
    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row:
        # Update the potatoes count if the user exists
        c.execute("UPDATE users SET uid = ? WHERE user_id = ?", (wb_uid, user_id))
    else:
        stats = requests.get(f"https://wbapi.wbpjs.com/players/getPlayer?uid={wb_uid}").json()
        try:
            stats["uid"]
        except:
            raise UserNotFoundError
        # Insert a new user with the potato count
        c.execute("INSERT INTO users (user_id, uid) VALUES (?, ?)", (user_id, wb_uid))

    conn.commit()
    conn.close() 
        
def fetch_uid(user_id):
    """
    Fetch's users WB uid using Discord uid (if linked)"""
    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()

    c.execute("SELECT uid FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row:
        return row[0]
    else:
        raise UserNotFoundError(f"Discord user_id \"{user_id}\" not found in the database.")
    

def reset_uid(user_id):
    """
    Completely resets a player's message count
    """

    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()

    c.execute("DELETE FROM message_counts WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()


def add_message_to_uid(user_id):
    """
    Adds 1 to the user's message count.
    """

    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()

    year = datetime.now().year # get current year
    
    c.execute('''
        INSERT INTO message_counts (user_id, year, message_count)
        VALUES (?, ?, 1)
        ON CONFLICT(user_id, year) DO UPDATE SET
        message_count = message_count + 1;
    ''', (user_id, year))

    conn.commit()
    conn.close()


def fetch_message_count_by_uid(user_id, year=None):
    """
    Gets user's message count, using their discord uid.
    Optional argument year, which returns their count for that year.
    """

    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()

    if year:
        c.execute("SELECT message_count FROM message_counts WHERE user_id = ? AND year = ?", (user_id, year))
    else:
        c.execute("SELECT SUM(message_count) FROM message_counts WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row:
        return row[0]
    
    raise UserNotFoundError(f"Discord user_id \"{user_id}\" not found in the database.")

def reset_message_count(user_id, year):
    """
    Resets a user's message count for the specified year.
    """

    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()

    c.execute("UPDATE message_counts SET message_count = 0 WHERE user_id = ? AND year = ?", (user_id, year))

    conn.commit()
    conn.close()

def message_count(year:int=None):
    """
    Gets the total message count. 
    Can specify year, else returns total
    """

    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()

    if year:
        c.execute("SELECT SUM(message_count) FROM message_counts WHERE year = ?", (year,))
    else:
        c.execute("SELECT SUM(message_count) FROM message_counts")

    total_messages = c.fetchone()[0] # returns as e.g. (500,). Isolates value

    if total_messages is None: # if no messages, it will return None
        total_messages = 0

    return total_messages

def total_users():
    """
    Returns total users from db, along with their id's
    """

    conn = sqlite3.connect('utils/database_stuff/users.db')
    c = conn.cursor()

    c.execute("SELECT DISTINCT user_id FROM message_counts")

    user_ids = c.fetchall()

    c.execute("SELECT COUNT(DISTINCT user_id) FROM message_counts")

    total_users = c.fetchone()[0]

    return total_users, user_ids