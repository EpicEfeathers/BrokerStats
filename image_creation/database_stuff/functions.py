import sqlite3
import time
import requests

class UserNotFoundError(Exception):
    pass

def init_db():
    conn = sqlite3.connect('image_creation/database_stuff/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    uid INTEGER
                );
            ''')
    conn.commit()
    conn.close()

def link_user(user_id, wb_uid):
    conn = sqlite3.connect('image_creation/database_stuff/users.db')
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
    conn = sqlite3.connect('image_creation/database_stuff/users.db')
    c = conn.cursor()

    c.execute("SELECT uid FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row:
        return row[0]
    else:
        raise UserNotFoundError(f"Discord user_id \"{user_id}\" not found in the database.")
    

def reset_uid(user_id):
    conn = sqlite3.connect('image_creation/database_stuff/users.db')
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()