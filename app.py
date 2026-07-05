from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create table
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        date TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        total = 0

    return render_template(
        'index.html',
        expenses=expenses,
        total=total
    )


@app.route('/add', methods=['POST'])
def add_expense():
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    description = request.form['description']

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses(amount, category, date, description)
    VALUES (?, ?, ?, ?)
    """, (amount, category, date, description))

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)