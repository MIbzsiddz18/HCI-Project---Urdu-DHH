"""Deterministic, in-memory smart-home simulator used by the study UI."""

from copy import deepcopy
import re

INITIAL_STATE = {
    "light": "off", "light_color": "white", "timer": None,
    "reminder": None, "calendar": "No events today",
    "weather": "Not checked", "recipe": "Not shown",
}
state = deepcopy(INITIAL_STATE)


def reset_state():
    """Reset and return the shared simulated home state."""
    state.clear()
    state.update(deepcopy(INITIAL_STATE))
    return deepcopy(state)


def get_state():
    """Return a copy so callers cannot accidentally mutate simulator state."""
    return deepcopy(state)


def _apply_command(home_state, command):
    text = str(command or "").strip().lower()
    text = text.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    normalized = re.sub(r"\s+", " ", text)
    if any(x in normalized for x in ("turn on light", "light on", "بتی جل", "لائٹ آن")):
        home_state["light"] = "on"
    elif any(x in normalized for x in ("turn off light", "light off", "بتی بند", "لائٹ آف")):
        home_state["light"] = "off"
    color = next((c for c in ("blue", "red", "green", "white") if c in normalized), None)
    urdu_colors = {"نیلا": "blue", "سرخ": "red", "سبز": "green", "سفید": "white"}
    if color or any(c in normalized for c in urdu_colors):
        home_state["light_color"] = color or next(v for k, v in urdu_colors.items() if k in normalized)
        home_state["light"] = "on"
    timer_match = re.search(r"(\d+)\s*(?:minutes?|mins?|منٹ)", normalized)
    if timer_match and ("timer" in normalized or "ٹائمر" in normalized):
        home_state["timer"] = f"{timer_match.group(1)} minutes"
    elif "ٹائمر" in normalized and "پانچ" in normalized:
        home_state["timer"] = "5 minutes"
    elif "ٹائمر" in normalized and "دس" in normalized:
        home_state["timer"] = "10 minutes"
    if "weather" in normalized or "موسم" in normalized:
        home_state["weather"] = "Lahore: Sunny, 28°C (simulated)"
    if "biryani" in normalized or "بریانی" in normalized:
        home_state["recipe"] = "Biryani recipe displayed"
    if "fajr" in normalized or "فجر" in normalized:
        home_state["reminder"] = "Fajr"
    if "calendar" in normalized or "کیلنڈر" in normalized:
        home_state["calendar"] = "No events today"
    return home_state


def update_state(command):
    """Apply a recognized command to the simulator and return a state copy."""
    _apply_command(state, command)
    return get_state()


def preview_state(command):
    """Return the state that a command would produce without changing the simulator."""
    return _apply_command(get_state(), command)


def get_state_display(home_state=None):
    """Return a compact bilingual display string for the Gradio state panel."""
    labels = {"light": "Light / بتی", "light_color": "Color / رنگ", "timer": "Timer / ٹائمر", "reminder": "Reminder / یاد دہانی", "calendar": "Calendar / کیلنڈر", "weather": "Weather / موسم", "recipe": "Recipe / ترکیب"}
    display_state = state if home_state is None else home_state
    return "\n".join(f"{labels[key]}: {value if value is not None else 'None'}" for key, value in display_state.items())
