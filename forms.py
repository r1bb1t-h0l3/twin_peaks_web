from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange
from datetime import time


# Define form model
class ReservationForm(FlaskForm):
    """
    A Flask-WTF form model for collecting reservation details.

    """

    name = StringField(
        "Name", validators=[DataRequired()], render_kw={"placeholder": "Your Name"}
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="email is invalid")],
        render_kw={"placeholder": "me@example.com"},
    )
    num_people = IntegerField(
        "Number of People",
        validators=[DataRequired(), NumberRange(min=1, max=6, message="For reservations of more than 6 people, please contact us directly.")],
        render_kw={"placeholder": "2"},
    )
    date = DateField(
        "Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "1990-04-08"},
    )
    time = SelectField("Time", validators=[DataRequired()], coerce=str, choices=[], validate_choice=False, render_kw={"placeholder": "Select a time"})
    submit = SubmitField("Reserve Table")
