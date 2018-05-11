from flask import render_template, flash, redirect

from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sujay'}
    posts = [
        {
            'author' : {'username' : 'Aditya'},
            'body' : 'Best Flask Tutorial'
        },
        {
            'author' : {'username' : 'Jitendra'},
            'body' : 'Learn Python in 24 Hrs'
        }
    ]
    return render_template('index.html', title = 'Web Log', user = user, posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user: {}, remeber_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign In', form = form)