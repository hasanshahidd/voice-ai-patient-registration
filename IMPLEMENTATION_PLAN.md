# Voice AI Agent - Patient Registration System
## IMPLEMENTATION PLAN

### Time Allocation (3 Hours)
- **Hour 1**: Backend API + Database Setup (40 min) + Telephony Integration (20 min)
- **Hour 2**: Voice Agent LLM Configuration + Testing (60 min)
- **Hour 3**: Deployment + End-to-End Testing + Documentation (60 min)

---

## PHASE 1: Backend API & Database (40 minutes)

### Database Schema
```sql
CREATE TABLE patients (
  patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  date_of_birth DATE NOT NULL,
  sex VARCHAR(30) NOT NULL,
  phone_number VARCHAR(15) NOT NULL,
  email VARCHAR(255),
  address_line_1 VARCHAR(255) NOT NULL,
  address_line_2 VARCHAR(255),
  city VARCHAR(100) NOT NULL,
  state VARCHAR(2) NOT NULL,
  zip_code VARCHAR(10) NOT NULL,
  insurance_provider VARCHAR(255),
  insurance_member_id VARCHAR(100),
  preferred_language VARCHAR(50) DEFAULT 'English',
  emergency_contact_name VARCHAR(100),
  emergency_contact_phone VARCHAR(15),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_phone_number ON patients(phone_number);
CREATE INDEX idx_last_name ON patients(last_name);
```

### REST API Endpoints
1. **GET /patients** - List all patients (supports ?last_name=, ?date_of_birth=, ?phone_number=)
2. **GET /patients/:id** - Get single patient by UUID
3. **POST /patients** - Create new patient (with validation)
4. **PUT /patients/:id** - Update patient (partial updates allowed)
5. **DELETE /patients/:id** - Soft delete (set deleted_at)
6. **POST /vapi/webhook** - Webhook for Vapi.ai integration

### Validation Rules
- first_name, last_name: 1-50 chars, alphabetic + hyphens/apostrophes
- date_of_birth: Valid date, not in future, format MM/DD/YYYY
- sex: Enum (Male, Female, Other, Decline to Answer)
- phone_number: Valid U.S. 10-digit format
- email: Valid email format (optional)
- state: Valid 2-letter U.S. state abbreviation
- zip_code: 5-digit or ZIP+4 format

---

## PHASE 2: Telephony + Voice AI Integration (20 minutes)

### Vapi.ai Setup
1. Create Vapi.ai account
2. Provision U.S. phone number
3. Configure assistant with:
   - Custom system prompt
   - Function calling for data persistence
   - Confirmation flow

### LLM System Prompt (Critical Component)
```
You are a friendly patient registration assistant for a medical clinic. Your job is to collect patient demographic information through natural conversation.

REQUIRED INFORMATION:
1. First Name
2. Last Name
3. Date of Birth (MM/DD/YYYY format)
4. Sex (Male, Female, Other, or Decline to Answer)
5. Phone Number (10-digit U.S. number)
6. Address (Street address, City, State, ZIP code)

OPTIONAL INFORMATION (ask if caller wants to provide):
- Email address
- Insurance provider and member ID
- Emergency contact name and phone
- Preferred language

CONVERSATION FLOW:
1. Greet warmly: "Hello! I'm calling to help you register as a new patient. This will only take a few minutes. May I have your first name?"
2. Collect required fields naturally - don't just read a list
3. If caller provides info out of order, acknowledge and adapt
4. Handle corrections: "Actually, that's spelled..."
5. Validate as you go:
   - DOB cannot be in the future
   - Phone must be 10 digits
   - State must be valid 2-letter code
6. After required fields, offer: "I can also collect your insurance information, emergency contact, and preferred language. Would you like to provide any of those?"
7. BEFORE SAVING: Read back ALL information and ask "Is this information correct, or would you like to change anything?"
8. On confirmation, call the save_patient function
9. Confirm success: "Perfect! You're all registered, [First Name]. We look forward to seeing you!"

ERROR HANDLING:
- Invalid date: "I need a valid date of birth. Could you provide that in month, day, year format?"
- Invalid phone: "I need a 10-digit phone number. Could you provide that again?"
- Future DOB: "That date is in the future. What's your correct date of birth?"
- Unclear response: "I didn't catch that. Could you repeat [field]?"

Be conversational, empathetic, and professional. You're representing a healthcare provider.
```

### Function Definition for Vapi
```json
{
  "name": "save_patient",
  "description": "Saves confirmed patient demographic information to the database",
  "parameters": {
    "type": "object",
    "properties": {
      "first_name": {"type": "string"},
      "last_name": {"type": "string"},
      "date_of_birth": {"type": "string", "description": "MM/DD/YYYY format"},
      "sex": {"type": "string", "enum": ["Male", "Female", "Other", "Decline to Answer"]},
      "phone_number": {"type": "string"},
      "email": {"type": "string"},
      "address_line_1": {"type": "string"},
      "address_line_2": {"type": "string"},
      "city": {"type": "string"},
      "state": {"type": "string"},
      "zip_code": {"type": "string"},
      "insurance_provider": {"type": "string"},
      "insurance_member_id": {"type": "string"},
      "preferred_language": {"type": "string"},
      "emergency_contact_name": {"type": "string"},
      "emergency_contact_phone": {"type": "string"}
    },
    "required": ["first_name", "last_name", "date_of_birth", "sex", "phone_number", "address_line_1", "city", "state", "zip_code"]
  }
}
```

