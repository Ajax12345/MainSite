import sqlite3
import collections
#name, lastname, email, password, username, verified
#COMMITTED: added set_verified() and delete_user() functions
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
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    user = collections.namedtuple("user", "name, lastname, email, password, username, verified")
    final_list = map(user._make, list(cur.execute("SELECT name, lastname, email, password, username, verified from users")))
    cur.close()
    return any(i.email == email and i.verified == "yes" for i in final_list)

def get_user_name(email, password):
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    user = collections.namedtuple("user", "name, lastname, email, password, username, verified")
    final_list = map(user._make, list(cur.execute("SELECT name, lastname, email, password, username, verified from users")))
    cur.close()
    return [i.name for i in final_list if i.email == email and i.password == password and i.verified == "yes"]
def get_username(email, password):
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    user = collections.namedtuple("user", "name, lastname, email, password, username, verified")
    final_list = map(user._make, list(cur.execute("SELECT name, lastname, email, password, username, verified from users")))
    cur.close()
    return [i.username for i in final_list if i.email == email and i.password == password]

def set_verified(email):
    conn = sqlite3.connect("userdata.db")

    conn.execute("UPDATE users SET verified = 'yes' WHERE email = ?", (email,))
    conn.commit()
    conn.close()


def delete_user(email):
    conn = sqlite3.connect("userdata.db")

    #"DELETE FROM users WHERE email=?", (email)
    conn.execute("DELETE FROM users WHERE email=(?)", (email,))
    conn.commit()
    conn.close()

def get_email_list(): #is generator expression
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    user = collections.namedtuple("user", "name, lastname, email, password, username, verified")
    final_list = map(user._make, list(cur.execute("SELECT name, lastname, email, password, username, verified from users")))
    cur.close()
    for i in final_list:
        yield i.email
