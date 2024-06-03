from flask import Flask, render_template, request, redirect
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
 



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        feeling = request.form['feeling']
        feedback_text = request.form['feedback']

        # Save feedback (in-memory storage)
        feedback_storage.append({
            'name': name,
            'feeling': feeling,
            'feedback': feedback_text
        })

        return redirect(url_for('feedback'))

    return render_template('feedback.html', feedbacks=feedback_storage)

if __name__ == "__main__":
    app.run(debug=True)