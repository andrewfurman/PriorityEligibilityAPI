from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from member.member_model import Base, Member

# Get database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create engine
engine = create_engine(DATABASE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()