from app import create_app
from app import backup_db

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    backup_db.start_backup()