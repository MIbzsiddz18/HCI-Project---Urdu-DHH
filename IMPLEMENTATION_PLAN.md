# Implementation Plan: Urdu LLM-Assisted Touch Interface for DHH Users

**Project:** Replication & Cultural Adaptation of DeVries et al. (CHI 2026)  
**Team:** Faraz, Ashhal, Ibrahim  
**Timeline:** 48 hours (MVP) + 1 week (full study, due Nov 1)  
**Budget:** $0 (free-tier only)

---

## 1. Project Scope (What We ARE Building)

We build **only the LLM-assisted touch interface condition** from the original paper, adapted for Pakistani Urdu-speaking DHH users.

### In Scope
- Gradio web app with Urdu/English UI
- Groq API (Llama 3.1 8B Instant) for LLM-generated command suggestions
- Simulated smart home environment (in-app state dictionary)
- 5 culturally localized tasks (Urdu)
- Bilingual SUS + Adjective Scale + NPS questionnaires
- Semi-structured interviews (Urdu)
- 5–8 DHH participants (convenience sample)

### Out of Scope (Document as Limitations)
- Voice conditions (Natural Deaf Speech, Wizard-of-Oz)
- Real Amazon Echo Show / Philips Hue hardware
- Urdu ASR / WER analysis
- Large sample (N=20) or statistical power
- Validated Urdu SUS translation

---

## 2. Technical Stack

| Component | Tool | Why |
|---|---|---|
| **LLM** | Groq API — `llama-3.1-8b-instant` | Free (14,400 req/day), ultra-fast (~500 tok/s), reliable instruction-following |
| **Frontend** | Gradio (Python) | 100–150 lines, no HTML/CSS needed, runs locally |
| **Smart Home** | Python dictionary (simulated) | No hardware, instant state updates, safe |
| **Questionnaires** | Google Forms (bilingual) | Free, easy to share, auto-exports to Sheets |
| **Audio Recording** | Phone voice recorder | Free, no setup |
| **Transcription** | Manual (bilingual team member) | No budget for paid transcription |
| **Analysis** | Python (pandas, matplotlib) + manual thematic coding | Free |
| **Version Control** | GitHub (free) | Backup + team collaboration |

**Fallback Plan:** If Llama 3.1 8B's Urdu output is poor, LLM will output English internally; app will map to hardcoded Urdu strings for display. This guarantees clean Urdu UI regardless of LLM quality.

---

## 3. Directory Structure

```text
urdu-ipa-project/
│
├── README.md                    # Setup + run instructions
├── requirements.txt             # gradio, groq, pandas, python-dotenv
├── .env                         # GROQ_API_KEY (gitignored)
├── .gitignore
│
├── app/
│   ├── main.py                  # Gradio app entry point
│   ├── llm_client.py            # Groq API wrapper + prompts
│   ├── smart_home.py            # Simulated state dict + update logic
│   ├── prompts.py               # All Urdu/English LLM prompts
│   ├── translations.py          # Hardcoded Urdu strings (fallback)
│   └── tasks.py                 # Localized task lists
│
├── questionnaires/
│   ├── sus_bilingual.pdf        # Urdu + English SUS
│   ├── adjective_nps.pdf        # Adjective Scale + NPS
│   └── consent_form.pdf         # Bilingual consent
│
├── study/
│   ├── protocol.md              # Step-by-step session procedure
│   ├── interview_guide_urdu.md  # 5 interview questions (Urdu + English)
│   ├── demographics_survey.md   # Pre-experiment survey
│   └── session_log_template.csv # For recording per-participant data
│
├── data/
│   ├── raw/                     # Raw session logs, audio files
│   ├── transcripts/             # Interview transcripts
│   └── processed/               # SUS scores, cleaned data
│
├── analysis/
│   ├── sus_scores.py            # SUS calculation + descriptive stats
│   ├── latency_analysis.py      # Mean latency per command
│   └── thematic_coding.md       # Theme tracking (shared doc)
│
└── docs/
    ├── final_report.md          # Final submission (Nov 1)
    ├── presentation.pdf
    └── limitations.md           # Drafted limitations section
```

---

## 4. Three-Way Work Division

### FARAZ — Study Design & Analysis Lead

**Responsibilities:** Experimental protocol, participant recruitment, session running, data analysis, final report.

