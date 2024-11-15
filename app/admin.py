from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from dotenv import load_dotenv
import os
from app.sqlite_model import *
from datetime import timedelta

# Загрузка переменных окружения из .env файла
load_dotenv()

admin_bp = Blueprint('admin', __name__)

# Пользовательская модель
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@admin_bp.route('/login_check', methods=['POST'])
def login_check():
    login_data = request.form
    if login_data['username'] == os.getenv('LOGIN') and login_data['password'] == os.getenv('PASSWORD'):
        user = User(id=login_data['username'])
        login_user(user, duration=timedelta(hours=int(os.getenv('LOGIN_TIME'))))
        return redirect(url_for('admin.admin')), 302
    else:
        return 401

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@admin_bp.route('/admin')
@login_required
def admin(name=None):
    return render_template('admin.html', person=name)

@admin_bp.route('/getCriteria', methods=['GET'])
def get_criteria():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, criteria_user FROM criteria")
        data = cur.fetchall()
    return jsonify([{'id': row[0], 'criteria_user': row[1]} for row in data])

@admin_bp.route('/addClass', methods=['POST'])
@login_required
def add_class():
    new_class = request.form
    school_class = new_class['className']

    if len(school_class) > 4:
        return jsonify({'message': 'Klase nebija pievinoti, jo klašu simbolu skaits vairak neka 4'}), 415

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        
        # Проверка, существует ли уже запись с таким именем
        cur.execute('SELECT * FROM classes WHERE name = ?', (school_class,))
        existing_item = cur.fetchone()
        
        if existing_item:
            return redirect(url_for("admin.admin")), 401
        
        # Добавление новой записи
        conn.execute("INSERT INTO classes (name, points) VALUES (?, ?)", (school_class, 0))
        conn.execute("INSERT INTO explanations (item_name, explanation, points) VALUES (?, ?, ?)",
                     (school_class, 'Klases izveidošana', 0))
        conn.commit()
    
    return redirect(url_for("admin.admin")), 302



@admin_bp.route('/addPoints', methods=['POST'])
@login_required
def add_points():
    class_name = request.form['existingClassSelect']
    points = request.form['classPoints']

    try:
        points = float(points)
    except ValueError:
        points = 0

    if points > int(os.getenv('MAX_INTERVAL')) or points < int(os.getenv('MIN_INTERVAL')):
         points = 0

    if points == 0:
        return jsonify({'message': 'Punkti nebija pievinoti, jo punktu skaits neatbilst intervalam'}), 415
         
    explanation = request.form['criteriaSelect']

    if explanation == "cits":
        explanation = request.form['classExplanation']

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
            return redirect(url_for("admin.admin")), 302
        else:
            return jsonify({'message': 'Klase nebija atrasta'}), 400
        
@admin_bp.route('/addCriteria', methods=['POST'])
@login_required
def add_criteria():
    criteriaUser = request.form['criteriaUser']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        conn.execute("INSERT INTO criteria (criteria_user) VALUES (?)", (f"{criteriaUser}",))

        conn.commit()
        return redirect(url_for("admin.admin")), 302


@admin_bp.route('/upload_criteria', methods=['POST'])
@login_required
def pdfs():

    UPLOAD_FOLDER = os.getenv('PDF_FOLDER')  # Указавает путь к папке для сохранения

    message = None
    if request.method == 'POST':
        files = request.files
        
        if 'pdf' in files:
            file1 = files['pdf']
            
            if file1.filename == '':
                return redirect(url_for('admin.admin', message='No selected file for the first PDF')), 302
            
            if file1 and file1.filename.endswith('.pdf'):
                filename1 = 'kriterijas.pdf'
                file_path1 = os.path.join(UPLOAD_FOLDER, filename1)
                file1.save(file_path1)
                message = 'Kriterija bija atjanotas'
            else:
                return redirect(url_for('admin.admin', message='Invalid file format for the first PDF, only PDFs are allowed')), 302
        
        if 'pdf_1' in files:
            file2 = files['pdf_1']
            
            if file2.filename == '':
                return redirect(url_for('admin.admin', message='No selected file for the second PDF')), 302
            
            if file2 and file2.filename.endswith('.pdf'):
                filename2 = 'grafiks.pdf'
                file_path2 = os.path.join(UPLOAD_FOLDER, filename2)
                file2.save(file_path2)
                message = 'Dežures grafiks bija atjanotas'
            else:
                return redirect(url_for('admin.admin', message='Invalid file format for the second PDF, only PDFs are allowed')), 302
        
        if 'pdf' not in files and 'pdf_1' not in files:
            return redirect(url_for('admin.admin', message='No files part'))

    return redirect(url_for('admin.admin', message=message)), 302


@admin_bp.route('/clear_database', methods=['POST'])
@login_required
def clear_database(): 
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        
        # Проверка, существует ли уже запись с таким именем
        cur.execute("DELETE FROM classes")
        cur.execute("DELETE FROM explanations")
        cur.execute("DELETE FROM criteria")
        conn.commit() 
    return redirect(url_for("admin.admin")), 302

