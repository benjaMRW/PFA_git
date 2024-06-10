from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 
from datetime import datetime
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

@app.route("/level/<int:id1>/<int:id2>")
def level(id1, id2):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()
    
    # Fetch data from Sports table
    cur.execute('SELECT * FROM Sports WHERE id=?', (id1,))
    sports_data = cur.fetchone()
    
    # Fetch data from Level table
    cur.execute('SELECT * FROM Level WHERE id=?', (id2,))
    level_data = cur.fetchone()
    

    
    conn.close()
    
    # Check if data exists
    if not sports_data or not level_data:
        return "Data not found", 404

    # Pass both sets of data to the template
    return render_template('level.html', sports=sports_data, level=level_data)


@app.route("/plan/<int:id1>/<int:id2>/<int:id3>")
def plan(id1, id2, id3):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()

    # Fetch sports data
    cur.execute('SELECT * FROM Sports WHERE id=?', (id1,))
    sports_data = cur.fetchone()

    # Fetch level data
    cur.execute('SELECT * FROM Level WHERE id=?', (id2,))
    level_data = cur.fetchone()

    # Fetch plan data; ensure the query matches your table schema
    cur.execute('''SELECT plan.* FROM plan
                   JOIN LevelPlans ON plan.id = LevelPlans.pid
                   WHERE LevelPlans.lid = ? AND Plan.id = ?''', (id2,id3))
    plan_data = cur.fetchone()
    
    conn.close()
    
   

    return render_template('plan.html', sports=sports_data, level=level_data, plan=plan_data)
 
app.secret_key = 'your_secret_key'

# Initialize the database
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        content TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route to render the feedback form and handle form submission
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = request.form.get('username')
        content = request.form.get('content')

        if not username or not content:
            return "Username and content are required", 400

        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO feedback (username, content) VALUES (?, ?)', (username, content))
        conn.commit()
        conn.close()

        return redirect(url_for('view_feedback', username=username))

    return render_template('feedback.html')

# Route to display feedback for a specific user
@app.route('/user/<username>')
def view_feedback(username):
    feedbacks = []

    if username:
        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute('SELECT content, date FROM feedback WHERE username = ? ORDER BY date DESC', (username,))
        feedbacks = cursor.fetchall()
        conn.close()

    return render_template('UsersInfo.html', feedbacks=feedbacks, username=username)

# Route to display all feedback
@app.route('/DisplayFeedback')
def display():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, content, date FROM feedback ORDER BY date DESC')
    feedbacks = cursor.fetchall()
    conn.close()

    return render_template('DisplayFeedback.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
conn = sqlite3.connect('feedback.db') 
cursor = conn.cursor() 
delete_statement = "DELETE FROM feedback WHERE id = 1, 2, 3, 4, 5, 6, 7;" 
cursor.execute(delete_statement) 
conn.commit() 
conn.close()  
