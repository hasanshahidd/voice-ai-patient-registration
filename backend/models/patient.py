"""
SQLAlchemy ORM model for patient demographic information.
"""

from sqlalchemy import Column, String, Date, DateTime, func, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from config.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    sex = Column(String(30), nullable=False)
    phone_number = Column(String(15), nullable=False, index=True)
    
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    
    email = Column(String(255), nullable=True)
    
    insurance_provider = Column(String(255), nullable=True)
    insurance_member_id = Column(String(100), nullable=True)
    
    preferred_language = Column(String(50), nullable=True, default="English")
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(15), nullable=True)
    
    # Add check constraints
    __table_args__ = (
        CheckConstraint("sex IN ('Male', 'Female', 'Other', 'Decline to Answer')", name="check_sex_values"),
        CheckConstraint("length(first_name) >= 1 AND length(first_name) <= 50", name="check_first_name_length"),
        CheckConstraint("length(last_name) >= 1 AND length(last_name) <= 50", name="check_last_name_length"),
        CheckConstraint("phone_number ~ '^[0-9]{10}$'", name="check_phone_format"),
        CheckConstraint("length(state) = 2", name="check_state_length"),
        CheckConstraint("zip_code ~ '^[0-9]{5}(-[0-9]{4})?$'", name="check_zip_format"),
    )
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "patient_id": str(self.patient_id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "sex": self.sex,
            "phone_number": self.phone_number,
            "email": self.email,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "insurance_provider": self.insurance_provider,
            "insurance_member_id": self.insurance_member_id,
            "preferred_language": self.preferred_language,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }
    
    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name} ({self.patient_id})>"
