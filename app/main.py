"""Gradio study interface with Groq suggestions and durable session logging."""

from __future__ import annotations

from copy import deepcopy
import os
import time

import gradio as gr

try:
    from . import llm_client, session_store, translations
    from .smart_home import get_state, get_state_display, preview_state, reset_state, update_state
    from .tasks import TASKS
except ImportError:  # pragma: no cover - supports `python app/main.py`
    import llm_client
    import session_store
    import translations
    from smart_home import get_state, get_state_display, preview_state, reset_state, update_state
    from tasks import TASKS


ACTION_VERBS = [
    {"urdu": "روشن کریں", "english": "Turn on"},
    {"urdu": "بند کریں", "english": "Turn off"},
    {"urdu": "سیٹ کریں", "english": "Set"},
    {"urdu": "دکھائیں", "english": "Show"},
    {"urdu": "چیک کریں", "english": "Check"},
    {"urdu": "بدلیں", "english": "Change"},
    {"urdu": "یاد دہانی لگائیں", "english": "Set a reminder"},
    {"urdu": "مدد لیں", "english": "Get help"},
]

APP_CSS = """
/* Visual design for the bilingual DHH study UI.
   Rules never set `display` on components Gradio toggles with `.hidden`,
   so visibility stays controlled by the Python handlers. */
:root, .gradio-container, .dark .gradio-container {
  color-scheme: light;
  --canvas: #eef2f1;
  --surface: #ffffff;
  --surface-tint: #e5f2ef;
  --readout: #f4f7f6;
  --ink: #15232a;
  --muted: #56656c;
  --line: #d5dfdd;
  --accent: #0b6b66;
  --accent-pressed: #08524e;
  --accent-ring: #7cc2b9;
  --preview: #fff7e6;
  --preview-line: #f0cf8a;
  --preview-ink: #7a4f00;
  --danger: #a8322b;
  --danger-line: #e6c3c0;
  --danger-tint: #fbeceb;
  --focus: #d4651c;
  --radius-card: 20px;
  --radius-control: 12px;
  --shadow-1: 0 1px 2px rgba(14,44,41,.06), 0 2px 8px rgba(14,44,41,.04);
  --shadow-2: 0 1px 2px rgba(14,44,41,.06), 0 8px 24px rgba(14,44,41,.07);
  --font-mix: "Atkinson Hyperlegible","Noto Nastaliq Urdu","Jameel Noori Nastaleeq","Urdu Typesetting","Segoe UI",system-ui,sans-serif;
  --font-urdu: "Noto Nastaliq Urdu","Jameel Noori Nastaleeq","Urdu Typesetting","Segoe UI",serif;
  /* Pin Gradio theme variables to the light palette, even if the OS is in dark mode. */
  --body-background-fill: var(--canvas) !important;
  --background-fill-primary: var(--surface) !important;
  --background-fill-secondary: var(--readout) !important;
  --block-background-fill: var(--surface) !important;
  --input-background-fill: #ffffff !important;
  --body-text-color: var(--ink) !important;
  --body-text-color-subdued: var(--muted) !important;
  --block-label-text-color: var(--muted) !important;
  --block-title-text-color: var(--ink) !important;
  --border-color-primary: var(--line) !important;
  --block-border-color: var(--line) !important;
  --color-accent: var(--accent) !important;
  --color-accent-soft: var(--surface-tint) !important;
}
body, .gradio-container {
  background: var(--canvas) !important;
  color: var(--ink) !important;
  font-family: var(--font-mix) !important;
  font-size: 16px !important;
  line-height: 1.6 !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.gradio-container { max-width: 1360px !important; margin: 0 auto !important; padding: 16px 24px 24px !important; }
.gradio-container > .main, .gradio-container .main > .wrap { gap: 14px !important; }
.gradio-container h1, .gradio-container h2, .gradio-container h3, .gradio-container h4 {
  color: var(--ink) !important; text-wrap: balance;
}
.gradio-container p { color: var(--muted); text-wrap: pretty; }

/* Header: compact so the task and choices stay above the fold on a 1366x768 laptop */
.block.app-header { padding: 0 4px !important; }
.app-header h1 { font-size: 1.3rem !important; font-weight: 700 !important; line-height: 1.9 !important; letter-spacing: -.01em; margin: 0 !important; }
.app-header p { font-size: .92rem !important; margin: 0 !important; }

/* Two-column layout; the sidebar stays in view while the main column scrolls */
.app-layout { align-items: flex-start !important; gap: 18px !important; }
.side-col { position: sticky; top: 12px; align-self: flex-start !important; }

/* Cards: shadows give elevation, borders only mark state */
.study-card {
  border: 0 !important; border-radius: var(--radius-card) !important;
  background: var(--surface) !important; padding: 20px 22px !important;
  box-shadow: var(--shadow-2) !important; overflow: visible !important;
}
.study-card > *, .study-card .form { gap: 14px !important; }
.study-card .form, .study-card .block { border: 0 !important; box-shadow: none !important; background: transparent !important; }
.study-card > .styler { background: transparent !important; }
.study-card .block.padded { padding: 4px 0 !important; }
/* Gradio wraps adjacent inputs in a .form whose background acts as a divider colour; open it up into spaced fields */
.gradio-container .form { background: transparent !important; border: 0 !important; box-shadow: none !important; gap: 12px !important; overflow: visible !important; }
.gradio-container .form > .block { border-radius: 0 !important; }
.welcome-head h3 { font-size: 1.25rem !important; margin: 0 0 4px !important; }
.welcome-head p { font-size: .94rem !important; max-width: 70ch; }

/* Task card: progress eyebrow, Urdu instruction dominant and right-to-left */
.block.task-card {
  background: var(--surface) !important; border-radius: var(--radius-card) !important;
  box-shadow: var(--shadow-2) !important; padding: 14px 22px 16px !important; border: 0 !important;
}
.task-card h3 {
  font-size: .8rem !important; font-weight: 700 !important; letter-spacing: .06em !important;
  text-transform: uppercase; color: var(--accent) !important; margin: 0 0 2px !important;
  font-variant-numeric: tabular-nums; line-height: 2 !important;
}
.task-card p { margin: 0 !important; }
.task-card p:nth-of-type(1) {
  direction: rtl; text-align: right; font-family: var(--font-urdu) !important;
  font-size: 1.55rem !important; line-height: 2.15 !important; color: var(--ink) !important;
}
.task-card p:nth-of-type(2) { font-size: 1.05rem !important; color: var(--muted) !important; }
.task-card strong { font-family: var(--font-mix); font-size: .8rem; font-weight: 700; color: var(--muted); margin-inline-end: 6px; }
.stage-heading { padding: 0 4px !important; }
.stage-heading h3 { font-size: 1.02rem !important; font-weight: 700 !important; margin: 0 !important; line-height: 2 !important; }

/* Choice tiles: large, evenly spaced targets; Urdu line first and larger */
.choice-grid { gap: 12px !important; }
.choice-grid > .row { display: grid !important; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px !important; }
.choice-grid > .row:not(:has(button:not(.hidden))) { display: none !important; }
.choice-grid button:not(.hidden) {
  display: block !important; width: 100% !important; min-width: 0 !important;
  min-height: 92px !important; height: auto !important; padding: 10px 14px !important;
  border: 1.5px solid transparent !important; border-radius: 16px !important;
  background: var(--surface) !important; color: var(--ink) !important;
  font-family: var(--font-mix) !important; font-size: 1rem !important; font-weight: 700 !important;
  line-height: 1.85 !important; text-align: center !important;
  white-space: pre-line !important; overflow-wrap: anywhere; unicode-bidi: plaintext;
  box-shadow: var(--shadow-1) !important; cursor: pointer;
  transition: border-color .15s ease, background-color .15s ease, box-shadow .15s ease, transform .1s ease-out !important;
  -webkit-tap-highlight-color: transparent;
}
.choice-grid button::first-line { font-family: var(--font-urdu); font-size: 1.3em; font-weight: 600; }
.choice-grid button:hover { border-color: var(--accent-ring) !important; box-shadow: var(--shadow-2) !important; }
.choice-grid button:active { transform: scale(.96); background: var(--surface-tint) !important; border-color: var(--accent) !important; }

/* Buttons */
.gradio-container button { -webkit-tap-highlight-color: transparent; }
.primary-action button, .gradio-container button.primary, .gradio-container button.btn-next {
  min-height: 54px !important; padding: 10px 22px !important; border: 0 !important; border-radius: 14px !important;
  background: var(--accent) !important; color: #fff !important; font-weight: 700 !important; font-size: 1.04rem !important;
  box-shadow: 0 1px 2px rgba(11,107,102,.3), 0 4px 12px rgba(11,107,102,.18) !important;
  transition: background-color .15s ease, transform .1s ease-out !important;
}
.primary-action button:hover, .gradio-container button.primary:hover, .gradio-container button.btn-next:hover { background: var(--accent-pressed) !important; }
.primary-action button:active, .gradio-container button.primary:active, .gradio-container button.btn-next:active,
.gradio-container button.btn-quiet:active, .gradio-container button.stop:active { transform: scale(.96); }
.gradio-container button.btn-quiet {
  min-height: 52px !important; padding: 10px 20px !important; border-radius: 14px !important;
  background: transparent !important; color: var(--muted) !important; font-weight: 700 !important;
  border: 1.5px solid var(--line) !important; box-shadow: none !important;
  transition: background-color .15s ease, border-color .15s ease, color .15s ease, transform .1s ease-out !important;
}
.gradio-container button.btn-quiet:hover { background: var(--surface) !important; color: var(--ink) !important; border-color: #b9c6c3 !important; }
.gradio-container button.stop {
  min-height: 48px !important; border-radius: 12px !important; width: 100%;
  background: transparent !important; color: var(--danger) !important; font-weight: 700 !important;
  border: 1.5px solid var(--danger-line) !important; box-shadow: none !important;
  transition: background-color .15s ease, transform .1s ease-out !important;
}
.gradio-container button.stop:hover { background: var(--danger-tint) !important; }

/* Task action row: secondary action at natural width, primary action fills the rest */
.task-actions { justify-content: flex-end !important; gap: 12px !important; align-items: stretch !important; }
.task-actions > .column:not(:has(button:not(.hidden))) { display: none !important; }
.task-actions > button.btn-quiet { flex: 0 0 auto !important; flex-grow: 0 !important; width: auto !important; }

/* Confirmation summary */
.confirm-box textarea {
  background: var(--surface-tint) !important; border: 0 !important; border-radius: 12px !important;
  font-size: 1.02rem !important; line-height: 2 !important; color: var(--ink) !important;
  padding: 12px 16px !important; resize: none !important; unicode-bidi: plaintext;
}
.confirm-box { background: var(--surface) !important; border-radius: var(--radius-card) !important; box-shadow: var(--shadow-2) !important; padding: 14px 18px 16px !important; border: 0 !important; }

/* Form controls */
.gradio-container label > span, .gradio-container [data-testid="block-info"] {
  color: #33434a !important; font-weight: 700 !important; font-size: .88rem !important;
  background: transparent !important; padding: 0 !important; box-shadow: none !important;
}
.gradio-container input, .gradio-container textarea, .gradio-container [role="listbox"], .gradio-container select {
  border: 1.5px solid var(--line) !important; border-radius: var(--radius-control) !important;
  background: #fff !important; color: var(--ink) !important; box-shadow: none !important;
  font: inherit !important; min-height: 48px;
  transition: border-color .15s ease, box-shadow .15s ease !important;
}
.gradio-container input:focus, .gradio-container textarea:focus {
  border-color: var(--accent) !important; box-shadow: 0 0 0 4px rgba(11,107,102,.14) !important;
}
.gradio-container textarea { line-height: 1.75 !important; }
/* Dropdowns: the outer wrapper is the field; the inner input stays borderless */
.gradio-container .wrap:has(> .wrap-inner) {
  border: 1.5px solid var(--line) !important; border-radius: var(--radius-control) !important;
  background: #fff !important; box-shadow: none !important; min-height: 48px;
  transition: border-color .15s ease, box-shadow .15s ease !important;
}
.gradio-container .wrap:has(> .wrap-inner):focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 4px rgba(11,107,102,.14) !important; }
.gradio-container .wrap-inner input { border: 0 !important; min-height: 0 !important; background: transparent !important; box-shadow: none !important; }
.gradio-container .wrap-inner input:focus { box-shadow: none !important; }
.gradio-container input::placeholder, .gradio-container textarea::placeholder { color: #7d898e !important; }
.gradio-container input[type="number"] { font-variant-numeric: tabular-nums; }
.gradio-container input[type="checkbox"] { min-height: 0 !important; width: 24px !important; height: 24px !important; border-radius: 7px !important; accent-color: var(--accent); }
.consent-row { background: var(--surface-tint) !important; border-radius: 14px !important; padding: 12px 16px !important; }
.consent-row label { gap: 12px !important; align-items: center !important; font-weight: 700 !important; color: var(--ink) !important; min-height: 32px; }

/* Sidebar */
.side-heading h3 { font-size: .98rem !important; font-weight: 700 !important; margin: 0 !important; line-height: 2 !important; }
.study-state textarea, .study-history textarea {
  border: 0 !important; border-radius: 12px !important; background: var(--readout) !important;
  color: #22323a !important; font-family: var(--font-mix) !important; font-size: .92rem !important;
  line-height: 1.95 !important; unicode-bidi: plaintext; resize: none !important;
  font-variant-numeric: tabular-nums; padding: 10px 14px !important;
}
.study-state textarea { min-height: 200px !important; }
.study-history textarea { min-height: 140px !important; font-size: .85rem !important; color: var(--muted) !important; }
/* While the Confirm button is on screen, the home panel shows a preview: mark it amber (the label text also says so). */
.gradio-container:has(button.confirm-btn:not(.hidden)) .study-state textarea {
  background: var(--preview) !important; box-shadow: inset 0 0 0 1.5px var(--preview-line) !important;
}
.gradio-container:has(button.confirm-btn:not(.hidden)) .study-state [data-testid="block-info"] { color: var(--preview-ink) !important; }
.study-card .block.status-note { background: var(--surface-tint) !important; border-radius: 12px !important; padding: 10px 12px 10px 30px !important; position: relative; margin-top: 4px; }
.study-card .block.status-note::before { content: ""; position: absolute; left: 13px; top: 19px; width: 8px; height: 8px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 0 3px rgba(11,107,102,.18); }
.status-note p { color: #1f4a44 !important; font-size: .86rem !important; line-height: 1.6 !important; margin: 0 !important; }

/* Questionnaire */
.gradio-container .accordion, .survey-panel {
  border: 0 !important; border-radius: var(--radius-card) !important; background: #fff !important;
  box-shadow: var(--shadow-2) !important; overflow: hidden;
}
.gradio-container .label-wrap { margin-bottom: 6px !important; font-weight: 700 !important; font-size: 1.04rem !important; }
.survey-section { background: #f6f9f8 !important; border-radius: 14px !important; padding: 12px 14px !important; gap: 10px !important; }
.survey-section h4 { font-size: .92rem !important; margin: 0 !important; }
.survey-section input { font-variant-numeric: tabular-nums; }
.survey-section .row, .survey-section .row > .form { flex-wrap: nowrap !important; }
.survey-section .block { min-width: 0 !important; background: transparent !important; border: 0 !important; box-shadow: none !important; padding: 2px 0 !important; }
.survey-panel .label-wrap span { font-size: 1.04rem !important; font-weight: 700 !important; color: var(--ink) !important; }
.interview-grid:not(:has(> .form)), .interview-grid > .form {
  display: grid !important; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px !important;
  border: 0 !important; background: transparent !important; box-shadow: none !important;
}

/* Keyboard focus: orange, distinct from the teal selection colour */
.gradio-container button:focus-visible, .gradio-container textarea:focus-visible,
.gradio-container input:focus-visible, .gradio-container [role="listbox"]:focus-visible {
  outline: 3px solid var(--focus) !important; outline-offset: 3px !important;
}

/* Tablet landscape (about 1024-1180px) */
@media (max-width: 1180px) {
  .gradio-container { padding: 14px 18px 20px !important; }
  .choice-grid button:not(.hidden) { min-height: 96px !important; }
}
@media (max-width: 900px) {
  .study-card, .task-card { padding: 16px !important; }
  .side-col { position: static; }
  .interview-grid:not(:has(> .form)), .interview-grid > .form { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .gradio-container { padding: 12px !important; }
  .choice-grid > .row { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 9px !important; }
  .choice-grid button:not(.hidden) { min-height: 88px !important; padding: 10px !important; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; animation-duration: .01ms !important; }
  .choice-grid button:active, .gradio-container button:active { transform: none !important; }
}
@media (prefers-contrast: more) {
  .study-card, .task-card, .confirm-box, .gradio-container .accordion { box-shadow: 0 0 0 1.5px var(--ink) !important; }
  .choice-grid button:not(.hidden) { border-color: var(--ink) !important; }
}
"""


