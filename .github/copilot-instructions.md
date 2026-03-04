# AI Agent Instructions - Voice AI Patient Registration System

## Architecture Overview

This is a **voice-first patient registration system** with three interconnected layers:

```
Patient Phone → Vapi.ai (telephony/STT/TTS) → OpenAI GPT-4o (LLM conversation)
    → FastAPI Webhook (validation/persistence) → PostgreSQL (storage)
    ← Web Dashboard (vanilla JS) ←
```

**Critical Flow**: Voice calls trigger Vapi webhooks at `/api/vapi/webhook` which invoke `save_patient` or `check_duplicate` functions. Backend validates via Pydantic, checks duplicates, persists to PostgreSQL, and returns structured responses that Vapi relays to the LLM → caller.

## Project Structure

```
backend/                    # Python FastAPI server
├── app.py                 # Main application w/ lifespan, CORS, global exception handler
├── config/
│   ├── settings.py        # Pydantic Settings (env vars from .env)
│   └── database.py        # Async SQLAlchemy engine + session factory
├── models/patient.py      # SQLAlchemy ORM (UUID PK, soft delete via deleted_at)
├── schemas/patient_schemas.py  # Pydantic validation (phone regex, DOB future check)
└── routers/
    ├── patients.py        # REST CRUD endpoints (GET/POST/PUT/DELETE)
    └── vapi.py           # Vapi webhook handler (save_patient, check_duplicate)

frontend/public/           # Vanilla JS (zero build step)
├── js/
│   ├── config.js         # API_BASE_URL configuration
│   ├── api.js            # Fetch wrapper with error handling
│   └── app.js            # State management, rendering, navigation
└── server.py             # Python dev server (port 3000) with CORS

database/schema.sql        # PostgreSQL schema w/ CHECK constraints, indexes, triggers
docs/VAPI_SETUP.md        # Complete system prompt + function definitions
```

## Critical Patterns

### 1. Async Everywhere
**All database operations use `async/await`**. Use `AsyncSession`, not `Session`:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db

@router.get("/")
async def list_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient))  # ← await required
    patients = result.scalars().all()
```

### 2. Soft Deletes (Not Hard Deletes)
**Never use `DELETE FROM`**. Set `deleted_at` timestamp:

```python
patient.deleted_at = datetime.utcnow()  # Soft delete
await db.commit()
```

All queries filter: `where(Patient.deleted_at.is_(None))`.

### 3. Three-Layer Validation
1. **LLM Prompt** (docs/VAPI_SETUP.md): "DOB cannot be future", "phone must be 10 digits"
2. **Pydantic** (schemas/patient_schemas.py): `@field_validator` for regex, date checks
3. **PostgreSQL** (database/schema.sql): `CHECK (date_of_birth <= CURRENT_DATE)`

### 4. Webhook Response Structure
Vapi expects `{"result": {...}}` envelope. Return structured responses:

```python
return {
    "result": {
        "success": True,
        "message": "Thank you! Your registration is complete.",
        "patient_id": str(new_patient.patient_id)
    }
}
```

On error: `"success": False, "error": True, "message": "Friendly error for caller"`

### 5. Explicit Payload Logging
**Critical requirement**: Log full JSON payloads in webhooks for debugging/audit:

```python
import json
logger.info("=" * 80)
logger.info(f"Raw parameters:\n{json.dumps(parameters, indent=2)}")
logger.info("=" * 80)
```

### 6. Phone as VARCHAR, Not INT
Phone numbers are `VARCHAR(15)` to preserve leading zeros (e.g., international formats). Always clean input:

```python
phone = ''.join(filter(str.isdigit, raw_phone))  # Remove dashes, spaces, parens
```

### 7. Duplicate Detection by Phone
Check before insert to prevent double registration:

```python
existing = await db.execute(
    select(Patient).where(
        and_(
            Patient.phone_number == phone,
            Patient.deleted_at.is_(None)  # ← Exclude soft-deleted
        )
    )
)
if existing.scalar_one_or_none():
    return {"result": {"success": False, "duplicate": True, "message": "..."}}
```

## Developer Workflows

### Running Locally

**Backend** (port 8001):
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # Edit with your DATABASE_URL
uvicorn app:app --reload --port 8001
```

**Frontend** (port 3000):
```bash
cd frontend
python server.py  # Simple HTTP server with CORS
```

**Database Setup**:
```bash
psql -U postgres -d voice_ai_agent -f database/schema.sql
```

### Testing API Directly

```powershell
# List patients
Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/patients" | ConvertFrom-Json

# Create patient (will return 422 if validation fails)
Invoke-WebRequest -Method POST -Uri "http://127.0.0.1:8001/api/patients" `
  -ContentType "application/json" `
  -Body '{"first_name":"Test",...}'

# Test webhook (simulate Vapi call)
Invoke-WebRequest -Method POST -Uri "http://127.0.0.1:8001/api/vapi/webhook" `
  -ContentType "application/json" `
  -Body '{"message":{"type":"function-call","functionCall":{"name":"save_patient","parameters":{...}}}}'
```

