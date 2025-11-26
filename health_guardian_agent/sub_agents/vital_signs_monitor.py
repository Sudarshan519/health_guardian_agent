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

from ..config import config
from ..agent_utils import suppress_output_callback
from ..tools import fetch_health_data
from ..validation_checkers import HealthDataValidationChecker

vital_signs_monitor = Agent(
    model=config.worker_model,
    name="vital_signs_monitor",
    description="Monitors and analyzes patient vital signs and health data.",
    instruction="""
    You are a health data analyst. Your job is to analyze patient vital signs and health data.
    The health data will be available in the `health_data` state key from the fetch_health_data tool.
    Analyze the vital signs, lab results, medications, and conditions.
    Provide a summary of the patient's current health status, including any concerning trends.
    Focus on key metrics like blood pressure, heart rate, glucose levels, etc.
    Your output should be a clear summary in structured format.
    """,
    tools=[fetch_health_data],
    output_key="health_data_summary",
    after_agent_callback=suppress_output_callback,
)

robust_vital_signs_monitor = LoopAgent(
    name="robust_vital_signs_monitor",
    description="A robust vital signs monitor that retries if it fails.",
    sub_agents=[
        vital_signs_monitor,
        HealthDataValidationChecker(name="health_data_validation_checker"),
    ],
    max_iterations=3,
    after_agent_callback=suppress_output_callback,
)