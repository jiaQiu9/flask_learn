from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
# the login_required, means that the user needs to login in order to access 
# the content


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)

    
# ADD METHOD SO THAT THE ROUTER METHOD COULD GET AND POST INFO
@app.route('/register', methods=['GET','POST'])
def register_page():
    # what happens when user submits forms
    form = RegisterForm()
    if form.validate_on_submit():

        user_to_create=User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        # submit changes to db
        db.session.add(user_to_create)
        db.session.commit()
        # redirect user to registered user page, or different page
        # after the user clicked the submit button

        # cross site request forgery (CSRF) - one of the know hacker attacks, steal and perform attacks on database
        
        # the following two lines of code allows us to redirect and login the user after creating the account
        # if no error occured, then login the user
        login_user(user_to_create)
        # flash is the build in function, that provides extra information to the user
        flash(f'Accoutn created successfully! You are now logged in as {user_to_create.username}',category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}: # if there are no errors from validation
        for err_msg in form.errors.values():
            flash(f' There was an error with creating a user : {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    # runs two function behind, validate information, hide submit conditional
    if form.validate_on_submit():
        # .first grabs the data
        attempted_user = User.query.filter_by(username=form.username.data).first()
        # to overcome the hasing encoding of the password
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            # flash is the build in function, that provides extra information to the user
            flash(f'Success! You are logged in as :{attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else: 
            # danger is for displaying the red message. 
            flash(f'Username and password are not matched! Please try again.', category='danger')

    return render_template('login.html',form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out!', category='info')
    return redirect(url_for("home_page"))