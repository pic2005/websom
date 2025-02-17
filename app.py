from flask import Flask, render_template, redirect, url_for
from forms import LoginForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Ensure the templates folder is correctly referenced
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# ...existing code...

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    website_name = "Women's Stories"
    if form.validate_on_submit():
        # Add your authentication logic here
        return redirect(url_for('home'))
    return render_template('home.html', form=form, website_name=website_name)

# ...existing code...m)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Add your authentication logic here
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

