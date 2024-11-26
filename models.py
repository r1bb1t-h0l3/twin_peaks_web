from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Date, DateTime
from datetime import datetime, timezone
from datetime import date as dt_date

# define basse class for all models
class Base(DeclarativeBase):
    pass

# define the Reservation model
class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    num_people: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[dt_date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda:datetime.now(timezone.utc)
        )


def __repr__(self) -> str:
    return f"<Reservation {self.name} for {self.num_people} on {self.date}>"