def _initial_flow():
    return {
        "stage": "welcome",
        "session": None,
        "task_index": 0,
        "task_started_epoch": None,
        "options": [],
        "selected_verb": None,
        "selected_option": None,
        "history": [],
    }


def _history_text(history):
    if not history:
        return "No selections yet."
    return "\n".join(f"{index}. {entry}" for index, entry in enumerate(history, start=1))


def _button_updates(options, visible):
    updates = []
    for index in range(9):
        if visible and index < len(options):
            option = options[index]
            updates.append(gr.update(value=f"{option['urdu']}\n{option['english']}", visible=True))
        else:
            updates.append(gr.update(value="", visible=False))
    return updates


def _task_prompt(flow):
    index = flow["task_index"]
    task = TASKS[index]
    return (
        f"### Task {index + 1} of {len(TASKS)} / کام {index + 1} از {len(TASKS)}\n\n"
        f"**اردو:** {task['urdu']}\n\n**English:** {task['english']}"
    )


def _render(flow, notice=""):
    stage = flow["stage"]
    session_active = flow.get("session") is not None
    task_active = session_active and stage in {"verbs", "suggestions", "confirm"}
    preview = None
    if stage == "confirm" and session_active:
        preview = preview_state(TASKS[flow["task_index"]]["command"])
    heading = {
        "verbs": "### Choose an action / عمل منتخب کریں",
        "suggestions": "### Choose a suggestion / تجویز منتخب کریں",
        "confirm": "### Confirm the simulated command / فرضی حکم کی تصدیق کریں",
    }.get(stage, "")
    button_options = flow["options"] if stage in {"verbs", "suggestions"} else []
    if not notice and session_active:
        notice = f"Session active — participant code {flow['session']['participant_id']}. Progress is saved locally."
    return [
        gr.update(visible=not session_active),
        gr.update(value=_task_prompt(flow) if task_active else "", visible=task_active),
        gr.update(value=heading, visible=bool(heading)),
        *_button_updates(button_options, stage in {"verbs", "suggestions"}),
        gr.update(value=flow.get("confirmation", ""), visible=stage in {"confirm", "task_done"}),
        gr.update(visible=stage == "confirm"),
        gr.update(visible=task_active),
        gr.update(visible=stage == "task_done"),
        gr.update(visible=stage == "survey"),
        gr.update(visible=session_active),
        gr.update(
            value=get_state_display(preview) if preview is not None else get_state_display(),
            label=("Preview — applies after confirmation / پیش منظر — تصدیق کے بعد لاگو ہوگا"
                   if preview is not None else "Current simulated home / موجودہ فرضی گھر"),
        ),
        gr.update(value=_history_text(flow.get("history", []))),
        gr.update(value=notice),
    ]


