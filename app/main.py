"""Gradio touch interface for the Urdu smart-home study."""

from copy import deepcopy

import gradio as gr

try:  # Supports both `python app/main.py` and package imports.
    from .smart_home import get_state_display, preview_state, update_state
except ImportError:  # pragma: no cover - script execution path
    from smart_home import get_state_display, preview_state, update_state


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

TASK_OPTIONS = [
    {
        "urdu": "لاہور کا آج کا موسم دیکھیں",
        "english": "Check today's weather in Lahore",
        "command": "check weather in Lahore",
    },
    {
        "urdu": "چائے کے لیے ۵ منٹ کا ٹائمر لگائیں",
        "english": "Set a 5-minute tea timer",
        "command": "set timer for 5 minutes",
    },
    {
        "urdu": "بتی کا رنگ نیلا کریں",
        "english": "Set the light to blue",
        "command": "set light color to blue",
    },
    {
        "urdu": "بریانی کی ترکیب دکھائیں",
        "english": "Show a biryani recipe",
        "command": "show biryani recipe",
    },
    {
        "urdu": "فجر کے لیے یاد دہانی لگائیں",
        "english": "Set a Fajr reminder",
        "command": "set Fajr reminder",
    },
    {
        "urdu": "آج کا کیلنڈر دکھائیں",
        "english": "Show today's calendar",
        "command": "show calendar",
    },
    {
        "urdu": "بتی جلائیں",
        "english": "Turn on the light",
        "command": "turn on light",
    },
    {
        "urdu": "بتی بند کریں",
        "english": "Turn off the light",
        "command": "turn off light",
    },
]

APP_CSS = """
:root {
    --study-ink: #183330;
    --study-teal: #0d5d56;
    --study-teal-dark: #08453f;
    --study-paper: #f4f3ec;
    --study-surface: #ffffff;
    --study-border: #c8d4ce;
}

body,
.gradio-container {
    background: var(--study-paper) !important;
    color: var(--study-ink) !important;
    font-family: "Noto Naskh Arabic", "Noto Nastaliq Urdu", "Segoe UI", Tahoma, sans-serif !important;
    font-size: 19px !important;
    line-height: 1.65 !important;
}

.gradio-container {
    max-width: 1240px !important;
    margin: 0 auto !important;
    padding: 24px !important;
}

.gradio-container h1 {
    color: var(--study-teal-dark) !important;
    font-size: 2.15rem !important;
    line-height: 1.35 !important;
}

.gradio-container h2,
.gradio-container h3 {
    color: var(--study-teal-dark) !important;
    line-height: 1.5 !important;
}

.gradio-container h3 {
    font-size: 1.4rem !important;
}

.gradio-container p,
.gradio-container li,
.gradio-container label {
    color: var(--study-ink) !important;
}

.welcome-copy ul {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px 24px;
    padding-inline-start: 24px;
}

.welcome-copy li {
    padding: 8px 10px;
    border-radius: 10px;
    background: #eef3ef;
    font-size: 1.08rem;
    line-height: 1.75;
}

.welcome-copy p {
    font-size: 1.08rem;
}

.study-card {
    border: 1px solid var(--study-border) !important;
    border-radius: 18px !important;
    background: var(--study-surface) !important;
    padding: 22px !important;
    box-shadow: 0 4px 16px rgba(24, 51, 48, 0.07) !important;
}

.study-card > .styler,
.study-card > .form,
.study-state.block {
    background: transparent !important;
}

.gradio-container em {
    color: var(--study-muted, #455b57) !important;
}

.choice-grid > .row {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    align-items: stretch !important;
    gap: 14px !important;
}

.choice-grid button {
    width: 100% !important;
    min-width: 0 !important;
    height: 148px !important;
    min-height: 148px !important;
    padding: 12px !important;
    border: 2px solid #aebfb8 !important;
    border-bottom: 6px solid #879e95 !important;
    border-radius: 14px !important;
    background: linear-gradient(180deg, #ffffff 0%, #f2f6f3 100%) !important;
    color: var(--study-ink) !important;
    font-size: 1.03rem !important;
    font-weight: 650 !important;
    line-height: 1.5 !important;
    white-space: pre-line !important;
    overflow-wrap: anywhere;
    unicode-bidi: plaintext;
    box-shadow: 0 3px 7px rgba(24, 51, 48, 0.13) !important;
    transition: background-color 120ms ease, border-color 120ms ease, box-shadow 120ms ease, transform 120ms ease;
}

.choice-grid button:hover {
    border-color: var(--study-teal) !important;
    border-bottom-color: var(--study-teal-dark) !important;
    background: linear-gradient(180deg, #ffffff 0%, #e7f3ee 100%) !important;
    box-shadow: 0 5px 10px rgba(24, 51, 48, 0.18) !important;
    transform: translateY(-2px);
}

.choice-grid button:active {
    border-bottom-width: 2px !important;
    box-shadow: 0 1px 2px rgba(24, 51, 48, 0.16) !important;
    transform: translateY(3px);
}

.gradio-container button:focus-visible,
.gradio-container textarea:focus-visible {
    outline: 4px solid #b65a37 !important;
    outline-offset: 3px !important;
}

.primary-action button {
    min-height: 64px !important;
    border-radius: 12px !important;
    background: var(--study-teal) !important;
    color: white !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
}

.primary-action button:hover {
    background: var(--study-teal-dark) !important;
}

.study-state textarea {
    min-height: 250px !important;
    border: 2px solid var(--study-border) !important;
    border-radius: 12px !important;
    background: #fbfcfa !important;
    color: var(--study-ink) !important;
    font-family: inherit !important;
    font-size: 1rem !important;
    line-height: 1.8 !important;
    opacity: 1 !important;
}

@media (max-width: 760px) {
    .gradio-container {
        padding: 12px !important;
    }

    .welcome-copy ul {
        grid-template-columns: 1fr;
    }

    .choice-grid button {
        height: 132px !important;
        min-height: 132px !important;
        padding: 8px !important;
        font-size: 0.94rem !important;
    }
}

@media (max-width: 520px) {
    .choice-grid > .row {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .choice-grid button {
        height: 140px !important;
        min-height: 140px !important;
        font-size: 0.98rem !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
    }
}
"""


