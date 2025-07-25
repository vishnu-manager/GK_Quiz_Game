from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import random

app = Flask(__name__)
app.secret_key = "quiz_secret_123"

# DB connection
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_pass",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/set_name', methods=["POST"])
def set_name():
    session["player_name"] = request.form["player_name"]
    return redirect(url_for("index"))

@app.route('/quiz/<subject>')
def quiz(subject):
    if "player_name" not in session:
        return redirect(url_for("index"))
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

    return render_template("result.html", score=score, total=total, subject=subject, player=session["player_name"])

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')
