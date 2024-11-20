from sqlalchemy import Column, Integer, String, Boolean, Numeric, Date, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Plan(Base):
    __tablename__ = "plans"

    # Primary and Identifying Fields
    plan_id = Column(Integer, primary_key=True)
    plan_name = Column(Text)
    plan_code = Column(Text)
    plan_type = Column(Text)
    sub_type = Column(Text)
    is_active = Column(Boolean, default=True)

    # Network Information
    network_name = Column(Text)
    network_region = Column(Text)
    network_type = Column(Text)

    # Financial Information
    deductible_individual = Column(Numeric(10, 2))
    deductible_family = Column(Numeric(10, 2))
    oop_max_individual = Column(Numeric(10, 2))
    oop_max_family = Column(Numeric(10, 2))
    premium_base_rate = Column(Numeric(10, 2))

    # Coverage Details
    prior_auth_requirements = Column(Text)
    copay_structure = Column(Text)
    covered_services_summary = Column(Text)
    exclusions = Column(Text)

    # Additional Benefits
    dental_coverage = Column(Text)
    vision_coverage = Column(Text)
    hearing_coverage = Column(Text)
    fitness_benefits = Column(Text)
    telehealth_coverage = Column(Text)

    # Vendor Information
    dental_vendor = Column(Text)
    vision_vendor = Column(Text)
    hearing_vendor = Column(Text)
    fitness_vendor = Column(Text)

    # Administrative Fields
    effective_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Text, nullable=False)
    last_modified_by = Column(Text)

    # External Network Access
    external_network_vendors = Column(Text)