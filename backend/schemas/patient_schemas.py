"""
Pydantic schemas for patient data validation.
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date, datetime
from uuid import UUID
import re

US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
]

SEX_OPTIONS = ['Male', 'Female', 'Other', 'Decline to Answer']

class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: date
    sex: str
    phone_number: str = Field(..., pattern=r'^\d{10}$')
    email: Optional[EmailStr] = None
    address_line_1: str = Field(..., min_length=1, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    insurance_provider: Optional[str] = Field(None, max_length=255)
    insurance_member_id: Optional[str] = Field(None, max_length=100)
    preferred_language: Optional[str] = Field("English", max_length=50)
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v):
        if not re.match(r"^[A-Za-z\-']+$", v):
            raise ValueError('Name can only contain letters, hyphens, and apostrophes')
        return v
    
    @field_validator('sex')
    @classmethod
    def validate_sex(cls, v):
        if v not in SEX_OPTIONS:
            raise ValueError(f'Sex must be one of: {", ".join(SEX_OPTIONS)}')
        return v
    
    @field_validator('state')
    @classmethod
    def validate_state(cls, v):
        v_upper = v.upper()
        if v_upper not in US_STATES:
            raise ValueError(f'Invalid U.S. state abbreviation')
        return v_upper
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_dob(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    """All fields optional for partial updates."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    date_of_birth: Optional[date] = None
    sex: Optional[str] = None
    phone_number: Optional[str] = Field(None, pattern=r'^\d{10}$')
    email: Optional[EmailStr] = None
    address_line_1: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    zip_code: Optional[str] = Field(None, pattern=r'^\d{5}(-\d{4})?$')
    insurance_provider: Optional[str] = Field(None, max_length=255)
    insurance_member_id: Optional[str] = Field(None, max_length=100)
    preferred_language: Optional[str] = Field(None, max_length=50)
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, pattern=r'^\d{10}$')

class PatientResponse(PatientBase):
    """Schema for patient response"""
    patient_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PatientListResponse(BaseModel):
    """Schema for list of patients response"""
    data: list[PatientResponse]
    count: int
    error: Optional[str] = None
    timestamp: datetime

class PatientSingleResponse(BaseModel):
    """Schema for single patient response"""
    data: Optional[PatientResponse]
    error: Optional[str] = None
    message: Optional[str] = None
    timestamp: datetime

class DuplicateCheckResponse(BaseModel):
    """Schema for duplicate check response"""
    exists: bool
    patient: Optional[dict] = None
