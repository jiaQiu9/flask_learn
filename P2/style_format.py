from flask import Flask, render_template
app=Flask(__name__)


# change route to home.html, direct to html files
# the templates store html files


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#boostrap, ready styling format