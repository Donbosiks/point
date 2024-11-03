from flask import Flask, request, jsonify, render_template
import sqlite3
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

app = Flask(__name__)

@app.route('/')
def main(name=None):
    return render_template('index.html', person=name)

@app.route('/admin')
def admin(name=None):
    return render_template('admin.html', person=name)

@app.route('/login', methods=['POST'])
def login():
    login_data = request.json
    if login_data['username'] == os.getenv('LOGIN') and login_data['password'] == os.getenv('PASSWORD'):
        200
    else:
        return jsonify(message='Nepareiz logins vai parole'), 500

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS classes 
                        (id INTEGER PRIMARY KEY, name TEXT, points FLOAT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS explanations
                        (id INTEGER PRIMARY KEY, item_name TEXT, explanation TEXT, points FLOAT)''')
        conn.commit()

@app.route('/getClassDetails', methods=['POST'])
def get_class_details():
    class_name = request.json['class']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT points FROM classes WHERE name = ?", (class_name,))
        data = cur.fetchone()
        cur.execute("SELECT explanation FROM explanations WHERE item_name = ?", (class_name,))
        explanation_data = cur.fetchall()
        explanations = [row[0] for row in explanation_data]
    return jsonify(count=data[0], recent=explanations)

@app.route('/getTopClasses', methods=['GET'])
def get_top_classes():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, points FROM classes ORDER BY points DESC LIMIT 3")
        data = cur.fetchall()
    return jsonify([{'name': row[0], 'points': row[1]} for row in data])

@app.route('/addClass', methods=['POST'])
def add_class():
    new_class = request.json
    school_class = new_class['name']

    if len(school_class) > 4:
        return jsonify(message='Класс не добавлен'), 500

    with sqlite3.connect('database.db') as conn:
        conn.execute("INSERT INTO classes (name, points) VALUES (?, ?)",
                     (school_class, 0))
        conn.execute("INSERT INTO explanations (item_name, explanation) VALUES (?, ?)",
                     (school_class, new_class.get('explanation', 'Creation class')))
        conn.commit()
    return jsonify(message='Класс добавлен успешно')

@app.route('/getClasses', methods=['GET'])
def get_classes():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM classes")
        data = cur.fetchall()
    return jsonify([{'id': row[0], 'name': row[1]} for row in data])

@app.route('/addPoints', methods=['POST'])
def add_points():
    class_name = request.json['name']
    points = request.json['points']

    try:
        points = float(points)
    except ValueError:
        points = 0

    if points > 999 or points < -101:
         points = 0

    if points == 0:
        return jsonify({'message': 'Punkti nebija pievinoti'}), 500
         
    explanation = request.json['explanation']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM classes WHERE name = ?", (class_name,))
        class_id = cur.fetchone()

        if class_id:
            cur.execute("UPDATE classes SET points = points + ? WHERE id = ?",
                        (points, class_id[0]))
            cur.execute("INSERT INTO explanations (item_name, explanation, points) VALUES (?, ?, ?)",
                        (class_name, explanation, points))
            conn.commit()
            return jsonify({'message': 'Points added successfully'})
        else:
            return jsonify({'message': 'Class not found'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
