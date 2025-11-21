from app import create_app

# Create application using the factory
app = create_app()


if __name__ == "__main__":
    # Run development server
    app.run(debug=True)
