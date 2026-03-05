"""
One-time script to fix empty email strings in the database.
Converts empty strings to NULL for optional email fields.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.patient import Patient

async def fix_empty_emails():
    """Fix all patients with empty email strings."""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    # Create async engine
    engine = create_async_engine(database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Find all patients with empty email strings
        result = await session.execute(
            select(Patient).where(Patient.email == '')
        )
        patients = result.scalars().all()
        
        print(f"\nFound {len(patients)} patients with empty email strings")
        
        if patients:
            # Update all empty emails to NULL
            await session.execute(
                update(Patient)
                .where(Patient.email == '')
                .values(email=None)
            )
            
            await session.commit()
            print(f"✅ Successfully updated {len(patients)} patient records")
            
            for patient in patients:
                print(f"   - {patient.first_name} {patient.last_name} (ID: {patient.patient_id})")
        else:
            print("✅ No patients found with empty email strings")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix_empty_emails())
