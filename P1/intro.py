# need to use the export FLASK_APP=intro.py
# then flask run

from flask import Flask 
app= Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1> hello world  but bigger, changed</h1>'

# behavior of dynamic routes
@app.route('/about/<username>')
def about_page(username):
    return f'<h1>this is the about page of {username}</h1>'