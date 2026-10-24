#!/usr/bin/env python3
"""Analyze task completion latency data for a usability study.

Sample input CSV format:

participant_id,condition,task_id,latency_seconds
P01,natural_deaf_speech,T1,12.5
P01,natural_deaf_speech,T2,15.0
P02,facilitated,T1,9.7
P02,facilitated,T2,11.3
P03,llm_touch,T1,6.8
P03,llm_touch,T2,7.2

This script reads a CSV file containing participant-level latency observations,
computes summary statistics by condition, computes per-participant mean latency
per condition, handles missing values gracefully, and can optionally save a
bar chart of mean latency by condition.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover - optional dependency
    plt = None


VALID_CONDITIONS = {"natural_deaf_speech", "facilitated", "llm_touch"}


def parse_latency(value):
    """Convert a cell to a float, returning None for missing/blank values."""
    if value is None:
        return None

    text = str(value).strip()
    if text == "" or text.lower() in {"na", "n/a", "nan", "null", "none"}:
        return None

    try:
        return float(text)
    except ValueError:
        return None


def read_latency_csv(csv_path: str):
    """Read the latency CSV and return a list of row dictionaries."""
    rows = []

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {"participant_id", "condition", "task_id", "latency_seconds"}
        missing = required_columns.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"CSV is missing required columns: {sorted(missing)}"
            )

        for row in reader:
            condition = str(row.get("condition", "")).strip()
            if condition not in VALID_CONDITIONS:
                # Allow unknown values to pass through but warn later; schema is still validated
                pass

            latency = parse_latency(row.get("latency_seconds"))
            rows.append(
                {
                    "participant_id": str(row.get("participant_id", "")).strip(),
                    "condition": condition,
                    "task_id": str(row.get("task_id", "")).strip(),
                    "latency_seconds": latency,
                }
            )

    return rows


def summarize_condition(records):
    """Compute summary statistics for a list of latency values."""
    valid_values = [value for value in records if value is not None]
    if not valid_values:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "stddev": None,
            "min": None,
            "max": None,
        }

    return {
        "count": len(valid_values),
        "mean": sum(valid_values) / len(valid_values),
        "median": statistics.median(valid_values),
        "stddev": statistics.pstdev(valid_values) if len(valid_values) > 1 else 0.0,
        "min": min(valid_values),
        "max": max(valid_values),
    }


def summarize_by_condition(records):
    """Return a dictionary of condition -> summary stats."""
    grouped = {condition: [] for condition in sorted(VALID_CONDITIONS)}

    for row in records:
        condition = row["condition"]
        if condition in grouped:
            grouped[condition].append(row["latency_seconds"])

    return {condition: summarize_condition(values) for condition, values in grouped.items()}


def per_participant_mean_latency(records):
    """Compute per-participant mean latency for each condition."""
    grouped = {}

    for row in records:
        participant_id = row["participant_id"]
        condition = row["condition"]
        latency = row["latency_seconds"]

        key = (participant_id, condition)
        if key not in grouped:
            grouped[key] = []

        if latency is not None:
            grouped[key].append(latency)

    results = {}
    for (participant_id, condition), values in grouped.items():
        if values:
            results.setdefault(participant_id, {})[condition] = sum(values) / len(values)

    return results


def print_summary_table(condition_summary):
    """Print a formatted summary table of condition x stats."""
    print("Latency Summary by Condition")
    print("-" * 100)
    print(f"{'Condition':<22} {'Mean':>12} {'Median':>12} {'Std Dev':>12} {'Min':>12} {'Max':>12} {'Count':>8}")
    print("-" * 100)

    for condition in sorted(VALID_CONDITIONS):
        stats = condition_summary.get(condition, {})
        mean = stats.get("mean")
        median = stats.get("median")
        stddev = stats.get("stddev")
        minimum = stats.get("min")
        maximum = stats.get("max")
        count = stats.get("count", 0)

        print(
            f"{condition:<22} "
            f"{(mean if mean is not None else 'N/A'):>12} "
            f"{(median if median is not None else 'N/A'):>12} "
            f"{(stddev if stddev is not None else 'N/A'):>12} "
            f"{(minimum if minimum is not None else 'N/A'):>12} "
            f"{(maximum if maximum is not None else 'N/A'):>12} "
            f"{count:>8}"
        )

    print("-" * 100)


def save_mean_latency_chart(condition_summary, output_path="latency_by_condition.png"):
    """Optionally save a grouped bar chart of mean latency by condition."""
    if plt is None:
        print("Matplotlib is not installed; skipping chart generation.")
        return

    conditions = []
    means = []

    for condition in sorted(VALID_CONDITIONS):
        stats = condition_summary.get(condition, {})
        mean = stats.get("mean")
        if mean is not None:
            conditions.append(condition)
            means.append(mean)

    if not conditions:
        print("No valid latency data available to plot.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(conditions, means, color=["#4C72B0", "#55A868", "#C44E52"])
    ax.set_title("Mean Latency by Condition")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Mean latency (seconds)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved chart to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze usability study latency data by condition and participant."
    )
    parser.add_argument("csv_file", help="Path to CSV file with participant_id, condition, task_id, latency_seconds.")
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Save a grouped bar chart of mean latency by condition as latency_by_condition.png.",
    )
    parser.add_argument(
        "--output",
        default="latency_by_condition.png",
        help="Output filename for the latency chart (default: latency_by_condition.png).",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    records = read_latency_csv(str(csv_path))
    condition_summary = summarize_by_condition(records)

    print_summary_table(condition_summary)

    participant_means = per_participant_mean_latency(records)
    print("\nPer-participant mean latency by condition")
    print("-" * 80)
    if participant_means:
        for participant_id in sorted(participant_means):
            print(f"{participant_id}: {participant_means[participant_id]}")
    else:
        print("No participant-level latency data available.")

    if args.plot:
        save_mean_latency_chart(condition_summary, args.output)


if __name__ == "__main__":
    main()
