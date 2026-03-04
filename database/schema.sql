/**
 * Database Schema for Patient Registration System
 * PostgreSQL DDL
 * 
 * Creates the patients table with all required fields
 * and constraints according to U.S. healthcare standards.
 */

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop table if exists (for development/testing only)
-- DROP TABLE IF EXISTS patients CASCADE;

-- Create patients table
CREATE TABLE patients (
  -- Auto-generated fields
  patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,

  -- Required demographic fields
  first_name VARCHAR(50) NOT NULL CHECK (LENGTH(first_name) >= 1),
  last_name VARCHAR(50) NOT NULL CHECK (LENGTH(last_name) >= 1),
  date_of_birth DATE NOT NULL CHECK (date_of_birth <= CURRENT_DATE),
  sex VARCHAR(30) NOT NULL CHECK (sex IN ('Male', 'Female', 'Other', 'Decline to Answer')),
  phone_number VARCHAR(15) NOT NULL CHECK (phone_number ~ '^\d{10}$'),

  -- Required address fields
  address_line_1 VARCHAR(255) NOT NULL,
  address_line_2 VARCHAR(255),
  city VARCHAR(100) NOT NULL CHECK (LENGTH(city) >= 1),
  state VARCHAR(2) NOT NULL CHECK (state ~ '^[A-Z]{2}$'),
  zip_code VARCHAR(10) NOT NULL CHECK (zip_code ~ '^\d{5}(-\d{4})?$'),

  -- Optional contact field
  email VARCHAR(255) CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),

  -- Optional insurance fields
  insurance_provider VARCHAR(255),
  insurance_member_id VARCHAR(100),

  -- Optional additional fields
  preferred_language VARCHAR(50) DEFAULT 'English',
  emergency_contact_name VARCHAR(100),
  emergency_contact_phone VARCHAR(15) CHECK (emergency_contact_phone IS NULL OR emergency_contact_phone ~ '^\d{10}$')
);

-- Create indexes for common queries
CREATE INDEX idx_patients_last_name ON patients(last_name);
CREATE INDEX idx_patients_phone_number ON patients(phone_number);
CREATE INDEX idx_patients_date_of_birth ON patients(date_of_birth);
CREATE INDEX idx_patients_created_at ON patients(created_at DESC);
CREATE INDEX idx_patients_deleted_at ON patients(deleted_at) WHERE deleted_at IS NULL;

-- Create a composite index for common filter combinations
CREATE INDEX idx_patients_search ON patients(last_name, date_of_birth, phone_number) 
WHERE deleted_at IS NULL;

-- Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at
CREATE TRIGGER trigger_update_patients_updated_at
BEFORE UPDATE ON patients
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE patients IS 'Patient demographic information for registration system';
COMMENT ON COLUMN patients.patient_id IS 'Unique patient identifier (UUID)';
COMMENT ON COLUMN patients.first_name IS 'Patient first name (1-50 chars, alphabetic + hyphens/apostrophes)';
COMMENT ON COLUMN patients.last_name IS 'Patient last name (1-50 chars, alphabetic + hyphens/apostrophes)';
COMMENT ON COLUMN patients.date_of_birth IS 'Patient date of birth (cannot be in future)';
COMMENT ON COLUMN patients.sex IS 'Patient sex (Male, Female, Other, Decline to Answer)';
COMMENT ON COLUMN patients.phone_number IS 'Primary contact phone (10-digit U.S. format)';
COMMENT ON COLUMN patients.email IS 'Email address (optional)';
COMMENT ON COLUMN patients.address_line_1 IS 'Street address';
COMMENT ON COLUMN patients.address_line_2 IS 'Apartment/Suite/Unit (optional)';
COMMENT ON COLUMN patients.city IS 'City name';
COMMENT ON COLUMN patients.state IS '2-letter U.S. state abbreviation';
COMMENT ON COLUMN patients.zip_code IS '5-digit or ZIP+4 format';
COMMENT ON COLUMN patients.insurance_provider IS 'Insurance company name (optional)';
COMMENT ON COLUMN patients.insurance_member_id IS 'Insurance member/subscriber ID (optional)';
COMMENT ON COLUMN patients.preferred_language IS 'Preferred language (default: English)';
COMMENT ON COLUMN patients.emergency_contact_name IS 'Emergency contact full name (optional)';
COMMENT ON COLUMN patients.emergency_contact_phone IS 'Emergency contact phone 10-digit (optional)';
COMMENT ON COLUMN patients.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN patients.updated_at IS 'Record last update timestamp';
COMMENT ON COLUMN patients.deleted_at IS 'Soft delete timestamp (NULL if active)';

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON patients TO your_app_user;
