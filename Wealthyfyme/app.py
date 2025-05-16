# app.py
from flask import Flask, render_template, redirect, url_for,request
from forms import LoginForm,RegistrationForm
from config import Config
from db import mysql  # Import mysql from db.py
from services import check_user,registration
from pymongo import MongoClient
from datetime import datetime
import urllib.parse
from flask import session
from datetime import datetime,timedelta
from sqlalchemy import desc


from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_object(Config)

mysql=MySQL(app)  # Initialize MySQL with app     

# MongoDB Configuration

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client["wealthyfyme"]
mongo_transactions = mongo_db["transactions"]

CATEGORIES = [
    "Food", "Housing", "Transportation", "Entertainment", 
    "Shopping", "Utilities", "Healthcare", "Education"
]


@app.route('/')
def home():
    return render_template("index.html")

from flask import session

from flask import session

@app.route('/login', methods=["GET", "POST"])
def login():
    msg = session.get('msg', '')  # Retrieve the message from session if it exists
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        res = check_user(email, password)
        
        if res:
            return redirect(url_for('dashboard_home'))
        else:
            session['msg'] = "unsuccessful"  # Set the error message in session
            return redirect(url_for('login'))  # Redirect to avoid re-posting form data
    
    # Clear the message from session on GET request
    
    session.pop('msg', None)  
    
    return render_template("login.html", form=form, msg=msg)  # Pass msg to the template




# @app.route('/login', methods=["GET", "POST"])
# def login():
#     msg = ""
#     form = LoginForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         res = check_user(email, password)
#         if res:
#             return redirect(url_for('dashboard'))
#         else:
#             msg = "unsuccessful"
        
#         form.email.data = ""
#         form.password.data = ""
#         form.remember.data = False

#     return render_template("login.html", form=form, msg=msg)  # Pass msg to the template

from flask import session

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = RegistrationForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            res = registration(name, email, password, confirm_password)
            if res:
                return redirect(url_for('login'))
            else:
                session['msg'] = "Please, Enter a Valid Email !!!"
                return redirect(url_for('register'))  # Redirect clears POST data
        else:
            # If form has errors, store them in session to show after redirect
            session['form_errors'] = form.errors
            return redirect(url_for('register'))

    # GET request - render a fresh form with no data
    msg = session.pop('msg', '')
    form_errors = session.pop('form_errors', {})
    form = RegistrationForm()  # New form, fresh fields
    return render_template("registration.html", form=form, msg=msg, form_errors=form_errors)





# @app.route('/register', methods=["GET", "POST"])
# def register():
#     msg=''
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         # Get data from the form
#         name = form.name.data
#         email = form.email.data
#         password = form.password.data
#         confirm_password = form.confirm_password.data

#         # Insert user data into MySQL database
#         res = registration(name, email, password, confirm_password)
#         if res:
#             return redirect(url_for('login'))
#         else:
#             msg="Please, Enter Validate Mail !!!"
        

#     return render_template("registration.html", form=form,msg=msg)

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



@app.route('/dashboard_home')
def dashboard_home():
    current_date = datetime(2025, 5, 1)

    monthly_income = 0
    monthly_expenses = 0
    total_balance = 0

    # Get current month range
    start_date = current_date.replace(day=1)
    end_date = (start_date + timedelta(days=31)).replace(day=1)

    # Get transactions of the current month
    transactions = mongo_transactions.find({
        'date': {'$gte': start_date.strftime('%Y-%m-%d'), '$lt': end_date.strftime('%Y-%m-%d')}
    })

    # For expenses by category
    category_expenses = {}

    for txn in transactions:
        txn_type = txn.get('type', '').lower()
        amount = txn.get('amount', 0)
        if txn_type == 'income':
            monthly_income += amount
        elif txn_type == 'expense':
            monthly_expenses += amount
            category = txn.get('category', 'Uncategorized')
            category_expenses[category] = category_expenses.get(category, 0) + amount

    total_balance = monthly_income - monthly_expenses

    # Prepare sorted categories for display
    sorted_categories = sorted(
        [(cat, abs(amt)) for cat, amt in category_expenses.items()],
        key=lambda x: x[1],
        reverse=True
    )

    # Get data for monthly summary chart (last 6 months)
    monthly_summary = []
    for i in range(6, 0, -1):
        month_start = (current_date - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=31)).replace(day=1)
        
        month_txns = mongo_transactions.find({
            'date': {'$gte': month_start.strftime('%Y-%m-%d'), '$lt': month_end.strftime('%Y-%m-%d')}
        })
        
        month_income = 0
        month_expenses = 0
        
        for txn in month_txns:
            txn_type = txn.get('type', '').lower()
            amount = txn.get('amount', 0)
            if txn_type == 'income':
                month_income += amount
            elif txn_type == 'expense':
                month_expenses += amount
        
        monthly_summary.append({
            'month': month_start.strftime('%b %Y'),
            'income': month_income,
            'expenses': abs(month_expenses),  # Use absolute value for chart
            'savings': month_income - abs(month_expenses)
        })

    # Fetch recent transactions
    recent_transactions = mongo_transactions.find().sort('date', -1).limit(5)
    formatted_recent = []

    for txn in recent_transactions:
        try:
            txn_date = datetime.strptime(txn.get('date', ''), '%Y-%m-%d')
        except Exception:
            txn_date = datetime.min

        formatted_recent.append({
            'date': txn_date,
            'category': txn.get('category', ''),
            'description': txn.get('description', ''),
            'amount': txn.get('amount', 0),
            'type': txn.get('type', '')
        })

    return render_template("dashboard_home.html",
                           total_balance=total_balance,
                           monthly_income=monthly_income,
                           monthly_expenses=monthly_expenses,
                           recent_transactions=formatted_recent,
                           sorted_categories=sorted_categories,
                           monthly_data={
                               'labels': [m['month'] for m in monthly_summary],
                               'income': [m['income'] for m in monthly_summary],
                               'expenses': [m['expenses'] for m in monthly_summary],
                               'savings': [m['savings'] for m in monthly_summary]
                           },
                           category_data={
                               'labels': [cat[0] for cat in sorted_categories],
                               'data': [cat[1] for cat in sorted_categories]
                           })





