from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange


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
        validators=[DataRequired(), NumberRange(min=1)],
        render_kw={"placeholder": "2"},
    )
    date = DateField(
        "Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "1990-04-08"},
    )
    submit = SubmitField("Reserve Table")
