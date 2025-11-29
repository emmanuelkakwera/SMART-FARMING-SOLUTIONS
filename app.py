from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Farm, SoilRecord, AnimalHealth
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create tables
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user_farms = Farm.query.filter_by(user_id=current_user.id).all()

        # Fixed query - only get records that exist
        recent_soil_tests = []
        recent_animal_health = []

        # Only try to get soil tests if farms exist
        if user_farms:
            farm_ids = [farm.id for farm in user_farms]
            recent_soil_tests = SoilRecord.query.filter(
                SoilRecord.farm_id.in_(farm_ids)
            ).order_by(SoilRecord.test_date.desc()).limit(3).all()

            recent_animal_health = AnimalHealth.query.filter(
                AnimalHealth.farm_id.in_(farm_ids)
            ).order_by(AnimalHealth.treatment_date.desc()).limit(3).all()

        return render_template('dashboard.html',
                               farms=user_farms,
                               soil_tests=recent_soil_tests,
                               animal_health=recent_animal_health)

    except Exception as e:
        print(f"Dashboard error: {e}")
        # Return empty dashboard if there's an error
        return render_template('dashboard.html',
                               farms=[],
                               soil_tests=[],
                               animal_health=[])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("🚨 === REGISTRATION FORM SUBMITTED ===")

        # Get form data
        username = request.form.get('username', '').strip()
        phone = request.form.get('phone', '').strip()
        full_name = request.form.get('full_name', '').strip()
        location = request.form.get('location', '').strip()
        password = request.form.get('password', '').strip()

        # Debug print all form data
        print(f"📝 Username: '{username}'")
        print(f"📝 Phone: '{phone}'")
        print(f"📝 Full Name: '{full_name}'")
        print(f"📝 Location: '{location}'")
        print(f"📝 Password: '{password}'")

        # Check if any field is empty
        if not all([username, phone, full_name, location, password]):
            print("❌ Missing form fields!")
            flash('Please fill in all fields', 'error')
            return redirect(url_for('register'))

        # Check if user exists
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            print("❌ User already exists with this phone")
            flash('Phone number already registered', 'error')
            return redirect(url_for('register'))

        try:
            # Create new user
            user = User(
                username=username,
                phone=phone,
                full_name=full_name,
                location=location,
                password_hash=password
            )

            db.session.add(user)
            db.session.commit()
            print("✅ USER CREATED SUCCESSFULLY IN DATABASE!")

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            print(f"❌ DATABASE ERROR: {e}")
            flash(f'Registration failed: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("🚨 === LOGIN ATTEMPT STARTED ===")

        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()

        print(f"📱 Phone entered: '{phone}'")
        print(f"🔑 Password entered: '{password}'")

        # Check if fields are empty
        if not phone or not password:
            print("❌ Missing login fields!")
            flash('Please fill in all fields', 'error')
            return redirect(url_for('login'))

        # Find user by phone
        user = User.query.filter_by(phone=phone).first()

        if user:
            print(f"✅ User found: {user.username}")
            print(f"🔑 Password check: stored='{user.password_hash}', entered='{password}'")

            if user.password_hash == password:
                login_user(user)
                print("🎉 LOGIN SUCCESSFUL!")
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                print("❌ Password incorrect!")
                flash('Invalid phone number or password', 'error')
        else:
            print("❌ User not found!")
            flash('Invalid phone number or password', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.location = request.form.get('location')
        current_user.language = request.form.get('language')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html')


@app.route('/farm/create', methods=['GET', 'POST'])
@login_required
def create_farm():
    if request.method == 'POST':
        farm_name = request.form.get('farm_name')
        farm_size = request.form.get('farm_size')
        farm_type = request.form.get('farm_type')
        soil_type = request.form.get('soil_type')
        main_crops = request.form.get('main_crops')
        livestock_types = request.form.get('livestock_types')

        farm = Farm(
            user_id=current_user.id,
            farm_name=farm_name,
            farm_size=float(farm_size),
            farm_type=farm_type,
            soil_type=soil_type,
            main_crops=main_crops,
            livestock_types=livestock_types
        )

        db.session.add(farm)
        db.session.commit()

        flash('Farm profile created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_farm.html')


# Simple routes for soil and animals (no database queries)
@app.route('/soil')
@login_required
def soil():
    return render_template('soil.html')


@app.route('/animals')
@login_required
def animals():
    return render_template('animals.html')


@app.route('/animals/<category>')
@login_required
def animal_category(category):
    return render_template('animal_category.html', category=category)


if __name__ == '__main__':
    app.run(debug=True)