# Testing Guide

> Comprehensive testing procedures for the Voice AI Patient Registration System

---

## 🚨 Core Functionality Tests

### Test 1: Normal Registration Flow

**Objective**: Verify complete end-to-end patient registration.

**Steps**:
1. Call the phone number: **+1 (276) 582-5544**
2. Provide all required information naturally
3. Listen for confirmation read-back
4. Confirm "yes"
5. Verify success message

**Expected Results**:
- Conversation feels natural (not robotic)
- Agent confirms ALL fields before saving
- Success message mentions your first name
- Call ends gracefully

**Verify Backend**:
```bash
# Check patient was saved
curl https://voice-ai-patient-registration-production.up.railway.app/api/patients?phone=YOUR_PHONE
```

**Verify Dashboard**:
- Open [Dashboard](https://voice-ai-patient-registration-production.up.railway.app/)
- See new patient in table
- Click row → see all details

---

### Test 2: Duplicate Phone Detection

**Objective**: Ensure system prevents duplicate registrations.

**Steps**:
1. Call the number again with same phone number
2. Provide same phone number during registration
3. Listen for duplicate detection message

**Expected Result**:
Agent says: "It looks like we already have a record for [Your Name] with this phone number. Would you like to update your existing information instead of creating a new record?"

**Backend Verification**:
```bash
# Count patients with your phone (should still be 1, not 2)
curl https://voice-ai-patient-registration-production.up.railway.app/api/patients?phone=YOUR_PHONE
```

---

### Test 3: Input Validation

**Objective**: Verify agent catches and corrects invalid inputs.

#### Test 3a: Future Date of Birth
1. Call the number
2. When asked for DOB, provide a future date (e.g., "December 25, 2030")
3. Verify error handling

**Expected**: "That date is in the future. What's your correct date of birth?"

#### Test 3b: Invalid Phone Number
1. When asked for phone, say "555" (too short)
2. Verify error handling

**Expected**: "I need a 10-digit phone number. Could you please provide your phone number with the area code?"

#### Test 3c: Invalid State Format
1. When asked for state, say "California" (full name, not 2-letter)
2. Verify error handling

**Expected**: "And which state is that? Please use the 2-letter abbreviation."

---

## 🔥 Edge Case Testing

### Test 4: "Start Over" Command

**Objective**: Verify caller can reset conversation mid-flow.

**Steps**:
1. Call the number
2. Provide first name, last name
3. Say "Wait, can we start over?"
4. Verify reset confirmation

**Expected**: "No problem! Let's start fresh. What's your first name?"

---

### Test 5: Out-of-Order Information

**Objective**: Agent adapts when caller volunteers multiple fields at once.

**Steps**:
1. Call the number
2. When agent asks for first name, provide multiple fields:
   "Hi, I'm John Smith, my date of birth is March 15, 1985, and my phone number is 555-123-4567"
3. Verify agent's response

**Expected**: Agent acknowledges ALL provided info and doesn't re-ask for already-provided fields.

---

### Test 6: Interruption Handling

**Objective**: Verify agent responds to caller interruptions.

**Steps**:
1. Call the number
2. While agent is speaking, interrupt with "Wait!"
3. Correct information: "Actually, that phone number is wrong"
4. Verify response

**Expected**:
- Agent acknowledges interruption
- Agent asks which field to correct
- Correction handled gracefully

---

### Test 7: Connection Issues

**Objective**: Graceful handling of network problems.

**Steps**:
1. Call the number
2. Mid-conversation, say "I can't hear you, you're breaking up"
3. Verify response
4. Optionally hang up and call back

**Expected**: Agent acknowledges connection issue and explains call-back process if needed.

---

### Test 8: Unclear Input

**Objective**: Agent handles unclear responses gracefully.

**Steps**:
1. Call the number
2. When asked for a field, provide unclear/garbled response
3. Verify re-prompt

**Expected**: "I didn't catch that. Could you repeat your [field name]?"

---

## ⚙️ Backend API Testing

### Test 9: Webhook Error Handling

**Objective**: Verify backend errors return friendly messages.

**Steps**:
1. Simulate a database error (if possible)
2. Complete registration through confirmation
3. Verify response after confirmation

**Expected**: Friendly error message to caller (not silence or technical jargon).

**Verify Logs**: Backend should log full error with stack trace.

---

### Test 10: API Endpoint Testing

#### Test 10a: Create with Invalid Data
```bash
# Should return 422 Validation Error
curl -X POST https://voice-ai-patient-registration-production.up.railway.app/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "date_of_birth": "2030-12-25",
    "sex": "Male",
    "phone_number": "123",
    "address_line_1": "123 Main St",
    "city": "LA",
    "state": "CA",
    "zip_code": "90001"
  }'
```

**Expected**: HTTP 422 with error details for `date_of_birth` (future) and `phone_number` (too short).

#### Test 10b: Soft Delete
```bash
# Delete a patient
curl -X DELETE https://voice-ai-patient-registration-production.up.railway.app/api/patients/{PATIENT_ID}

# Verify soft-deleted (not visible in GET but still in DB)
curl https://voice-ai-patient-registration-production.up.railway.app/api/patients/{PATIENT_ID}
```

**Expected**: Deleted patient returns 404, but `deleted_at` timestamp is set in database.

#### Test 10c: Search Filters
```bash
# By last name
curl https://voice-ai-patient-registration-production.up.railway.app/api/patients?last_name=Smith

# By phone
curl https://voice-ai-patient-registration-production.up.railway.app/api/patients?phone=5551234567
```

---

## 📊 Dashboard Functionality Testing

### Test 11: Frontend Dashboard

**Objective**: Verify dashboard correctly displays and filters patients.

**Steps**:
1. Open dashboard URL in browser
2. Verify stats cards show correct counts
3. Test search box (type last name)
4. Click patient row → verify details display
5. Test navigation (Dashboard, Patients, Appointments, History)

**Expected**:
- Stats cards match database count
- Search filters table in real-time
- Patient details show all 18 fields
- Navigation works correctly

**Browser Console**: Check for JavaScript errors (should be clean).

---

## 🐛 Common Issues & Debugging

### Issue: Agent Doesn't Confirm Before Saving
**Symptom**: Patient saved without read-back confirmation  
**Check**: Vapi prompt "CONFIRMATION (CRITICAL)" section  
**Test**: Listen carefully to full call flow

---

### Issue: Second Call Creates Duplicate
**Symptom**: Same phone number creates multiple records  
**Check**: `backend/routers/vapi.py` duplicate detection logic  
**Test**: Call twice with same phone, verify database count

---

### Issue: Agent Sounds Robotic
**Symptom**: Unnatural conversation flow  
**Check**: Vapi system prompt for natural phrasing  
**Test**: Use contractions and questions instead of commands

---

### Issue: Webhook Doesn't Log Payload
**Symptom**: Backend logs missing structured JSON  
**Check**: `backend/routers/vapi.py` logging statements  
**Verify**: Logs should show full payload with indentation

---

## 🚀 Emergency Debugging

**Agent doesn't call save_patient function**:
- Check Vapi logs for function call attempts
- Verify function schema matches prompt
- Ensure prompt explicitly calls function on confirmation

**Webhook returns 500**:
- Check Railway logs for exceptions
- Test database connection
- Verify environment variables

**Dashboard doesn't load patients**:
- Check browser console for CORS errors
- Verify API_BASE_URL in `frontend/public/js/config.js`
- Test API directly with curl

**Phone number doesn't ring**:
- Check Vapi dashboard: number assigned to assistant?
- Verify assistant is "Active" status
- Test from different phone

---

## ✅ Pre-Release Checklist

Before going live, confirm:

- [ ] All 11 functional tests passing
- [ ] API endpoints validated with curl
- [ ] Dashboard loads without errors
- [ ] Phone system connected and answering
- [ ] Backend logs showing proper payload logging
- [ ] Database has proper constraints and indexes
- [ ] Environment variables properly configured
- [ ] No secrets committed to repository
- [ ] Documentation reflects live URLs
- [ ] Error handling tested and verified

---

## 📞 Live System URLs

- **Phone Number**: +1 (276) 582-5544
- **API Base**: https://voice-ai-patient-registration-production.up.railway.app
- **Dashboard**: [Coming Soon - Frontend Service URL]
- **Documentation**: See [README.md](README.md) and [docs/VAPI_SETUP.md](docs/VAPI_SETUP.md)

---

**Last Updated**: March 2026  
**Status**: Production Ready
