from flask import (
    Flask,
    render_template,
    json,
    jsonify,
    request,
    redirect,
    flash,
    url_for,
)
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Date, DateTime
from datetime import datetime, timezone
from forms import ReservationForm
from models import Reservation
from database import SessionLocal
import os

app = Flask(__name__, instance_relative_config=True)

app.config["SECRET_KEY"] = "my_secret_key"  # for CSRF protection
# Configure the SQLite database

# route for the home page
@app.route("/")
def home():
    return render_template("index.html")


# route for menu page
@app.route("/menu")
def menu():
    food_items, drink_items = load_menu()
    return render_template("menu.html", food_items=food_items, drink_items=drink_items)


# helper function to load data
def load_menu():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_directory, "menu.json")
    with open(json_path, "r") as file:
        menu_data = json.load(file)

    # access items key
    items = menu_data["items"]

    # categorise items
    food_items = [item for item in items if item["category"] == "Food"]
    drink_items = [item for item in items if item["category"] == "Drinks"]

    return food_items, drink_items


# route for about us page
@app.route("/about_us")
def about_us():
    return render_template("about_us.html")


# route for reservations
@app.route("/reservations", methods=["GET", "POST"])
def reservations():
    # Log type of request
    if request.method == "POST":
        print("POST request received")
    else:
        print("GET request received")

    # create form object
    form = ReservationForm()

    # handle form submission
    if form.validate_on_submit():  # POST request with valid form data
        # open a database session
        db_session = SessionLocal()

        # Create and save reservation
        reservation = Reservation(
            name=form.name.data,
            email=form.email.data,
            num_people=form.num_people.data,
            date=form.date.data,
        )
        db_session.add(reservation)
        db_session.commit()
        db_session.close() #close session after committing

        
        # flash success message
        return jsonify({
            "message": f"Your reservation for {form.num_people.data} people on {form.date.data} has been "
            f"successfully added {form.name.data}. If any issues arise, we will contact you at {form.email.data}."
        })

        # # redirect back to the same route
        # return redirect(url_for("reservations"))
        

    # handle GET request
    return render_template("reservations.html", form=form)


# route for contacts
@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
