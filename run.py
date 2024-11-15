from app import create_app
from app import backup_db
import threading
import time

app = create_app()

if __name__ == '__main__':
    # Создаем потоки для каждой функции
    thread1 = threading.Thread(app.run(debug=True))
    thread2 = threading.Thread(backup_db.start_backup())

    # Запускаем потоки
    thread1.start()
    thread2.start()

    # app.run(debug=True)
    # backup_db.start_backup()


