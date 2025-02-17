from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, CharacterForm
from werkzeug.security import generate_password_hash, check_password_hash
import os
import calendar
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)

# Ensure the templates folder is correctly referenced
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Import models
from models.user import User
from models.data import Tag

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    website_name = "Women's Stories"
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('home.html', form=form, website_name=website_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('choose_character'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken. Please choose another one.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/choose_character', methods=['GET', 'POST'])
def choose_character():
    form = CharacterForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            user.character = form.character.data
            db.session.commit()
            flash('Character selected successfully!', 'success')
            return redirect(url_for('profile'))
    return render_template('choose_character.html', form=form)

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/what_is_period')
def what_is_period():
    return render_template('what_is_period.html')

@app.route('/abnormalities')
def abnormalities():
    return render_template('abnormalities.html')

@app.route('/period_color')
def period_color():
    return render_template('period_color.html')

@app.route('/period_pain')
def period_pain():
    return render_template('period_pain.html')

@app.route('/period_pain_treatment')
def period_pain_treatment():
    return render_template('period_pain_treatment.html')

@app.route('/abnormal_period_pain_treatment')
def abnormal_period_pain_treatment():
    return render_template('abnormal_period_pain_treatment.html')

@app.route('/calendar')
def calendar_view():
    cal = ""
    for year in range(2025, 2031):
        cal += f"<h2>{year}</h2>"
        cal += calendar.HTMLCalendar().formatyear(year)
    return render_template('calendar.html', calendar=cal)

@app.route('/next_page')
def next_page():
    return render_template('next_page.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)