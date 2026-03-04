# Backend README

## Voice AI Agent - Patient Registration Backend

Backend REST API service for the Voice AI Agent Patient Registration System.

## Tech Stack

- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **Database**: PostgreSQL
- **Voice AI**: Vapi.ai integration
- **Validation**: Joi
- **Security**: Helmet, CORS

## Project Structure

```
backend/
├── src/
│   ├── config/
│   │   └── database.js          # Database connection pool
│   ├── models/
│   │   └── Patient.js            # Patient data model
│   ├── controllers/
│   │   └── patientController.js  # Business logic
│   ├── routes/
│   │   ├── patients.js           # REST API routes
│   │   └── vapi.js               # Vapi webhook routes
│   ├── middleware/
│   │   └── validation.js         # Input validation
│   ├── services/
│   │   └── vapiService.js        # Vapi API client
│   └── app.js                    # Main application
├── database/
│   ├── schema.sql                # Database schema
│   └── seed.sql                  # Sample data
├── package.json
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
PORT=3000
NODE_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/patient_registration
VAPI_API_KEY=your_vapi_api_key
VAPI_PHONE_NUMBER_ID=your_phone_number_id
```

### 3. Setup Database

**Option A: Local PostgreSQL**

```bash
# Create database
createdb patient_registration

# Run schema
psql patient_registration < database/schema.sql

# (Optional) Load seed data
psql patient_registration < database/seed.sql
```

**Option B: Railway / Hosted PostgreSQL**

1. Create PostgreSQL database on Railway
2. Copy DATABASE_URL to `.env`
3. Run migrations using a client or pgAdmin

### 4. Start Server

**Development mode (with auto-reload):**
```bash
npm run dev
```

**Production mode:**
```bash
npm start
```

Server will start on `http://localhost:3000`

## API Endpoints

### Health Check
```
GET /health
```

### Patients

#### List all patients
```
GET /api/patients
Query params: ?last_name=, ?date_of_birth=, ?phone_number=
```

#### Get single patient
```
GET /api/patients/:id
```

#### Create patient
```
POST /api/patients
Body: {
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1985-03-15",
  "sex": "Male",
  "phone_number": "5551234567",
  "address_line_1": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001"
}
```

#### Update patient
```
PUT /api/patients/:id
Body: { "email": "new@example.com" }
```

#### Delete patient (soft delete)
```
DELETE /api/patients/:id
```

#### Check duplicate
```
GET /api/patients/check-duplicate/:phoneNumber
```

### Vapi Webhook

```
POST /api/vapi/webhook
```

This endpoint receives function calls from the Vapi voice agent.

## Response Format

All API responses follow this format:

```json
{
  "data": { ... },
  "error": null,
  "timestamp": "2024-03-03T10:00:00.000Z"
}
```

Error responses:

```json
{
  "data": null,
  "error": "Error message",
  "message": "Detailed description",
  "timestamp": "2024-03-03T10:00:00.000Z"
}
```

## Validation Rules

- **first_name, last_name**: 1-50 chars, letters + hyphens/apostrophes only
- **date_of_birth**: Valid date, cannot be in future, format: YYYY-MM-DD or MM/DD/YYYY
- **sex**: Must be one of: Male, Female, Other, Decline to Answer
- **phone_number**: Exactly 10 digits (U.S. format)
- **email**: Valid email format (optional)
- **state**: Valid 2-letter U.S. state abbreviation
- **zip_code**: 5-digit or ZIP+4 format (12345 or 12345-6789)

## Database Schema

### patients table

| Column | Type | Required | Constraints |
|--------|------|----------|-------------|
| patient_id | UUID | Auto | Primary key |
| first_name | VARCHAR(50) | Yes | 1-50 chars |
| last_name | VARCHAR(50) | Yes | 1-50 chars |
| date_of_birth | DATE | Yes | Not in future |
| sex | VARCHAR(30) | Yes | Enum values |
| phone_number | VARCHAR(15) | Yes | 10 digits |
| email | VARCHAR(255) | No | Valid format |
| address_line_1 | VARCHAR(255) | Yes | - |
| address_line_2 | VARCHAR(255) | No | - |
| city | VARCHAR(100) | Yes | - |
| state | VARCHAR(2) | Yes | 2 letters |
| zip_code | VARCHAR(10) | Yes | 5 or 9 digits |
| insurance_provider | VARCHAR(255) | No | - |
| insurance_member_id | VARCHAR(100) | No | - |
| preferred_language | VARCHAR(50) | No | Default: English |
| emergency_contact_name | VARCHAR(100) | No | - |
| emergency_contact_phone | VARCHAR(15) | No | 10 digits |
| created_at | TIMESTAMP | Auto | Default: now |
| updated_at | TIMESTAMP | Auto | Auto-update |
| deleted_at | TIMESTAMP | No | Soft delete |

## Testing

Test the API using curl:

```bash
# Health check
curl http://localhost:3000/health

# Create patient
curl -X POST http://localhost:3000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Patient",
    "date_of_birth": "1990-01-01",
    "sex": "Male",
    "phone_number": "5551234567",
    "address_line_1": "123 Test St",
    "city": "Test City",
    "state": "NY",
    "zip_code": "10001"
  }'

# List patients
curl http://localhost:3000/api/patients

# Get specific patient
curl http://localhost:3000/api/patients/<patient_id>
```

## Deployment

### Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Add PostgreSQL: `railway add postgresql`
5. Deploy: `railway up`
6. Set environment variables in Railway dashboard

### Other Platforms

- **Render**: Connect GitHub repo, add PostgreSQL database
- **Fly.io**: Use `fly launch` and add Postgres
- **Heroku**: Use Heroku Postgres add-on

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| PORT | Server port | No (default: 3000) |
| NODE_ENV | Environment | No (default: development) |
| DATABASE_URL | PostgreSQL connection string | Yes |
| VAPI_API_KEY | Vapi.ai API key | Yes |
| VAPI_PHONE_NUMBER_ID | Vapi phone number ID | Yes |

## Troubleshooting

### Database Connection Issues

```bash
# Test connection
psql $DATABASE_URL -c "SELECT NOW();"
```

### Port Already in Use

```bash
# Change PORT in .env or kill process
lsof -ti:3000 | xargs kill -9
```

### Validation Errors

Check that date format is YYYY-MM-DD and phone numbers are 10 digits (no formatting).

## Security Notes

⚠️ **This is a demo system. For production:**

- Add authentication (JWT, OAuth)
- Implement rate limiting
- Add HIPAA compliance measures
- Use HTTPS only
- Validate webhook signatures
- Implement proper logging and monitoring
- Add backup and disaster recovery

## License

MIT
