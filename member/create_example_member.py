from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from member_model import Member
import uuid

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_example_member():
    db = SessionLocal()
    try:
        example_member = Member(
            member_id=str(uuid.uuid4())[:8],
            first_name="Matt",
            last_name="Hill",
            relationship="Self",
            created_by="system"
        )
        
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