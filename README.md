# HealthGuardian Agent

## Project Overview

This project contains the core logic for HealthGuardian Agent, a multi-agent system designed to assist patients in managing chronic conditions and improving health outcomes. The agent is built using Google Agent Development Kit (ADK) and follows a modular architecture.

## Problem Statement

Patients with chronic conditions often struggle to manage their health effectively due to complex treatment regimens, lack of personalized education, and challenges in coordinating care across multiple healthcare providers. This leads to poor adherence, frequent hospitalizations, and reduced quality of life. Healthcare systems are overwhelmed, and patients need better tools for self-management and proactive care.

## Solution Statement

HealthGuardian Agent orchestrates specialized AI agents to provide comprehensive health management support. The system analyzes patient data, assesses risks, creates personalized educational content, and develops actionable care plans. By leveraging Google's Gemini AI, it delivers accurate, patient-friendly health guidance while maintaining strict safety standards.

## Architecture

Core to HealthGuardian Agent is the `interactive_health_guardian_agent` -- a prime example of a multi-agent system. It's not a monolithic application but an ecosystem of specialized agents, each contributing to a different stage of health management. This modular approach, facilitated by Google's Agent Development Kit, allows for a sophisticated and robust workflow.

The `interactive_health_guardian_agent` is constructed using the `Agent` class from the Google ADK. Its definition highlights several key parameters: the `name`, the `model` it uses for its reasoning capabilities, and a detailed `description` and `instruction` set that governs its behavior. Crucially, it also defines the `sub_agents` it can delegate tasks to and the `tools` it has at its disposal.

The real power of the `health_guardian_agent` lies in its team of specialized sub-agents, each an expert in its domain.

**Vital Signs Monitor: `robust_vital_signs_monitor`**

This agent analyzes patient health data from various sources, providing summaries of current health status and identifying concerning trends.

**Risk Assessor: `robust_health_risk_analyzer`**

This agent evaluates patient conditions and predicts potential complications, using medical knowledge to assess risks and recommend monitoring priorities.

**Patient Educator: `robust_health_education_specialist`**

This agent creates personalized educational materials that help patients understand their conditions, medications, and lifestyle modifications in accessible language.

**Care Coordinator: `robust_treatment_planner`**

This agent develops comprehensive care plans, including medication management, appointment scheduling, and emergency action plans.

## Essential Tools and Utilities

The `health_guardian_agent` and its sub-agents are equipped with a variety of tools to perform their tasks effectively.

**Health Report Saving (`save_health_report_to_file`)**

A simple yet essential tool that allows the `interactive_health_guardian_agent` to export the final health report to a Markdown file.

**Health Data Fetching (`fetch_health_data`)**

This tool retrieves patient health data from integrated sources, ensuring comprehensive analysis.

**Validation Checkers**

These custom `BaseAgent` implementations ensure the quality and safety of health assessments and recommendations.

## Conclusion

The beauty of the `health_guardian_agent` lies in its iterative and collaborative workflow. The `interactive_health_guardian_agent` acts as a care coordinator, orchestrating the efforts of its specialized team. It delegates tasks, gathers patient feedback, and ensures that each stage of health management is completed successfully. This multi-agent coordination, powered by the Google ADK, results in a system that is modular, reusable, and scalable.

## Value Statement

HealthGuardian Agent empowers patients to take control of their health, potentially reducing hospital readmissions by 20-30% through proactive management and personalized care plans. It bridges the gap between clinical care and daily health management, making complex medical information accessible and actionable.

## Installation

This project was built against Python 3.11.3.

It is suggested you create a virtual environment using your preferred tooling e.g. uv.

Install dependencies e.g. pip install -r requirements.txt

### Running the Agent in ADK Web mode

From the command line of the working directory execute the following command.

```bash
adk web
```

**Run the integration test:**

```bash
python -m pytest tests/
```

## Project Structure

The project is organized as follows:

*   `health_guardian_agent/`: The main Python package for the agent.
    *   `agent.py`: Defines the main `interactive_health_guardian_agent` and orchestrates the sub-agents.
    *   `sub_agents/`: Contains the individual sub-agents, each responsible for a specific health management task.
        *   `vital_signs_monitor.py`: Monitors and analyzes health data.
        *   `health_risk_analyzer.py`: Assesses health risks and complications.
        *   `health_education_specialist.py`: Creates educational content.
        *   `treatment_planner.py`: Develops care plans.
    *   `tools.py`: Defines the custom tools used by the agents.
    *   `config.py`: Contains the configuration for the agents, such as the models to use.
    *   `validation_checkers.py`: Safety validation for health content.
*   `tests/`: Contains integration tests for the agent.

## Workflow

The `interactive_health_guardian_agent` follows this workflow:

1.  **Monitor:** Analyze the patient's health data using the `robust_vital_signs_monitor`.
2.  **Assess:** Evaluate health risks using the `robust_health_risk_analyzer`.
3.  **Educate:** Create personalized education content with the `robust_health_education_specialist`.
4.  **Plan:** Develop a comprehensive care plan using the `robust_treatment_planner`.
5.  **Review:** Present the complete health report to the patient for feedback.
6.  **Refine:** Incorporate patient feedback and iterate on the plan.
7.  **Export:** Save the final health report as a markdown file.