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
from typing import Dict, Any

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
        # No data found, ask user to provide it
        return {"health_data": "No health data found for this patient. Please provide your health information including vital signs, lab results, medications, and conditions."}


def store_health_data(patient_id: str, data_type: str, data: Dict[str, Any]) -> dict:
    """Stores health data for a patient in the database."""
    success = db.store_patient_data(patient_id, data_type, data)
    return {"status": "success" if success else "error"}


def store_assessment(patient_id: str, assessment_type: str, content: str) -> dict:
    """Stores assessment results in the database."""
    success = db.store_assessment(patient_id, assessment_type, content)
    return {"status": "success" if success else "error"}


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