# Urdu LLM-Assisted Touch Interface for DHH Users

**A replication & cultural adaptation of DeVries et al. (CHI 2026) for Pakistani Urdu-speaking Deaf and Hard of Hearing users.**

## Overview

This project builds a Gradio web app that simulates a smart home assistant interface for Pakistani Urdu-speaking Deaf and Hard of Hearing (DHH) users. The app uses bilingual action buttons, Groq-generated Urdu suggestions when configured, and a simulated smart home.

### What This Project Is

- **Bilingual touch interface** — Participants use large Urdu and English buttons instead of typing or speaking.
- **Groq suggestions** — Contextual Urdu command suggestions are generated for each assigned task. If Groq is unavailable, the app uses the localized task text as a safe fallback.
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

Open the local URL printed by Gradio. If using a virtual environment, activate it before installing requirements and starting the app. Add `GROQ_API_KEY` and `GROQ_MODEL` to `.env` to enable generated suggestions. The app does not call Groq at startup; it makes a request when a participant chooses an action during a task. Groq usage may be billable depending on the account tier and model.

## Study sessions and saved data

Use a participant code rather than a participant name. Confirm consent before starting a session. The app presents the five planned tasks in order, measures task latency, records chosen actions and suggestions, and stores task outcomes. Questionnaire and interview fields save as they are entered. Use **Reset session and home** between participants; an unfinished session is retained with a reset status.

The app writes de-identified data locally under `data/raw/`:

- `session_log.csv` — demographics, SUS item responses and score, adjective rating, NPS, interview notes, task completion rate, and mean latency.
- `task_log.csv` — one row per planned task, including status, latency, selected action, suggestion, and model/fallback status.
- `sessions/<session_id>.json` — full event history and all captured fields.

These files are ignored by Git. Keep them backed up securely and do not add identifiable participant information. The app does not record audio; audio recordings, if consented to, remain managed separately by the research team.

Run analyses after collecting data:

```powershell
python analysis\sus_scores.py data\raw\session_log.csv
python analysis\latency_analysis.py data\raw\task_log.csv
```
