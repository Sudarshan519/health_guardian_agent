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
from ..validation_checkers import RiskAssessmentValidationChecker

health_risk_analyzer = Agent(
    model=config.worker_model,
    name="health_risk_analyzer",
    description="Analyzes health risks and predicts potential complications.",
    instruction="""
    You are a medical risk assessor. Your job is to analyze patient health data and assess risks.
    The health data summary will be available in the `health_data_summary` state key.
    Evaluate the patient's conditions, vital signs, and lab results to identify potential risks.
    Consider factors like medication interactions, disease progression, and lifestyle impacts.
    Use medical knowledge to predict potential complications or adverse events.
    Provide a risk assessment with severity levels and recommended monitoring.
    Your output should be a structured risk assessment report.
    Use Google Search for current medical guidelines and risk factors.
    """,
    tools=[google_search],
    output_key="risk_assessment",
    after_agent_callback=suppress_output_callback,
)

robust_health_risk_analyzer = LoopAgent(
    name="robust_health_risk_analyzer",
    description="A robust health risk analyzer that retries if it fails.",
    sub_agents=[
        health_risk_analyzer,
        RiskAssessmentValidationChecker(name="risk_assessment_validation_checker"),
    ],
    max_iterations=3,
    after_agent_callback=suppress_output_callback,
)