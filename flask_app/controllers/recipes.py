from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe

# Route handler for creating a new recipe


@app.route('/new/recipe')
def new_recipe():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    # Retrieve user data and render the new recipe form
    return render_template('new_recipe.html', user=user.User.get_by_id(data))

# Route handler for processing the creation of a new recipe


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    # Validate the recipe form data
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': int(request.form['under30']),
        'date_made': request.form['date_made'],
        'user_id': session['user_id']
    }
    # Save the new recipe and redirect to the dashboard
    recipe.Recipe.save(data)
    return redirect('/dashboard')

# Route handler for editing a recipe


@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    id = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    user_data = user.User.get_by_id(user_data)
    # Retrieve the recipe data and render the edit recipe form
    return render_template('edit_recipe.html', user=user_data, edit=recipe.Recipe.get_one(id))

# Route handler for updating a recipe


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    # Validate the updated recipe form data
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': int(request.form['under30']),
        'date_made': request.form['date_made'],
        'user_id': session['user_id']
    }
    # Update the recipe and redirect to the dashboard
    recipe.Recipe.update(data)
    return redirect('/dashboard')

# Route handler for showing a recipe


@app.route('/recipe/<int:id>')
def show_recipe(id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    id = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    # Retrieve the recipe and user data, and render the recipe view
    return render_template(
        'show_recipe.html', recipe=recipe.Recipe.get_one(user_data),
        user=user.User.get_by_id(user_data))

# Route handler for deleting a recipe


@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    # Delete the recipe and redirect to the dashboard
    recipe.Recipe.destroy(data)
    return redirect('/dashboard')
