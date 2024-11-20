import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def verify_db_connection() -> bool:
    try:
        # Get database URL from environment variable
        database_url = os.environ['DATABASE_URL']
        
        # Create engine
        engine = create_engine(database_url)
        
        # Try to connect
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            print("Database connection successful!")
            return True
            
    except SQLAlchemyError as e:
        print(f"Database connection failed: {str(e)}")
        return False
    except KeyError:
        print("DATABASE_URL environment variable is not set")
        return False