### Debugging Webhooks

1. Check Railway logs: `railway logs`
2. Look for structured logs with `===` separators
3. Verify payload: `logger.info(f"Raw parameters:\n{json.dumps(parameters, indent=2)}")`
4. Test locally with ngrok: `ngrok http 8001` → update Vapi webhook URL

## Integration Points

### Vapi.ai Webhooks
- **Endpoint**: `POST /api/vapi/webhook`
- **Message Types**: `function-call`, `end-of-call-report`
- **Functions**: `save_patient` (creates patient), `check_duplicate` (checks by phone)
- **Response**: Return `{"result": {success, message}}` for LLM to speak

### Database Connection
- **Engine**: Async SQLAlchemy with `asyncpg` driver
- **Pool**: 5 connections, max overflow 10
- **Session**: Use `get_db()` dependency injection (auto-closes connection)

### Frontend API Client
- **Base URL**: Configured in `frontend/public/js/config.js`
- **Wrapper**: `api.js` provides `API.getPatients()`, `API.createPatient()`, etc.
- **Error Handling**: Returns 422 for validation errors with detailed field messages

## Environment Variables

Required in `backend/.env`:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5433/voice_ai_agent
VAPI_API_KEY=your_vapi_key         # Optional for API calls
OPENAI_API_KEY=your_openai_key     # Optional if using directly
CORS_ORIGINS=["*"]                 # JSON array format
```

## Conventions

- **Logging Format**: `logger.info("📞 Vapi webhook received")` with emojis for readability
- **HTTP Status Codes**: 201 (created), 409 (duplicate), 422 (validation), 500 (server error)
- **UUID PKs**: Use `uuid4()` for distributed-system compatibility
- **Timestamps**: `created_at`, `updated_at` (auto-updated via trigger), `deleted_at` (soft delete)
- **Error Responses**: `{"data": null, "error": "User-friendly message"}`
- **Success Responses**: `{"data": {...}, "message": "Success message"}`

## Common Pitfalls

1. **Don't forget `await`**: All DB operations are async (`await db.execute()`, `await db.commit()`)
2. **Don't hard delete**: Use `patient.deleted_at = datetime.utcnow()`, not `db.delete(patient)`
3. **Don't skip duplicate check**: Always check phone before insert in webhook handler
4. **Don't return stack traces**: Global exception handler returns generic 500, logs full trace
5. **Don't mix sync/async**: Use `asyncpg`, not `psycopg2`; use `AsyncSession`, not `Session`

## Key Files for Context

**Understanding the system**:
- `TECHNICAL_EXPLANATION.md` - Complete technical walkthrough (3,500 lines)
- `docs/VAPI_SETUP.md` - Full system prompt (confirmation flow is CRITICAL)
- `CRITICAL_ITEMS_AUDIT.md` - 10 common mistakes + fixes

**Making changes**:
- `backend/schemas/patient_schemas.py` - Add field validators here
- `backend/routers/vapi.py` - Webhook logic + Vapi response formatting
- `database/schema.sql` - Database constraints (always add CHECK for validation)
- `frontend/public/js/app.js` - UI state management + rendering logic

## Modifying the System

**Add new patient field**:
1. Update `database/schema.sql` (add column + CHECK constraint)
2. Update `models/patient.py` (add `Mapped[type]` field)
3. Update `schemas/patient_schemas.py` (add to PatientBase + add `@field_validator` if needed)
4. Update `docs/VAPI_SETUP.md` (add to collection flow in prompt)
5. Update Vapi function schema (add to `save_patient` parameters)
6. Run migration or recreate DB

**Add new Vapi function**:
1. Add handler in `backend/routers/vapi.py` (e.g., `handle_update_patient`)
2. Add function schema in Vapi dashboard
3. Update system prompt to call new function
4. Test with curl: `POST /api/vapi/webhook` with mock payload

**Debug validation errors**:
- 422 from Pydantic → check `schemas/patient_schemas.py` validators
- 500 from database → check `database/schema.sql` CHECK constraints match Pydantic
- Agent doesn't validate in call → update prompt in `docs/VAPI_SETUP.md` VALIDATE section

## Production Deployment

**Backend** (Railway):
```bash
railway login
railway init
railway add postgresql
railway up
railway logs  # Check for errors
```

**Vapi Configuration**:
1. Copy full prompt from `docs/VAPI_SETUP.md`
2. Add `save_patient` function with schema from doc
3. Set webhook URL: `https://your-railway-url.up.railway.app/api/vapi/webhook`
4. Buy phone number, assign to assistant

**Critical Post-Deploy**:
- Test confirmation read-back (agent MUST read all fields before saving)
- Test duplicate detection (call twice with same phone)
- Test invalid data (future DOB, short phone) - agent should re-prompt
- Check logs show full JSON payload with `json.dumps(parameters, indent=2)`
