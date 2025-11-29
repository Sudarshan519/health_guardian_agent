# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import sqlite3
from typing import Dict, Any, Optional, Union

from .database import db


def save_health_report_to_file(health_report: str, filename: str) -> dict:
    """Saves the health report to a file."""
    with open(filename, "w") as f:
        f.write(health_report)
    return {"status": "success"}


def fetch_health_data(patient_id: str) -> dict:
    """Fetches health data for a patient from the database."""
    # Try to get data from database first
    stored_data = db.get_patient_data(patient_id)

    if stored_data:
        # Return stored data
        health_data = {
            "patient_id": patient_id,
            **stored_data
        }
        return {"health_data": json.dumps(health_data, indent=2)}
    else:
        # No data found, ask user to provide medical images
        return {"health_data": "No health data found for this patient. Please upload images of your medical reports, lab results, or doctor's notes, and I'll analyze them to extract your health information."}


def store_patient_info(patient_id: str, name: str, phone: str) -> dict:
    """Stores basic patient information."""
    success = db.store_patient_info(patient_id, name, phone)
    return {"status": "success" if success else "error"}


def store_health_data(patient_id: str, data_type: str, data: Dict[str, Any]) -> dict:
    """Stores health data for a patient in the database."""
    success = db.store_patient_data(patient_id, data_type, data)
    return {"status": "success" if success else "error"}


def store_assessment(patient_id: str, assessment_type: str, content: str) -> dict:
    """Stores assessment results in the database."""
    success = db.store_assessment(patient_id, assessment_type, content)
    return {"status": "success" if success else "error"}



def generate_patient_id() -> dict:
    """Generate a unique patient ID in format PAT001, PAT002, etc."""
    try:
        with sqlite3.connect(db.db_path) as conn:
            # Get all existing patient IDs
            cursor = conn.execute("SELECT patient_id FROM patients")
            existing_ids = [row[0] for row in cursor.fetchall()]

            # Extract numbers from PATxxx format
            numbers = []
            for pid in existing_ids:
                if pid.startswith('PAT') and len(pid) == 6:
                    try:
                        num = int(pid[3:])
                        numbers.append(num)
                    except ValueError:
                        continue

            # Find next available number
            next_num = 1
            if numbers:
                next_num = max(numbers) + 1

            # Format as PATxxx (3 digits)
            patient_id = f"PAT{next_num:03d}"

            return {"patient_id": patient_id}
    except Exception as e:
        print(f"Error generating patient ID: {e}")
        return {"patient_id": "PAT001"}  # Fallback


def find_patient_by_name_or_phone(name: Optional[str] = None, phone: Optional[str] = None) -> dict:
    """Find existing patient by name or phone number."""
    try:
        with sqlite3.connect(db.db_path) as conn:
            if name and phone:
                cursor = conn.execute("""
                    SELECT patient_id, name, phone
                    FROM patients
                    WHERE name = ? OR phone = ?
                """, (name, phone))
            elif name:
                cursor = conn.execute("""
                    SELECT patient_id, name, phone
                    FROM patients
                    WHERE name = ?
                """, (name,))
            elif phone:
                cursor = conn.execute("""
                    SELECT patient_id, name, phone
                    FROM patients
                    WHERE phone = ?
                """, (phone,))
            else:
                return {"found": False, "message": "Please provide name or phone to search"}

            rows = cursor.fetchall()
            if rows:
                # Return the first match
                patient_id, found_name, found_phone = rows[0]
                return {
                    "found": True,
                    "patient_id": patient_id,
                    "name": found_name,
                    "phone": found_phone
                }
            else:
                return {"found": False, "message": "No patient found with the provided information"}
    except Exception as e:
        print(f"Error searching for patient: {e}")
        return {"found": False, "message": "Error occurred while searching"}




def validate_medical_content(content: str) -> dict:
    """Basic validation for medical content - checks for common safety indicators."""
    # Simple validation - in production, use medical NLP models
    safety_flags = []
    if "emergency" in content.lower() and "seek immediate" not in content.lower():
        safety_flags.append("Potential emergency not properly flagged")
    if len(content.split()) < 50:
        safety_flags.append("Content may be too brief for medical advice")

    return {
        "is_valid": len(safety_flags) == 0,
        "safety_flags": safety_flags
    }