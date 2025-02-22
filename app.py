from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, PeriodAndPainLogForm
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
import os
import calendar
from flask_migrate import Migrate
from datetime import datetime
from models import db
from models import User,PainLog
from flask import Flask, request, redirect, url_for, flash, session




app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# Ensure the templates folder is correctly referenced
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Import models


# # Create database tables
# with app.app_context():
#     db.create_all()

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
            return redirect(url_for('profile'))  # เปลี่ยนเส้นทางไปยังหน้าโปรไฟล์
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



from datetime import datetime, timedelta

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = db.session.get(User, user_id)  # ใช้ Session.get() แทน Query.get()
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('login'))

    current_date = datetime.now().strftime("%d-%m-%Y")  # รูปแบบวันที่เป็น วัน-เดือน-ปี
    next_period_date = None

    if request.method == 'POST':
        period_start_date = request.form.get('period_start_date')
        period_end_date = request.form.get('period_end_date')

        try:
            if period_start_date:
                user.period_start_date = datetime.strptime(period_start_date, "%Y-%m-%d")
            if period_end_date:
                user.period_end_date = datetime.strptime(period_end_date, "%Y-%m-%d")
                next_period_date = user.period_end_date + timedelta(days=28)  # คำนวณวันที่ประจำเดือนรอบถัดไป

            db.session.commit()
            flash('Period dates updated successfully!', 'success')
        except ValueError as e:
            db.session.rollback()
            flash(f'Invalid date format: {e}', 'error')

    # ดึงประวัติการบันทึกอาการ
    pain_logs = PainLog.query.filter_by(user_id=user_id).order_by(PainLog.log_date.desc()).all()

    # จัดรูปแบบวันที่สำหรับแสดงผล
    period_start_date = user.period_start_date.strftime("%Y-%m-%d") if user.period_start_date else None
    period_end_date = user.period_end_date.strftime("%Y-%m-%d") if user.period_end_date else None
    next_period_date = next_period_date.strftime("%d-%m-%Y") if next_period_date else None

    return render_template(
        'profile.html',
        user=user,
        current_date=current_date,
        period_start_date=period_start_date,
        period_end_date=period_end_date,
        next_period_date=next_period_date,
        pain_logs=pain_logs  # ส่งข้อมูลประวัติการบันทึกไปยังเทมเพลต
    )

@app.route('/save_period_and_pain_log', methods=['POST'])
def save_period_and_pain_log():
    user_id = session.get('user_id')
    if not user_id:
        flash('กรุณาเข้าสู่ระบบก่อนบันทึกข้อมูล', 'danger')
        return redirect(url_for('profile'))

    user = db.session.get(User, user_id)
    if not user:
        flash('ไม่พบผู้ใช้', 'danger')
        return redirect(url_for('profile'))

    # ดึงข้อมูลจากฟอร์ม
    period_start_date = request.form.get('period_start_date')
    period_end_date = request.form.get('period_end_date')
    pain_level = request.form.get('pain_level')
    pain_note = request.form.get('pain_note')

    # ตรวจสอบข้อมูล
    if not period_start_date or not period_end_date:
        flash('กรุณากรอกวันที่เริ่มและหมดประจำเดือน', 'danger')
        return redirect(url_for('profile'))

    if not pain_level or int(pain_level) not in range(1, 6):
        flash('กรุณาเลือกระดับความเจ็บปวดที่ถูกต้อง', 'danger')
        return redirect(url_for('profile'))

    try:
        # ตรวจสอบวันที่
        start_date = datetime.strptime(period_start_date, "%Y-%m-%d")
        end_date = datetime.strptime(period_end_date, "%Y-%m-%d")
        if start_date > end_date:
            flash('วันที่เริ่มประจำเดือนต้องไม่เกินวันที่หมดประจำเดือน', 'danger')
            return redirect(url_for('profile'))

        # บันทึกข้อมูลประจำเดือน
        user.period_start_date = start_date
        user.period_end_date = end_date

        # บันทึกอาการเจ็บปวด
        new_pain_log = PainLog(
            user_id=user_id,
            pain_level=pain_level,
            pain_note=pain_note
        )
        db.session.add(new_pain_log)

        db.session.commit()
        flash('บันทึกข้อมูลประจำเดือนและอาการสำเร็จ!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'เกิดข้อผิดพลาดในการบันทึกข้อมูล: {str(e)}', 'danger')

    return redirect(url_for('profile'))
    
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

@app.route('/calendar', methods=['GET', 'POST'])
def calendar_view():
    now = datetime.now()
    cal = ""
    for year in range(2025, 2031):
        cal += f"<h2>{year}</h2>"
        for month in range(1, 13, 2):
            cal += "<div class='row'>"
            cal += "<div class='month'>"
            cal += calendar.HTMLCalendar().formatmonth(year, month)
            cal += "</div>"
            if month + 1 <= 12:
                cal += "<div class='month'>"
                cal += calendar.HTMLCalendar().formatmonth(year, month + 1)
                cal += "</div>"
            cal += "</div>"
    
    user_id = session.get('user_id')
    period_start_date = None
    if user_id:
        user = User.query.get(user_id)
        if request.method == 'POST':
            period_start_date = request.form.get('period_start_date')
            if period_start_date:
                user.period_start_date = datetime.strptime(period_start_date, "%Y-%m-%d")
                db.session.commit()
                flash('Period start date updated successfully!', 'success')
        period_start_date = user.period_start_date.strftime("%Y-%m-%d") if user.period_start_date else None
    
    return render_template('calendar.html', calendar=cal, current_day=now.day, current_month=now.month, current_year=now.year, period_start_date=period_start_date)

@app.route('/period_start_date')
def period_start_date():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        period_start_date = user.period_start_date.strftime("%d-%m-%Y") if user.period_start_date else "ไม่พบข้อมูล"
        return render_template('period_start_date.html', period_start_date=period_start_date)
    return redirect(url_for('login'))
    
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