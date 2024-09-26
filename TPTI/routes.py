from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
import sqlite3 
from datetime import datetime
import re

from bs4 import BeautifulSoup
#homepage

app = Flask(__name__)




# Home page
@app.route('/')
def home():
    return render_template("home.html")

# Sport page where you choose the level
@app.route("/sport/<int:id>")
def sport(id):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM sport WHERE id=?', (id,))
    sport = cur.fetchone()
    conn.close()  

    if not sport:
        abort(404)

    return render_template('sport.html', sport=sport)

# Level page where you choose what plan you choose
@app.route("/level/<int:id1>/<int:id2>")
def level(id1, id2):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM sport WHERE id=?', (id1,))
    sports_data = cur.fetchone()

    cur.execute('SELECT * FROM Level WHERE id=?', (id2,))
    level_data = cur.fetchone()

    conn.close()

    if not sports_data or not level_data:
        abort(404)

    return render_template('level.html', sports=sports_data, level=level_data)

# Plan page where the plan is displayed
@app.route("/plan/<int:id1>/<int:id2>/<int:id3>")
def plan(id1, id2, id3):
    conn = sqlite3.connect('PFA.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM sport WHERE id=?', (id1,))
    sports_data = cur.fetchone()

    cur.execute('SELECT * FROM Level WHERE id=?', (id2,))
    level_data = cur.fetchone()

    cur.execute('''SELECT plan.* FROM plan
                   JOIN LevelPlans ON plan.id = LevelPlans.pid
                   WHERE LevelPlans.lid = ? AND plan.id = ?''', (id2, id3))
    plan_data = cur.fetchone()

    conn.close()

    if not sports_data or not level_data or not plan_data:
        abort(404)

    return render_template('plan.html', sports=sports_data, level=level_data, plan=plan_data)

# Submit feedback
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    username = request.form.get('username')
    content = request.form.get('content')
    plan = request.form.get('plan')

    if has_bad_words(username, content):
        return render_template('inappropiate.html')

    conn = sqlite3.connect('PFA.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO feedback (username, content, plan, date) VALUES (?, ?, ?, ?)',
                   (username, content, plan, datetime.now()))
    conn.commit()
    conn.close()

    return redirect('/DisplayFeedback')

# Display feedback
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
        date_str = date_str.split('.')[0]
        formatted_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        formatted_feedbacks.append((username, content, formatted_date, plan))

    return render_template('DisplayFeedback.html', feedbacks=formatted_feedbacks)

# Check for bad words in username and feedback
# List of bad words for content filtering
bad_words = [
    '/Vigger','abuse', 'asshole', 'bastard', 'bitch', 'cock', 'cunt', 'damn', 'dick',
    'fuck', 'jerk', 'piss', 'shit', 'slut', 'whore', 'nigger', 'faggot',
    'retard', 'spastic', 'twat', 'wanker', 'arsehole', 'bollocks', 'bugger',
    'chink', 'coon', 'crap', 'douche', 'dyke', 'fag', 'gook', 'guido', 'heeb',
    'homo', 'jap', 'kike', 'kraut', 'lesbo', 'limey', 'mick', 'nazi', 'paki',
    'pollack', 'prick', 'raghead', 'spic', 'tard', 'tranny', 'wetback', 'zipperhead', 'sex',
    # Variations with numbers or special characters
    'nigg4', 'f4ggot', 'c*nt', 'sh!t', 'b!tch', 'd!ck'
]


# Function to check for bad words
def has_bad_words(username, feedback):
    # Convert inputs to lowercase to make the filter case-insensitive
    username_lower = username.lower()
    feedback_lower = feedback.lower()

    # Define a dictionary of common letter substitutions
    substitutions = {
        'a': '[a4@]',
        'b': '[b8]',
        'c': '[c\\(]',
        'e': '[e3]',
        'g': '[g9]',
        'i': '[i1!|]',
        'l': '[l1!|]',
        'o': '[o0]',
        's': '[s5\\$]',
        't': '[t7+]',
        'u': '[uµ]',
        'z': '[z2]'
    }
    

    # Function to create regex pattern with substitutions
    def create_pattern(word):
        pattern = ''
        for char in word:
            pattern += substitutions.get(char, char)
        return pattern

    # Create regex patterns to match bad words with variations
    patterns = [create_pattern(word) for word in bad_words]
    
    # Combine patterns into one regex
    combined_pattern = r'(' + '|'.join(patterns) + r')'
    
    # Check if either username or feedback contains any of the bad words or their variations
    if re.search(combined_pattern, username_lower) or re.search(combined_pattern, feedback_lower):
        return True  # Found a bad word

    return False  # No bad words found

# Handle 404 errors with a custom page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