def _append_history(flow, entry):
    flow.setdefault("history", []).append(entry)


def _start_task(flow, task_index):
    task = TASKS[task_index]
    flow["task_index"] = task_index
    flow["selected_verb"] = None
    flow["selected_option"] = None
    if task_index == 0 and not flow.get("action_verbs"):
        generated = llm_client.get_action_verbs(history=flow.get("history", []), home_env=get_state())
        normalized = []
        for index, urdu in enumerate(generated[:8]):
            normalized.append({
                "urdu": urdu,
                "english": _english_action(urdu, ACTION_VERBS[index % len(ACTION_VERBS)]["english"]),
            })
        flow["action_verbs"] = normalized or deepcopy(ACTION_VERBS)
        backend = llm_client.get_backend_status()
        session_store.record_event(flow["session"], "action_verbs_generated", {
            "options": flow["action_verbs"],
            "backend": {key: value for key, value in backend.items() if key != "raw_response_preview"},
            "latency_seconds": llm_client.get_last_latency_seconds(),
        })
    flow["options"] = deepcopy(flow.get("action_verbs") or ACTION_VERBS)
    flow["stage"] = "verbs"
    # Begin task timing only after the screen's first set of choices is ready.
    started_at = session_store.utc_now()
    flow["task_started_epoch"] = time.time()
    task_session = flow["session"]
    session_store.update_task(
        task_session,
        task_index,
        {"status": "in_progress", "task_started_at": started_at},
        "task_started",
        {"task_id": task["id"], "task_order": task_index + 1},
    )
    _append_history(flow, f"Started task {task_index + 1}: {task['english']} / {task['urdu']}")


