# app.py
from flask import Flask, render_template, redirect, url_for,request
from forms import LoginForm,RegistrationForm
from config import Config
from db import mysql  # Import mysql from db.py
from services import check_user,registration
from pymongo import MongoClient
from datetime import datetime
import urllib.parse

from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_object(Config)

mysql=MySQL(app)  # Initialize MySQL with app     

# MongoDB Configuration
username = urllib.parse.quote_plus("anurag1049be21")
password = urllib.parse.quote_plus("Bruno@9988")
mongo_uri = f"mongodb+srv://{username}:{password}@mongoclustert.qb8fbj8.mongodb.net/?retryWrites=true&w=majority&appName=MongoClustert"

mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client["wealthyfyme"]
mongo_transactions = mongo_db["transactions"]

CATEGORIES = [
    "Food", "Housing", "Transportation", "Entertainment", 
    "Shopping", "Utilities", "Healthcare", "Education"
]


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
            return redirect(url_for('dashboard'))
        else:
            msg = "unsuccessful"

    return render_template("login.html", form=form, msg=msg)  # Pass msg to the template


@app.route('/register', methods=["GET", "POST"])
def register():
    msg=''
    form = RegistrationForm()
    if form.validate_on_submit():
        # Get data from the form
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Insert user data into MySQL database
        res = registration(name, email, password, confirm_password)
        if res:
            return redirect(url_for('login'))
        else:
            msg="Please, Enter Validate Mail !!!"
        

    return render_template("registration.html", form=form,msg=msg)


@app.route('/dashboard')
def dashboard():
    # Fetch transactions from MongoDB
    mongo_transactions_list = mongo_transactions.find().sort("date", -1).limit(8)

    transactions = []
    for txn in mongo_transactions_list:
        try:
            parsed_date = datetime.strptime(txn.get("date", ""), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            parsed_date = datetime.min.date()  # fallback if invalid/missing

        transactions.append({
            "date": parsed_date,
            "category": txn.get("category", "No Category"),
            "description": txn.get("description", "No description"),
            "amount": txn.get("amount", 0.0)
        })

    # Calculate total amount and category totals
    total_amount = sum(txn["amount"] for txn in transactions)
    category_totals = {}
    for txn in transactions:
        category = txn["category"]
        category_totals[category] = category_totals.get(category, 0) + txn["amount"]

    category_summary = [{"category": cat, "total": amount} for cat, amount in category_totals.items()]
    category_summary.sort(key=lambda x: x["total"], reverse=True)

    return render_template(
        'dashboard.html',
        transactions=transactions,
        total_amount=total_amount,
        category_totals=category_summary,
        categories=CATEGORIES
    )


@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"]
        date = request.form["date"]

        mongo_transactions.insert_one({
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        })

        return redirect("/transactions")

    mongo_transactions_list = mongo_transactions.find().sort("date", -1)

    transactions = []
    for txn in mongo_transactions_list:
        try:
            parsed_date = datetime.strptime(txn.get("date", ""), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            parsed_date = datetime.min.date()

        transactions.append({
            "date": parsed_date,
            "category": txn.get("category", "No Category"),
            "description": txn.get("description", "No description"),
            "amount": txn.get("amount", 0.0)
        })

    return render_template("transactions.html", transactions=transactions)

@app.route("/api/summary", methods=["GET"])
def summary():
    mongo_transactions_list = mongo_transactions.find()

    income = 0.0
    expenses = 0.0

    for txn in mongo_transactions_list:
        amount = txn.get("amount", 0.0)
        if amount >= 0:
            income += amount
        else:
            expenses += abs(amount)

    balance = income - expenses

    return {
        "balance": balance,
        "income": income,
        "expenses": expenses
    }






if __name__ == '__main__':
    app.run(debug=True)