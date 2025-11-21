# Flask Profile Manager

A complete Flask web application for managing user profiles with registration, viewing, and updating capabilities. Includes both UI and REST API endpoints.

## Features

✨ **User Management**
- Register new profiles with validation
- View all stored profiles dynamically
- Update existing profiles with preloaded form
- SQLite persistent storage

🔐 **Form Validation (Flask-WTF)**
- Required field validation
- Email format validation
- Age range validation (10–120)
- Duplicate email detection

🏗️ **Architecture**
- Flask app factory pattern
- Blueprint-based routing
- SQLAlchemy ORM with models
- WTForms for form handling
- Bootstrap 5 responsive UI

🔌 **API Endpoints**
- `GET /api/users` — List all users
- `POST /api/users` — Create new user
- `PUT /api/users/<id>` — Update user
- `GET /` — Home page (UI)
- `GET /register` — Registration form
- `POST /register` — Submit registration
- `GET /update/<id>` — Update form (preloaded)
- `POST /update/<id>` — Submit update

## Project Structure

```
flask_profile_app/
├── app/
│   ├── __init__.py           # App factory & extensions
│   ├── models.py             # User SQLAlchemy model
│   ├── forms.py              # WTForms registration & update
│   ├── routes.py             # Blueprint with UI & API routes
│   ├── templates/
│   │   ├── base.html         # Base template with navbar & styles
│   │   ├── register.html     # Registration form
│   │   ├── profile.html      # List all profiles
│   │   └── update.html       # Update profile form
│   └── static/               # Static assets (CSS, JS, images)
├── tests/
│   └── test_app.py           # Pytest test cases (8 tests)
├── run.py                    # Entry point
├── requirements.txt          # Production dependencies
├── Procfile                  # Deployment config (Heroku/gunicorn)
└── README.md                 # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/flask_profile_app.git
   cd flask_profile_app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

**Development Server:**
```bash
python run.py
```
Visit `http://127.0.0.1:5000` in your browser.

**Production (with gunicorn):**
```bash
gunicorn run:app
```

## Testing

Run all pytest tests:
```bash
pytest -q
```

**Test Coverage:**
- Valid registration
- Missing fullname validation
- Invalid email format
- Age out of range validation
- Duplicate email detection
- API user creation and listing
- API user update

## API Examples

### Create User (JSON)
```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"fullname": "John Doe", "email": "john@example.com", "age": 30, "bio": "Software developer"}'
```

### Get All Users
```bash
curl http://127.0.0.1:5000/api/users
```

### Update User
```bash
curl -X PUT http://127.0.0.1:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"fullname": "Jane Doe", "email": "jane@example.com", "age": 28}'
```

## Code Quality

✓ **8+ meaningful comments** explaining:
  - App factory initialization
  - Database model design
  - Form validation logic
  - Route handlers and API responses
  - Email uniqueness checks

✓ **Best Practices:**
  - Separation of concerns (models, forms, routes)
  - DRY (Don't Repeat Yourself) principle
  - Consistent error handling
  - CSRF protection via Flask-WTF
  - SQL injection prevention via SQLAlchemy ORM

## UI Features

🎨 **Bootstrap 5 Styling**
- Gradient navbar with icons
- Responsive card-based layouts
- Smooth transitions and hover effects
- Error validation feedback
- Empty state messaging
- Professional color scheme

## Dependencies

- Flask >= 2.0
- Flask-WTF >= 1.0
- Flask-SQLAlchemy >= 3.0
- email-validator >= 1.0
- WTForms >= 3.0
- gunicorn >= 20.0

## Deployment

### Heroku
```bash
git push heroku main
```

### Other Platforms
Use `Procfile`:
```
web: gunicorn run:app
```

## License

MIT License - Feel free to use this project for educational purposes.

## Author

Created as a formative assessment Flask application with full CRUD operations, validation, and modern web practices.
