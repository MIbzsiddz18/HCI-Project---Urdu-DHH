# Urdu LLM-Assisted Touch Interface for DHH Users

**A replication & cultural adaptation of DeVries et al. (CHI 2026) for Pakistani Urdu-speaking Deaf and Hard of Hearing users.**

## Overview

This project builds a Gradio web app that simulates a smart home assistant interface. It uses an LLM (via Groq API) to generate context-aware command suggestions in Urdu, helping Deaf and Hard of Hearing (DHH) users interact with a simulated smart home environment without relying on voice input.

### What This Project Is

- **LLM-assisted touch interface** — Users select from LLM-generated Urdu command options instead of typing or speaking.
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

### 1. Clone & Enter

```bash
git clone <your-repo-url>