from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Simple HTML templates
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<body>
    <h2>Login Test</h2>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div style="color: red;">{{ messages[0] }}</div>
        {% endif %}
    {% endwith %}
    <form method="POST">
        <input type="text" name="phone" placeholder="Phone" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p><a href="/test-register">Register</a></p>
</body>
</html>
'''

REGISTER_HTML = '''
<!DOCTYPE html>
<html>
<body>
    <h2>Register Test</h2>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div style="color: red;">{{ messages[0] }}</div>
        {% endif %}
    {% endwith %}
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="text" name="phone" placeholder="Phone" required><br><br>
        <input type="text" name="full_name" placeholder="Full Name" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Register</button>
    </form>
    <p><a href="/test-login">Login</a></p>
</body>
</html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<body>
    <h2>Dashboard</h2>
    <p>Welcome, {{ current_user.full_name }}!</p>
    <p>You are logged in successfully! 🎉</p>
    <a href="/test-logout">Logout</a>
</body>
</html>
'''


@app.route('/test-login', methods=['GET', 'POST'])
def test_login():
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()

        print(f"🔑 LOGIN ATTEMPT - Phone: '{phone}', Password: '{password}'")

        user = User.query.filter_by(phone=phone).first()
        print(f"🔍 User found: {user}")

        if user and user.password_hash == password:
            login_user(user)
            print("✅ LOGIN SUCCESS!")
            return redirect('/test-dashboard')
        else:
            print("❌ LOGIN FAILED")
            flash('Invalid credentials')

    return render_template_string(LOGIN_HTML)


@app.route('/test-register', methods=['GET', 'POST'])
def test_register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        phone = request.form.get('phone', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '').strip()

        print(f"📝 REGISTER - Username: '{username}', Phone: '{phone}'")

        if User.query.filter_by(phone=phone).first():
            flash('Phone already exists')
            return redirect('/test-register')

        user = User(
            username=username,
            phone=phone,
            full_name=full_name,
            password_hash=password
        )

        db.session.add(user)
        db.session.commit()
        print("✅ USER REGISTERED!")
        flash('Registration successful! Please login.')
        return redirect('/test-login')

    return render_template_string(REGISTER_HTML)


@app.route('/test-dashboard')
@login_required
def test_dashboard():
    return render_template_string(DASHBOARD_HTML)


@app.route('/test-logout')
@login_required
def test_logout():
    logout_user()
    return redirect('/test-login')


# Initialize database
with app.app_context():
    db.create_all()
    # Create a test user if none exists
    if not User.query.first():
        test_user = User(
            username="test",
            phone="123",
            full_name="Test User",
            password_hash="test"
        )
        db.session.add(test_user)
        db.session.commit()
        print("✅ Test user created: phone='123', password='test'")

if __name__ == '__main__':
    print("🚀 Starting TEST server...")
    print("📱 Test with: phone='123', password='test'")
    app.run(debug=True, port=5001)