def _english_action(urdu, default):
    """Map common generated Urdu action phrases to concise English labels."""
    text = str(urdu).strip()
    if "یاد دہانی" in text:
        return "Set a reminder"
    if "مدد" in text:
        return "Get help"
    if any(token in text for token in ("بند", "آف")):
        return "Turn off"
    if any(token in text for token in ("آن", "روشن")):
        return "Turn on"
    if any(token in text for token in ("چیک", "معلوم", "دیکھ")):
        return "Check"
    if "بدل" in text or "تبدیل" in text:
        return "Change"
    if "دکھ" in text or "بتائیں" in text:
        return "Show"
    if "ٹائمر" in text or "سیٹ" in text or "لگائیں" in text:
        return "Set"
    return default


def _start_session(
    participant_id, age, gender, hearing_status, hearing_device, language_background,
    prior_ipa_experience, voice_assistant_frequency, accessibility_needs, consent_confirmed,
):
    if not str(participant_id or "").strip():
        raise gr.Error("Enter a participant code (for example P01). Do not enter the participant's name.")
    if not consent_confirmed:
        raise gr.Error("Confirm that the participant completed the consent process before starting.")
    demographics = {
        "age": age if age is not None else "",
        "gender": gender or "",
        "hearing_status": hearing_status or "",
        "hearing_device": hearing_device or "",
        "language_background": language_background or "",
        "prior_ipa_experience": prior_ipa_experience or "",
        "voice_assistant_frequency": voice_assistant_frequency or "",
        "accessibility_needs": accessibility_needs or "",
        "consent_confirmed": bool(consent_confirmed),
    }
    try:
        session = session_store.create_session(participant_id, demographics, TASKS)
    except Exception as exc:
        raise gr.Error(f"Could not start and save this session: {exc}") from exc
    reset_state()
    flow = _initial_flow()
    flow["session"] = session
    _start_task(flow, 0)
    return [flow, *_render(flow, f"Session {session['session_id']} started. Task and interaction data save automatically under data/raw/.")]


