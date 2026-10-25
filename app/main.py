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
:root { --ink:#183330; --teal:#0d5d56; --teal-dark:#08453f; --paper:#f4f3ec; --border:#c8d4ce; }
body,.gradio-container { background:var(--paper)!important; color:var(--ink)!important; font-family:"Noto Naskh Arabic","Noto Nastaliq Urdu","Segoe UI",Tahoma,sans-serif!important; font-size:18px!important; line-height:1.65!important; }
.gradio-container { max-width:1240px!important; margin:0 auto!important; padding:22px!important; }
.gradio-container h1,.gradio-container h2,.gradio-container h3 { color:var(--teal-dark)!important; line-height:1.4!important; }
.study-card { border:1px solid var(--border)!important; border-radius:18px!important; background:#fff!important; padding:20px!important; box-shadow:0 4px 16px rgba(24,51,48,.07)!important; }
.choice-grid>.row { display:grid!important; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px!important; }
.choice-grid button { width:100%!important; min-width:0!important; height:138px!important; min-height:138px!important; padding:12px!important; border:2px solid #aebfb8!important; border-bottom:6px solid #879e95!important; border-radius:14px!important; background:linear-gradient(180deg,#fff 0%,#f2f6f3 100%)!important; color:var(--ink)!important; font-size:1rem!important; font-weight:650!important; line-height:1.5!important; white-space:pre-line!important; overflow-wrap:anywhere; unicode-bidi:plaintext; box-shadow:0 3px 7px rgba(24,51,48,.13)!important; }
.choice-grid button:hover { border-color:var(--teal)!important; background:#e7f3ee!important; }
.primary-action button { min-height:58px!important; border-radius:12px!important; background:var(--teal)!important; color:#fff!important; font-weight:700!important; }
.primary-action button:hover { background:var(--teal-dark)!important; }
.study-state textarea,.study-history textarea { min-height:200px!important; border:2px solid var(--border)!important; border-radius:12px!important; background:#fbfcfa!important; color:var(--ink)!important; font-family:inherit!important; line-height:1.7!important; unicode-bidi:plaintext; }
.gradio-container button:focus-visible,.gradio-container textarea:focus-visible,.gradio-container input:focus-visible { outline:4px solid #b65a37!important; outline-offset:3px!important; }
@media(max-width:720px){.gradio-container{padding:12px!important}.choice-grid>.row{grid-template-columns:repeat(2,minmax(0,1fr))}.choice-grid button{height:128px!important;min-height:128px!important;padding:8px!important;font-size:.94rem!important}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition-duration:.01ms!important}}
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
        theme=gr.themes.Soft(primary_hue="teal", neutral_hue="stone"),
        css=APP_CSS,
    ) as demo:
        gr.Markdown(
            "# Urdu Smart Home Assistant | اردو اسمارٹ ہوم اسسٹنٹ\n"
            "A touch-based, bilingual smart-home simulation for the usability study."
        )
        flow = gr.State(_initial_flow())

        with gr.Row():
            with gr.Column(scale=2):
                with gr.Group(elem_classes=["study-card"]) as welcome_panel:
                    gr.Markdown(
                        "### Welcome / خوش آمدید\n"
                        "The app will present the five study tasks in order. The researcher should give the participant the same task shown on screen. "
                        "No participant name is collected; use a study code."
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
                    consent_confirmed = gr.Checkbox(label="Consent was completed before starting / سیشن سے پہلے رضامندی لی گئی ہے", value=False)
                    with gr.Row(elem_classes=["primary-action"]):
                        start_button = gr.Button("Start session / سیشن شروع کریں", variant="primary")

                task_prompt = gr.Markdown(visible=False)
                stage_heading = gr.Markdown(visible=False)
                choice_buttons = []
                with gr.Column(elem_classes=["choice-grid"]):
                    for _ in range(3):
                        with gr.Row():
                            for _ in range(3):
                                choice_buttons.append(gr.Button(visible=False))

                confirmation_box = gr.Textbox(label="Confirmation / تصدیق", lines=4, interactive=False, visible=False)
                with gr.Row():
                    with gr.Column(elem_classes=["primary-action"]):
                        confirm_button = gr.Button("Confirm / تصدیق کریں", variant="primary", visible=False)
                    fail_button = gr.Button("Could not complete / مکمل نہیں ہوا", visible=False)
                    next_task_button = gr.Button("Next task / اگلا کام", visible=False)

                with gr.Accordion("Questionnaire and interview / سوالنامہ اور انٹرویو", open=True, visible=False) as questionnaire_panel:
                    gr.Markdown("Complete these entries after the participant finishes all five tasks. Responses save automatically as they are entered.")
                    gr.Markdown("#### SUS — choose 1 (strongly disagree) to 5 (strongly agree) for each item")
                    sus_inputs = []
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
                    for label in interview_labels:
                        interview_inputs.append(gr.Textbox(label=f"Interview notes — {label}", lines=2))
                    session_notes = gr.Textbox(label="Researcher session notes / محقق کے نوٹس", lines=3)
                    with gr.Row(elem_classes=["primary-action"]):
                        finish_button = gr.Button("Save and finish session / محفوظ کرکے ختم کریں", variant="primary")

            with gr.Column(scale=1):
                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### Home status / گھر کی حالت")
                    state_display = gr.Textbox(value=get_state_display(), label="Simulated state / فرضی حالت", lines=9, interactive=False, elem_classes=["study-state"])
                    gr.Markdown("### Selections / انتخاب")
                    history_display = gr.Textbox(value="No selections yet.", label="Session history", lines=9, interactive=False, elem_classes=["study-history"])
                    data_status = gr.Markdown("Session data has not been started.")
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
