from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy (will be bound to app in the factory)
db = SQLAlchemy()


def create_app(test_config=None):
    """Application factory. Creates and configures the Flask app.

    Args:
        test_config (dict|None): Optional configuration for testing.

    Returns:
        Flask: configured Flask application
    """
    app = Flask(__name__, instance_relative_config=False)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY="devkey",
        SQLALCHEMY_DATABASE_URI="sqlite:///profiles.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Allow overriding config (useful for tests)
    if test_config:
        app.config.update(test_config)

    # Initialize extensions with app
    db.init_app(app)

    # Import and register routes blueprint
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Create DB tables if they don't exist (safe for development)
    with app.app_context():
        db.create_all()

    return app
