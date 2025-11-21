from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, NumberRange


class RegistrationForm(FlaskForm):
    # Full name is required
    fullname = StringField("Full Name", validators=[DataRequired()])

    # Email is required and must be valid
    email = StringField("Email", validators=[DataRequired(), Email()])

    # Age is optional but if provided must be between 10 and 120
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=10, max=120)])

    # Short biography (optional)
    bio = TextAreaField("Bio", validators=[Optional()])

    submit = SubmitField("Register")


class UpdateForm(FlaskForm):
    # Same validations as registration for updating
    fullname = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=10, max=120)])
    bio = TextAreaField("Bio", validators=[Optional()])
    submit = SubmitField("Update")
