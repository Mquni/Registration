from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'admission.db'

# Create table if not exists
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
    conn.commit()
    conn.close()

    return redirect('/students')

@app.route('/students')
def students():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    all_students = c.fetchall()
    conn.close()
    return render_template('students.html', students=all_students)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
