# services.py
from db import mysql  

def check_user(email, password):
    con = mysql.connect
    cur = con.cursor()
    cur.execute("SELECT * FROM login WHERE email=%s AND password=%s", (email, password))
    res = cur.fetchone()
    cur.close()
    con.close()

    if res:
        return True
    return False

