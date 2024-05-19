from flask import Flask, render_template
import sqlite3 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/sport/<int:id>")
def Sports(id):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()
    cur.execute('select * FROM Sports WHERE id=?', (id,))
    Sports = cur.fetchone()

    return render_template('sport.html', Sports = Sports)

@app.route("/level/<int:id>")
def level(id):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()
    cur.execute('select * FROM level WHERE id=?', (id,))
    level = cur.fetchone()

    return render_template('level.html', level = level)

@app.route("/plan/<int:id>")
def plan(id):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()
    cur.execute('select * FROM plan WHERE id=?', (id,))
    plan = cur.fetchone()

    return render_template('plan.html', plan = plan)
if __name__ == "__main__":
    app.run(debug=True)