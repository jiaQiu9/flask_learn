from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm
from market import db


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

# ADD METHOD SO THAT THE ROUTER METHOD COULD GET AND POST INFO
@app.route('/register', methods=['GET','POST'])
def register_page():
    # what happens when user submits forms
    form = RegisterForm()
    if form.validate_on_submit():

        user_to_create=User(username=form.username.data, email_address=form.email_address.data, password_hash=form.password1.data)
        # submit changes to db
        db.session.add(user_to_create)
        db.session.commit()
        # redirect user to registered user page, or different page
        # after the user clicked the submit button

        # cross site request forgery (CSRF) - one of the know hacker attacks, steal and perform attacks on database
        
        return redirect(url_for('market_page'))
    if form.errors != {}: # if there are no errors from validation
        for err_msg in form.errors.values():
            flash(f' There was an error with creating a user : {err_msg}', category='danger')

    return render_template('register.html', form=form)