**Deliverables (48 hours):**
- `study/protocol.md` — step-by-step session procedure
- `study/session_log_template.csv`
- `analysis/sus_scores.py`
- `analysis/latency_analysis.py`
- `docs/limitations.md` — drafted limitations
- **Recruit 2–3 pilot participants** for Sunday
- `docs/presentation.pdf` — slides for Sunday submission

**Timeline:**

| Hours | Task |
|---|---|
| 0–2 | Write `study/protocol.md`: consent → pre-survey → exploration → 5 tasks → SUS → interview. 30–40 min per session. |
| 2–6 | Write `session_log_template.csv`. Write `sus_scores.py` (SUS scoring + descriptive stats). |
| 6–10 | Write `latency_analysis.py`. Draft `limitations.md`. Draft experimental plan document (due Sunday). |
| 10–14 | Recruit 2–3 pilot participants (DHH if possible, otherwise bilingual hearing for UX pilot). Schedule Sunday sessions. |
| 14–18 | Build `presentation.pdf` skeleton (intro, methods, expected results, limitations). |
| 18–22 | Run pilot sessions (with Ashhal). Note what breaks. |
| 22–24 | Finalize experimental plan document. Submit with app screenshots + presentation. |

**Full Study Week:** Recruit 5–8 DHH participants, schedule sessions, run analysis (SUS + thematic coding), write final report, prepare final presentation.

**LLM Chat Prompts for Faraz:**

```
Prompt 1 (protocol.md):
"I am writing a step-by-step experimental protocol for a usability study 
of an LLM-assisted touch interface for Pakistani Deaf and Hard of Hearing 
Urdu speakers. The session should take 30-40 minutes: consent, 
pre-survey, 5-minute exploration, 5 tasks, SUS questionnaire, and a 
5-minute semi-structured interview. Write a detailed protocol.md in 
Markdown with numbered steps for the researcher to follow. Include 
estimated time per step."

Prompt 2 (sus_scores.py):
"Write a Python script that calculates the System Usability Scale (SUS) 
score from 10 Likert responses (1-5). Odd-numbered items (1,3,5,7,9) 
are scored as (response - 1). Even-numbered items (2,4,6,8,10) are 
scored as (5 - response). The total is multiplied by 2.5 to give a 
0-100 score. Also compute mean, standard deviation, and median across 
multiple participants. Read data from a CSV file and print results."

Prompt 3 (session_log_template.csv):
"Create a CSV template for logging per-participant session data for a 
usability study. Columns should include: participant_id, date, age, 
gender, hearing_status (Deaf/HoH), hearing_device (cochlear implant/
hearing aid/none), language_background (Urdu/English/PSL mix), 
prior_ipa_experience, task_completion_rate, mean_latency_seconds, 
sus_score, adjective_score, nps_score, session_notes."
```

---

### ASHHAL — Frontend & UX Lead

**Responsibilities:** Gradio app UI, task flow, questionnaires, participant-facing materials.

**Deliverables (48 hours):**
- `app/main.py` — full Gradio app (working)
- `questionnaires/sus_bilingual.pdf` — Urdu + English SUS
- `questionnaires/adjective_nps.pdf`
- `questionnaires/consent_form.pdf`
- `study/interview_guide_urdu.md`
- `study/demographics_survey.md`

**Timeline:**

| Hours | Task |
|---|---|
| 0–2 | Design Gradio layout (sketch on paper). Decide: 3×3 button grid, history panel, state display. |
| 2–8 | Build `main.py` skeleton: start screen → task selection → verb buttons → option buttons → command confirmation → state update. Use dummy LLM responses first. |
| 8–14 | Integrate Faraz's `llm_client.py` (wait for Faraz to finish it by Hour 10). Test full flow. Fix UI bugs. |
| 14–18 | Create bilingual SUS + Adjective + NPS + consent form (Google Docs → PDF). Translate with team. |
| 18–22 | Write `interview_guide_urdu.md` (5 questions, Urdu + English). Write `demographics_survey.md`. |
| 22–24 | Full app dry-run with Faraz. Document UX issues. |

**Full Study Week:** Run participant sessions (primary facilitator), take notes, collect questionnaires, transcribe interviews.

**LLM Chat Prompts for Ashhal:**

