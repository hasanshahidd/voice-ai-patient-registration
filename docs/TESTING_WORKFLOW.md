# Testing & Deployment Workflow

## 🔵 CURRENT STAGE: Local Testing (What Works NOW)

### What You Can Test Right Now:
✅ **Frontend Dashboard** - http://localhost:3000
  - View all patients (5 seed patients)
  - Search and filter patients
  - Click patient rows to view details
  - Navigation between Dashboard/Patients pages
  - Professional UI with stats

✅ **Backend API** - http://localhost:8001
  - GET /api/patients - List all patients
  - GET /api/patients/{id} - Get one patient
  - POST /api/patients - Create new patient
  - PUT /api/patients/{id} - Update patient
  - DELETE /api/patients/{id} - Soft delete
  - GET /api/patients/check-duplicate/{phone} - Check if phone exists

### Current Test Commands (PowerShell):
```powershell
# Get all patients
Invoke-WebRequest "http://127.0.0.1:8001/api/patients"

# Create test patient
$body = @{
    first_name = "Test"
    last_name = "Patient"
    date_of_birth = "1990-05-15"
    sex = "Male"
    phone_number = "5559876543"
    address_line1 = "123 Test St"
    city = "TestCity"
    state = "CA"
    zip_code = "90210"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/patients" -Method POST -Body $body -ContentType "application/json"
```

---

## 🟡 STAGE 2: Deploy Backend (15 minutes)

### Why Deploy First?
- Vapi webhook needs a PUBLIC URL (not localhost)
- Must get a live URL like: `https://your-app-production.up.railway.app`

### Deployment Steps:
1. **Go to Railway.app** - https://railway.app
2. **Click "New Project" → "Deploy from GitHub"**
3. **Upload backend folder** or connect your GitHub repo
4. **Add PostgreSQL database** - Railway provides this free
5. **Set Environment Variables:**
   ```
   PORT=8000
   OPENAI_API_KEY=sk-proj-vwPp...
   CORS_ORIGINS=["*"]
   DATABASE_URL=postgresql://... (Railway will provide this)
   ```
6. **Deploy** - Railway auto-deploys
7. **Get Public URL** - Copy the URL like `https://voice-ai-agent-production.up.railway.app`

### Test After Backend Deployment:
```powershell
# Replace with YOUR Railway URL
$url = "https://voice-ai-agent-production.up.railway.app/api/patients"
Invoke-WebRequest $url

# Should return 5 patients
```

---

## 🟢 STAGE 3: Configure Vapi (10 minutes)

### Why Vapi Comes After Backend Deployment?
- Vapi needs your PUBLIC backend URL for webhooks
- Vapi will send patient data to: `https://your-app.railway.app/api/vapi/webhook`

### Vapi Configuration Steps:
1. **Login to Vapi.ai** - https://dashboard.vapi.ai
2. **Go to your "Riley" assistant** (or create new one)
3. **Update System Prompt:**
   - Copy from: `docs/VAPI_SETUP.md` lines 8-161
   - Paste into Vapi assistant's "System Message" field
4. **Add Function: save_patient**
   - Name: `save_patient`
   - Description: "Save patient registration to database"
   - Copy JSON schema from `docs/VAPI_SETUP.md` lines 165-199
5. **Add Function: check_duplicate**
   - Name: `check_duplicate`
   - Parameters: `phone_number` (string)
6. **Set Server URL:**
   - `https://YOUR-RAILWAY-URL.up.railway.app/api/vapi/webhook`
7. **Select Model:** GPT-4o-mini
8. **Buy Phone Number:**
   - Go to "Phone Numbers" tab
   - Click "Buy Number" 
   - Choose USA number - costs $10 (you have free credit)
   - Assign to your assistant
9. **Note the phone number** - Example: +1-555-123-4567

---

## 🟣 STAGE 4: End-to-End Testing (After Vapi Setup)

### What You Can Test NOW (Full Voice AI):

### Test 1: Successful Registration
```
1. Call the Vapi phone number from your phone
2. Assistant: "Hello, welcome to our patient registration..."
3. Say: "My name is Michael Thompson"
4. Say: "March 15, 1985" (date of birth)
5. Say: "Male" (gender)
6. Say: "555-777-8888" (phone)
7. Say: "123 Main Street" (address)
8. Say: "Springfield" (city)
9. Say: "Illinois" (state)
10. Say: "62701" (zip)
11. Say: "No" (no insurance)

Assistant should read back all info and say "Registration complete!"
```

