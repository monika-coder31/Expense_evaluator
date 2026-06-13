from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "your_mysql_password"
app.config["MYSQL_DB"] = "finvue_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = generate_password_hash(request.form["password"])

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tbl_users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            flash("Email already exists", "danger")
            return redirect(url_for("register"))

        cur.execute(
            "INSERT INTO tbl_users (username, email, password_hash, currency_code) VALUES (%s, %s, %s, %s)",
            (username, email, password, "INR")
        )
        mysql.connection.commit()
        cur.close()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tbl_users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["currency_code"] = user["currency_code"]
            flash("Login successful", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN c.flow_type = 'Income' THEN t.amount ELSE 0 END), 0) AS total_income,
            COALESCE(SUM(CASE WHEN c.flow_type = 'Expense' THEN t.amount ELSE 0 END), 0) AS total_expense
        FROM tbl_transactions t
        JOIN tbl_categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
    """, (session["user_id"],))

    totals = cur.fetchone()
    total_income = totals["total_income"] or 0
    total_expense = totals["total_expense"] or 0
    net_balance = total_income - total_expense

    cur.execute("""
        SELECT t.transaction_id, t.amount, t.description, t.actual_date, c.name, c.flow_type
        FROM tbl_transactions t
        JOIN tbl_categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
        ORDER BY t.actual_date DESC, t.transaction_id DESC
    """, (session["user_id"],))

    transactions = cur.fetchall()
    cur.close()

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        transactions=transactions,
        currency_code=session.get("currency_code", "INR")
    )


@app.route("/transactions", methods=["GET", "POST"])
def transaction_page():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    if request.method == "POST":
        category_id = request.form["category_id"]
        amount = request.form["amount"]
        description = request.form["description"]
        actual_date = request.form["actual_date"]

        cur.execute(
            "INSERT INTO tbl_transactions (user_id, category_id, amount, description, actual_date) VALUES (%s, %s, %s, %s, %s)",
            (session["user_id"], category_id, amount, description, actual_date)
        )
        mysql.connection.commit()
        flash("Transaction added successfully", "success")
        cur.close()
        return redirect(url_for("transaction_page"))

    cur.execute("""
        SELECT t.transaction_id, t.amount, t.description, t.actual_date, c.name, c.flow_type
        FROM tbl_transactions t
        JOIN tbl_categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
        ORDER BY t.actual_date DESC, t.transaction_id DESC
    """, (session["user_id"],))
    transactions = cur.fetchall()

    cur.execute("SELECT category_id, name, flow_type FROM tbl_categories ORDER BY flow_type, name")
    categories = cur.fetchall()
    cur.close()

    return render_template("transactions.html", transactions=transactions, categories=categories)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)