```
Prompt 1 (main.py skeleton):
"Create a Gradio web app in Python for a smart home assistant research 
study. The app should have: (1) a welcome screen with a task list, 
(2) a 3x3 grid of buttons showing 8 LLM-generated action verb options 
in Urdu + English, (3) after selection, another 3x3 grid of task options, 
(4) a confirmation screen showing the final command, (5) a smart home 
state display showing light status, timer, calendar, etc. Use dummy 
hardcoded responses for now. Structure it so the LLM call can be 
plugged in later via a function called get_llm_options(verb, history)."

Prompt 2 (interview_guide_urdu.md):
"Write a semi-structured interview guide in Markdown for a usability 
study of a smart home touchscreen app for Pakistani Deaf and Hard of 
Hearing users. Include 5 questions in both Urdu script and English 
translation. Topics: (1) easiest/hardest part of using the app, 
(2) quality of Urdu translations, (3) privacy concerns about AI 
remembering habits, (4) interest in hands-free alternatives (voice/sign), 
(5) suggestions for improvement. Include probing follow-ups."

Prompt 3 (demographics_survey.md):
"Create a bilingual (Urdu + English) pre-experiment demographic survey 
in Markdown. Include: age, gender, hearing status (Deaf/HoH/Deaf-Blind), 
hearing device (cochlear implant/hearing aid/none), preferred 
communication languages (Urdu/English/PSL/other), prior experience 
with voice assistants (yes/no, frequency), and any accessibility needs."
```

---

### IBRAHIM — LLM & Backend Lead

**Responsibilities:** Groq API integration, prompt engineering, smart home simulation, LLM fallback logic.

**Deliverables (48 hours):**
- `app/llm_client.py` — working Groq wrapper with error handling
- `app/prompts.py` — all prompts translated from paper's Appendix C to Urdu/English
- `app/smart_home.py` — state dictionary + update functions
- `app/translations.py` — hardcoded Urdu fallback strings
- `app/tasks.py` — localized task list
- `requirements.txt` + `.env.example`
- Test Llama 3.1 8B with 10 sample commands. Document output quality.

**Timeline:**

| Hours | Task |
|---|---|
| 0–2 | Get Groq API key. Test Llama 3.1 8B with 5 sample Urdu prompts. Report quality. |
| 2–6 | Write `prompts.py` (all 6 prompts from Appendix C, localized). |
| 6–10 | Write `llm_client.py` + `smart_home.py`. Test end-to-end via terminal. **Deliver `llm_client.py` to Ashhal by Hour 10.** |
| 10–14 | Write `translations.py` fallback. Test all 5 tasks end-to-end. Fix bugs. |
| 14–18 | Write `tasks.py` with localized task list. Final LLM testing. |
| 18–24 | Buffer: fix bugs found by Ashhal/Faraz. Document LLM quirks. |

**Full Study Week:** Fix bugs, optimize prompts based on pilot feedback, help with data analysis.

**LLM Chat Prompts for Ibrahim:**

```
Prompt 1 (llm_client.py):
"Write a Python module llm_client.py that wraps the Groq API to generate 
smart home command options in Urdu. Use the groq Python SDK with model 
'llama-3.1-8b-instant'. Include functions: (1) get_action_verbs(history, 
home_env) returns a list of 8 Urdu verbs, (2) get_task_options(verb, 
history, home_env) returns 8 task options, (3) needs_more_info(task) 
returns bool, (4) get_followup_question(task) returns a question, 
(5) get_followup_options(question) returns 8 answer options, 
(6) build_final_command(task, question, answer) returns a complete 
command. Include error handling for API failures and a fallback to 
hardcoded responses if the API is unreachable."

Prompt 2 (prompts.py):
"Write a Python file prompts.py containing all LLM prompt templates for 
a smart home assistant study. The prompts must generate Urdu-language 
options for: (1) initial action verbs, (2) task options for a chosen 
verb, (3) whether a task needs more info, (4) a follow-up question, 
(5) answer options for the follow-up, (6) final command assembly. 
Each prompt should consider: the smart home environment (lights, timer, 
calendar, weather, recipe), user command history, and culturally 
relevant Pakistani tasks (biryani recipe, Fajr reminder, Lahore weather, 
tea timer). Include a note that if Urdu output is inconsistent, the 
LLM should output English internally with a mapping to Urdu."

Prompt 3 (smart_home.py):
"Write a Python module smart_home.py that simulates a smart home state 
dictionary. State includes: light (off/on), light_color 
(white/blue/red/green), timer (None or duration string), reminder 
(None or string), calendar (string), weather (string), recipe (string). 
Include functions: update_state(command) parses a command string and 
updates the relevant field, get_state_display() returns a formatted 
string showing current state for the UI, reset_state() resets all fields."

Prompt 4 (tasks.py):
"Write a Python file tasks.py with a list of 5 culturally localized 
smart home tasks for Pakistani Urdu speakers. Each task has an Urdu 
string, an English translation, and an expected smart home state change. 
Tasks: (1) Check Lahore weather, (2) Set a 5-minute tea timer, 
(3) Set light color to blue, (4) Show a biryani recipe, 
(5) Set a Fajr prayer reminder."

Prompt 5 (translations.py):
"Write a Python file translations.py with hardcoded Urdu strings that 
map to English smart home commands. Include translations for: turn on/
off light, set light color to blue/red/green, set timer for 5/10 minutes, 
check weather in Lahore, show biryani recipe, set Fajr reminder, show 
calendar. Format as a dictionary with English keys and Urdu values."
```

