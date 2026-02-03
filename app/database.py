import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from .config import DB_URL

engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

# Retry DB connection on startup
for i in range(10):
    try:
        with engine.connect() as conn:
            print("Database connected!")
            break
    except OperationalError:
        print("Waiting for database...")
        time.sleep(3)
else:
    raise Exception("Could not connect to database")
