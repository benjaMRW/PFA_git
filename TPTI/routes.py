from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3 
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


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

 


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    username = request.form.get('username')
    content = request.form.get('content')
    plan = request.form.get('plan')

    if not username or not content or not plan:
        return "Username, content, and plan are required", 400

    # Check for bad words in the content
    if has_bad_words(content, username):
        return jsonify({'error': 'Feedback contains inappropriate content'}), 400

    conn = sqlite3.connect('PFA.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO feedback (username, content, plan, date) VALUES (?, ?, ?, ?)',
                   (username, content, plan, datetime.now()))
    conn.commit()
    conn.close()

    return redirect('/DisplayFeedback')

@app.route('/DisplayFeedback')
def display_feedback():
    conn = sqlite3.connect('PFA.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, content, date, plan FROM feedback')
    feedbacks = cursor.fetchall()
    conn.close()

    formatted_feedbacks = []
    for feedback in feedbacks:
        username, content, date_str, plan = feedback
        # Remove any trailing milliseconds if present
        date_str = date_str.split('.')[0]
        formatted_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        formatted_feedbacks.append((username, content, formatted_date, plan))

    return render_template('DisplayFeedback.html', feedbacks=formatted_feedbacks)

bad_words = [
    'abuse', 'asshole', 'bastard', 'bitch', 'cock', 'cunt', 'damn', 'dick',
    'fuck', 'jerk', 'piss', 'shit', 'slut', 'whore', 'nigger', 'faggot',
    'retard', 'spastic', 'twat', 'wanker', 'arsehole', 'bollocks', 'bugger',
    'chink', 'coon', 'crap', 'douche', 'dyke', 'fag', 'gook', 'guido', 'heeb',
    'homo', 'jap', 'kike', 'kraut', 'lesbo', 'limey', 'mick', 'nazi', 'paki',
    'pollack', 'prick', 'raghead', 'spic', 'tard', 'tranny', 'wetback', 'zipperhead', " sex",
    # Variations with numbers or special characters
    'nigg4', 'f4ggot', 'c*nt', 'sh!t', 'b!tch', 'd!ck'
]

# Function to check for bad words
def has_bad_words(username, feedback):
    # Convert inputs to lowercase to make the filter case-insensitive
    username_lower = username.lower()
    feedback_lower = feedback.lower()

    # Create regex patterns to match bad words with variations
    patterns = [re.escape(word).replace('\\*', '[*]').replace('\\!', '[!]').replace('4', '[4a@]') for word in bad_words]
    
    # Combine patterns into one regex
    combined_pattern = r'(' + '|'.join(patterns) + r')'
    
    # Check if either username or feedback contains any of the bad words or their variations
    if re.search(combined_pattern, username_lower) or re.search(combined_pattern, feedback_lower):
        return True  # Found a bad word

    return False  # No bad words found



def delete_feedback_records(ids):
    # Connect to the database
    conn = sqlite3.connect('PFA.db')
    curs = conn.cursor()

    # Create a parameterized query to delete records with specific ids
    query = "DELETE FROM feedback WHERE id IN ({})".format('12 ,'.join('?' for _ in ids))
    curs.execute(query, ids)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Call the function with the IDs to delete
delete_feedback_records([12])

            
          

if __name__ == '__main__':
    app.run(debug=True)
   
   