def get_llm_options(verb, history):
    """Return hardcoded bilingual task options as a future LLM replacement seam.

    Replace this fixture with the model call when the study is ready for LLM
    integration. The arguments intentionally match that future interface.
    """
    del verb, history
    return deepcopy(TASK_OPTIONS)


def _button_label(option):
    return f"{option['urdu']}\n{option['english']}"


def _option_button_updates(options):
    return [
        gr.update(value=_button_label(options[index]) if index < len(options) else "", visible=index < len(options))
        for index in range(9)
    ]


def _history_text(history):
    if not history:
        return "_No selections yet._"
    return "\n".join(f"{index}. {entry}" for index, entry in enumerate(history, start=1))


def _start_flow(history):
    options = deepcopy(ACTION_VERBS)
    return (
        "verbs",
        options,
        None,
        None,
        None,
        history,
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
        *_option_button_updates(options),
        gr.update(value="", visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(value="", visible=False),
        gr.update(visible=False),
        gr.update(
            value=get_state_display(),
            label="Current simulated home / موجودہ فرضی گھر",
        ),
        _history_text(history),
    )


def _select_option(index, stage, options, selected_verb, history):
    history = list(history or [])
    if stage == "verbs":
        selected_verb = options[index]
        history.append(f"Action: {selected_verb['urdu']} / {selected_verb['english']}")
        options = get_llm_options(selected_verb["english"], history)
        return (
            "tasks",
            options,
            selected_verb,
            None,
            None,
            history,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            *_option_button_updates(options),
            gr.update(value="", visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(value="", visible=False),
            gr.update(visible=False),
            gr.update(
                value=get_state_display(),
                label="Current simulated home / موجودہ فرضی گھر",
            ),
            _history_text(history),
        )

    if stage == "tasks" and index < len(options):
        selected_task = options[index]
        history.append(f"Task: {selected_task['urdu']} / {selected_task['english']}")
        confirmation = (
            f"**Urdu:** {selected_task['urdu']}\n\n"
            f"**English:** {selected_task['english']}\n\n"
            f"**Command:** `{selected_task['command']}`"
        )
        return (
            "confirm",
            options,
            selected_verb,
            selected_task,
            selected_task["command"],
            history,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            *[gr.update(visible=False) for _ in range(9)],
            gr.update(value=confirmation, visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(value="", visible=False),
            gr.update(visible=False),
            gr.update(
                value=get_state_display(preview_state(selected_task["command"])),
                label="Preview — not applied until confirmed / پیش منظر — تصدیق کے بعد لاگو ہوگا",
            ),
            _history_text(history),
        )

    return (
        stage,
        options,
        selected_verb,
        None,
        None,
        history,
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        *[gr.update() for _ in range(9)],
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(),
        gr.update(
            value=get_state_display(),
            label="Current simulated home / موجودہ فرضی گھر",
        ),
        _history_text(history),
    )


def _apply_command(command):
    update_state(command)
    return (
        "complete",
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        *[gr.update(visible=False) for _ in range(9)],
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(
            value=f"Command applied to the simulated home: `{command}`",
            visible=True,
        ),
        gr.update(visible=True),
        gr.update(
            value=get_state_display(),
            label="Current simulated home / موجودہ فرضی گھر",
        ),
        gr.update(visible=False),
        gr.update(visible=False),
    )


def _continue_flow(history):
    return _start_flow(history)


def build_app():
    """Create and return the Gradio Blocks application."""
    with gr.Blocks(
        title="Urdu Smart Home Assistant",
        theme=gr.themes.Soft(primary_hue="teal", neutral_hue="stone"),
        css=APP_CSS,
    ) as demo:
        gr.Markdown(
            "# Urdu Smart Home Assistant | اردو اسمارٹ ہوم اسسٹنٹ\n"
            "Use the large buttons to choose what you want the simulated home to do. "
            "You can read each choice in Urdu and English."
        )

        stage = gr.State("welcome")
        options_state = gr.State([])
        selected_verb_state = gr.State(None)
        selected_task_state = gr.State(None)
        command_state = gr.State(None)
        history_state = gr.State([])

        with gr.Row():
            with gr.Column(scale=2):
                with gr.Group(elem_classes=["study-card"]):
                    welcome_copy = gr.Markdown(
                        "### Welcome / خوش آمدید\n"
                        "Start by choosing one of these tasks. You will then choose an action and confirm it.\n\n"
                        + "\n".join(
                            f"- {task['urdu']} — {task['english']}"
                            for task in TASK_OPTIONS
                        ),
                        elem_classes=["welcome-copy"],
                    )
                    with gr.Row(elem_classes=["primary-action"]):
                        start_button = gr.Button("Start / شروع کریں", variant="primary")

                    action_heading = gr.Markdown(
                        "### Choose an action / عمل منتخب کریں",
                        visible=False,
                    )
                    task_heading = gr.Markdown(
                        "### Choose a task / کام منتخب کریں",
                        visible=False,
                    )
                    confirmation_heading = gr.Markdown(
                        "### Confirm your command / اپنے حکم کی تصدیق کریں",
                        visible=False,
                    )
                    option_buttons = []
                    with gr.Column(elem_classes=["choice-grid"]):
                        for _ in range(3):
                            with gr.Row():
                                for _ in range(3):
                                    option_buttons.append(gr.Button(visible=False))

                    confirmation_text = gr.Markdown(visible=False)
                    with gr.Row():
                        with gr.Column(elem_classes=["primary-action"]):
                            confirm_button = gr.Button(
                                "Confirm / تصدیق کریں",
                                variant="primary",
                                visible=False,
                            )
                        back_button = gr.Button(
                            "Choose another task / واپس",
                            visible=False,
                        )

                    completion_message = gr.Markdown(visible=False)
                    with gr.Row(elem_classes=["primary-action"]):
                        continue_button = gr.Button(
                            "Start another task / ایک اور کام شروع کریں",
                            visible=False,
                        )

            with gr.Column(scale=1, elem_classes=["study-card"]):
                gr.Markdown("### Home status / گھر کی حالت")
                state_display = gr.Textbox(
                    value=get_state_display(),
                    label="Current simulated home / موجودہ فرضی گھر",
                    lines=10,
                    interactive=False,
                    elem_classes=["study-state"],
                )
                gr.Markdown("### Study selections / مطالعے کے انتخاب")
                history_display = gr.Markdown("_No selections yet._")

        start_outputs = [
            stage,
            options_state,
            selected_verb_state,
            selected_task_state,
            command_state,
            history_state,
            welcome_copy,
            start_button,
            action_heading,
            task_heading,
            confirmation_heading,
            *option_buttons,
            confirmation_text,
            confirm_button,
            back_button,
            completion_message,
            continue_button,
            state_display,
            history_display,
        ]
        start_button.click(_start_flow, inputs=history_state, outputs=start_outputs)

        selection_outputs = [
            stage,
            options_state,
            selected_verb_state,
            selected_task_state,
            command_state,
            history_state,
            welcome_copy,
            start_button,
            action_heading,
            task_heading,
            confirmation_heading,
            *option_buttons,
            confirmation_text,
            confirm_button,
            back_button,
            completion_message,
            continue_button,
            state_display,
            history_display,
        ]
        for index, button in enumerate(option_buttons):
            button.click(
                lambda current_stage, options, verb, history, item_index=index: _select_option(
                    item_index, current_stage, options, verb, history
                ),
                inputs=[stage, options_state, selected_verb_state, history_state],
                outputs=selection_outputs,
            )

        confirm_button.click(
            _apply_command,
            inputs=command_state,
            outputs=[
                stage,
                action_heading,
                task_heading,
                confirmation_heading,
                *option_buttons,
                confirmation_text,
                confirm_button,
                back_button,
                completion_message,
                continue_button,
                state_display,
                welcome_copy,
                start_button,
            ],
        )

        back_button.click(
            lambda options: (
                "tasks",
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                *_option_button_updates(options),
                gr.update(value="", visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(value="", visible=False),
                gr.update(visible=False),
                gr.update(
                    value=get_state_display(),
                    label="Current simulated home / موجودہ فرضی گھر",
                ),
                gr.update(visible=False),
                gr.update(visible=False),
            ),
            inputs=options_state,
            outputs=[
                stage,
                task_heading,
                action_heading,
                confirmation_heading,
                *option_buttons,
                confirmation_text,
                confirm_button,
                back_button,
                completion_message,
                continue_button,
                state_display,
                welcome_copy,
                start_button,
            ],
        )

        continue_button.click(
            _continue_flow,
            inputs=history_state,
            outputs=start_outputs,
        )

    return demo


demo = build_app()


if __name__ == "__main__":
    demo.launch()