def _choose_option(index, flow):
    if flow.get("session") is None or index >= len(flow.get("options", [])):
        return [flow, *_render(flow)]
    option = flow["options"][index]
    task_index = flow["task_index"]
    task = TASKS[task_index]
    session = flow["session"]

    if flow["stage"] == "verbs":
        flow["selected_verb"] = option
        _append_history(flow, f"Action selected: {option['english']} / {option['urdu']}")
        session_store.record_event(session, "action_selected", {
            "task_id": task["id"], "english": option["english"], "urdu": option["urdu"],
        })
        prompt_history = list(flow["history"]) + [f"Most recent assigned user request: {task['english']} / {task['urdu']}"]
        suggestions = llm_client.get_task_options(option["english"], prompt_history, home_env=get_state())
        backend = llm_client.get_backend_status()
        latency = llm_client.get_last_latency_seconds()
        session_store.update_task(
            session,
            task_index,
            {
                "action_verb_english": option["english"],
                "llm_model": os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
                "llm_latency_seconds": round(latency, 3) if latency is not None else None,
                "llm_used_fallback": bool(backend["used_fallback"] or backend["used_local_list_fallback"]),
                "llm_error": backend.get("error") or "",
            },
            "suggestions_generated",
            {
                "task_id": task["id"],
                "suggestions": suggestions,
                "backend": {key: value for key, value in backend.items() if key != "raw_response_preview"},
                "latency_seconds": latency,
            },
        )
        if backend["used_fallback"] or backend["used_local_list_fallback"]:
            suggestions = [task["urdu"]]
        flow["options"] = [
            {"urdu": text, "english": task["english"], "command": task["command"]}
            for text in suggestions
        ]
        flow["stage"] = "suggestions"
        return [flow, *_render(flow, "Suggestions are ready. They are tied to the assigned study task.")]

    if flow["stage"] == "suggestions":
        flow["selected_option"] = option
        flow["stage"] = "confirm"
        flow["confirmation"] = (
            f"Selected suggestion / منتخب تجویز: {option['urdu']}\n"
            f"Assigned task / مقررہ کام: {task['english']}\n"
            f"Simulated command / فرضی حکم: {task['command']}"
        )
        _append_history(flow, f"Suggestion selected: {option['urdu']}")
        session_store.record_event(session, "suggestion_selected", {
            "task_id": task["id"], "suggestion_urdu": option["urdu"], "command": task["command"],
        })
        return [flow, *_render(flow)]

    return [flow, *_render(flow)]


