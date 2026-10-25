"""Groq wrapper with bounded outputs and deterministic Urdu fallbacks."""

import json
import os
import re
import time

try:  # Supports both `python app/main.py` and package imports.
    from . import prompts, translations
except ImportError:  # pragma: no cover - script execution path
    import prompts
    import translations

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
_client = None
LAST_ERROR = None
LAST_RAW_RESPONSE = None
LAST_PARSE_USED_FALLBACK = False
LAST_LATENCY_SECONDS = None


def _get_client():
    global _client
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:  # pragma: no cover - dependency is in requirements.txt
        pass
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set")
        from groq import Groq
        _client = Groq(api_key=api_key)
    return _client


def _history_text(history):
    if not history:
        return "(none)"
    if isinstance(history, str):
        return history[-2000:]
    return json.dumps(history[-12:], ensure_ascii=False, default=str)


def _home_text(home_env):
    if home_env is None:
        try:
            from .smart_home import get_state
        except ImportError:  # pragma: no cover
            from smart_home import get_state
        home_env = get_state()
    return json.dumps(home_env, ensure_ascii=False, default=str)


def _complete(template, fallback, *, json_mode=False, **values):
    """Call Groq, returning parsed content or fallback on any service issue."""
    global LAST_ERROR, LAST_RAW_RESPONSE, LAST_PARSE_USED_FALLBACK, LAST_LATENCY_SECONDS
    LAST_ERROR = None
    LAST_RAW_RESPONSE = None
    LAST_PARSE_USED_FALLBACK = False
    LAST_LATENCY_SECONDS = None
    prompt = template.format(**values)
    started = time.perf_counter()
    try:
        client = _get_client()  # Loads .env before model selection.
        model = os.getenv("GROQ_MODEL", MODEL)
        # GPT-OSS spends part of its completion budget on reasoning. Keep that
        # effort low and exclude reasoning from the user-facing command output.
        request_options = {
            "max_completion_tokens": 512,
        }
        if model.startswith("openai/gpt-oss-"):
            request_options.update({"reasoning_effort": "low", "include_reasoning": False})
        if json_mode:
            request_options["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(
            # Read after _get_client loads .env so a chosen model there takes effect.
            model=model,
            # Groq's GPT-OSS guidance recommends putting instructions in the
            # user message instead of relying on a system message.
            messages=[{"role": "user", "content": f"{prompts.SYSTEM_PROMPT}\n\n{prompt}"}],
            temperature=0.2,
            **request_options,
        )
        content = response.choices[0].message.content or ""
        LAST_RAW_RESPONSE = content.strip()
        LAST_LATENCY_SECONDS = time.perf_counter() - started
        return content.strip(), LAST_LATENCY_SECONDS
    except Exception as exc:
        LAST_ERROR = f"{type(exc).__name__}: {exc}"
        LAST_LATENCY_SECONDS = time.perf_counter() - started
        return fallback, LAST_LATENCY_SECONDS


def get_backend_status():
    """Report API failure and whether list parsing needed local options."""
    return {
        "used_fallback": LAST_ERROR is not None,
        "error": LAST_ERROR,
        "used_local_list_fallback": LAST_PARSE_USED_FALLBACK or LAST_ERROR is not None,
        "raw_response_preview": (LAST_RAW_RESPONSE or "")[:500],
    }


def _parse_list(content, fallback, limit=8):
    global LAST_PARSE_USED_FALLBACK
    try:
        match = re.search(r"\[[\s\S]*\]", content)
        values = json.loads(match.group(0)) if match else None
        if not isinstance(values, list):
            raise ValueError("not a JSON list")
    except (ValueError, json.JSONDecodeError, TypeError):
        # A truncated JSON array can still contain complete quoted options.
        # Recover those before falling back to the hardcoded list.
        values = []
        for quoted in re.findall(r'"((?:\\.|[^"\\])*)"', content):
            try:
                values.append(json.loads(f'"{quoted}"'))
            except json.JSONDecodeError:
                continue
        if not values:
            values = [line.strip(" -•\t\"'") for line in content.splitlines() if line.strip()]
    cleaned = []
    for item in values:
        if isinstance(item, str) and item.strip() and item.strip() not in cleaned:
            cleaned.append(item.strip())
    # Preserve a shorter valid answer rather than adding unrelated generic
    # buttons. The hardcoded list is used only when no options were recoverable.
    LAST_PARSE_USED_FALLBACK = not cleaned
    if not cleaned:
        cleaned = list(fallback)
    return cleaned[:limit]


def _list_call(template, fallback, **values):
    # List prompts intentionally return a top-level JSON array. Groq's
    # json_object mode rejects arrays, so parse the model's JSON directly.
    raw, _ = _complete(template, json.dumps(fallback, ensure_ascii=False), **values)
    return _parse_list(raw, fallback)


def get_action_verbs(history=None, home_env=None):
    return _list_call(prompts.ACTION_VERBS_PROMPT, translations.ACTION_VERBS_UR,
                      history=_history_text(history), home_env=_home_text(home_env),
                      fallbacks=json.dumps(translations.ACTION_VERBS_UR, ensure_ascii=False))


def get_task_options(verb, history=None, home_env=None):
    return _list_call(prompts.TASK_OPTIONS_PROMPT, translations.TASK_OPTIONS_UR,
                      verb=verb, history=_history_text(history), home_env=_home_text(home_env),
                      fallbacks=json.dumps(translations.TASK_OPTIONS_UR, ensure_ascii=False))


def get_llm_options(verb, history=None, home_env=None):
    """Compatibility adapter for Ashhal's planned Gradio callback name."""
    return get_task_options(verb, history, home_env)


def needs_more_info(task):
    raw, _ = _complete(prompts.NEEDS_MORE_INFO_PROMPT, '{"needs_more_info": false}',
                       json_mode=True, task=task, home_env=_home_text(None))
    try:
        match = re.search(r"\{[\s\S]*\}", raw)
        return bool(json.loads(match.group(0))["needs_more_info"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        return False


def get_followup_question(task):
    fallback = "آپ کس وقت کی یاد دہانی چاہتے ہیں؟"
    raw, _ = _complete(prompts.FOLLOWUP_QUESTION_PROMPT, fallback,
                       task=task, home_env=_home_text(None))
    return raw.strip().strip('"') or fallback


def get_followup_options(question, task=""):
    return _list_call(prompts.FOLLOWUP_OPTIONS_PROMPT, translations.FOLLOWUP_OPTIONS_UR,
                      question=question, task=task, home_env=_home_text(None),
                      fallbacks=json.dumps(translations.FOLLOWUP_OPTIONS_UR, ensure_ascii=False))


def build_final_command(task, question=None, answer=None):
    fallback = str(task).strip()
    raw, _ = _complete(prompts.FINAL_COMMAND_PROMPT, fallback,
                       task=task, question=question or "(none)", answer=answer or "(none)",
                       home_env=_home_text(None))
    return raw.strip().strip('"') or fallback


def get_last_latency_seconds():
    """Return the duration of the most recent API attempt, in seconds."""
    return LAST_LATENCY_SECONDS
