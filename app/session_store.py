"""Persist de-identified study sessions and analysis-ready CSV exports."""

from __future__ import annotations

import csv
import json
import os
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SESSIONS_DIR = RAW_DIR / "sessions"
SESSION_CSV = RAW_DIR / "session_log.csv"
TASK_CSV = RAW_DIR / "task_log.csv"

SUS_COLUMNS = [f"q{i}" for i in range(1, 11)]
INTERVIEW_COLUMNS = [f"interview_{i}" for i in range(1, 6)]
SESSION_COLUMNS = [
    "session_id", "participant_id", "condition", "status", "started_at", "ended_at",
    "age", "gender", "hearing_status", "hearing_device", "language_background",
    "prior_ipa_experience", "voice_assistant_frequency", "accessibility_needs", "consent_confirmed",
    "task_completion_rate", "completed_tasks", "total_tasks", "mean_latency_seconds",
    *SUS_COLUMNS, "sus_score", "adjective_score", "nps_score",
    *INTERVIEW_COLUMNS, "session_notes",
]
TASK_COLUMNS = [
    "session_id", "participant_id", "condition", "task_id", "task_order",
    "task_goal_english", "task_goal_urdu", "status", "task_started_at", "task_ended_at",
    "latency_seconds", "action_verb_english", "selected_option_urdu", "command",
    "llm_model", "llm_latency_seconds", "llm_used_fallback", "llm_error",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_session(participant_id: str, demographics: dict, tasks: list[dict]) -> dict:
    """Create and immediately persist a session using a non-identifying UUID."""
    participant_id = str(participant_id or "").strip()
    if not participant_id:
        raise ValueError("Enter the participant's study code before starting.")
    now = utc_now()
    session = {
        "schema_version": 1,
        "session_id": uuid.uuid4().hex,
        "participant_id": participant_id,
        "condition": "llm_touch",
        "status": "in_progress",
        "started_at": now,
        "ended_at": None,
        "demographics": dict(demographics),
        "tasks": [
            {
                "task_id": task["id"],
                "task_order": index,
                "task_goal_english": task["english"],
                "task_goal_urdu": task["urdu"],
                "expected_command": task["command"],
                "status": "not_started",
                "task_started_at": None,
                "task_ended_at": None,
                "latency_seconds": None,
                "action_verb_english": None,
                "selected_option_urdu": None,
                "command": None,
                "llm_model": None,
                "llm_latency_seconds": None,
                "llm_used_fallback": None,
                "llm_error": None,
            }
            for index, task in enumerate(tasks, start=1)
        ],
        "events": [],
        "questionnaire": {"sus_responses": {}, "adjective_score": None, "nps_score": None},
        "interview_responses": {},
        "session_notes": "",
    }
    record_event(session, "session_started", {"demographics": demographics}, persist=False)
    persist_session(session)
    return session


def record_event(session: dict, event_type: str, details: dict | None = None, *, persist: bool = True) -> dict:
    event = {"timestamp": utc_now(), "event": event_type, "details": details or {}}
    session.setdefault("events", []).append(event)
    if persist:
        persist_session(session)
    return event


def update_task(session: dict, task_index: int, updates: dict, event_type: str, event_details: dict | None = None) -> None:
    session["tasks"][task_index].update(updates)
    record_event(session, event_type, event_details or updates)


def update_questionnaire(session: dict, responses: dict, interview: dict, notes: str) -> None:
    session["questionnaire"]["sus_responses"] = {
        f"q{index}": _optional_int(value)
        for index, value in enumerate(responses[:10], start=1)
        if value is not None and str(value).strip() != ""
    }
    session["questionnaire"]["adjective_score"] = _optional_int(responses[10]) if len(responses) > 10 else None
    session["questionnaire"]["nps_score"] = _optional_int(responses[11]) if len(responses) > 11 else None
    session["interview_responses"] = {
        f"interview_{index}": value or "" for index, value in enumerate(interview, start=1)
    }
    session["session_notes"] = notes or ""
    record_event(session, "questionnaire_updated", {
        "answered_sus_items": len(session["questionnaire"]["sus_responses"]),
        "adjective_score": session["questionnaire"]["adjective_score"],
        "nps_score": session["questionnaire"]["nps_score"],
    })


def end_session(session: dict, status: str = "complete") -> None:
    session["status"] = status
    session["ended_at"] = utc_now()
    record_event(session, "session_ended", {"status": status})


def persist_session(session: dict) -> None:
    """Atomically save the full JSON record and regenerate the two CSV exports."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = SESSIONS_DIR / f"{session['session_id']}.json"
    _write_json_atomic(path, session)
    _rebuild_csv_exports()


def _write_json_atomic(path: Path, value: dict) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", delete=False, dir=path.parent,
            prefix=f".{path.stem}.", suffix=".tmp",
        ) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        _replace_with_retry(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _write_csv_atomic(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8-sig", newline="", delete=False, dir=path.parent,
            prefix=f".{path.stem}.", suffix=".tmp",
        ) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        _replace_with_retry(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _all_sessions() -> list[dict]:
    if not SESSIONS_DIR.exists():
        return []
    sessions = []
    for path in sorted(SESSIONS_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as stream:
            sessions.append(json.load(stream))
    return sessions


def _replace_with_retry(source: Path, destination: Path) -> None:
    """Retry brief Windows file-indexer/antivirus locks during CSV replacement."""
    for attempt in range(5):
        try:
            os.replace(source, destination)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.05 * (attempt + 1))


def _session_row(session: dict) -> dict:
    demo = session.get("demographics", {})
    questionnaire = session.get("questionnaire", {})
    sus = questionnaire.get("sus_responses", {})
    completed = [task for task in session.get("tasks", []) if task.get("status") == "complete"]
    total = len(session.get("tasks", []))
    latencies = [task["latency_seconds"] for task in completed if task.get("latency_seconds") is not None]
    sus_values = [_optional_int(sus.get(f"q{i}")) for i in range(1, 11)]
    sus_score = None
    if all(value is not None and 1 <= value <= 5 for value in sus_values):
        score = sum((value - 1) if index % 2 else (5 - value) for index, value in enumerate(sus_values, start=1))
        sus_score = score * 2.5
    row = {
        "session_id": session.get("session_id"),
        "participant_id": session.get("participant_id"),
        "condition": session.get("condition", "llm_touch"),
        "status": session.get("status"),
        "started_at": session.get("started_at"),
        "ended_at": session.get("ended_at"),
        **demo,
        "task_completion_rate": round(len(completed) / total, 4) if total else 0,
        "completed_tasks": len(completed),
        "total_tasks": total,
        "mean_latency_seconds": round(sum(latencies) / len(latencies), 3) if latencies else "",
        **{f"q{i}": sus.get(f"q{i}", "") for i in range(1, 11)},
        "sus_score": sus_score if sus_score is not None else "",
        "adjective_score": questionnaire.get("adjective_score") if questionnaire.get("adjective_score") is not None else "",
        "nps_score": questionnaire.get("nps_score") if questionnaire.get("nps_score") is not None else "",
        **session.get("interview_responses", {}),
        "session_notes": session.get("session_notes", ""),
    }
    return row


def _task_rows(session: dict) -> list[dict]:
    rows = []
    for task in session.get("tasks", []):
        rows.append({
            "session_id": session.get("session_id"),
            "participant_id": session.get("participant_id"),
            "condition": session.get("condition", "llm_touch"),
            **task,
        })
    return rows


def _rebuild_csv_exports() -> None:
    sessions = _all_sessions()
    _write_csv_atomic(SESSION_CSV, SESSION_COLUMNS, [_session_row(item) for item in sessions])
    _write_csv_atomic(TASK_CSV, TASK_COLUMNS, [row for item in sessions for row in _task_rows(item)])


def _optional_int(value):
    if value is None or str(value).strip() == "":
        return None
    return int(value)
