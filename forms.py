from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class PeriodAndPainLogForm(FlaskForm):
    period_start_date = DateField('วันที่เริ่มมีประจำเดือน', validators=[DataRequired()])
    period_end_date = DateField('วันที่หมดประจำเดือน', validators=[DataRequired()])
    pain_level = SelectField('ระดับความเจ็บปวด', choices=[
        ('1', '😊 ไม่เจ็บ'),
        ('2', '😐 เจ็บเล็กน้อย'),
        ('3', '😕 เจ็บปานกลาง'),
        ('4', '😣 เจ็บมาก'),
        ('5', '😫 เจ็บมากที่สุด')
    ], validators=[DataRequired()])
    pain_note = StringField('บันทึกอาการเพิ่มเติม', validators=[Length(max=500)])
    submit = SubmitField('บันทึกข้อมูล')