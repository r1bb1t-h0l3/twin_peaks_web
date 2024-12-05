from flask import (
    Flask,
    render_template,
    json,
    jsonify,
    request,
)

from forms import ReservationForm
from models import Reservation
from database import SessionLocal
from datetime import datetime, timedelta, time
import os

app = Flask(__name__, instance_relative_config=True)

cached_slots = None

app.config["SECRET_KEY"] = "my_secret_key"  # for CSRF protection
# Configure the SQLite database


# route for the home page
@app.route("/")
def home():
    """
    Render the home page.

    Returns:
        Rendered HTML template for the home page.
    """
    return render_template("index.html")


# route for menu page
@app.route("/menu")
def menu():
    """
    Render the menu page with categorized food and drink items.

    Returns:
        Rendered HTML template for the menu page with food and drink items passed as context.
    """
    food_items, drink_items = load_menu()
    return render_template("menu.html", food_items=food_items, drink_items=drink_items)


# helper function to load data
def load_menu():
    """
    Load and categorize menu items from a JSON file.

    Returns:
        tuple: A tuple containing two lists:
            - food_items (list): Items categorized as food.
            - drink_items (list): Items categorized as drinks.
    """
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
    """
    Render the About Us page.

    Returns:
        Rendered HTML template for the About Us page.
    """
    return render_template("about_us.html")

#route to get available timeslots from db
def get_available_slots(date, tables=6, interval=30):
    """
    Get available time slots for a given date.
    
    Args:
        date (date): The date to check availability.
        tables (int): Number of tables in the restaurant.
        interval (int): Interval in minutes between reservations (e.g., 30).
    
    Returns:
        dict: Available time slots with the number of free tables per slot.
    """
    print(f"looking for date {date}")
    
    db_session = SessionLocal()
    reservations = db_session.query(Reservation)
    reservations = reservations.filter(Reservation.date == date)
    reservations = reservations.all()
    db_session.close()

    # Generate time slots
    opening_time = datetime.strptime("17:00", "%H:%M").time()  # 5:00 PM
    closing_time = datetime.strptime("23:00", "%H:%M").time()  # 11:00 PM
    current_time = datetime.combine(date, opening_time)
    end_time = datetime.combine(date, closing_time)
    slots = {}

    while current_time < end_time:
        slot_time = current_time.time()
        slots[slot_time] = tables  # Initially, all tables are available
        current_time += timedelta(minutes=interval)

    # Adjust availability based on reservations
    for reservation in reservations:
        reserved_time = reservation.time
        reserved_end_time = (datetime.combine(date, reserved_time) +
                             timedelta(hours=reservation.duration)).time()

        for slot_time in slots.keys():
            if reserved_time <= slot_time < reserved_end_time:
                slots[slot_time] -= 1

    return slots

#route to get available timeslots API
@app.route("/get_available_slots/<date_str>", methods=["GET"])
def get_available_slots_api(date_str):
    """
    Fetch available slots for a given date.
    
    Args:
        date (str): Date in YYYY-MM-DD format.
    
    Returns:
        json: Available slots and their availability count.
    """
    global cached_slots
    date = datetime.strptime(date_str, "%Y-%m-%d")
    slots = get_available_slots(date) 
    slots_serializable = [key.strftime("%H:%M") for key, value in slots.items()]
    # result = {"slots": available_slots}

    cached_slots = [key for key, value in slots.items() if value > 0]

    return jsonify({"slots": slots_serializable})

# route for reservations
@app.route("/reservations", methods=["GET", "POST"])
def reservations():
    """
    Handle the reservations page.

    Handles both GET and POST requests:
    - GET: Renders the reservations form.
    - POST: Validates and processes the reservation form data, saves it to the database,
      and returns a success or error message as JSON.

    Returns:
        - Rendered HTML template for the reservations page (GET).
        - JSON response with success or error messages (POST).
    """
    global cached_slots
    # Create form object
    form = ReservationForm(form=request.form)

    # Log type of request
    if request.method == "POST":
        print("POST request received")
        # handle GET request
        # return render_template("reservations.html", form=form)

        print("POST request received")

        # handle form submission
        if not form.validate_on_submit():  # POST request with invalid form data
            # Collect error messages for invalid fields
            error_messages = {
                field_name: error_list[0] 
                for field_name, error_list in form.errors.items()
            }
            return jsonify(
                {
                    "message": "Invalid form data. Please correct and try again.",
                    "errors": error_messages,
                    "is_valid": False
                }
            )

        selected_time = datetime.strptime(form.time.data, "%H:%M").time()
        # If form is valid open a database session
        db_session = SessionLocal()

        # Create and save reservation
        reservation = Reservation(
            name=form.name.data,
            email=form.email.data,
            num_people=form.num_people.data,
            date=form.date.data,
            time=selected_time,
        )
        db_session.add(reservation)
        db_session.commit()
        db_session.close()  # close session after committing

        # Send success message as JSON
        return jsonify(
            {
                "message": f"Your reservation for {form.num_people.data} people on {form.date.data} has been "
                f"successfully added {form.name.data}. If any issues arise, we will contact you at {form.email.data}.",
                "is_valid": True,
            }
        )

    # Handle GET request or form validation failure
    print("GET request received")

    # Dynamically populate time choices if a date is selected
    if form.date.data:  # If a date is selected, fetch available slots
        slots = get_available_slots(form.date.data)
        available_slots = [key.strftime("%H:%M") for key, value in slots.items() if value > 0]
        form.time.choices = [(slot, slot) for slot in available_slots]
    else:
        form.time.choices = []  # No slots available yet

    # Render the reservations page
    return render_template("reservations.html", form=form)


# route for contacts
@app.route("/contact")
def contact():
    """
    Render the contact page.

    Returns:
        Rendered HTML template for the contact page.
    """
    return render_template("contact.html")


if __name__ == "__main__":
    """
    Initialize the database schema and run the Flask application in debug mode.

    This ensures that the required database tables are created (if they do not already exist)
    before the application starts. The app is then launched in debug mode, which provides
    enhanced error messages and automatic reloading for development purposes.
    """
    from database import initialize_db

    initialize_db()
    app.run(debug=True)
