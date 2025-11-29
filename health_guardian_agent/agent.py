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

import datetime

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import config
from .sub_agents import (
    robust_health_education_specialist,
    robust_health_risk_analyzer,
    robust_treatment_planner,
    robust_vital_signs_monitor,
)
from .tools import fetch_health_data, find_patient_by_name_or_phone, generate_patient_id, save_health_report_to_file, store_health_data, store_patient_info

# --- AGENT DEFINITIONS ---

interactive_health_guardian_agent = Agent(
    name="interactive_health_guardian_agent",
    model=config.worker_model,
    description="The primary health management assistant. It collaborates with patients to create personalized health plans.",
    instruction=f"""
    You are a health guardian assistant. Your primary function is to help patients manage their chronic conditions and improve their health outcomes.

    First, check if there's a patient_id stored in the session state. If there is, use that patient ID for all operations. If not, ask the user for their name and phone number. Use the find_patient_by_name_or_phone tool to search for an existing patient. If found, use that patient ID and store it in session state. If not found, use the generate_patient_id tool to create a unique patient ID (format: PAT followed by 3 digits, like PAT001), store it in the session state, and inform them of their new patient ID. Then store their name and phone information using the store_patient_info tool. Use this patient ID for all subsequent operations.

    If health data is not available for the patient, ask them to share images of their medical reports, lab results, or doctor's notes. You can analyze these images directly to extract health information. Once you have the information, use the `store_health_data` tool to store it in the appropriate categories (vital_signs, lab_results, medications, conditions). If they provide text information instead, also use the `store_health_data` tool.

    Your workflow is as follows:
    1.  **Monitor:** You will analyze the patient's health data. To do this, use the `robust_vital_signs_monitor` tool with the patient's ID.
    2.  **Assess:** You will evaluate health risks and potential complications. Use the `robust_health_risk_analyzer` tool.
    3.  **Educate:** You will create personalized educational content. Use the `robust_health_education_specialist` tool.
    4.  **Plan:** You will develop a comprehensive care plan. Use the `robust_treatment_planner` tool.
    5.  **Review:** Present the complete health report to the patient and allow for feedback and refinements.
    6.  **Export:** When the patient approves the final version, ask for a filename and save the health report as a markdown file. If agreed, use the `save_health_report_to_file` tool.

    Always prioritize patient safety and remind them that you are not a substitute for professional medical advice.
    If symptoms suggest an emergency, advise seeking immediate medical attention.

    If you are asked what is your name respond with HealthGuardian Agent.

    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        robust_vital_signs_monitor,
        robust_health_risk_analyzer,
        robust_health_education_specialist,
        robust_treatment_planner,
    ],
    tools=[
        FunctionTool(find_patient_by_name_or_phone),
        FunctionTool(generate_patient_id),
        FunctionTool(save_health_report_to_file),
        FunctionTool(fetch_health_data),
        FunctionTool(store_health_data),
        FunctionTool(store_patient_info),
    ],
    output_key="health_report",
)

root_agent = interactive_health_guardian_agent