"""
Patient REST API endpoints (CRUD operations).
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional
from datetime import datetime, date
import logging
import uuid

from config.database import get_db
from models.patient import Patient
from schemas.patient_schemas import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientListResponse,
    PatientSingleResponse,
    DuplicateCheckResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("", response_model=PatientListResponse)
async def get_patients(
    last_name: Optional[str] = Query(None),
    date_of_birth: Optional[date] = Query(None),
    phone_number: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(Patient).where(Patient.deleted_at.is_(None))
        
        if last_name:
            query = query.where(Patient.last_name.ilike(last_name))
        
        if date_of_birth:
            query = query.where(Patient.date_of_birth == date_of_birth)
        
        if phone_number:
            clean_phone = ''.join(filter(str.isdigit, phone_number))
            query = query.where(Patient.phone_number == clean_phone)
        
        query = query.order_by(Patient.created_at.desc())
        
        result = await db.execute(query)
        patients = result.scalars().all()
        
        return PatientListResponse(
            data=[PatientResponse.model_validate(p) for p in patients],
            count=len(patients),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error fetching patients: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check-duplicate/{phone_number}", response_model=DuplicateCheckResponse)
async def check_duplicate(
    phone_number: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        query = select(Patient).where(
            and_(
                Patient.phone_number == clean_phone,
                Patient.deleted_at.is_(None)
            )
        ).order_by(Patient.created_at.desc()).limit(1)
        
        result = await db.execute(query)
        existing_patient = result.scalar_one_or_none()
        
        if existing_patient:
            return DuplicateCheckResponse(
                exists=True,
                patient={
                    "patient_id": str(existing_patient.patient_id),
                    "first_name": existing_patient.first_name,
                    "last_name": existing_patient.last_name,
                    "date_of_birth": existing_patient.date_of_birth.isoformat()
                }
            )
        
        return DuplicateCheckResponse(exists=False)
        
    except Exception as e:
        logger.error(f"Error checking duplicate: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}", response_model=PatientSingleResponse)
async def get_patient(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get single patient by ID"""
    try:
        query = select(Patient).where(
            and_(
                Patient.patient_id == patient_id,
                Patient.deleted_at.is_(None)
            )
        )
        
        result = await db.execute(query)
        patient = result.scalar_one_or_none()
        
        if not patient:
            return PatientSingleResponse(
                data=None,
                error="Patient not found",
                message=f"No patient found with ID: {patient_id}",
                timestamp=datetime.utcnow()
            )
        
        return PatientSingleResponse(
            data=PatientResponse.model_validate(patient),
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error fetching patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=PatientSingleResponse, status_code=201)
async def create_patient(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new patient"""
    try:
        # Check for duplicate
        query = select(Patient).where(
            and_(
                Patient.phone_number == patient_data.phone_number,
                Patient.deleted_at.is_(None)
            )
        )
        result = await db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            logger.warning(f"Duplicate patient detected: {existing.patient_id}")
        
        # Create new patient
        new_patient = Patient(**patient_data.model_dump())
        db.add(new_patient)
        await db.commit()
        await db.refresh(new_patient)
        
        logger.info(f"Patient created: {new_patient.patient_id} - {new_patient.first_name} {new_patient.last_name}")
        
        return PatientSingleResponse(
            data=PatientResponse.model_validate(new_patient),
            message="Patient successfully registered",
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{patient_id}", response_model=PatientSingleResponse)
async def update_patient(
    patient_id: uuid.UUID,
    patient_data: PatientUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update existing patient"""
    try:
        # Get existing patient
        query = select(Patient).where(
            and_(
                Patient.patient_id == patient_id,
                Patient.deleted_at.is_(None)
            )
        )
        result = await db.execute(query)
        patient = result.scalar_one_or_none()
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Update fields
        update_data = patient_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)
        
        patient.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(patient)
        
        logger.info(f"Patient updated: {patient_id}")
        
        return PatientSingleResponse(
            data=PatientResponse.model_validate(patient),
            message="Patient successfully updated",
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Soft delete patient"""
    try:
        # Get existing patient
        query = select(Patient).where(
            and_(
                Patient.patient_id == patient_id,
                Patient.deleted_at.is_(None)
            )
        )
        result = await db.execute(query)
        patient = result.scalar_one_or_none()
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Soft delete
        patient.deleted_at = datetime.utcnow()
        
        await db.commit()
        
        logger.info(f"Patient soft-deleted: {patient_id}")
        
        return {
            "data": {"patient_id": str(patient_id), "deleted": True},
            "message": "Patient successfully deleted",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))
