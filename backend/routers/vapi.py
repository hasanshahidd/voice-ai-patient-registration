"""
Vapi.ai webhook handler for voice agent function calls.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, date
import logging
import json

from config.database import get_db
from models.patient import Patient
from schemas.patient_schemas import PatientCreate

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def vapi_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        body = await request.json()
        logger.info(f"Vapi webhook received: {body.get('message', {}).get('type')}")
        
        message = body.get("message", {})
        message_type = message.get("type")
        
        # Handle both "function-call" and "tool-calls" formats
        if message_type in ["function-call", "tool-calls"]:
            # Try new format first (tool-calls)
            if message_type == "tool-calls":
                tool_calls = message.get("toolCalls", [])
                if tool_calls:
                    # Process each tool call and collect results
                    results = []
                    for tool_call in tool_calls:
                        function = tool_call.get("function", {})
                        function_name = function.get("name")
                        parameters = function.get("arguments", {})
                        
                        # Parse if it's a JSON string
                        if isinstance(parameters, str):
                            parameters = json.loads(parameters)
                        
                        if function_name == "save_patient":
                            result = await handle_save_patient(parameters, db)
                            results.append(result)
                        
                        elif function_name == "check_duplicate":
                            result = await handle_check_duplicate(parameters, db)
                            results.append(result)
                    
                    # Return the last result (usually save_patient if both tools called)
                    if results:
                        return results[-1]
            
            # Try old format (function-call)
            else:
                function_call = message.get("functionCall", {})
                function_name = function_call.get("name")
                parameters = function_call.get("parameters", {})
                
                if function_name == "save_patient":
                    return await handle_save_patient(parameters, db)
                
                elif function_name == "check_duplicate":
                    return await handle_check_duplicate(parameters, db)
        
        elif message_type == "end-of-call-report":
            duration = message.get("duration", 0)
            summary = message.get("summary", "")
            logger.info(f"Call ended. Duration: {duration}s")
            logger.info(f"Summary: {summary}")
        
        return {"success": True, "message": "Webhook received"}
        
    except Exception as e:
        logger.error(f"Vapi webhook error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

async def handle_save_patient(parameters: dict, db: AsyncSession):
    """Save patient from Vapi function call. Returns structured response for LLM to speak."""
    try:
        logger.info("=" * 80)
        logger.info("VAPI WEBHOOK - save_patient called")
        logger.info("=" * 80)
        logger.info(f"Raw parameters received:\n{json.dumps(parameters, indent=2)}")
        logger.info("=" * 80)
        
        # Vapi sends camelCase parameters, convert to snake_case for Python
        first_name = parameters.get('firstName') or parameters.get('first_name')
        last_name = parameters.get('lastName') or parameters.get('last_name')
        
        logger.info(f"Saving patient data: {first_name} {last_name}")
        
        dob_str = parameters.get("dateOfBirth") or parameters.get("date_of_birth", "")
        if '/' in dob_str:
            month, day, year = dob_str.split('/')
            dob = date(int(year), int(month), int(day))
        else:
            dob = date.fromisoformat(dob_str)
        
        phone = ''.join(filter(str.isdigit, parameters.get("phoneNumber") or parameters.get("phone_number", "")))
        emergency_phone = parameters.get("emergencyContactPhone") or parameters.get("emergency_contact_phone")
        if emergency_phone:
            emergency_phone = ''.join(filter(str.isdigit, emergency_phone))
        
        query = select(Patient).where(
            and_(
                Patient.phone_number == phone,
                Patient.deleted_at.is_(None)
            )
        )
        result = await db.execute(query)
        existing_patient = result.scalar_one_or_none()
        
        if existing_patient:
            logger.warning(f"Duplicate detected: {existing_patient.patient_id}")
            return {
                "result": {
                    "success": False,
                    "duplicate": True,
                    "patient_id": str(existing_patient.patient_id),
                    "first_name": existing_patient.first_name,
                    "last_name": existing_patient.last_name,
                    "message": f"A patient record already exists for {existing_patient.first_name} {existing_patient.last_name}. Would you like to update it instead?"
                }
            }
        
        patient_data = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": dob,
            "sex": parameters.get("sex"),
            "phone_number": phone,
            "email": parameters.get("email"),
            "address_line_1": parameters.get("addressLine1") or parameters.get("address_line_1"),
            "address_line_2": parameters.get("addressLine2") or parameters.get("address_line_2"),
            "city": parameters.get("city"),
            "state": (parameters.get("state") or "").upper(),
            "zip_code": parameters.get("zipCode") or parameters.get("zip_code"),
            "insurance_provider": parameters.get("insuranceProvider") or parameters.get("insurance_provider"),
            "insurance_member_id": parameters.get("insuranceMemberId") or parameters.get("insurance_member_id"),
            "preferred_language": parameters.get("preferredLanguage") or parameters.get("preferred_language", "English"),
            "emergency_contact_name": parameters.get("emergencyContactName") or parameters.get("emergency_contact_name"),
            "emergency_contact_phone": emergency_phone
        }
        
        logger.info(f"Final structured patient data to save:\n{json.dumps({k: str(v) for k, v in patient_data.items()}, indent=2)}")
        
        new_patient = Patient(**patient_data)
        db.add(new_patient)
        await db.commit()
        await db.refresh(new_patient)
        
        logger.info(f"Patient created successfully via Vapi webhook")
        logger.info(f"   Patient ID: {new_patient.patient_id}")
        logger.info(f"   Name: {new_patient.first_name} {new_patient.last_name}")
        logger.info(f"   Phone: {new_patient.phone_number}")
        logger.info(f"   Timestamp: {new_patient.created_at}")
        logger.info("=" * 80)
        
        return {
            "result": {
                "success": True,
                "duplicate": False,
                "patient_id": str(new_patient.patient_id),
                "first_name": new_patient.first_name,
                "last_name": new_patient.last_name,
                "message": f"Thank you, {new_patient.first_name}. Your registration is complete!"
            }
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error saving patient via Vapi: {e}", exc_info=True)
        
        return {
            "result": {
                "success": False,
                "error": True,
                "message": "I apologize, but there was an error saving your information. Please try again or contact our office directly."
            }
        }

async def handle_check_duplicate(parameters: dict, db: AsyncSession):
    """Check if patient exists by firstName, lastName, and dateOfBirth."""
    try:
        # Vapi sends camelCase, support both formats
        first_name = parameters.get("firstName") or parameters.get("first_name", "")
        last_name = parameters.get("lastName") or parameters.get("last_name", "") or parameters.get("lastName\r\n", "")
        dob_str = parameters.get("dateOfBirth") or parameters.get("date_of_birth", "")
        
        logger.info(f"Check duplicate: {first_name} {last_name} {dob_str}")
        
        # Parse date
        if dob_str:
            dob = date.fromisoformat(dob_str)
        else:
            return {"result": {"exists": False, "error": True, "message": "Date of birth required"}}
        
        query = select(Patient).where(
            and_(
                Patient.first_name == first_name,
                Patient.last_name == last_name,
                Patient.date_of_birth == dob,
                Patient.deleted_at.is_(None)
            )
        )
        result = await db.execute(query)
        existing_patient = result.scalar_one_or_none()
        
        if existing_patient:
            logger.info(f"Duplicate found: {existing_patient.patient_id}")
            return {
                "result": {
                    "exists": True,
                    "patient_id": str(existing_patient.patient_id),
                    "first_name": existing_patient.first_name,
                    "last_name": existing_patient.last_name,
                    "date_of_birth": existing_patient.date_of_birth.isoformat()
                }
            }
        
        logger.info(f"No duplicate found")
        return {"result": {"exists": False}}
        
    except Exception as e:
        logger.error(f"Error checking duplicate: {e}", exc_info=True)
        return {"result": {"exists": False, "error": True, "message": str(e)}}

@router.post("/check-duplicate")
async def check_duplicate_endpoint(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Standalone endpoint for checking duplicate patients."""
    try:
        body = await request.json()
        logger.info(f"Check duplicate request: {body}")
        
        # Support both direct parameters or nested message structure
        parameters = body.get("message", {}).get("functionCall", {}).get("parameters", body)
        
        return await handle_check_duplicate(parameters, db)
        
    except Exception as e:
        logger.error(f"Check duplicate error: {e}", exc_info=True)
        return {"result": {"exists": False, "error": True, "message": str(e)}}

@router.get("/status")
async def vapi_status(request: Request):
    webhook_url = f"{request.url.scheme}://{request.url.netloc}/api/vapi/webhook"
    
    return {
        "status": "active",
        "webhook_url": webhook_url,
        "timestamp": datetime.utcnow().isoformat()
    }
