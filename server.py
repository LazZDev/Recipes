from flask_app import app

# Import user and recipe controllers
from flask_app.controllers import users, recipes

# Check if the script is directly executed
if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True, host='localhost', port=5000)
