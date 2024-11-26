from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange


# Define form model
class ReservationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email",description="Enter your email", validators=[DataRequired(), Email(message="email is invalid")])
    num_people = IntegerField(
        "Number of People", validators=[DataRequired(), NumberRange(min=1)]
    )
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    submit = SubmitField("Reserve Table")
