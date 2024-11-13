import sqlite3
from flask import Blueprint, jsonify, render_template, request

user_bp = Blueprint('user', __name__, template_folder="../templates", static_folder="../static")

@user_bp.route('/')
def main(name=None):
    return render_template('index.html', person=name)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@user_bp.route('/pdf', methods=['GET', 'POST'])
def pdf():
    return render_template('pdf.html')

@user_bp.route('/grafiks', methods=['GET', 'POST'])
def grafiks():
    return render_template('grafiks.html')

@user_bp.route('/getTopClasses', methods=['POST'])
def get_top_classes():
    group = request.json['group']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        print(group)
        if group == True:
            cur.execute("SELECT name, points FROM classes  WHERE CAST(SUBSTR(name, 1, INSTR(name, '.') - 1) AS INTEGER) BETWEEN 7 AND 12 ORDER BY points DESC LIMIT 3")
        else:
            cur.execute("SELECT name, points FROM classes WHERE CAST(SUBSTR(name, 1, INSTR(name, '.') - 1) AS INTEGER) BETWEEN 2 AND 6 ORDER BY points DESC LIMIT 3")
        data = cur.fetchall()
    return jsonify([{'name': row[0], 'points': row[1]} for row in data])

@user_bp.route('/getClasses', methods=['POST'])
def get_classes():
    group = request.json['group']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        match group:
            case True:
                cur.execute("SELECT id, name FROM classes WHERE CAST(SUBSTR(name, 1, INSTR(name, '.') - 1) AS INTEGER) BETWEEN 7 AND 12")
            case False:
                cur.execute("SELECT id, name FROM classes WHERE CAST(SUBSTR(name, 1, INSTR(name, '.') - 1) AS INTEGER) BETWEEN 2 AND 6")
            case _:
                cur.execute("SELECT id, name FROM classes")
        data = cur.fetchall()
    return jsonify([{'id': row[0], 'name': row[1]} for row in data])

@user_bp.route('/getClassDetails', methods=['POST'])
def get_class_details():
    class_name = request.json['class']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        
        # Получение общего количества пунктов для класса
        cur.execute("SELECT points FROM classes WHERE name = ?", (class_name,))
        total_points = cur.fetchone()
        
        # Получение последних трех добавлений пунктов для класса
        cur.execute("SELECT explanation, points FROM explanations WHERE item_name = ? ORDER BY id DESC LIMIT 3", (class_name,))
        last_three_additions = cur.fetchall()
        
        data = {
            'total_points': total_points[0],
            'details': [{'explanation': row[0], 'points_added': row[1]} for row in last_three_additions]
        }
        
    return jsonify(data)