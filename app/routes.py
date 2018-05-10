from flask import render_template

from app import app

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