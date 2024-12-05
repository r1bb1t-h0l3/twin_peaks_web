import os
import pytest
from flask import Flask
from app import (
    app,
    Reservation,
    SessionLocal,
    get_available_slots
)  # Import necessary components such as flask app and database
from forms import ReservationForm
from database import SessionLocal, initialize_db
from sqlalchemy.sql import text
from datetime import datetime
from unittest.mock import MagicMock, patch
from datetime import datetime, time



@pytest.fixture
def client():
    """
    Pytest fixture to create a test client for the Flask application.
    It initializes a temporary SQLite database for testing.
    """
    # Configure the app for testing
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory DB
    app.config["SECRET_KEY"] = "test"

    with app.test_client() as client:
        with app.app_context():
            # Initialize test database
            initialize_db()

            yield client  # Provide the test client to the tests

            # Cleanup: Drop all tables
            with SessionLocal() as session:
                session.execute(text("DROP TABLE IF EXISTS reservations"))
                session.commit()


def test_home_page(client):
    """
    Test the home page renders successfully.
    """
    response = client.get("/")
    assert response.status_code == 200

    # Check specific content from `index.html loads` - index menu items
    assert b"Twin Peaks Diner" in response.data  # Title from `base.html`
    assert b"Menu" in response.data
    assert b"Reservations" in response.data
    assert b"About Us" in response.data
    assert b"Contact" in response.data

    # Check that images render
    assert b"images/menu.jpg" in response.data
    assert b"images/reservations.jpg" in response.data
    assert b"images/about_us.jpg" in response.data
    assert b"images/contact.jpg" in response.data


def test_menu_page(client):
    """
    Test the menu page renders successfully and contains expected content.
    """
    response = client.get("/menu")
    assert response.status_code == 200
    assert b"Menu" in response.data  # Adjust to match your template content


def test_reservations_page_get(client):
    """
    Test that the reservations page renders the form on a GET request.
    """
    response = client.get("/reservations")
    assert response.status_code == 200
    assert b"Reserve Table" in response.data  # Check the form's submit button text


def test_reservations_page_post_invalid_email(client):
    """
    Test submitting invalid email in the reservation form.
    """
    invalid_data = {
        "name": "Jane Doe",
        "email": "not-an-email",
        "num_people": 2,
        "date": "2024-12-01",
    }
    response = client.post("/reservations", data=invalid_data)
    assert response.status_code == 200
    assert b"email is invalid" in response.data  # Check for error message


def test_about_us_page(client):
    """
    Test the About Us page renders successfully.
    """
    response = client.get("/about_us")
    assert response.status_code == 200

    # check `base.html content loads correctly`
    assert b"Twin Peaks Diner" in response.data  # Title from `base.html`
    assert b"menu" in response.data
    assert b"reservations" in response.data
    assert b"about us" in response.data
    assert b"contact" in response.data

    # Check headers and images load
    assert b"Norma Jennings" in response.data
    assert b"Shelley Briggs" in response.data
    assert b"images/shelley.png" in response.data
    assert b"images/norma.png" in response.data


def test_contact_page(client):
    """
    Test the contact page renders successfully and contains the iframe.
    """
    # Send a GET request to the /contact route
    response = client.get("/contact")

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that specific iframe-related content is present in the HTML
    assert b'<iframe src="https://www.google.com/maps/embed?pb=' in response.data

    # Optionally, check for other content specific to the contact page
    assert b"Opening hours: 09:00 - 00:00" in response.data
    assert b"Phone number: 425-831-5512" in response.data
    assert b"Address: 135 W North Bend Way, North Bend, Washington"


@patch("app.SessionLocal")
def test_get_available_slots(mock_session):
    # Mock database session
    mock_db_session = MagicMock()
    mock_session.return_value = mock_db_session

    # Mock reservations
    mock_reservations = [
        MagicMock(date=datetime(2024, 12, 5).date(), time=time(17, 0), duration=1),
        MagicMock(date=datetime(2024, 12, 5).date(), time=time(17, 30), duration=1),
    ]
    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_reservations

    # Call the function
    date_to_test = datetime(2024, 12, 5)
    slots = get_available_slots(date_to_test)

    # Assertions
    assert slots[time(17, 0)] == 5  # Decremented once
    assert slots[time(17, 30)] == 4  # Decremented twice
    assert slots[time(18, 0)] == 5  # Decremented once
    assert slots[time(18, 30)] == 6  # Not decremented

@patch("app.get_available_slots")
def test_get_available_slots_api(mock_get_slots, client):
    # Mock available slots
    mock_slots = {time(17, 0): 5, time(17, 30): 6}
    mock_get_slots.return_value = mock_slots

    # Make the request
    response = client.get("/get_available_slots/2024-12-05?time=17:00")

    # Parse the response
    data = response.get_json()

    # Assertions
    assert response.status_code == 200
    assert data["17:00"] == 5

@patch("app.get_available_slots")
@patch("app.SessionLocal")
def test_reservations_post(mock_session, mock_get_slots, client):
    # Mock database session
    mock_db_session = MagicMock()
    mock_session.return_value = mock_db_session

    # Mock available slots
    mock_slots = {datetime.strptime("17:00", "%H:%M").time(): 5}
    mock_get_slots.return_value = mock_slots

    # Mock form data
    form_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "num_people": 2,
        "date": "2024-12-05",
        "time": "17:00",
    }

    # Make the POST request
    response = client.post("/reservations", data=form_data)

    # Assertions
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["is_valid"] is True
    assert "successfully added" in response_data["message"]
    mock_db_session.add.assert_called_once()  # Ensure reservation was added
    mock_db_session.commit.assert_called_once()  # Ensure commit was called