@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"]
        date = request.form["date"]
        txn_type = request.form.get("type", "expense")  # default to expense

        mongo_transactions.insert_one({
            "amount": amount,
            "category": category,
            "description": description,
            "date": date,
            "type": txn_type
        })

        return redirect("/transactions")

    # Fetch transactions from MongoDB only
    mongo_transactions_list = mongo_transactions.find().sort("date", -1)

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
            "amount": txn.get("amount", 0.0),
            "type": txn.get("type", "expense")  # <-- Include type here
        })

    # Sort by parsed date
    transactions.sort(key=lambda x: x["date"], reverse=True)

    return render_template("transactions.html", transactions=transactions)

@app.route('/budgets')
def budgets():
    # Get all budgets from MongoDB
    budgets_data = list(mongo_db.budgets.find())

    # Aggregate expenses grouped by category
    pipeline = [
        {"$match": {"type": "expense"}},
        {"$group": {"_id": "$category", "total_spent": {"$sum": "$amount"}}}
    ]
    expense_sums = list(mongo_db.transactions.aggregate(pipeline))
    spent_map = {e['_id']: e['total_spent'] for e in expense_sums}

    # Combine budgets with actual spent sums & compute progress
    for b in budgets_data:
        category = b['category']
        limit = b.get('limit', 0)
        spent = spent_map.get(category, 0)
        b['spent'] = spent
        b['progress'] = (spent / limit) * 100 if limit > 0 else 0

    return render_template('budgets.html', budgets=budgets_data)


from flask import request, redirect, url_for, flash

@app.route('/add-budget', methods=['POST'])
def add_budget():
    category = request.form.get('category')
    limit = float(request.form.get('limit'))

    if not category or limit <= 0:
        flash("Invalid budget input!", "danger")
        return redirect(url_for('budgets'))

    # Optional: prevent duplicates
    existing = mongo_db.budgets.find_one({"category": category})
    if existing:
        flash(f"Budget for '{category}' already exists.", "warning")
        return redirect(url_for('budgets'))

    # Insert into MongoDB
    mongo_db.budgets.insert_one({
        "category": category,
        "limit": limit,
    })

    flash(f"Budget for '{category}' added!", "success")
    return redirect(url_for('budgets'))

from bson.objectid import ObjectId

@app.route('/edit-budget/<budget_id>', methods=['POST'])
def edit_budget(budget_id):
    category = request.form.get('category')
    limit = float(request.form.get('limit'))
    mongo_db.budgets.update_one(
        {"_id": ObjectId(budget_id)},
        {"$set": {"category": category, "limit": limit}}
    )
    flash("Budget updated.", "success")
    return redirect(url_for('budgets'))



@app.route('/delete-budget/<budget_id>', methods=['POST'])
def delete_budget(budget_id):
    mongo_db.budgets.delete_one({"_id": ObjectId(budget_id)})
    flash("Budget deleted.", "info")
    return redirect(url_for('budgets')) 


@app.route('/alerts')
def alerts():
    # Get all budgets from MongoDB
    budgets_data = list(mongo_db.budgets.find())

    # Aggregate expenses grouped by category
    pipeline = [
        {"$match": {"type": "expense"}},
        {"$group": {"_id": "$category", "total_spent": {"$sum": "$amount"}}}
    ]
    expense_sums = list(mongo_transactions.aggregate(pipeline))
    spent_map = {e['_id']: e['total_spent'] for e in expense_sums}

    # Build alert data
    alerts = []
    for b in budgets_data:
        category = b['category']
        limit = b.get('limit', 0)
        spent = spent_map.get(category, 0)
        percentage = (spent / limit) * 100 if limit > 0 else 0

        if percentage >= 90:
            alerts.append({
                'category': category,
                'limit': limit,
                'spent': spent,
                'percentage': round(percentage, 2)
            })

    return render_template('alerts.html', alerts=alerts)





if __name__ == '__main__':
    app.run(debug=True)
