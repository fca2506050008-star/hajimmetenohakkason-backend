from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///users.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# Import models so that they are registered on `Base`'s metadata,
# then create tables if they don't exist yet.
try:
    import models  # noqa: F401: registers models with Base
    Base.metadata.create_all(bind=engine)
except Exception:
    # If something goes wrong during import (e.g., circular import during
    # startup), don't crash—table creation can be done manually later.
    pass