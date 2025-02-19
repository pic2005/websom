from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
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

class CharacterForm(FlaskForm):
    character = SelectField('Choose your character', choices=[
        ('😀', '😀'), ('😃', '😃'), ('😄', '😄'), ('😁', '😁'), ('😆', '😆'),
        ('😅', '😅'), ('😂', '😂'), ('🤣', '🤣'), ('😊', '😊'), ('😇', '😇'),
        ('🙂', '🙂'), ('🙃', '🙃'), ('😉', '😉'), ('😌', '😌'), ('😍', '😍'),
        ('🥰', '🥰'), ('😘', '😘'), ('😗', '😗'), ('😙', '😙'), ('😚', '😚'),
        ('😋', '😋'), ('😛', '😛'), ('😜', '😜'), ('🤪', '🤪'), ('😝', '😝'),
        ('🤑', '🤑'), ('🤗', '🤗'), ('🤭', '🤭'), ('🤫', '🤫'), ('🤔', '🤔'),
        ('🤐', '🤐'), ('🤨', '🤨'), ('😐', '😐'), ('😑', '😑'), ('😶', '😶'),
        ('😏', '😏'), ('😒', '😒'), ('🙄', '🙄'), ('😬', '😬'), ('🤥', '🤥'),
        ('😌', '😌'), ('😔', '😔'), ('😪', '😪'), ('🤤', '🤤'), ('😴', '😴'),
        ('😷', '😷'), ('🤒', '🤒'), ('🤕', '🤕'), ('🤢', '🤢'), ('🤮', '🤮')
    ], validators=[DataRequired()])
    submit = SubmitField('Save')