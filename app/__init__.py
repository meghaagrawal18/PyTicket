# from flask import Flask
# 
# app = Flask(__name__)
# 
# # Import routes after app initialization
# from app import routes


from flask import Flask
from .db_config import init_db

app = Flask(__name__)

# Initialize database
init_db()

# Import routes after creating app to avoid circular imports
from . import routes