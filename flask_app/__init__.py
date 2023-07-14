from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Set the secret key for the application
app.secret_key = "The last of its kind"