def _confirm_command(flow):
    if flow.get("session") is None or flow["stage"] != "confirm":
        return [flow, *_render(flow)]
    task_index = flow["task_index"]
    task = TASKS[task_index]
    session = flow["session"]
    command = task["command"]
    state = update_state(command)
    latency = max(0.0, time.time() - (flow.get("task_started_epoch") or time.time()))
    ended_at = session_store.utc_now()
    session_store.update_task(
        session,
        task_index,
        {
            "status": "complete",
            "task_ended_at": ended_at,
            "latency_seconds": round(latency, 3),
            "selected_option_urdu": (flow.get("selected_option") or {}).get("urdu", ""),
            "command": command,
        },
        "task_completed",
        {"task_id": task["id"], "command": command, "latency_seconds": round(latency, 3), "state_after": state},
    )
    _append_history(flow, f"Confirmed task: {task['english']} ({latency:.2f}s)")
    flow["stage"] = "task_done"
    flow["options"] = []
    flow["confirmation"] = "Task completed in the simulated home. / فرضی گھر میں کام مکمل ہو گیا۔"
    return [flow, *_render(flow)]


def _mark_task_incomplete(flow):
    if flow.get("session") is None or flow["stage"] not in {"verbs", "suggestions", "confirm"}:
        return [flow, *_render(flow)]
    task_index = flow["task_index"]
    task = TASKS[task_index]
    latency = max(0.0, time.time() - (flow.get("task_started_epoch") or time.time()))
    session_store.update_task(
        flow["session"], task_index,
        {"status": "failed", "task_ended_at": session_store.utc_now(), "latency_seconds": round(latency, 3)},
        "task_not_completed", {"task_id": task["id"], "latency_seconds": round(latency, 3)},
    )
    _append_history(flow, f"Task not completed: {task['english']} ({latency:.2f}s)")
    flow["stage"] = "task_done"
    flow["options"] = []
    flow["confirmation"] = "Task marked not completed. / کام نامکمل درج کیا گیا۔"
    return [flow, *_render(flow)]


def _next_task(flow):
    if flow.get("session") is None or flow["stage"] != "task_done":
        return [flow, *_render(flow)]
    next_index = flow["task_index"] + 1
    if next_index >= len(TASKS):
        flow["stage"] = "survey"
        flow["options"] = []
        session_store.record_event(flow["session"], "questionnaire_started", {"completed_tasks": next_index})
        return [flow, *_render(flow, "All five tasks are logged. Complete the SUS, adjective rating, NPS, and interview notes below.")]
    _start_task(flow, next_index)
    return [flow, *_render(flow, f"Task {next_index + 1} of {len(TASKS)} is ready.")]


def _survey_values(sus_values, adjective_score, nps_score, interview_values, notes):
    return [*sus_values, adjective_score, nps_score], interview_values, notes


def _autosave_survey(flow, *values):
    if flow.get("session") is None:
        return [flow, gr.update(value="No active session to save.")]
    sus_values = values[:10]
    adjective_score, nps_score = values[10:12]
    interview_values = values[12:17]
    notes = values[17] or ""
    responses, interview, notes = _survey_values(sus_values, adjective_score, nps_score, interview_values, notes)
    session_store.update_questionnaire(flow["session"], responses, interview, notes)
    return [flow, gr.update(value="Questionnaire and interview entries saved locally.")]


def _finish_session(flow, *values):
    if flow.get("session") is None:
        raise gr.Error("There is no active session to finish.")
    _autosave_survey(flow, *values)
    session = flow["session"]
    session_store.end_session(session, "complete")
    session_id = session["session_id"]
    reset_state()
    cleared = _initial_flow()
    notice = f"Session saved ({session_id}). Summary CSV, task CSV, and full JSON are in data/raw/."
    return [cleared, *_render(cleared, notice), *_clear_form_updates()]


