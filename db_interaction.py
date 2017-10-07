import sqlite3
import collections
#name, lastname, email, password, username, verified

def check_user(email):
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    user = collections.namedtuple("user", "name, lastname, email, password, username, verified")
    final_list = map(user._make, list(cur.execute("SELECT name, lastname, email, password, username, verified from users")))
    cur.close()
    return any(i.email == email for i in final_list)
def add_user(*user_info):
    my_database = sqlite3.connect('userdata.db')
    my_database.execute("INSERT INTO users (name, lastname, email, password, username, verified) VALUES (?, ?, ?, ?, ?, ?)", user_info)
    my_database.commit()
    my_database.close()

def is_verified(email):
    pass
