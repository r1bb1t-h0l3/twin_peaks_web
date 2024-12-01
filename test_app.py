import os
import pytest
from flask import Flask
from app import (
    app,
    Reservation,
    SessionLocal,
)  # Import necessary components such as flask app and database
from forms import ReservationForm
from database import SessionLocal, initialize_db
from sqlalchemy.sql import text
from datetime import datetime


@pytest.fixture
def client():
    """
    Pytest fixture to create a test client for the Flask application.
    """
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_reservations.db"
    test_client = app.test_client()

    # Initialize test database
    initialize_db()

    yield test_client

    # Clean up database after tests
    with SessionLocal() as session:
        session.execute(text("DROP TABLE IF EXISTS reservation"))
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


def test_reservations_page_post_valid_data(client):
    """
    Test submitting valid reservation data via POST.
    """
    valid_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "num_people": 4,
        "date": "2024-12-01",
    }
    
    response = client.post(
        "/reservations",
        data=valid_data,
        content_type="multipart/form-data",  # Simulate form submission
    )

    print(response.data)

    assert response.status_code == 200
    assert b"Your reservation for" in response.data  # Check for success message


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


def test_database_interaction(client):
    """
    Test that a reservation is correctly added to the database.
    """
    with app.app_context():
        session = SessionLocal()
        new_reservation = Reservation(
            name="Alice Example",
            email="alice@example.com",
            num_people=3,
            date=datetime.strptime("2024-12-10", "%Y-%m-%d").date(),
        )
        session.add(new_reservation)
        session.commit()

        # Query the database
        reservation = (
            session.query(Reservation).filter_by(email="alice@example.com").first()
        )
        assert reservation is not None
        assert reservation.name == "Alice Example"
        assert reservation.num_people == 3
        assert reservation.email == "alice@example.com"
        assert reservation.date == datetime.strptime("2024-12-10", "%Y-%m-%d").date()
        session.close()