def _reset_session(flow):
    session = flow.get("session")
    notice = "Home and participant session reset. Any started session was saved as incomplete."
    if session is not None:
        if flow.get("stage") in {"verbs", "suggestions", "confirm"}:
            index = flow["task_index"]
            task = session["tasks"][index]
            if task.get("status") == "in_progress":
                latency = max(0.0, time.time() - (flow.get("task_started_epoch") or time.time()))
                session_store.update_task(
                    session, index,
                    {"status": "incomplete", "task_ended_at": session_store.utc_now(), "latency_seconds": round(latency, 3)},
                    "session_reset_during_task", {"task_id": task["task_id"], "latency_seconds": round(latency, 3)},
                )
        session_store.end_session(session, "reset")
        notice = f"Session {session['session_id']} saved as incomplete; home reset for the next participant."
    reset_state()
    cleared = _initial_flow()
    return [cleared, *_render(cleared, notice), *_clear_form_updates()]


def _clear_form_updates():
    return [
        gr.update(value=""), gr.update(value=None), gr.update(value=None), gr.update(value=None),
        gr.update(value=None), gr.update(value=""), gr.update(value=None), gr.update(value=""),
        gr.update(value=""), gr.update(value=False),
        *[gr.update(value=None) for _ in range(12)],
        *[gr.update(value="") for _ in range(6)],
    ]


