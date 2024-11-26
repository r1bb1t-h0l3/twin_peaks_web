from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


# database connection URI
DATABASE_URI = "sqlite:///instance/reservations.db"

# create SQLALchemy engine
engine = create_engine(DATABASE_URI, echo=True)

# create a session factory
SessionLocal = sessionmaker(bind=engine)

# create tables if they don't exist
Base.metadata.create_all(engine)