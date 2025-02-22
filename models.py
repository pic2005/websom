from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# กำหนดโมเดล PainLog ก่อน User
class PainLog(db.Model):
    __tablename__ = 'pain_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_date = db.Column(db.DateTime, default=datetime.utcnow)
    pain_level = db.Column(db.String(10), nullable=False)
    pain_note = db.Column(db.String(500), nullable=True)

# กำหนดโมเดล User หลังจาก PainLog
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    period_start_date = db.Column(db.DateTime, nullable=True)
    period_end_date = db.Column(db.DateTime, nullable=True)
    pain_logs = db.relationship('PainLog', backref='user', lazy=True)