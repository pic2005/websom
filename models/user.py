from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    character = db.Column(db.String(1), nullable=True)
    period_start_date = db.Column(db.Date, nullable=True)  # เพิ่มคอลัมน์นี้
    period_end_date = db.Column(db.Date, nullable=True)  # เพิ่มคอลัมน์นี้

    def __repr__(self):
        return f'<User {self.username}>'