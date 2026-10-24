# Urdu LLM-Assisted Touch Interface for DHH Users

**A replication & cultural adaptation of DeVries et al. (CHI 2026) for Pakistani Urdu-speaking Deaf and Hard of Hearing users.**

## Overview

This project builds a Gradio web app that simulates a smart home assistant interface for Pakistani Urdu-speaking Deaf and Hard of Hearing (DHH) users. The current UI uses hardcoded bilingual suggestions and a simulated home; the repository also includes a Groq client for future LLM integration.

### What This Project Is

- **Bilingual touch interface** — Users select Urdu + English command options instead of typing or speaking; the current Gradio UI uses hardcoded fixtures.
- **Simulated smart home** — Light state, timer, calendar, weather, and recipe are tracked in-app; no real IoT hardware required.
- **Culturally localized tasks** — Lahore weather, tea timer, biryani recipe, Fajr reminder.
- **Bilingual questionnaires** — SUS, Adjective Scale, and NPS in Urdu + English.
- **DHH-focused** — Recruits 5–8 DHH Urdu speakers for usability testing and interviews.

### What This Project Is NOT

- No voice input / speech recognition (documented as limitation).
- No real Amazon Echo Show or Philips Hue hardware (simulated in-app).
- No Wizard-of-Oz condition (future work).
- No large-scale statistical power (pilot study, N=5–8).

## Quick Start

### Run the Gradio study app

Install the dependencies and start the app from the repository root:

```powershell
python -m pip install -r requirements.txt
python -m app.main
```

Open the local URL printed by Gradio. The current study UI uses hardcoded
bilingual action and task options and updates only the in-memory simulated
home. Replace `get_llm_options(verb, history)` in `app/main.py` when connecting
an LLM to the interface.