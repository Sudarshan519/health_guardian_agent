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

from google.adk.agents import Agent, LoopAgent
from google.adk.tools import google_search

from ..config import config
from ..agent_utils import suppress_output_callback
from ..validation_checkers import EducationContentValidationChecker

health_education_specialist = Agent(
    model=config.worker_model,
    name="health_education_specialist",
    description="Creates personalized health education content.",
    instruction="""
    You are a health education specialist. Your job is to create personalized educational content.
    The health data summary and risk assessment will be available in the state keys.
    Create educational materials that help patients understand their conditions and management.
    Include information about their specific conditions, medications, lifestyle modifications, and warning signs.
    Make the content patient-friendly, using simple language and clear explanations.
    Include actionable tips and when to seek medical attention.
    Your output should be comprehensive educational content in readable format.
    Use Google Search for current health education resources and guidelines.
    """,
    tools=[google_search],
    output_key="education_content",
    after_agent_callback=suppress_output_callback,
)

robust_health_education_specialist = LoopAgent(
    name="robust_health_education_specialist",
    description="A robust health education specialist that retries if it fails.",
    sub_agents=[
        health_education_specialist,
        EducationContentValidationChecker(name="education_content_validation_checker"),
    ],
    max_iterations=3,
    after_agent_callback=suppress_output_callback,
)