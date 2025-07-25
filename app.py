from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret123"

# DB Connection
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        if user:
            session["user"] = email
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/quiz/<subject>')
def quiz(subject):
    if "user" not in session:
        return redirect(url_for('login'))
    cur.execute("SELECT id, question, option_a, option_b, option_c, option_d FROM questions WHERE subject=%s ORDER BY RANDOM() LIMIT 5", (subject,))
    questions = cur.fetchall()
    return render_template("quiz.html", questions=questions, subject=subject)

@app.route('/submit', methods=["POST"])
def submit():
    score = 0
    total = int(request.form["total"])
    subject = request.form["subject"]

    for qid in request.form.getlist("qid"):
        selected = request.form.get(f"q_{qid}")
        cur.execute("SELECT correct_option FROM questions WHERE id=%s", (qid,))
        correct = cur.fetchone()[0]
        if selected == correct:
            score += 1

    return render_template("result.html", score=score, total=total, subject=subject)

if __name__ == '__main__':
    app.run(debug=True)
