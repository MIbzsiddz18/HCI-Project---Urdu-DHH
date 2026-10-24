"""Prompt templates for the six suggestion stages in the study interface.

The original paper's Appendix C was not included as a source file in this
repository. These prompts are a localized adaptation of the six stages
specified in IMPLEMENTATION_PLAN.md, not a verbatim reproduction.
"""

SYSTEM_PROMPT = """You are a concise, accessible smart-home assistant for Pakistani
Urdu-speaking Deaf and Hard of Hearing users. The user interacts by touching
suggestions. Use familiar Pakistani Urdu in Urdu script. Consider only the
simulated devices and capabilities supplied in the context; never claim to
have performed an action. Return exactly the requested format. If Urdu is
unreliable, reason in English internally and use clear Urdu phrasing while
preserving the requested action and its details."""

ACTION_VERBS_PROMPT = """Suggest exactly 8 short action labels for starting a command.
Return a JSON array of strings only. Write natural, concise Urdu in Urdu script.
Use respectful/formal phrasing such as کریں and دکھائیں; avoid casual forms such
as کرو, دیکھو, or چلاؤ.
Use the available smart-home environment and recent command history to avoid
irrelevant or duplicate actions. Do not include examples or explanations.

Environment: {home_env}
Recent commands: {history}"""

TASK_OPTIONS_PROMPT = """The user chose this action: {verb}
The most recent user request in the history is the task they are trying to
complete. Suggest up to 8 distinct, short Urdu command options that help
complete that request using the chosen action. Every option must be relevant
to that latest request. Options must express meaningfully different choices
or details, not the same command rephrased with synonyms. If fewer than 8
meaningfully different options exist, return fewer; never pad with duplicates
or unrelated categories. If the request is specific (for example a duration,
color, place, or named event), preserve that detail in the options. Use Urdu
script and natural, respectful Pakistani Urdu. Do not add explanations or
invent capabilities.
Return a JSON array of strings only.

Environment: {home_env}
Recent commands, oldest to newest: {history}"""

NEEDS_MORE_INFO_PROMPT = """Decide if this smart-home request needs a choice or missing
detail before it can be completed safely and unambiguously. Reply with only
JSON: {{"needs_more_info": true}} or {{"needs_more_info": false}}.
Requests such as setting a timer for 5 minutes, checking Lahore weather,
showing biryani, setting a Fajr reminder, or setting a light blue are complete.
Request: {task}
Environment: {home_env}"""

FOLLOWUP_QUESTION_PROMPT = """Write one brief, clear follow-up question in Urdu script
to obtain the single most important missing detail for this request. Return
only the question, without quotes or explanation.
Request: {task}
Environment: {home_env}"""

FOLLOWUP_OPTIONS_PROMPT = """For this follow-up question: {question}
Generate exactly 8 concise, distinct answer choices in Urdu script. Return a
JSON array of strings only. Make each choice answer the question and fit the
task. Do not include unrelated generic options or imply that a choice was
already applied.
Task: {task}
Environment: {home_env}"""

FINAL_COMMAND_PROMPT = """Assemble one concise executable command from the selected
task and answer. Return one English command string only, suitable for the
local simulator parser (examples: 'set timer for 5 minutes', 'set light color
to blue', 'check weather in Lahore', 'show biryani recipe', 'set Fajr
reminder', 'show calendar'). Do not claim it has been executed.
Task: {task}
Follow-up question: {question}
Selected answer: {answer}
Environment: {home_env}"""

PROMPTS = {
    "action_verbs": ACTION_VERBS_PROMPT,
    "task_options": TASK_OPTIONS_PROMPT,
    "needs_more_info": NEEDS_MORE_INFO_PROMPT,
    "followup_question": FOLLOWUP_QUESTION_PROMPT,
    "followup_options": FOLLOWUP_OPTIONS_PROMPT,
    "final_command": FINAL_COMMAND_PROMPT,
}
