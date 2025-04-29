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

def registration(name,email,password,confirm_password):
    if(password==confirm_password):
        con=mysql.connect
        cur=con.cursor()
        cur.execute("insert into registration(name,email,password) values(%s,%s,%s)",(name,email,password))
        con.commit()
        cur.close()
        con.close()
        return True
    else:
        return False
