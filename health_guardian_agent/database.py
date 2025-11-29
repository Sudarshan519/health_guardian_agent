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

import sqlite3
import json
from typing import Dict, Any, Optional, List
from pathlib import Path


class HealthDatabase:
    """Simple SQLite database for storing patient health data."""

    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id TEXT PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS health_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT,
                    data_type TEXT,  -- 'vital_signs', 'lab_results', 'medications', 'conditions'
                    data_json TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT,
                    assessment_type TEXT,  -- 'risk_assessment', 'education_content', 'care_plan'
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)

    def store_patient_info(self, patient_id: str, name: str = None, phone: str = None) -> bool:
        """Store or update patient basic information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                if name or phone:
                    # Update existing patient or insert new
                    conn.execute("""
                        INSERT INTO patients (patient_id, name, phone)
                        VALUES (?, ?, ?)
                        ON CONFLICT(patient_id) DO UPDATE SET
                            name = COALESCE(EXCLUDED.name, patients.name),
                            phone = COALESCE(EXCLUDED.phone, patients.phone),
                            updated_at = CURRENT_TIMESTAMP
                    """, (patient_id, name, phone))
                else:
                    # Just ensure patient exists
                    conn.execute("""
                        INSERT OR IGNORE INTO patients (patient_id)
                        VALUES (?)
                    """, (patient_id,))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing patient info: {e}")
            return False

    def get_patient_info(self, patient_id: str) -> Dict[str, Any]:
        """Get patient basic information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT name, phone, created_at, updated_at
                    FROM patients
                    WHERE patient_id = ?
                """, (patient_id,))

                row = cursor.fetchone()
                if row:
                    name, phone, created_at, updated_at = row
                    return {
                        "patient_id": patient_id,
                        "name": name,
                        "phone": phone,
                        "created_at": created_at,
                        "updated_at": updated_at
                    }
                return {}
        except Exception as e:
            print(f"Error retrieving patient info: {e}")
            return {}

    def store_patient_data(self, patient_id: str, data_type: str, data: Dict[str, Any]) -> bool:
        """Store patient health data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Ensure patient exists
                self.store_patient_info(patient_id)

                # Store the data
                conn.execute("""
                    INSERT INTO health_data (patient_id, data_type, data_json)
                    VALUES (?, ?, ?)
                """, (patient_id, data_type, json.dumps(data)))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing patient data: {e}")
            return False

    def get_patient_data(self, patient_id: str, data_type: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve patient health data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                if data_type:
                    cursor = conn.execute("""
                        SELECT data_json, recorded_at
                        FROM health_data
                        WHERE patient_id = ? AND data_type = ?
                        ORDER BY recorded_at DESC
                        LIMIT 1
                    """, (patient_id, data_type))
                else:
                    cursor = conn.execute("""
                        SELECT data_type, data_json, recorded_at
                        FROM health_data
                        WHERE patient_id = ?
                        ORDER BY recorded_at DESC
                    """, (patient_id,))

                rows = cursor.fetchall()

                if data_type and rows:
                    return json.loads(rows[0][0])
                elif not data_type:
                    result = {}
                    for row in rows:
                        data_type_key, data_json, recorded_at = row
                        if data_type_key not in result:
                            result[data_type_key] = json.loads(data_json)
                    return result
                else:
                    return {}
        except Exception as e:
            print(f"Error retrieving patient data: {e}")
            return {}

    def store_assessment(self, patient_id: str, assessment_type: str, content: str) -> bool:
        """Store assessment results."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO assessments (patient_id, assessment_type, content)
                    VALUES (?, ?, ?)
                """, (patient_id, assessment_type, content))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing assessment: {e}")
            return False

    def get_latest_assessment(self, patient_id: str, assessment_type: str) -> Optional[str]:
        """Get the latest assessment of a specific type."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT content
                    FROM assessments
                    WHERE patient_id = ? AND assessment_type = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (patient_id, assessment_type))

                row = cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            print(f"Error retrieving assessment: {e}")
            return None

    def get_conversation_history(self, patient_id: str, session_id: str) -> List[tuple]:
        """Get conversation history for a patient session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT message_type, message_content, timestamp
                    FROM conversations
                    WHERE patient_id = ? AND session_id = ?
                    ORDER BY timestamp ASC
                """, (patient_id, session_id))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving conversation history: {e}")
            return []

    def store_conversation_message(self, patient_id: str, session_id: str, message_type: str, content: str) -> bool:
        """Store a conversation message."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO conversations (patient_id, session_id, message_type, message_content)
                    VALUES (?, ?, ?, ?)
                """, (patient_id, session_id, message_type, content))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing conversation message: {e}")
            return False


# Global database instance
db = HealthDatabase()