---

## 5. 48-Hour Master Timeline

### Saturday (Day 1) — Build

| Time | Faraz | Ashhal | Ibrahim |
|---|---|---|---|
| **09:00–11:00** | Write protocol.md | Gradio layout design | Groq setup + LLM test |
| **11:00–13:00** | Write session_log + sus_scores.py | Build main.py skeleton | Write prompts.py |
| **13:00–14:00** | *Lunch* | *Lunch* | *Lunch* |
| **14:00–17:00** | latency_analysis.py + draft limitations | Integrate LLM (dummy first), test flow | llm_client.py + smart_home.py |
| **17:00–19:00** | Recruit pilot participants | Fix UI bugs | **Deliver llm_client.py to Ashhal** + translations.py |
| **19:00–20:00** | *Dinner* | *Dinner* | *Dinner* |
| **20:00–23:00** | Build presentation skeleton | Create questionnaires + interview guide | tasks.py + final LLM testing |
| **23:00–00:00** | Buffer: support team | Full dry-run with Faraz | Full dry-run with Ashhal |

### Sunday (Day 2) — Test & Submit

| Time | Faraz | Ashhal | Ibrahim |
|---|---|---|---|
| **09:00–12:00** | Run pilot sessions | Run pilot sessions | Fix bugs from pilot |
| **12:00–14:00** | Analyze pilot data | Fix UX issues | Optimize prompts based on pilot |
| **14:00–17:00** | Write experimental plan doc | Final questionnaire check | Final testing |
| **17:00–19:00** | Build presentation slides | Build presentation slides | Help with presentation |
| **19:00–21:00** | Review everything | Review everything | Review everything |
| **21:00–00:00** | **SUBMIT:** experimental plan + app + presentation | | |

### Week (Oct 25 – Nov 1) — Full Study

| Day | Task |
|---|---|
| **Mon–Tue** | Recruit 5–8 DHH participants via Deaf Reach, PAD, personal networks. Schedule sessions. |
| **Wed–Thu** | Run all sessions (Ashhal facilitates, Faraz notes, Ibrahim handles tech). |
| **Fri** | Transcribe interviews (Ibrahim + Ashhal split). Faraz computes SUS + latency stats. |
| **Sat** | Thematic coding (Faraz + Ashhal). Ibrahim writes results section. |
| **Sun (Nov 1)** | Finalize report + presentation. **Submit by night.** |

---

## 6. Key Implementation Details

### 6.1 LLM Prompt Strategy

Use the paper's Appendix C prompts as templates. Key adaptation:

```
You are an Urdu-speaking smart home assistant for Pakistani users. 
Generate 8 action verbs in Urdu script (اردو) for starting commands. 
Examples: "روشن کریں" (turn on), "سیٹ کریں" (set), "دکھائیں" (show). 
Consider this smart home: {lights, timer, calendar, weather, recipe}. 
User history: {commands_so_far}. 
Return only the verbs, one per line, no numbering, no quotes.
```

**Test criterion:** If 6/8 verbs are correct Urdu and contextually relevant → keep Urdu output. Otherwise → switch to English-internal/Urdu-display fallback.

### 6.2 Simulated Smart Home

```python
state = {
    "light": "off",           # off / on
    "light_color": "white",   # white / blue / red / green
    "timer": None,            # None / "5 min" / "10 min"
    "reminder": None,         # None / "Fajr" / "lunch"
    "calendar": "No events today",
    "weather": "Not checked",
    "recipe": "Not shown"
}
```

