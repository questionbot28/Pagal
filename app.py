import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app = Flask(__name__)

# Ensure we have required environment variables
required_env_vars = ['SESSION_SECRET', 'DATABASE_URL']
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Configure secret key
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure database - handle potential SSL requirement for Render
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'discord_auth.login'

# Import routes after app is created to avoid circular imports
with app.app_context():
    try:
        import models
        from routes import *
        from discord_auth import discord_auth
        app.register_blueprint(discord_auth)

        # Create database tables
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        raise