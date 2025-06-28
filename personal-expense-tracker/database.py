import sqlite3

DB_NAME = "expenses.db"

def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    """Initializes both expenses and users tables."""
    conn = connect()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create expenses table (with user_id foreign key)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            user_id INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized. Tables 'expenses' and 'users' are ready!")


def add_expense(date, category, amount, description, user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (date, category, amount, description, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (date, category, amount, description, user_id))
    conn.commit()
    conn.close()


def view_all_expenses(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, category, amount, description
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def filter_expenses_by_category(category, user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, category, amount, description
        FROM expenses
        WHERE category = ? AND user_id = ?
        ORDER BY date DESC
    """, (category, user_id))
    rows = cursor.fetchall()
    conn.close()
    return rows


def filter_expenses_by_date(start_date, end_date, user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, category, amount, description
        FROM expenses
        WHERE date BETWEEN ? AND ? AND user_id = ?
        ORDER BY date ASC
    """, (start_date, end_date, user_id))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_total_spent(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0.0


def add_user(name, email, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user
