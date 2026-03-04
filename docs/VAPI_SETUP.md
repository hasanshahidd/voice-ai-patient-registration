# Vapi.ai Setup Guide

Complete guide to setting up the Vapi.ai voice agent for patient registration.

## Step 1: Create Vapi Account

1. Go to [https://vapi.ai/](https://vapi.ai/)
2. Sign up for an account
3. Navigate to Settings → API Keys
4. Copy your API key

## Step 2: Provision Phone Number

1. In Vapi dashboard, go to **Phone Numbers**
2. Click **Buy Phone Number**
3. Select **United States**
4. Choose an available number
5. Complete purchase ($2-5/month typically)
6. Copy the **Phone Number ID**

## Step 3: Create Assistant

### 3.1 Navigate to Assistants

1. Go to **Assistants** in the Vapi dashboard
2. Click **Create Assistant**

### 3.2 Configure Basic Settings

**Name**: `Patient Registration Agent`

**Model**: `gpt-4o-mini` (or `gpt-4o` for better quality)

**Voice**: Choose a natural-sounding voice:
- **Provider**: ElevenLabs or Azure
- **Voice**: `Rachel` (friendly female) or `Matthew` (professional male)
- **Speed**: 1.0
- **Stability**: 0.8

### 3.3 System Prompt

Copy this exact prompt into the **System Message** field:

```
You are a friendly and professional patient registration assistant for a medical clinic. Your job is to collect patient demographic information through natural conversation.

REQUIRED INFORMATION TO COLLECT:
1. First Name
2. Last Name
3. Date of Birth (MM/DD/YYYY format)
4. Sex (Male, Female, Other, or Decline to Answer)
5. Phone Number (10-digit U.S. number)
6. Complete Address:
   - Street address
   - Apartment/Suite number (if applicable)
   - City
   - State (2-letter abbreviation)
   - ZIP code

OPTIONAL INFORMATION (ask if caller wants to provide):
7. Email address
8. Insurance provider and member ID
9. Emergency contact name and phone number
10. Preferred language

CONVERSATION FLOW:

1. GREETING:
   "Hello! Thank you for calling. I'm here to help you register as a new patient. This will only take a few minutes. May I start by getting your first name?"

2. COLLECT INFORMATION NATURALLY:
   - Don't just read a list of fields — be conversational and warm
   - **IMPORTANT: Accept information in ANY order** — caller may volunteer multiple fields at once
   - Track what you've collected and only ask for what's missing
   - Example: If they say "Hi, I'm John Smith calling about registration, my number is 555-123-4567"
     → "Great to meet you, John Smith! I have your phone number as 555-123-4567. Let me get your date of birth next..."
   - If caller interrupts or corrects mid-sentence, STOP and listen — don't keep talking

3. HANDLE CORRECTIONS GRACEFULLY:
   - If caller says "Actually, that's spelled..." or "Wait, I meant..."
   - Acknowledge: "No problem, let me update that."
   - Re-confirm the corrected information

4. VALIDATE AS YOU GO:
   - Date of Birth: Cannot be in the future
     → If invalid: "I need a valid date of birth. Could you provide that in month, day, year format?"
   - Phone Number: Must be 10 digits
     → If invalid: "I need a 10-digit phone number. Could you provide that again, including the area code?"
   - State: Must be a valid 2-letter U.S. state abbreviation
     → If unclear: "And which state is that? Please use the 2-letter abbreviation."
   - ZIP Code: Must be 5 digits or ZIP+4 format
     → If invalid: "I need a 5-digit ZIP code for your address."

5. OFFER OPTIONAL FIELDS:
   After collecting all required information:
   "Perfect! I have all the required information. I can also collect your insurance information, emergency contact, and preferred language if you'd like. Would you like to provide any of those?"
   
   - If YES: "Great! Do you have insurance?"
   - If NO: "No problem, we can update that later."

6. CONFIRMATION (CRITICAL):
   Before saving, read back ALL information:
   
   "Let me confirm your information:
   - Name: [First] [Last]
   - Date of Birth: [MM/DD/YYYY]
   - Sex: [Sex]
   - Phone Number: ([XXX]) [XXX-XXXX]
   - Address: [Address Line 1], [City], [State] [ZIP]
   [... optional fields if provided ...]
   
   Is this information correct, or would you like to change anything?"

7. HANDLE CONFIRMATION RESPONSE:
   - If "Yes, that's correct": Call save_patient function
   - If "No" or corrections needed: 
     → "What would you like to change?"
     → Update specific fields
     → Re-confirm only the changed information

8. AFTER SUCCESSFUL SAVE:
   "Perfect! You're all registered, [First Name]. We look forward to seeing you at your appointment. Have a great day!"

9. IF DUPLICATE DETECTED:
   "It looks like we already have a record for [Name] with this phone number. Would you like to update your existing information instead of creating a new record?"

ERROR HANDLING:

- INVALID DATE: "I need a valid date of birth. Could you provide that in month, day, year format? For example, March 15, 1990."

- INVALID PHONE: "I need a 10-digit phone number. Could you please provide your phone number with the area code?"

- FUTURE DATE OF BIRTH: "That date is in the future. What's your correct date of birth?"

- UNCLEAR RESPONSE: "I didn't catch that. Could you repeat [field name]?"

- CALLER WANTS TO START OVER:
  Trigger phrases: "start over", "reset", "begin again", "let me start again", "can we restart"
  → "No problem! Let's start fresh. What's your first name?"
  (Clear all collected data and restart from greeting)

- CALL DROP / CONNECTION ISSUES:
  If connection becomes unstable or caller says "I can't hear you" / "you're breaking up":
  → "I apologize for the connection issue. If we get disconnected, please call back and we can continue where we left off."

- CALLER INTERRUPTS / TALKS OVER YOU:
  STOP speaking immediately and listen. Resume after they finish:
  → "Sorry, go ahead. I'm listening."

- DATABASE ERROR (from save_patient function): "I apologize, but there was a technical issue saving your information. Please try calling back in a few minutes, or you can also register when you arrive for your appointment."

IMPORTANT GUIDELINES:

✅ DO:
- Be warm, friendly, and professional
- Speak naturally, not robotically
- **Acknowledge what the caller says BEFORE moving on** ("Got it!", "Perfect, thank you")
- Confirm each piece of information as you collect it ("And that's spelled J-O-H-N, correct?")
- **Handle interruptions gracefully** — STOP talking when caller interrupts, listen fully
- Use the caller's name once you know it (builds rapport)
- Thank them for their patience if collection takes time
- **Accept information in any order** — adapt to how caller naturally speaks

❌ DON'T:
- Rush through the conversation
- Sound scripted or mechanical ("Please provide your name" → "What's your first name?")
- **Ignore corrections or interruptions** — these are high priority
- Save information without full confirmation read-back
- Make assumptions about personal information
- Ask the same question twice unless genuinely unclear
- Keep talking if caller interrupts — yield the floor immediately

TONE: Professional yet warm and conversational, like a friendly medical receptionist.

Remember: You're representing a healthcare provider. Be empathetic, clear, and patient-focused.
```

### 3.4 Configure Functions

Add function for saving patient data:

**Function Name**: `save_patient`

**Description**: `Saves confirmed patient demographic information to the database after caller confirms all information is correct`

**Parameters** (JSON Schema):

```json
{
  "type": "object",
  "properties": {
    "first_name": {
      "type": "string",
      "description": "Patient's first name (1-50 characters, letters only)"
    },
    "last_name": {
      "type": "string",
      "description": "Patient's last name (1-50 characters, letters only)"
    },
    "date_of_birth": {
      "type": "string",
      "description": "Date of birth in MM/DD/YYYY format"
    },
    "sex": {
      "type": "string",
      "enum": ["Male", "Female", "Other", "Decline to Answer"],
      "description": "Patient's sex"
    },
    "phone_number": {
      "type": "string",
      "description": "10-digit U.S. phone number without formatting"
    },
    "email": {
      "type": "string",
      "description": "Email address (optional)"
    },
    "address_line_1": {
      "type": "string",
      "description": "Street address"
    },
    "address_line_2": {
      "type": "string",
      "description": "Apartment/Suite/Unit number (optional)"
    },
    "city": {
      "type": "string",
      "description": "City name"
    },
    "state": {
      "type": "string",
      "description": "2-letter U.S. state abbreviation (e.g., CA, NY, TX)"
    },
    "zip_code": {
      "type": "string",
      "description": "5-digit ZIP code or ZIP+4 format"
    },
    "insurance_provider": {
      "type": "string",
      "description": "Name of insurance company (optional)"
    },
    "insurance_member_id": {
      "type": "string",
      "description": "Insurance member/subscriber ID (optional)"
    },
    "preferred_language": {
      "type": "string",
      "description": "Preferred language (optional, default: English)"
    },
    "emergency_contact_name": {
      "type": "string",
      "description": "Emergency contact full name (optional)"
    },
    "emergency_contact_phone": {
      "type": "string",
      "description": "Emergency contact 10-digit phone number (optional)"
    }
  },
  "required": [
    "first_name",
    "last_name",
    "date_of_birth",
    "sex",
    "phone_number",
    "address_line_1",
    "city",
    "state",
    "zip_code"
  ]
}
```

### 3.5 Configure Server URL (Webhook)

**Function Server URL**: `https://your-backend-url.railway.app/api/vapi/webhook`

Replace `your-backend-url.railway.app` with your actual deployed backend URL.

If testing locally with ngrok:
```bash
ngrok http 3000
# Use the ngrok URL: https://xxxx-xx-xx-xx-xx.ngrok.io/api/vapi/webhook
```

## Step 4: Attach Assistant to Phone Number

1. Go back to **Phone Numbers**
2. Click on your purchased number
3. Under **Assistant**, select your newly created assistant
4. Save changes

## Step 5: Test

### Test Call Flow

1. **Dial the phone number** from any phone
2. **Listen to greeting** - Should hear friendly introduction
3. **Provide test information**:
   ```
   Agent: "May I have your first name?"
   You: "John"
   
   Agent: "And your last name?"
   You: "Smith"
   
   Agent: "What's your date of birth?"
   You: "March 15, 1985"
   
   Agent: "And your sex?"
   You: "Male"
   
   Agent: "What's your phone number?"
   You: "555-123-4567"
   
   Agent: "What's your street address?"
   You: "123 Oak Street"
   
   Agent: "City?"
   You: "Los Angeles"
   
   Agent: "State?"
   You: "California" or "CA"
   
   Agent: "And the ZIP code?"
   You: "90001"
   
   Agent: [Offers optional fields]
   You: "No thanks"
   
   Agent: [Reads back all information]
   "Is this information correct?"
   You: "Yes"
   
   Agent: "Perfect! You're all registered, John."
   ```

4. **Check database**:
   ```bash
   # In your backend terminal or psql
   psql $DATABASE_URL -c "SELECT * FROM patients ORDER BY created_at DESC LIMIT 1;"
   ```

### Test Error Handling

Try these scenarios:

1. **Invalid DOB**: "I was born tomorrow" → Should re-prompt
2. **Invalid Phone**: "555-CALL" → Should ask for 10 digits
3. **Correction**: "My name is John... wait, actually it's Jonathan" → Should update
4. **Interruption**: Start speaking while agent is talking → Should handle gracefully
5. **Out of Order**: "Hi, I'm John Smith at 555-1234" → Should capture available info

## Step 6: View Call Logs

1. In Vapi dashboard, go to **Calls**
2. See all calls with:
   - Duration
   - Transcript
   - Function calls made
   - Status (completed/failed)

## Step 7: Environment Variables

Update your backend `.env`:

```env
VAPI_API_KEY=your_actual_vapi_api_key
VAPI_PHONE_NUMBER_ID=your_phone_number_id
VAPI_ASSISTANT_ID=your_assistant_id
```

## Troubleshooting

### Issue: Function not being called

**Solution**: Check webhook URL is correct and accessible. Test with:
```bash
curl -X POST https://your-backend.railway.app/api/vapi/webhook \
  -H "Content-Type: application/json" \
  -d '{"message":{"type":"function-call"}}'
```

### Issue: Agent sounds robotic

**Solution**: 
- Use GPT-4o instead of GPT-4o-mini
- Adjust voice speed to 0.95
- Use ElevenLabs voices (more natural)

### Issue: Information not saving

**Solution**:
1. Check backend logs for errors
2. Verify DATABASE_URL is correct
3. Ensure schema is applied
4. Test webhook endpoint manually

### Issue: Agent not understanding

**Solution**:
- Add more examples to system prompt
- Use GPT-4o for better comprehension
- Adjust temperature (0.7-0.8 for balanced)

## Advanced Configuration

### Background Sounds

Enable background denoising:
- Go to Assistant settings
- Enable "Background Sound Suppression"
- Set to "High" for noisy environments

### End of Call Behavior

Configure what happens after call:
- Send confirmation SMS (requires Twilio integration)
- Send email summary
- Log transcript to database

### Multi-language Support

To add Spanish:
1. Duplicate assistant
2. Translate system prompt to Spanish
3. Set voice to Spanish-speaking voice
4. Add language detection at start of call

## Cost Estimation

**Monthly costs** (assuming 100 calls/month, 3 min average):

| Service | Cost |
|---------|------|
| Vapi.ai | $0.15/min → ~$45 |
| OpenAI GPT-4o-mini | $0.002/min → ~$0.60 |
| Phone Number | $2-5 |
| **Total** | **~$50/month** |

For production, consider:
- GPT-4o: Higher quality, higher cost ($0.01/min)
- Volume discounts available
- Voice options affect pricing

## Next Steps

1. ✅ Test with multiple scenarios
2. ✅ Review call transcripts in Vapi dashboard
3. ✅ Adjust system prompt based on real conversations
4. ✅ Add error handling edge cases
5. ✅ Consider adding appointment scheduling
6. ✅ Set up call recording storage

## Resources

- [Vapi.ai Documentation](https://docs.vapi.ai/)
- [Vapi Function Calling Guide](https://docs.vapi.ai/assistants/function-calling)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

---

**Questions?** Check the Vapi Discord community or docs.vapi.ai
