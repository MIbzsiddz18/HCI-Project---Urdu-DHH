"""Run the 10-command Urdu suggestion quality check described in the plan.

Usage from the repository root: python -m app.evaluate_llm
Review the printed Urdu suggestions manually; this script does not claim
automated linguistic validation.
"""

import json
import argparse
import time

try:
    from . import llm_client
    from .llm_client import get_action_verbs, get_task_options
    from .smart_home import get_state
except ImportError:  # pragma: no cover
    import llm_client
    from llm_client import get_action_verbs, get_task_options
    from smart_home import get_state

SAMPLE_COMMANDS = [
    "Check today's weather in Lahore",
    "Set a 5-minute timer for tea",
    "Set a 10-minute timer",
    "Turn on the living room light",
    "Turn off the light",
    "Set the light color to blue",
    "Set the light color to red",
    "Show a biryani recipe",
    "Set a reminder for Fajr prayer",
    "Show today's calendar",
]

ACTION_FOR_COMMAND = {
    "Check today's weather in Lahore": "چیک کریں",
    "Set a 5-minute timer for tea": "سیٹ کریں",
    "Set a 10-minute timer": "سیٹ کریں",
    "Turn on the living room light": "روشن کریں",
    "Turn off the light": "بند کریں",
    "Set the light color to blue": "بدلیں",
    "Set the light color to red": "بدلیں",
    "Show a biryani recipe": "دکھائیں",
    "Set a reminder for Fajr prayer": "یاد دہانی لگائیں",
    "Show today's calendar": "دکھائیں",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=len(SAMPLE_COMMANDS),
                        help="number of task prompts to call (use 1 for a low-cost smoke check)")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    history = []
    env = get_state()
    print("Urdu LLM output review (manually assess correctness/context):")
    print("\nAction verbs:")
    started = time.perf_counter()
    verbs = get_action_verbs(history, env)
    print(json.dumps(verbs, ensure_ascii=False, indent=2))
    print(f"Latency: {time.perf_counter() - started:.2f}s")
    print("Backend:", llm_client.get_backend_status())
    for index, command in enumerate(SAMPLE_COMMANDS[:args.limit], 1):
        started = time.perf_counter()
        options = get_task_options(ACTION_FOR_COMMAND[command], history + [command], env)
        print(f"\n{index:02}. {command}")
        print(json.dumps(options, ensure_ascii=False))
        print(f"Latency: {time.perf_counter() - started:.2f}s")
        print("Backend:", llm_client.get_backend_status())
        history.append(command)


if __name__ == "__main__":
    main()
