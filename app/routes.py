from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from . import db
from .models import User
from .forms import RegistrationForm, UpdateForm
from email_validator import validate_email, EmailNotValidError

# Blueprint for main application routes
main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    """Show all stored profiles on the homepage."""
    users = User.query.all()
    return render_template("profile.html", users=users)


@main.route("/register", methods=["GET", "POST"])
def register():
    """Handle registration of a new profile.

    Validates form input, ensures email uniqueness, and saves to the DB.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check for duplicate email before creating user
        existing = User.query.filter_by(email=form.email.data.lower()).first()
        if existing:
            flash("Email already registered.", "danger")
            return render_template("register.html", form=form)

        user = User(
            fullname=form.fullname.data,
            email=form.email.data.lower(),
            age=form.age.data,
            bio=form.bio.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Profile created successfully.", "success")
        return redirect(url_for("main.index"))

    # On GET or validation failure, show the registration form
    return render_template("register.html", form=form)


# ----------------------
# JSON API Endpoints
# ----------------------


@main.route("/api/users", methods=["GET"])
def api_get_users():
    """Return all users as JSON.

    This provides an API alongside the UI for listing profiles.
    """
    users = User.query.all()
    data = [
        {"id": u.id, "fullname": u.fullname, "email": u.email, "age": u.age, "bio": u.bio}
        for u in users
    ]
    return jsonify(data)


@main.route("/api/users", methods=["POST"])
def api_create_user():
    """Create a new user from JSON payload.

    Validates required fields and email using email_validator. Returns JSON response.
    """
    payload = request.get_json() or {}
    fullname = payload.get("fullname")
    email = payload.get("email")
    age = payload.get("age")
    bio = payload.get("bio")

    # Basic validation: fullname and email required
    if not fullname:
        return jsonify({"error": "fullname required"}), 400
    if not email:
        return jsonify({"error": "email required"}), 400

    # Validate email format
    try:
        valid = validate_email(email)
        email = valid.email.lower()
    except EmailNotValidError as e:
        return jsonify({"error": "invalid email", "message": str(e)}), 400

    # Validate age if provided
    if age is not None:
        try:
            age = int(age)
        except (TypeError, ValueError):
            return jsonify({"error": "age must be an integer"}), 400
        if age < 10 or age > 120:
            return jsonify({"error": "age out of range"}), 400

    # Check for duplicate email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 400

    user = User(fullname=fullname, email=email, age=age, bio=bio)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "message": "created"}), 201


@main.route("/api/users/<int:user_id>", methods=["PUT"])
def api_update_user(user_id):
    """Update existing user with JSON payload.

    Mirrors the UI update logic but returns JSON responses.
    """
    user = User.query.get_or_404(user_id)
    payload = request.get_json() or {}
    fullname = payload.get("fullname")
    email = payload.get("email")
    age = payload.get("age")
    bio = payload.get("bio")

    if not fullname:
        return jsonify({"error": "fullname required"}), 400
    if not email:
        return jsonify({"error": "email required"}), 400

    # Validate email
    try:
        valid = validate_email(email)
        email = valid.email.lower()
    except EmailNotValidError as e:
        return jsonify({"error": "invalid email", "message": str(e)}), 400

    # Check email uniqueness
    other = User.query.filter_by(email=email).first()
    if other and other.id != user.id:
        return jsonify({"error": "email already registered by another user"}), 400

    # Validate age
    if age is not None:
        try:
            age = int(age)
        except (TypeError, ValueError):
            return jsonify({"error": "age must be an integer"}), 400
        if age < 10 or age > 120:
            return jsonify({"error": "age out of range"}), 400

    user.fullname = fullname
    user.email = email
    user.age = age
    user.bio = bio
    db.session.commit()

    return jsonify({"id": user.id, "message": "updated"})


@main.route("/update/<int:user_id>", methods=["GET", "POST"])
def update(user_id):
    """Preload existing user data into a form and allow updates.

    Uses db.session.commit() to persist changes.
    """
    user = User.query.get_or_404(user_id)
    form = UpdateForm(obj=user)  # preload form with object data

    if form.validate_on_submit():
        # Prevent changing to an email that belongs to someone else
        other = User.query.filter_by(email=form.email.data.lower()).first()
        if other and other.id != user.id:
            flash("Email already registered by another user.", "danger")
            return render_template("update.html", form=form, user=user)

        user.fullname = form.fullname.data
        user.email = form.email.data.lower()
        user.age = form.age.data
        user.bio = form.bio.data
        db.session.commit()  # persist changes
        flash("Profile updated.", "success")
        return redirect(url_for("main.index"))

    return render_template("update.html", form=form, user=user)
