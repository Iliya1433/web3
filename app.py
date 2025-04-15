# Импорт необходимых модулей Flask и Flask-Login
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
from datetime import timedelta

# Создание экземпляра Flask-приложения
app = Flask(__name__)
# Установка секретного ключа для подписи сессий и cookies
app.secret_key = 'your-secret-key-here'  # В реальном приложении используйте безопасный секретный ключ
# Настройка времени жизни сессии и remember cookie
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Срок жизни постоянной сессии
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)  # Срок жизни remember cookie

# Настройка Flask-Login для управления аутентификацией пользователей
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Страница для перенаправления неавторизованных пользователей
login_manager.remember_cookie_duration = timedelta(days=7)  # Срок жизни remember cookie для Flask-Login

# Класс пользователя, наследуемый от UserMixin для работы с Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username  # Уникальный идентификатор пользователя

# Создание тестового пользователя для демонстрации
user = User('user')

# Функция для загрузки пользователя по его ID
@login_manager.user_loader
def load_user(user_id):
    if user_id == 'user':
        return user
    return None

# Декоратор для проверки аутентификации с перенаправлением на страницу входа
def login_required_with_redirect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для доступа к этой странице необходимо войти в систему.')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Маршрут для главной страницы
@app.route('/')
def index():
    # Подсчет количества посещений страницы с использованием сессии
    if 'visits' not in session:
        session['visits'] = 0
    session['visits'] += 1
    return render_template('index.html', visits=session['visits'])

# Маршрут для страницы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получение данных из формы входа
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        # Проверка учетных данных (в реальном приложении здесь должна быть проверка с базой данных)
        if username == 'user' and password == 'qwerty':
            # Авторизация пользователя
            login_user(user, remember=remember, duration=timedelta(days=7) if remember else None)
            flash('Вы успешно вошли в систему!')
            # Перенаправление на запрошенную страницу или на главную
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль')
    
    return render_template('login.html')

# Маршрут для выхода из системы
@app.route('/logout')
@login_required  # Требуется авторизация
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('index'))

# Маршрут для защищенной страницы
@app.route('/secret')
@login_required_with_redirect  # Требуется авторизация с перенаправлением
def secret():
    return render_template('secret.html')

# Запуск приложения в режиме отладки
if __name__ == '__main__':
    app.run(debug=True) 