### Test 2: Check Patient Was Saved
```powershell
# Check your backend API
$url = "https://your-railway-url.up.railway.app/api/patients?last_name=Thompson"
Invoke-WebRequest $url

# Should return Michael Thompson patient
```

### Test 3: Duplicate Phone Detection
```
1. Call the Vapi number again
2. Complete registration with same phone: "555-777-8888"
3. Assistant should say: "This phone number is already registered..."
```

### Test 4: Invalid Date of Birth
```
1. Call the Vapi number
2. When asked for DOB, say: "January 1, 2030" (future date)
3. Assistant should say: "That date is in the future..."
4. Say a valid date like "July 10, 1990"
5. Registration continues
```

### Test 5: "Start Over" Command
```
1. Call the Vapi number
2. Provide name and DOB
3. Say: "Start over"
4. Assistant should restart from the beginning
```

### Test 6: View in Dashboard
```
1. Open frontend: http://localhost:3000
2. Update config.js API_BASE_URL to your Railway URL
3. Click "Patients" in sidebar
4. You should see Michael Thompson in the patient list
5. Click the row to view full details
```

---

## 📊 What Each System Does

### Local Backend (http://localhost:8001)
- **Purpose:** Development testing
- **What to test:** API endpoints, database operations, CRUD operations
- **Limitation:** Can't test Vapi (needs public URL)

### Deployed Backend (https://your-app.railway.app)
- **Purpose:** Production API
- **What to test:** Same as local, plus Vapi webhook integration
- **Connected to:** Vapi voice assistant

### Frontend (http://localhost:3000)
- **Purpose:** View and manage patients
- **What to test:** UI, patient list, search, filters, details
- **Note:** Change `config.js` to point to deployed backend URL

### Vapi Voice Assistant (Phone Number: +1-XXX-XXX-XXXX)
- **Purpose:** Voice-based patient registration
- **What to test:** Full conversation flow, data validation, error handling
- **Requires:** Deployed backend with public URL

---

## 🚀 Quick Testing Checklist

### Before Deployment:
- [ ] Backend runs locally on port 8001
- [ ] Frontend runs locally on port 3000
- [ ] Can see 5 seed patients in dashboard
- [ ] Can create/update/delete patients via API

### After Backend Deployment:
- [ ] Railway backend URL works: `curl https://your-app.railway.app/api/patients`
- [ ] Returns 5 patients
- [ ] Database connected

### After Vapi Configuration:
- [ ] Can call phone number
- [ ] Assistant responds with greeting
- [ ] Complete full registration
- [ ] Check patient appears in API
- [ ] Test duplicate phone detection
- [ ] Test invalid DOB rejection
- [ ] Test "start over" command

### Final Verification:
- [ ] Update frontend config.js to production URL
- [ ] View registered patients in dashboard
- [ ] Update README.md with phone number
- [ ] Ready to submit!

---

## ⏱️ Time Estimates

| Phase | Duration | What Happens |
|-------|----------|--------------|
| Local Testing (NOW) | 5 min | Test API and dashboard locally |
| Deploy Backend | 15 min | Railway deployment, get public URL |
| Configure Vapi | 10 min | Setup assistant, add functions, buy phone |
| End-to-End Testing | 10 min | Call phone, test full flow |
| **TOTAL** | **40 min** | From here to complete system |

---

## 🎯 Current Status

**✅ COMPLETED:**
- Backend API (Python/FastAPI)
- Frontend Dashboard
- Database with 5 patients
- Local testing successful
- Documentation complete

**⏳ NEXT UP:**
1. Deploy backend to Railway (15 min)
2. Configure Vapi assistant (10 min)
3. Test voice calls (10 min)

**📞 AFTER VAPI IS WORKING:**
- You'll have a phone number
- Anyone can call and register
- Data flows: Phone → Vapi → Backend → Database → Dashboard

---

## 💡 Why This Order?

**Local First (NOW):**
- Test API without spending money
- Fix bugs before deployment
- Understand how system works

**Backend Deployment Second:**
- Vapi NEEDS a public URL
- Can't use localhost for webhooks
- Get permanent URL for Vapi

**Vapi Last:**
- Requires stable backend
- Phone number costs $10
- Want everything working first

**This way, you test incrementally and catch issues early!**
