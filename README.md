# Voice AI Agent - Patient Registration System

> 🏥 **Production-ready voice-based AI agent** for automated U.S. patient demographic registration

[![System Status](https://img.shields.io/badge/status-ready-brightgreen)]()
[![Python](https://img.shields.io/badge/python-%3E%3D3.9-brightgreen)]()
[![PostgreSQL](https://img.shields.io/badge/postgresql-14%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## 📞 Live Demo

- **Phone Number**: `+1 (276) 582-5544`
- **Backend API**: `https://voice-ai-patient-registration-production.up.railway.app`
- **Frontend Dashboard**: Check your Railway dashboard at [railway.app/project/calm-spirit](https://railway.com/project/4d172bb5-f637-46df-8d32-df2ffb12a439)

### 📌 Important: Viewing New Patient Data

**After registering a new patient via phone call, you MUST hard refresh your browser to see the updated data on the dashboard:**

- **Windows/Linux**: `Ctrl + Shift + R` or `Ctrl + F5`
- **Mac**: `Cmd + Shift + R` or `Cmd + Option + R`
- **Alternative**: Clear browser cache and reload

This ensures you're viewing the latest patient records without cached data.

---

### 🎯 Try It Now

Call the number above to experience the voice AI agent firsthand!

---

## 🎯 Project Overview

This system provides a **voice-based AI agent** that:
- Answers phone calls via a real U.S. phone number
- Conducts natural conversations to collect patient demographics
- Validates and confirms information before saving
- Persists data to a PostgreSQL database
- Exposes patient records through a REST API
- Provides a web dashboard for viewing records

**Key Features:**
- ✅ Natural language conversation (LLM-powered)
- ✅ Real-time data validation
- ✅ Duplicate detection by phone number
- ✅ Confirmation flow before saving
- ✅ RESTful API with full CRUD operations
- ✅ Persistent database with proper constraints
- ✅ Optional web dashboard
- ✅ Production-ready deployment guide

---

## 🏗️ Architecture

```
┌─────────────┐
│   Caller    │
│   (Phone)   │
└──────┬──────┘
       │
       ↓
┌─────────────────────┐
│     Vapi.ai         │ ← Voice AI Platform
│  (Telephony + STT)  │   (Handles speech recognition,
└──────┬──────────────┘    text-to-speech, LLM routing)
       │
       ↓
┌─────────────────────┐
│   OpenAI GPT-4o     │ ← Large Language Model
│   (Conversation)    │   (Natural conversation logic)
└──────┬──────────────┘
       │
       ↓ Function Call
┌─────────────────────┐
│   FastAPI Server    │ ← Backend Server
│   (Python)          │   (Validation, business logic)
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│   PostgreSQL        │ ← Database
│   (Patient Data)    │   (Persistent storage)
└─────────────────────┘
       ↑
       │ REST API
┌─────────────────────┐
│   Web Dashboard     │ ← Frontend (Optional)
│   (Simple HTML/JS)  │   (View patient records)
└─────────────────────┘
```

---

## 📋 Tech Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| **Voice AI** | Vapi.ai | Fastest integration, handles telephony/STT/TTS complexity |
| **LLM** | OpenAI GPT-4o-mini | Cost-effective, sub-second latency, reliable |
| **Backend** | Python + FastAPI | Best for LLM integration, modern async framework, rich AI ecosystem |
| **Database** | PostgreSQL | Production-ready, proper constraints, ACID compliance |
| **Hosting** | Railway | Easy deployment, integrated PostgreSQL, free tier |
| **Frontend** | Vanilla HTML/CSS/JS | Zero build step, works everywhere, fast load |

---

## ⚖️ Known Limitations & Trade-offs

This system was built with **intentional trade-offs** to prioritize rapid development and core functionality:

### Current Limitations

| Limitation | Reason | Production Fix |
|------------|--------|----------------|
| **No Authentication** | Focus on core voice AI functionality | Add JWT auth + /login endpoint (2-4 hours) |
| **CORS allow_origins=["*"]** | Allow any origin during development | Restrict to specific domain in production |
| **Vanilla JS Frontend** | Zero build complexity, fast iteration | Migrate to React/Vue if team needs component reuse |
| **Vapi Vendor Dependency** | Fastest telephony integration (hours vs weeks) | Abstract behind interface if multi-vendor needed |
| **No Rate Limiting** | Simplified initial deployment | Add slowapi middleware (100 req/min per IP) |
| **Basic Error Logging** | Console/file logging sufficient for MVP | Add Sentry/Datadog for production monitoring |
| **Single Database Table** | Simple data model for MVP scope | Add appointments, providers, audit_log tables |
| **No Call Recording** | Privacy-first, HIPAA considerations | Enable Vapi recording if legally compliant |

### Intentional Design Decisions

**Why Async FastAPI?** → Handles concurrent webhook calls efficiently (important when multiple patients call simultaneously)

**Why Soft Deletes?** → Audit trail required for healthcare compliance (HIPAA), enables "undo" operations

**Why UUID Primary Keys?** → Distributed-system friendly, no collision risk if scaling horizontally

**Why Phone as VARCHAR?** → Preserves leading zeros (e.g., `0551234567` international format), allows formatting

**Why PostgreSQL CHECK Constraints?** → Defense-in-depth validation (Pydantic can have bugs; database is final authority)

### Next Steps for Production

See [TECHNICAL_EXPLANATION.md](docs/TECHNICAL_EXPLANATION.md) for full architecture details and [DEPLOYMENT_PLAN.md](docs/DEPLOYMENT_PLAN.md) for deployment guide.

---

## 🚀 Quick Start (Development)

### Prerequisites
- 🐍 Python 3.9+ ([Download](https://www.python.org/downloads/))
- 🐘 PostgreSQL 14+ ([Download](https://www.postgresql.org/download/))
- 🎤 Vapi.ai account ([Sign up](https://vapi.ai/))
- 🤖 OpenAI API key ([Get key](https://platform.openai.com/))

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd voice-ai-agent
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
# Or on macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

Edit `.env` with your credentials:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/patient_registration
VAPI_API_KEY=your_vapi_key
PORT=3000
```

### 3. Setup Database

```bash
# Create database
createdb patient_registration

# Run schema
psql patient_registration < ../database/schema.sql

# (Optional) Load seed data
psql patient_registration < ../database/seed.sql
```

### 4. Start Backend

```bash
# Development mode (with auto-reload)
python app.py

# Or with uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 3000
```

Server runs at `http://localhost:3000` ✅

Interactive API docs at `http://localhost:3000/docs` 🚀

### 5. Setup Frontend (Optional)

```bash
cd ../frontend
python server.py
```

Dashboard at `http://localhost:3000` ✅

> **Note**: After adding new patient data, hard refresh your browser (`Ctrl+Shift+R`) to see updated records.

### 6. Configure Vapi.ai

See detailed guide: [VAPI_SETUP.md](docs/VAPI_SETUP.md)

**Quick steps:**
1. Create Vapi account → Get API key
2. Provision U.S. phone number
3. Create assistant with system prompt (see `docs/VAPI_SETUP.md`)
4. Configure webhook: `https://your-backend-url.railway.app/api/vapi/webhook`
5. Call your number and test! 📞

---

## 🤖 Vapi System Prompt

The following prompt is configured in Vapi to guide the voice AI agent's conversation:

````
You are a friendly and professional patient registration assistant for a medical clinic. Your job is to collect patient demographic information through natural conversation.

REQUIRED INFORMATION TO COLLECT:
1. First Name
2. Last Name
3. Date of Birth (MM/DD/YYYY format)
4. Sex (Male, Female, Other, or Decline to Answer)
5. Phone Number (10-digit U.S. number)
6. Complete Address: Street address, Apartment/Suite (optional), City, State (2-letter), ZIP code

OPTIONAL INFORMATION (ask if caller wants to provide):
7. Email address
8. Insurance provider and member ID
9. Emergency contact name and phone number
10. Preferred language

CONVERSATION FLOW:

1. GREETING: "Hello! Thank you for calling. I'm here to help you register as a new patient. This will only take a few minutes. May I start by getting your first name?"

2. COLLECT INFORMATION NATURALLY - Be conversational and warm, adapt to caller's responses

3. VALIDATE AS YOU GO:
   - Date of Birth: Cannot be in the future
   - Phone: Must be 10 digits
   - State: Valid 2-letter abbreviation
   - ZIP: 5-digit or ZIP+4 format

4. OFFER OPTIONAL FIELDS: "Perfect! I have all the required information. I can also collect your insurance information, emergency contact, and preferred language if you'd like. Would you like to provide any of those?"

5. CONFIRMATION (CRITICAL): Before saving, read back ALL information:
   "Let me confirm your information:
   - Name: [First] [Last]
   - Date of Birth: [MM/DD/YYYY]
   - Sex: [Sex]
   - Phone Number: ([XXX]) [XXX-XXXX]
   - Address: [Address], [City], [State] [ZIP]
   [... optional fields if provided ...]
   
   Is this information correct, or would you like to change anything?"

6. AFTER SUCCESSFUL SAVE: "Perfect! You're all registered, [First Name]. We look forward to seeing you at your appointment. Have a great day!"

ERROR HANDLING:
- INVALID DATE: "I need a valid date of birth in month, day, year format."
- FUTURE DOB: "That date is in the future. What's your correct date of birth?"
- DATABASE ERROR: "I apologize, but there was a technical issue. Please try calling back in a few minutes."

 DO: Be warm, friendly, professional. Acknowledge responses. Handle interruptions gracefully.
 DON'T: Rush. Sound robotic. Save without confirmation.

TONE: Professional yet warm, like a friendly medical receptionist.
````

> **Note**: Full prompt with all details available in [docs/VAPI_SETUP.md](docs/VAPI_SETUP.md)

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Backend README](backend/README.md) | API endpoints, setup, deployment |
| [Vapi Setup Guide](docs/VAPI_SETUP.md) | Step-by-step Vapi.ai configuration |
| [Technical Explanation](docs/TECHNICAL_EXPLANATION.md) | Complete architecture and design decisions |
| [Deployment Guide](docs/DEPLOYMENT_PLAN.md) | Deploy to Railway with full configuration |
| [Testing Guide](docs/TESTING_GUIDE.md) | Comprehensive testing procedures |
| [Business Overview](docs/BUSINESS_OVERVIEW.md) | Use cases and business value |
| [Contributing](docs/CONTRIBUTING.md) | Contribution guidelines |
| [Changelog](docs/CHANGELOG.md) | Version history |

---

## 🧪 Testing

### Test REST API

```bash
# Health check
curl http://localhost:3000/health

# Create patient
curl -X POST http://localhost:3000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "date_of_birth": "1990-05-15",
    "sex": "Female",
    "phone_number": "5551234567",
    "address_line_1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001"
  }'

# List patients
curl http://localhost:3000/api/patients

# Search by last name
curl "http://localhost:3000/api/patients?last_name=Doe"
```

### Test Voice Agent

1. **Call the phone number** provisioned in Vapi: `+1 (276) 582-5544`
2. **Follow the conversation** - the agent will guide you
3. **Provide test information**:
   - First name: "John"
   - Last name: "Smith"
   - DOB: "March 15, 1985"
   - Sex: "Male"
   - Phone: "555-123-4567"
   - Address: "456 Oak Street, Los Angeles, California, 90001"
4. **Confirm information** when prompted
5. **Check database or dashboard**: Should see new patient record
   - **Important**: Hard refresh your browser (`Ctrl+Shift+R`) to see the new entry on the dashboard

---

## 📊 Patient Data Model

### Required Fields
- `first_name` (1-50 chars, letters only)
- `last_name` (1-50 chars, letters only)
- `date_of_birth` (valid date, not future)
- `sex` (Male, Female, Other, Decline to Answer)
- `phone_number` (10-digit U.S. format)
- `address_line_1` (street address)
- `city` (city name)
- `state` (2-letter U.S. state code)
- `zip_code` (5-digit or ZIP+4)

### Optional Fields
- `email` (valid email format)
- `address_line_2` (apt/suite)
- `insurance_provider`
- `insurance_member_id`
- `preferred_language` (default: English)
- `emergency_contact_name`
- `emergency_contact_phone`

### Auto-Generated
- `patient_id` (UUID)
- `created_at` (timestamp)
- `updated_at` (timestamp)
- `deleted_at` (soft delete)

---

## 🎨 Features

### ✅ Implemented
- [x] Voice agent with natural conversation
- [x] LLM-powered intent understanding
- [x] Real-time validation (DOB, phone, state, ZIP)
- [x] Confirmation flow before saving
- [x] Error handling and re-prompting
- [x] Database persistence with constraints
- [x] REST API with full CRUD
- [x] Duplicate detection by phone number
- [x] Soft delete (audit trail)
- [x] Query filters (name, DOB, phone)
- [x] Web dashboard for viewing records
- [x] Responsive design
- [x] Production deployment ready

### 🚀 Bonus Features (If Implemented)
- [ ] Multi-language support (Spanish)
- [ ] Call transcripts stored in DB
- [ ] Appointment scheduling
- [ ] SMS confirmation after registration
- [ ] Automated tests (Jest/Supertest)

---

## 🛠️ Project Structure

```
voice-ai-agent/
├── backend/                    # Node.js Express API
│   ├── src/
│   │   ├── config/            # Database connection
│   │   ├── models/            # Data models (Patient)
│   │   ├── controllers/       # Business logic
│   │   ├── routes/            # API routes
│   │   ├── middleware/        # Validation, error handling
│   │   ├── services/          # Vapi integration
│   │   └── app.js             # Main application
│   ├── package.json
│   ├── .env.example
│   └── README.md
├── frontend/                   # Simple web dashboard (optional)
│   ├── public/
│   │   ├── index.html
│   │   ├── css/styles.css
│   │   └── js/
│   │       ├── config.js
│   │       ├── api.js
│   │       └── app.js
│   └── package.json
├── database/                   # SQL schema and seeds
│   ├── schema.sql
│   └── seed.sql
├── docs/                       # Detailed documentation
│   ├── VAPI_SETUP.md          # Voice AI configuration
│   ├── TECHNICAL_EXPLANATION.md
│   ├── DEPLOYMENT_PLAN.md
│   ├── TESTING_GUIDE.md
│   ├── TESTING_WORKFLOW.md
│   ├── BUSINESS_OVERVIEW.md
│   ├── CONTRIBUTING.md
│   └── CHANGELOG.md
├── README.md                   # This file
└── .gitignore
```

---

## 🚢 Deployment

### Option 1: Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Add PostgreSQL
railway add postgresql

# Deploy backend
cd backend
railway up

# Set webhook in Vapi dashboard
# URL: https://your-project.railway.app/api/vapi/webhook
```

### Option 2: Render

1. Connect GitHub repository
2. Create Web Service for backend
3. Add PostgreSQL database
4. Set environment variables
5. Deploy

### Option 3: Fly.io

```bash
fly launch
fly postgres create
fly deploy
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

---

## ⚠️ Known Limitations & Trade-offs

### Trade-offs Made
1. **Vapi vs DIY**: Used Vapi to focus on integration, not STT/TTS implementation
2. **PostgreSQL vs SQLite**: Chose PostgreSQL for production-readiness (requires setup)
3. **No Authentication**: API is open (out of scope for 3-hour challenge)
4. **No HIPAA Compliance**: Demo system, not production healthcare app
5. **Soft Deletes Only**: Preserving audit trail, no hard deletes

### Known Limitations
- No rate limiting on API endpoints
- No authentication/authorization
- No call recording storage (only metadata)
- English language only (no i18n)
- Basic error handling (could be more robust)

---

## 🤝 Contributing

For production enhancements:
1. Add authentication (JWT, OAuth)
2. Implement HIPAA compliance
3. Add comprehensive test suite
4. Set up monitoring and logging
5. Implement rate limiting
6. Add backup and disaster recovery
7. Multi-language support
8. EMR/EHR integration

---

## 📝 License

MIT License - see LICENSE file for details

---

## � Support

For questions or issues, review documentation in `/docs` or test with sample data in `database/seed.sql`.

---

## 🎯 About This Project

This system demonstrates modern voice AI integration:
- **System Integration**: Connecting telephony, LLM, database, and API layers
- **Prompt Engineering**: Effective conversational design for voice interfaces
- **Data Validation**: Multi-layer validation (LLM → API → Database)
- **Production Thinking**: Deployment, error handling, and edge case management
- **Modern Architecture**: Async Python, RESTful design, cloud deployment

---

**Built with modern AI, voice, and cloud technologies**

