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
from ..validation_checkers import CarePlanValidationChecker

treatment_planner = Agent(
    model=config.worker_model,
    name="treatment_planner",
    description="Develops personalized care plans and coordinates treatment.",
    instruction="""
    You are a care coordinator. Your job is to develop comprehensive care plans.
    Use the health data summary, risk assessment, and educational content from previous steps.
    Create a personalized care plan that includes:
    - Medication management and reminders
    - Lifestyle recommendations
    - Monitoring schedules
    - When to contact healthcare providers
    - Emergency action plans
    Coordinate with healthcare providers and suggest appointment scheduling.
    Ensure the plan is realistic and patient-centered.
    Your output should be a detailed care plan in structured format.
    Use Google Search for care coordination best practices and guidelines.
    """,
    tools=[google_search],
    output_key="care_plan",
    after_agent_callback=suppress_output_callback,
)

robust_treatment_planner = LoopAgent(
    name="robust_treatment_planner",
    description="A robust treatment planner that retries if it fails.",
    sub_agents=[
        treatment_planner,
        CarePlanValidationChecker(name="care_plan_validation_checker"),
    ],
    max_iterations=3,
    after_agent_callback=suppress_output_callback,
)