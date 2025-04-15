# Импорт приложения из основного файла
from app import app

# Точка входа для WSGI-сервера
if __name__ == "__main__":
    app.run() 