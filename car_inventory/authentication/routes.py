
   
from flask import Blueprint, render_template, request
from car_inventory.forms import UserLoginForm
from car_inventory.models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        

        # create (instantiate) a new user class and add that user into the table
        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()

    
    return render_template('signup.html', form = form)

@auth.route('/signin')
def signin():
    return render_template('signin.html')