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
from typing import Dict, Any, List, Optional
from google.adk import Session, SessionService
from .database import db


class PersistentSessionService(SessionService):
    """A session service that persists conversations to SQLite database."""

    def __init__(self):
        # Ensure conversations table exists
        with sqlite3.connect(db.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT,
                    session_id TEXT,
                    message_type TEXT,
                    message_content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
                )
            """)

    async def create_session(self, app_name: str, user_id: str, session_id: str) -> Session:
        """Create a new session."""
        session = Session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state={}
        )
        return session

    async def get_session(self, app_name: str, user_id: str, session_id: str) -> Optional[Session]:
        """Retrieve a session and its conversation history."""
        # Load conversation history from database
        conversation_history = db.get_conversation_history(user_id, session_id)

        # Convert to the format expected by ADK
        messages = []
        for msg_type, content, timestamp in conversation_history:
            if msg_type == 'user':
                messages.append({
                    'role': 'user',
                    'content': content,
                    'timestamp': timestamp
                })
            elif msg_type == 'agent':
                messages.append({
                    'role': 'assistant',
                    'content': content,
                    'timestamp': timestamp
                })

        session = Session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state={'conversation_history': messages}
        )
        return session

    async def save_session(self, session: Session) -> None:
        """Save session data (conversation history) to database."""
        # This would be called after each interaction
        # For now, we'll save messages as they're added
        pass

    async def delete_session(self, app_name: str, user_id: str, session_id: str) -> None:
        """Delete a session."""
        # Optional: implement if needed
        pass

    async def list_sessions(self, app_name: str, user_id: str) -> List[str]:
        """List all session IDs for a user."""
        try:
            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.execute("""
                    SELECT DISTINCT session_id
                    FROM conversations
                    WHERE patient_id = ?
                """, (user_id,))
                return [row[0] for row in cursor.fetchall()]
        except Exception:
            return []

    def store_message(self, patient_id: str, session_id: str, message_type: str, content: str) -> None:
        """Store a conversation message."""
        db.store_conversation_message(patient_id, session_id, message_type, content)