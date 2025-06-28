from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from database import (
    init_db,
    add_expense,
    view_all_expenses,
    filter_expenses_by_category,
    filter_expenses_by_date,
    get_total_spent,
    add_user,
    get_user_by_email
)

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Replace in production
app.permanent_session_lifetime = timedelta(days=7)

init_db()


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    expenses = view_all_expenses(session["user_id"])
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["GET", "POST"])
def add_expense_route():
    if "user_id" not in session:
        flash("Please log in to add expenses.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        description = request.form["description"]
        user_id = session["user_id"]
        add_expense(date, category, amount, description, user_id)
        flash("Expense added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/filter-category", methods=["GET", "POST"])
def filter_category():
    if "user_id" not in session:
        flash("Please log in to filter expenses.", "warning")
        return redirect(url_for("login"))

    expenses = None
    if request.method == "POST":
        category = request.form["category"]
        expenses = filter_expenses_by_category(category, session["user_id"])
    return render_template("filter_category.html", expenses=expenses)


@app.route("/filter-date", methods=["GET", "POST"])
def filter_date():
    if "user_id" not in session:
        flash("Please log in to filter expenses.", "warning")
        return redirect(url_for("login"))

    expenses = None
    if request.method == "POST":
        start = request.form["start"]
        end = request.form["end"]
        expenses = filter_expenses_by_date(start, end, session["user_id"])
    return render_template("filter_date.html", expenses=expenses)


@app.route("/total")
def total():
    if "user_id" not in session:
        flash("Please log in to view total spending.", "warning")
        return redirect(url_for("login"))

    total_amount = get_total_spent(session["user_id"])
    return render_template("total.html", total=round(total_amount, 2))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if get_user_by_email(email):
            flash("⚠️ Email already registered. Please log in.", "warning")
            return redirect(url_for("login"))

        add_user(name, email, password)
        flash("✅ Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)
        if user and user[3] == password:
            session.permanent = True
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            flash(f"Welcome back, {user[1]}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You’ve been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
