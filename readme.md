# Twin Peaks Diner/Simple Restaurant Reservation System

This is a Flask-based web application designed to manage restaurant reservations, view menus, and provide dynamically updated time slots based on availability. I used a Twin Peaks theme for the visuals and descriptions to make the project more fun.🏞️

## Features

 **Home Page:** Provides an overview of the restaurant.🍴

 **Menu Page:** Displays categorized food and drink items.🥧

 **Reservations Page:**
    Users can book a reservation by filling out a form.
    Available time slots are dynamically updated based on existing reservations.
    Each reservation considers the number of available tables and reservation durations.🌶️

 **API Endpoints:**
    `/get_available_slots/<date_str>`: Fetch available slots for a given date, with an option to query specific time slots.
    📆

 **Contact Page:** Provides restaurant contact information.📇

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [API Documentation](#api-documentation)
* [Unit tests](#unit-tests)
* [Future Enhancements](#future-enhancements)
* [License](#licence)

## Installation

**Clone the repository:**
```
git clone https://github.com/yourusername/restaurant-reservation-system.git
cd restaurant-reservation-system
```
**Create and activate a virtual environment:**
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
**Install the required dependencies:**

`pip install -r requirements.txt`

**Initialize the database:**

`python3 database.py`

## Usage

**Run the Flask application:**

`flask run`

Access the application in your web browser at http://127.0.0.1:5000.

## API Documentation

`/get_available_slots/<date_str>`

Fetches available reservation slots for a given date.

**Method: GET**

Parameters:
    date_str (path): Date in YYYY-MM-DD format.
    time (query, optional): Specific time in HH:MM format.

Responses:
    For all available slots:
```
{
  "slots": ["17:00", "17:30", "18:00", "18:30"]
}
```
For a specific time:
```
{
  "17:00": 3
}
```
## Unit Tests
**Running Tests**

To run the unit tests, ensure that pytest is installed:

```plaintext
 pip install pytest
 pytest
```

**Test Cases**

`test_get_available_slots`:
    Tests the computation of available slots based on reservations.
    Verifies that overlapping reservation durations are handled correctly.

`test_get_available_slots_api`:
    Tests the /get_available_slots API endpoint.
    Verifies that the response contains accurate slot information for all or specific times.

`test_reservations`:
    Tests the reservation form submission.
    Validates form field errors and success messages.

**Example Test Output**

```plaintext
=========================== test session starts ============================
platform darwin -- Python 3.12.0, pytest-7.4.0
collected 3 items

test_app.py ...                                                      [100%]

=========================== 3 passed in 1.23s ======================
```

## Future Enhancements

**Email Notifications:**

* Notify users of successful reservations via email.
* Ability to cancel reservation via email with a cancel button.

## License

This project is licensed under the MIT License. See the LICENSE file for details.🐸