# from flask import Flask, request, jsonify, render_template
# import sqlite3

# app = Flask(__name__)

# @app.route('/')
# def main(name=None):
#     return render_template('index.html', person=name)

# @app.route('/admin')
# def admin(name=None):
#     return render_template('admin.html', person=name)

# def init_db():
#     with sqlite3.connect('database.db') as conn:
#         conn.execute('''CREATE TABLE IF NOT EXISTS classes 
#                         (id INTEGER PRIMARY KEY, name TEXT, points INTEGER, explanation TEXT)''')
#         conn.commit()

# @app.route('/getClassDetails', methods=['POST'])
# def get_class_details():
#     class_name = request.json['class']
#     with sqlite3.connect('database.db') as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT points, explanation FROM classes WHERE name = ?", (class_name,))
#         data = cur.fetchone()
#     return jsonify(count=data[0], recent=[data[1]])

# @app.route('/getTopClasses', methods=['GET'])
# def get_top_classes():
#     with sqlite3.connect('database.db') as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT name, points FROM classes ORDER BY points DESC LIMIT 3")
#         data = cur.fetchall()
#     return jsonify([{'name': row[0], 'points': row[1]} for row in data])

# @app.route('/addClass', methods=['POST'])
# def add_class():
#     new_class = request.json
#     with sqlite3.connect('database.db') as conn:
#         conn.execute("INSERT INTO classes (name, points, explanation) VALUES (?, ?, ?)",
#                      (new_class['name'], new_class['points'], new_class['explanation']))
#         conn.commit()
#     return jsonify(message='Класс добавлен успешно')

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def main(name=None):
    return render_template('index.html', person=name)

@app.route('/admin')
def admin(name=None):
    return render_template('admin.html', person=name)

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS classes 
                        (id INTEGER PRIMARY KEY, name TEXT, points INTEGER, explanation TEXT)''')
        conn.commit()

@app.route('/getClassDetails', methods=['POST'])
def get_class_details():
    class_name = request.json['class']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT points, explanation FROM classes WHERE name = ?", (class_name,))
        data = cur.fetchone()
    return jsonify(count=data[0], recent=[data[1]])

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
    points = new_class.get('points', 0)  # Устанавливаем значение по умолчанию
    with sqlite3.connect('database.db') as conn:
        conn.execute("INSERT INTO classes (name, points, explanation) VALUES (?, ?, ?)",
                     (new_class['name'], points, None))
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
    explanation = request.json['explanation']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM classes WHERE name = ?", (class_name,))
        class_id = cur.fetchone()

        if class_id:
            cur.execute("UPDATE classes SET points = points + ?, explanation = explanation || '; ' || ? WHERE id = ?",
                        (points, explanation, class_id[0]))
            conn.commit()
            return jsonify({'message': 'Points added successfully'})
        else:
            return jsonify({'message': 'Class not found'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
