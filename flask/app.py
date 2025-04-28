# app.py
from flask import Flask, render_template, redirect, url_for
from forms import LoginForm,RegistrationForm
from config import Config
from db import mysql  # Import mysql from db.py
from services import check_user


from flask_mysqldb import MySQL
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "33510jaswal"  # Your MySQL password
MYSQL_DB = "wealthyinfyme"
MYSQL_PORT = 3306  # Default MySQL port
MYSQL_UNIX_SOCKET = '/path/to/your/mysql/socket'  # Only needed for Unix socket connections
SECRET_KEY = "This_is_a_super_secret_key"
MYSQL_CURSORCLASS = 'DictCursor'


app = Flask(__name__)
app.config.from_object(Config)

mysql=MySQL(app)  # Initialize MySQL with app

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        res = check_user(email, password)
        if res:
            msg = "successful"
        else:
            msg = "unsuccessful"

    return render_template("login.html", form=form, msg=msg)  # Pass msg to the template

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Get data from the form
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Insert user data into MySQL database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO registration (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template("registration.html", form=form)  

if __name__ == '__main__':
    app.run(debug=True)