def build_app():
    with gr.Blocks(
        title="Urdu Smart Home Assistant",
        theme=gr.themes.Soft(
            primary_hue="teal",
            neutral_hue="stone",
            font=[
                gr.themes.GoogleFont("Atkinson Hyperlegible", weights=(400, 700)),
                gr.themes.GoogleFont("Noto Nastaliq Urdu", weights=(400, 600, 700)),
                gr.themes.Font("Segoe UI"),
                gr.themes.Font("sans-serif"),
            ],
        ),
        css=APP_CSS,
    ) as demo:
        gr.Markdown(
            "# Urdu Smart Home Assistant | اردو اسمارٹ ہوم اسسٹنٹ\n"
            "A touch-based, bilingual smart-home simulation for the usability study.",
            elem_classes=["app-header"],
        )
        flow = gr.State(_initial_flow())

        with gr.Row(elem_classes=["app-layout"]):
            with gr.Column(scale=2, min_width=520, elem_classes=["main-col"]):
                with gr.Group(elem_classes=["study-card"]) as welcome_panel:
                    gr.Markdown(
                        "### Welcome / خوش آمدید\n"
                        "The app will present the five study tasks in order. The researcher should give the participant the same task shown on screen. "
                        "No participant name is collected; use a study code.",
                        elem_classes=["welcome-head"],
                    )
                    with gr.Row():
                        participant_id = gr.Textbox(label="Participant code / شرکاء کا کوڈ", placeholder="P01")
                        age = gr.Number(label="Age / عمر", precision=0, minimum=18, maximum=120)
                    with gr.Row():
                        gender = gr.Dropdown(label="Gender / جنس", choices=["Woman", "Man", "Non-binary", "Another identity", "Prefer not to say"], value=None)
                        hearing_status = gr.Dropdown(label="Hearing status / سماعت", choices=["Deaf", "Hard of Hearing (HoH)", "Deaf-Blind", "Another description", "Prefer not to say"], value=None)
                    with gr.Row():
                        hearing_device = gr.Dropdown(label="Hearing device / سماعت کا آلہ", choices=["None", "Hearing aid", "Cochlear implant", "Other", "Prefer not to say"], value=None)
                        prior_ipa_experience = gr.Dropdown(label="Prior voice-assistant experience / سابقہ تجربہ", choices=["Yes", "No", "Not sure"], value=None)
                    with gr.Row():
                        language_background = gr.Textbox(label="Preferred languages / پسندیدہ زبانیں", placeholder="Urdu, English, PSL, other")
                        voice_assistant_frequency = gr.Textbox(label="Frequency / استعمال کی تعداد", placeholder="Daily, weekly, rarely, never")
                    accessibility_needs = gr.Textbox(label="Accessibility needs / رسائی کی ضروریات", lines=2)
                    consent_confirmed = gr.Checkbox(label="Consent was completed before starting / سیشن سے پہلے رضامندی لی گئی ہے", value=False, elem_classes=["consent-row"])
                    with gr.Row(elem_classes=["primary-action"]):
                        start_button = gr.Button("Start session / سیشن شروع کریں", variant="primary")

                task_prompt = gr.Markdown(visible=False, elem_classes=["task-card"])
                stage_heading = gr.Markdown(visible=False, elem_classes=["stage-heading"])
                choice_buttons = []
                with gr.Column(elem_classes=["choice-grid"]):
                    for _ in range(3):
                        with gr.Row():
                            for _ in range(3):
                                choice_buttons.append(gr.Button(visible=False))

                confirmation_box = gr.Textbox(label="Confirmation / تصدیق", lines=4, interactive=False, visible=False, elem_classes=["confirm-box"])
                with gr.Row(elem_classes=["task-actions"]):
                    with gr.Column(elem_classes=["primary-action"]):
                        confirm_button = gr.Button("Confirm / تصدیق کریں", variant="primary", visible=False, elem_classes=["confirm-btn"])
                    fail_button = gr.Button("Could not complete / مکمل نہیں ہوا", visible=False, elem_classes=["btn-quiet"])
                    next_task_button = gr.Button("Next task / اگلا کام", visible=False, elem_classes=["btn-next"])

                with gr.Accordion("Questionnaire and interview / سوالنامہ اور انٹرویو", open=True, visible=False, elem_classes=["survey-panel"]) as questionnaire_panel:
                    gr.Markdown("Complete these entries after the participant finishes all five tasks. Responses save automatically as they are entered.")
                    sus_inputs = []
                    with gr.Column(elem_classes=["survey-section"]):
                        gr.Markdown("#### SUS — choose 1 (strongly disagree) to 5 (strongly agree) for each item")
                        for start in (1, 6):
                            with gr.Row():
                                for item in range(start, start + 5):
                                    sus_inputs.append(gr.Dropdown(label=f"SUS {item}", choices=[1, 2, 3, 4, 5], value=None))
                    with gr.Row():
                        adjective_input = gr.Dropdown(label="Overall adjective rating (1–7)", choices=list(range(1, 8)), value=None)
                        nps_input = gr.Dropdown(label="NPS likelihood (0–10)", choices=list(range(0, 11)), value=None)
                    interview_inputs = []
                    interview_labels = [
                        "Easiest / hardest part", "Urdu wording and translations", "AI privacy concerns",
                        "Interest in hands-free voice/sign options", "Suggested improvement",
                    ]
                    with gr.Column(elem_classes=["interview-grid"]):
                        for label in interview_labels:
                            interview_inputs.append(gr.Textbox(label=f"Interview notes — {label}", lines=2))
                    session_notes = gr.Textbox(label="Researcher session notes / محقق کے نوٹس", lines=3)
                    with gr.Row(elem_classes=["primary-action"]):
                        finish_button = gr.Button("Save and finish session / محفوظ کرکے ختم کریں", variant="primary")

            with gr.Column(scale=1, min_width=300, elem_classes=["side-col"]):
                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### Home status / گھر کی حالت", elem_classes=["side-heading"])
                    state_display = gr.Textbox(value=get_state_display(), label="Simulated state / فرضی حالت", lines=9, interactive=False, elem_classes=["study-state"])
                    gr.Markdown("### Selections / انتخاب", elem_classes=["side-heading"])
                    history_display = gr.Textbox(value="No selections yet.", label="Session history", lines=9, interactive=False, elem_classes=["study-history"])
                    data_status = gr.Markdown("Session data has not been started.", elem_classes=["status-note"])
                    reset_button = gr.Button("Reset session and home / سیشن اور گھر ری سیٹ کریں", variant="stop", visible=False)

        view_components = [
            welcome_panel, task_prompt, stage_heading, *choice_buttons, confirmation_box,
            confirm_button, fail_button, next_task_button, questionnaire_panel,
            reset_button, state_display, history_display, data_status,
        ]
        metadata_inputs = [
            participant_id, age, gender, hearing_status, hearing_device, language_background,
            prior_ipa_experience, voice_assistant_frequency, accessibility_needs, consent_confirmed,
        ]
        survey_inputs = [
            *sus_inputs, adjective_input, nps_input, *interview_inputs, session_notes,
        ]
        blank_outputs = [participant_id, age, gender, hearing_status, hearing_device,
                         language_background, prior_ipa_experience, voice_assistant_frequency,
                         accessibility_needs, consent_confirmed, *sus_inputs, adjective_input,
                         nps_input, *interview_inputs, session_notes]

        start_button.click(
            _start_session,
            inputs=metadata_inputs,
            outputs=[flow, *view_components],
        )
        for index, button in enumerate(choice_buttons):
            button.click(
                lambda current_flow, selected=index: _choose_option(selected, current_flow),
                inputs=[flow], outputs=[flow, *view_components],
            )
        confirm_button.click(_confirm_command, inputs=[flow], outputs=[flow, *view_components])
        fail_button.click(_mark_task_incomplete, inputs=[flow], outputs=[flow, *view_components])
        next_task_button.click(_next_task, inputs=[flow], outputs=[flow, *view_components])
        reset_button.click(
            _reset_session, inputs=[flow], outputs=[flow, *view_components, *blank_outputs]
        )
        for component in survey_inputs:
            component.change(
                _autosave_survey, inputs=[flow, *survey_inputs], outputs=[flow, data_status]
            )
        finish_button.click(
            _finish_session, inputs=[flow, *survey_inputs],
            outputs=[flow, *view_components, *blank_outputs],
        )

    return demo


demo = build_app()


if __name__ == "__main__":
    demo.launch()
