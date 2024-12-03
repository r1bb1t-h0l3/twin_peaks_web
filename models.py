from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import String, Integer, Date, DateTime, Time
from datetime import datetime, timezone
from datetime import date as dt_date
from datetime import time as dt_time

Base = declarative_base()

# define the Reservation model
class Reservation(Base):
    """
    Represents a reservation in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database (`reservations`).
        id (int): The unique identifier for the reservation. Primary key.
        name (str): The name of the person making the reservation. Cannot be null.
        email (str): The email of the person making the reservation. Cannot be null.
        num_people (int): The number of people for the reservation. Cannot be null.
        date (datetime.date): The date of the reservation. Cannot be null.
        created_at (datetime.datetime): The timestamp when the reservation was created.
            Defaults to the current UTC time.
    """

    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    num_people: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[dt_date] = mapped_column(Date, nullable=False)
    time: Mapped[dt_time] = mapped_column(Time, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


def __repr__(self) -> str:
    """
    Return a string representation of the reservation instance.

    Returns:
        str: A string in the format "<Reservation {name} for {num_people} on {date}>"
    """
    return f"<Reservation {self.name} for {self.num_people} on {self.date}>"
