import os
from app import create_app

# Create application using the factory
app = create_app()


if __name__ == "__main__":
    # Development server (debug mode only in development)
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
