from app import create_app
from app import backup_db
import threading

app = create_app()

def start_backup():
    backup_db.start_backup()

if __name__ == '__main__':
    # Создаем поток для фоновой задачи
    thread = threading.Thread(target=start_backup)

    # Запускаем фоновую задачу
    thread.start()

    # Запускаем Flask-приложение в главном потоке
    app.run(debug=True)

    # Ожидаем завершения фоновой задачи
    thread.join()