When user confirms a command, parse it and update the relevant field. Display state visually (e.g., a "light bulb" icon changes color).

### 6.3 Localized Task List (5 Tasks)

1. **"Lahore mein aaj ka mausam check karein"** (Check today's weather in Lahore)
2. **"Chai ke liye 5 minute ka timer lagayein"** (Set a 5-minute tea timer)
3. **"Batti ko neela rang dein"** (Set the light to blue)
4. **"Biryani ki recipe dikhayein"** (Show a biryani recipe)
5. **"Fajr ke liye reminder lagayein"** (Set a Fajr reminder)

### 6.4 SUS Scoring

Standard SUS scoring in `sus_scores.py`:

```python
def sus_score(responses):
    # responses: list of 10 ints (1-5)
    # Odd items (1,3,5,7,9): score - 1
    # Even items (2,4,6,8,10): 5 - score
    total = 0
    for i, r in enumerate(responses, start=1):
        if i % 2 == 1:
            total += (r - 1)
        else:
            total += (5 - r)
    return total * 2.5  # 0-100
```

### 6.5 Fallback Plan (If Anything Breaks)

| Problem | Fallback |
|---|---|
| Groq API down/rate-limited | Switch to OpenRouter free tier (`meta-llama/llama-3.1-8b-instruct:free` — 50 req/day) or HuggingFace Inference API |
| Urdu LLM output poor | English-internal/Urdu-display fallback (see 6.1) |
| Gradio crashes | Run in simplest mode (no CSS, basic blocks) |
| Can't recruit DHH participants | Run with bilingual hearing participants for pilot; document as limitation; recruit DHH for full study week |
| No internet during session | Pre-cache LLM responses for all task paths (run through app once, save outputs to JSON, load offline) |

---

## 7. Free-Tier API Reference

| Provider | Model | Free Quota | Speed | Urdu Quality |
|---|---|---|---|---|
| **Groq** (primary) | `llama-3.1-8b-instant` | 14,400 req/day | Very fast | Moderate |
| Groq (backup) | `llama-3.3-70b-versatile` | 1,000 req/day | Fast | Better |
| OpenRouter (fallback) | `meta-llama/llama-3.1-8b-instruct:free` | 50 req/day | Slow | Moderate |
| HuggingFace (last resort) | Various | Limited | Slow | Varies |

**Recommendation:** Use Groq's Llama 3.1 8B for all development and testing. If Urdu quality is unacceptable, switch to Llama 3.3 70B (only for final study, not dev).

---

## 8. Final Deliverables Checklist

### Due Sunday Night (48 hours)
- [ ] Working Gradio app (runnable via `python app/main.py`)
- [ ] Experimental plan document (2–3 pages)
- [ ] Presentation slides (10–12 slides)
- [ ] Bilingual questionnaires (SUS, Adjective, NPS, consent)
- [ ] Interview guide (Urdu + English)
- [ ] Task list (5 localized tasks)
- [ ] Pilot data from 2–3 participants (if possible)

### Due Nov 1 (Full Study)
- [ ] 5–8 DHH participant sessions completed
- [ ] SUS + Adjective + NPS scores collected
- [ ] Interview transcripts + thematic analysis
- [ ] Final report (6–8 pages): intro, related work, methods, results, discussion, limitations, conclusion
- [ ] Final presentation

---

## 9. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM Urdu output poor | High | Medium | Fallback to English-internal/Urdu-display |
| Can't recruit DHH participants | Medium | High | Start recruitment immediately Sunday morning via personal networks; have hearing bilingual pilot as backup |
| Groq rate limit hit | Low | Low | 14,400/day is plenty; have OpenRouter backup |
| Gradio bugs | Medium | Medium | Keep UI simple; no custom CSS |
| Team member unavailable | Low | High | Cross-train: everyone knows how to run the app and the session protocol |
| Internet outage during session | Medium | High | Pre-cache LLM responses as JSON; run offline mode |

---

## 10. Communication Protocol

- **WhatsApp group:** Daily standup at 9 AM and 9 PM (5 min each)
- **GitHub:** Push code every 4 hours. Commit messages in English.
- **Shared Google Drive:** For questionnaires, transcripts, and drafts
- **Decision rule:** If a feature takes >2 hours to build and isn't in the "In Scope" list, cut it. Ship the MVP.
