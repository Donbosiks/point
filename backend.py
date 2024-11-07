from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from dotenv import load_dotenv
from datetime import timedelta
import os
# Загрузка переменных окружения из .env файла
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Устанавливаем время жизни сессии в 2 часа
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Пользовательская модель
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def main(name=None):
    return render_template('index.html', person=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
    return render_template('pdf.html')

@app.route('/grafiks', methods=['GET', 'POST'])
def grafiks():
    return render_template('grafiks.html')

@app.route('/login_check', methods=['POST'])
def login_check():
    login_data = request.json
    if login_data['username'] == os.getenv('LOGIN') and login_data['password'] == os.getenv('PASSWORD'):
        user = User(id=login_data['username'])
        login_user(user, duration=timedelta(hours=2))
        return jsonify({'redirect': url_for('admin')}), 200
    else:
        return jsonify({}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin(name=None):
    return render_template('admin.html', person=name)

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS classes 
                        (id INTEGER PRIMARY KEY, name TEXT, points FLOAT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS explanations
                        (id INTEGER PRIMARY KEY, item_name TEXT, explanation TEXT, points FLOAT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS criteria
                        (id INTEGER PRIMARY KEY, criteria_user TEXT)''')
        conn.commit()

@app.route('/getTopClasses', methods=['GET'])
def get_top_classes():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, points FROM classes ORDER BY points DESC LIMIT 3")
        data = cur.fetchall()
    return jsonify([{'name': row[0], 'points': row[1]} for row in data])

@app.route('/getClasses', methods=['GET'])
def get_classes():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM classes")
        data = cur.fetchall()
    return jsonify([{'id': row[0], 'name': row[1]} for row in data])

@app.route('/getCriteria', methods=['GET'])
def get_criteria():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, criteria_user FROM criteria")
        data = cur.fetchall()
    return jsonify([{'id': row[0], 'criteria_user': row[1]} for row in data])

@app.route('/addClass', methods=['POST'])
@login_required
def add_class():
    new_class = request.json
    school_class = new_class['name']

    if len(school_class) > 4:
        return jsonify(message='Klase nebija pievienota'), 401

    with sqlite3.connect('database.db') as conn:
        conn.execute("INSERT INTO classes (name, points) VALUES (?, ?)",
                     (school_class, 0))
        conn.execute("INSERT INTO explanations (item_name, explanation, points) VALUES (?, ?, ?)",
                     (school_class, 'Klases izveidosana', 0))
        conn.commit()
    return jsonify(message='Klase bija pievinota')


@app.route('/addPoints', methods=['POST'])
@login_required
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
        return jsonify({'message': 'Punkti nebija pievinoti'}), 415
         
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
            return jsonify({'message': 'Punkti pievinoti veiksmigi'})
        else:
            return jsonify({'message': 'Klase nebija atrasta'})
        
@app.route('/addCriteria', methods=['POST'])
@login_required
def add_criteria():
    criteriaUser = request.json['criteriaUser']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        print(criteriaUser)

        cur.execute("INSERT INTO criteria (criteria_user) VALUES (?)",
                    (criteriaUser))
        conn.commit()
        return jsonify({'message': 'Kriterijas pievinoti veiksmigi'})

@app.route('/getClassDetails', methods=['POST'])
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

@app.route('/upload_criteria', methods=['POST'])
def upload_criteria():
    UPLOAD_FOLDER = os.getenv('PDF_FOLDER', 'uploads')  # Указать путь к папке для загрузки
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    files = request.files
    
    if 'pdf' in files:
        file1 = files['pdf']
        
        if file1.filename == '':
            return jsonify({'error': 'No selected file for the first PDF'}), 400
        
        if file1 and file1.filename.endswith('.pdf'):
            filename1 = 'kriterijas.pdf'  # Задать имя для сохраненного первого файла
            file_path1 = os.path.join(UPLOAD_FOLDER, filename1)
            file1.save(file_path1)
            response_message = 'Kriterija bija atjanotas'
        else:
            return jsonify(error='Invalid file format for the first PDF, only PDFs are allowed'), 400
    
    if 'pdf_1' in files:
        file2 = files['pdf_1']
        
        if file2.filename == '':
            return jsonify({'error': 'No selected file for the second PDF'}), 400
        
        if file2 and file2.filename.endswith('.pdf'):
            filename2 = 'grafiks.pdf'  # Задать имя для сохраненного второго файла
            file_path2 = os.path.join(UPLOAD_FOLDER, filename2)
            file2.save(file_path2)
            response_message = 'Dežures grafiks bija atjanotas'
        else:
            return jsonify(error='Invalid file format for the second PDF, only PDFs are allowed'), 400
    
    if 'pdf' not in files and 'pdf_1' not in files:
        return jsonify({'error': 'No files part'}), 400
    
    return jsonify(message=response_message), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
