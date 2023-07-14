from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Route for the home page


@app.route('/')
def index():
    return render_template('register.html')

# Route for checking the session and displaying the dashboard


@app.route('/dashboard')
def check_session():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    all_recipes = recipe.Recipe.get_all()
    return render_template('dashboard.html', user=user.User.get_by_id(data), all_recipes=all_recipes)

# Route for handling user registration form submission


@app.route('/register', methods=['POST'])
def register():
    # Validate the registration form data
    if not user.User.validate_user(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "confirm_password": request.form['confirm_password']
    }
    # Save the user and set the user_id in the session
    id = user.User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

# Route for handling user login form submission


@app.route('/login', methods=['POST'])
def login():
    # Retrieve user data by email
    user_data = user.User.get_by_email(request.form)
    if not user_data:
        flash("Invalid Email!", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_data.password, request.form['password']):
        flash("Invalid Password!", "login")
        return redirect('/')
    # Set the user_id in the session
    session['user_id'] = user_data.id
    return redirect('/dashboard')

# Route for logging out


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the home page
    return redirect('/')
