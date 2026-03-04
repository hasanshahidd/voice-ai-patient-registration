/**
 * Seed Data for Patient Registration System
 * 
 * Provides sample patient records for testing and demonstration.
 * DO NOT use real patient data - this is for demo purposes only.
 */

-- Insert sample patients
INSERT INTO patients (
  first_name, last_name, date_of_birth, sex, phone_number,
  email, address_line_1, address_line_2, city, state, zip_code,
  insurance_provider, insurance_member_id, preferred_language,
  emergency_contact_name, emergency_contact_phone
) VALUES
(
  'John',
  'Doe',
  '1985-03-15',
  'Male',
  '5551234567',
  'john.doe@example.com',
  '123 Main Street',
  'Apt 4B',
  'New York',
  'NY',
  '10001',
  'Blue Cross Blue Shield',
  'BC123456789',
  'English',
  'Jane Doe',
  '5559876543'
),
(
  'Maria',
  'Garcia',
  '1990-07-22',
  'Female',
  '5552345678',
  'maria.garcia@example.com',
  '456 Oak Avenue',
  NULL,
  'Los Angeles',
  'CA',
  '90001',
  'Aetna',
  'AET987654321',
  'Spanish',
  'Carlos Garcia',
  '5558765432'
),
(
  'Robert',
  'Johnson',
  '1978-11-30',
  'Male',
  '5553456789',
  'robert.j@example.com',
  '789 Pine Road',
  'Suite 200',
  'Chicago',
  'IL',
  '60601',
  'UnitedHealthcare',
  'UHC456789123',
  'English',
  'Sarah Johnson',
  '5557654321'
),
(
  'Emily',
  'Chen',
  '1995-05-18',
  'Female',
  '5554567890',
  'emily.chen@example.com',
  '321 Elm Street',
  NULL,
  'San Francisco',
  'CA',
  '94102',
  'Kaiser Permanente',
  'KP789123456',
  'English',
  'Michael Chen',
  '5556543210'
),
(
  'James',
  'O''Brien',
  '1982-09-12',
  'Male',
  '5555678901',
  NULL,
  '654 Maple Drive',
  'Unit 3',
  'Boston',
  'MA',
  '02101',
  NULL,
  NULL,
  'English',
  'Patricia O''Brien',
  '5555432109'
);

-- Verify inserts
SELECT 
  patient_id,
  CONCAT(first_name, ' ', last_name) AS full_name,
  date_of_birth,
  phone_number,
  city,
  state,
  created_at
FROM patients
WHERE deleted_at IS NULL
ORDER BY created_at;

-- Display count
SELECT COUNT(*) AS total_patients FROM patients WHERE deleted_at IS NULL;
