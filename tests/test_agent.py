import asyncio
import json

from google.adk.runners import Runner
from health_guardian_agent.session_store import PersistentSessionService
from health_guardian_agent.agent import root_agent
from health_guardian_agent.database import db
from google.genai import types as genai_types


async def main():
    """Runs the agent with user-provided patient data and queries."""
    session_service = PersistentSessionService()
    await session_service.create_session(
        app_name="app", user_id="PAT001", session_id="test_session_001"
    )
    runner = Runner(
        agent=root_agent, app_name="app", session_service=session_service
    )


    print("Patient data stored. Now enter your queries. Type 'exit' to quit.")
    while True:
        query = input(">>> ")
        if query.lower() == 'exit':
            break
        # Store user message
        session_service.store_message("PAT001", "test_session_001", "user", query)

        async for event in runner.run_async(
            user_id="PAT001",
            session_id="test_session_001",
            new_message=genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text=query)]
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                agent_response = event.content.parts[0].text
                print(agent_response)
                # Store agent response
                session_service.store_message("PAT001", "test_session_001", "agent", agent_response)


if __name__ == "__main__":
    asyncio.run(main())