---

## PHASE 3: Deployment (30 minutes)

### Railway Deployment Steps
1. Create Railway project
2. Add PostgreSQL database
3. Deploy Python backend (FastAPI)
4. Configure environment variables
5. Connect Vapi webhook to Railway URL

### Environment Variables
```
DATABASE_URL=postgresql://...
PORT=3000
ENVIRONMENT=production
VAPI_API_KEY=your_vapi_key
VAPI_PHONE_NUMBER_ID=your_phone_number_id
```

---

## PHASE 4: Testing (30 minutes)

### Test Cases
1. **Happy Path**: Complete registration with all required fields
2. **Error Handling**: Provide invalid DOB, phone, state
3. **Corrections**: Change answers mid-conversation
4. **Optional Fields**: Decline optional information
5. **Confirmation Flow**: Say "no" to confirmation, correct a field
6. **API Testing**: Query patients via REST API
7. **Duplicate Detection**: Call with same phone number twice
8. **Persistence**: Restart server, verify data still exists

---

## EVALUATION CRITERIA FOCUS

### 1. Working System (20%)
- ✅ Phone number is callable
- ✅ Data persists to database
- ✅ API returns stored data
- ✅ Second call shows previous data

### 2. Conversational Quality (20%)
- ✅ Natural language processing
- ✅ Handles corrections gracefully
- ✅ Confirms before saving
- ✅ Handles interruptions

### 3. Technical Architecture (20%)
- ✅ Clear separation: Telephony | LLM | API | Database
- ✅ Proper schema with constraints
- ✅ RESTful endpoints with validation
- ✅ Documented prompt engineering

### 4. Code Quality & Documentation (20%)
- ✅ Organized, readable code
- ✅ Complete README with setup instructions
- ✅ Trade-offs documented
- ✅ LLM prompt included and commented

### 5. Edge Cases & Resilience (20%)
- ✅ Invalid data handling
- ✅ Connection drop handling
- ✅ Database failure handling
- ✅ Restart mid-conversation handling

---

## BONUS FEATURES (If Time Permits)

### Priority Order:
1. **Duplicate Detection** (15 min) - High value, easy implementation
2. **Call Transcript Storage** (10 min) - Useful for debugging
3. **Simple Dashboard** (20 min) - Visual appeal
4. **Automated Tests** (20 min) - Professional touch

---

## KNOWN LIMITATIONS & TRADE-OFFS

### Trade-offs Made:
1. **SQLite vs PostgreSQL**: Using PostgreSQL for production-readiness despite complexity
2. **Vapi vs DIY**: Using Vapi to focus on integration, not STT/TTS implementation
3. **No HIPAA Compliance**: This is a demo, not production healthcare system
4. **Basic Authentication**: No auth on API endpoints (out of scope)
5. **Soft Deletes Only**: Preserving audit trail, no hard deletes

### Known Limitations:
- No rate limiting on API
- No authentication/authorization
- No call recording storage (only transcripts)
- No multi-language support (English only)
- No appointment scheduling integration

---

## SUCCESS METRICS

The system is successful if:
1. ✅ Phone number answers and agent responds
2. ✅ Agent collects all required information naturally
3. ✅ Agent confirms information before saving
4. ✅ Data appears in database with correct types
5. ✅ REST API returns queryable patient records
6. ✅ System survives restart with data intact
7. ✅ Error handling works for invalid inputs
8. ✅ Documentation allows reproduction in < 10 minutes

---

## FILE STRUCTURE

```
voice-ai-agent/
├── backend/
│   ├── src/
│   │   ├── config/
│   │   │   └── database.js
│   │   ├── models/
│   │   │   └── Patient.js
│   │   ├── routes/
│   │   │   └── patients.py
│   │   ├── controllers/
│   │   │   └── patient_controller.py
│   │   ├── middleware/
│   │   │   └── validation.py
│   │   ├── services/
│   │   │   └── vapi_service.py
│   │   └── app.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/ (Optional - Simple Dashboard)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   └── app.js
│   └── package.json
├── database/
│   ├── schema.sql
│   └── seed.sql
├── docs/
│   ├── API.md
│   ├── VAPI_SETUP.md
│   └── DEPLOYMENT.md
├── .gitignore
├── README.md
└── IMPLEMENTATION_PLAN.md
```

---

## NEXT STEPS AFTER SUBMISSION

If this were to go to production:
1. Add HIPAA compliance (encryption at rest/transit, audit logs)
2. Implement authentication/authorization (JWT, OAuth)
3. Add rate limiting and DDoS protection
4. Set up monitoring and alerting (Sentry, DataDog)
5. Implement comprehensive test suite (Jest, Supertest)
6. Add call recording with consent
7. Multi-language support with i18n
8. Appointment scheduling integration
9. EMR/EHR system integration
10. Backup and disaster recovery procedures

---

*This plan is designed to deliver a working, impressive demo in 3 hours while maintaining code quality and demonstrating system design thinking.*
