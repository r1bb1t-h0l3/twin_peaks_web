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
from sqlalchemy import func
import os
import logging


app = Flask(__name__, instance_relative_config=True)

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
    Calculate the available time slots for reservations on a given date.

    This function generates time slots for the restaurant's operating hours 
    and adjusts their availability based on existing reservations. Each slot 
    represents a specific time interval (e.g., 30 minutes), and the number of 
    available tables per slot is updated based on overlapping reservations.

    Args:
        date (datetime): The specific date to check availability for reservations.
        tables (int): The total number of tables available in the restaurant. Default is 6.
        interval (int): The duration of each time slot in minutes (e.g., 30 minutes). Default is 30.

    Returns:
        dict: A dictionary where keys are time slots (as `datetime.time` objects) 
              and values are the number of available tables for each slot.
    """
    print(f"looking for date {date}")
    # Example: Querying reservations for a specific date and time
    
    db_session = SessionLocal()

    reservations = db_session.query(Reservation)
    reservations = reservations.filter(Reservation.date == date.date())
    reservations = reservations.all()


    print(f"Reservations on {date}: {[r.id for r in reservations]}")
    for reservation in db_session.query(Reservation).all():
        print(f"Reservation Date in DB: {reservation.date},(type: {type(reservation.date)})")
        print(f"Input Date: {date} (type: {type(date)})")


    for reservation in reservations:
        print(f"Reservation ID: {reservation.id}, Time: {reservation.time}, Duration: {reservation.duration}")

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
        reserved_time = reservation.time.replace(microsecond=0, second=0)  # Normalize time
        reserved_duration = reservation.duration or 1  # Default to 1 hour if no duration is specified
        reserved_end_time = (datetime.combine(date.date(), reserved_time) +
                             timedelta(hours=reserved_duration)).time()

        print(f"Reservation blocks from {reserved_time} to {reserved_end_time}")

        for slot_time in list(slots.keys()):  # Use list to safely modify dict
            # Check if the slot falls within the reservation period
            if reserved_time <= slot_time < reserved_end_time:
                if slots[slot_time] > 0:
                    print(f"Decrementing slot {slot_time} for reservation at {reserved_time}")
                    slots[slot_time] -= 1
                else:
                    print(f"No available tables left for slot {slot_time}")

    
    # remove fully booked slots
    slots = {slot: count for slot, count in slots.items() if count > 0}
    print(f"Final computed slots: {slots}")
    return slots

#route to get available timeslots API
@app.route("/get_available_slots/<date_str>", methods=["GET"])
def get_available_slots_api(date_str):
    """
    API endpoint to fetch available reservation slots for a specific date.

    This endpoint returns all available time slots for a given date, or a specific count 
    for a requested time slot if a `time` query parameter is provided. The available slots 
    are calculated based on the restaurant's capacity and existing reservations.

    Args:
        date_str (str): A date string in the format "YYYY-MM-DD" representing the date 
                        to fetch the available slots for.

    Query Parameters:
        time (str, optional): A specific time in "HH:MM" format. If provided, the API 
                              will return the count of available tables for that specific time slot.

    Returns:
        json: 
            If `time` query parameter is provided:
                {
                    "<time_str>": <number_of_available_tables>
                }
            If `time` is not provided:
                {
                    "slots": [
                        "<time_slot_1>",
                        "<time_slot_2>",
                        ...
                    ]
                }

    Example Usage:
        GET /get_available_slots/2024-12-05 -> Returns all available time slots for 2024-12-05.
        GET /get_available_slots/2024-12-05?time=17:00 -> Returns available table count for 17:00 on 2024-12-05.
    """
    time_str = request.args.get("time") # Optional timeslot filter
    date = datetime.strptime(date_str, "%Y-%m-%d")
    slots = get_available_slots(date) 
    

    if time_str:
        # Filter for specific time if provided
        specific_time = datetime.strptime(time_str, "%H:%M").time()
        count = slots.get(specific_time, 0)
        print(f"Specific time: {specific_time}, Count: {count}")
        return jsonify({time_str: count})
    else:
        print("Slots fetched successfully!") # Debug print
        app.logger.info(f"Slots fetched: {slots}")
        slots_serializable = [key.strftime("%H:%M") for key, value in slots.items()]


        return jsonify({"slots": slots_serializable})

# route for reservations
@app.route("/reservations", methods=["GET", "POST"])
def reservations():
    """
    Handle the reservations page, supporting both GET and POST requests.

    - **GET Request**: Renders the reservations form and dynamically populates the 
      time slot options based on available slots for the selected date.

    - **POST Request**: 
        - Validates the submitted reservation form data.
        - Saves the reservation details in the database if the form is valid.
        - Returns a JSON response indicating success or error.

    Form Fields:
        - `name`: Name of the customer (string).
        - `email`: Email address of the customer (string).
        - `num_people`: Number of people for the reservation (integer).
        - `date`: Date of the reservation (date).
        - `time`: Time slot for the reservation (select field with available times).

    Returns:
        - On GET: Rendered HTML template (`reservations.html`) containing the reservation form.
        - On POST:
            - **Success**: JSON response with a success message and reservation details.
            - **Failure**: JSON response with validation errors and a failure message.

    Example POST Success Response:
        {
            "message": "John Doe your reservation for 2 people on 2024-12-05 at 17:00 has been successfully added. If any issues arise, we will contact you at john.doe@example.com.",
            "is_valid": True
        }

    Example POST Failure Response:
        {
            "message": "Invalid form data. Please correct and try again.",
            "errors": {
                "email": "Invalid email address."
            },
            "is_valid": False
        }

    Notes:
        - The time slot options are dynamically updated based on the availability 
          retrieved via the `get_available_slots` function.
        - Uses Flask-WTF for form validation.
        - Commits valid reservations to the `reservations` database table.
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
                "message": f"{form.name.data} your reservation for {form.num_people.data} people on {form.date.data} at {form.time.data} has been "
                f"successfully added. If any issues arise, we will contact you at {form.email.data}.",
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
