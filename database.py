from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Base


print("Running database.py")

# database connection URI
DATABASE_URI = "sqlite:///instance/reservations.db"
"""
str: The URI for connecting to the SQLite database. 
     Uses a relative path pointing to 'instance/reservations.db'.
"""

# create SQLALchemy engine
engine = create_engine(DATABASE_URI, echo=True)
"""
sqlalchemy.engine.Engine: The database engine instance for managing connections 
                           to the SQLite database. 
                           `echo=True` enables logging of SQL statements.
"""

# create a session factory
SessionLocal = sessionmaker(bind=engine)
"""
sqlalchemy.orm.sessionmaker: A session factory bound to the database engine.
                              Sessions created by this factory handle database transactions.
"""

# Initialize tables
def initialize_db():
    """
    Create all tables defined in the models if they do not already exist.

    This function uses SQLAlchemy's `Base.metadata.create_all` method to ensure
    that all tables mapped to ORM models are created in the database.

    Returns:
        None
    """
    print("Creating tables")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

if __name__ == "__main__":
    initialize_db()
    print("Database setup complete")