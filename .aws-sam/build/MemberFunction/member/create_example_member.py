# create_example_member.py

# this file will contain a single function with no parameters that uses the database connection to create a sample member in the member database table. They should have an example name like Jane Smith, and make up other data related to this member.

from sqlalchemy.orm import Session
from member.create_member_database import get_db, SessionLocal
from member.member_model import Member
import uuid

def create_example_member():
    db = SessionLocal()
    try:
        # Create a new member with example data
        example_member = Member(
            member_id=str(uuid.uuid4())[:8],  # Generate a unique member ID
            first_name="Jane",
            last_name="Smith",
            relationship="Self",
            created_by="system"
        )
        
        # Add to database
        db.add(example_member)
        db.commit()
        db.refresh(example_member)
        
        print(f"Created example member: {example_member.first_name} {example_member.last_name}")
        return example_member
        
    except Exception as e:
        db.rollback()
        print(f"Error creating example member: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_example_member()