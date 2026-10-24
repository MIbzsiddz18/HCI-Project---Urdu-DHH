#!/usr/bin/env python3
"""Compute SUS scores from a CSV of 10 Likert responses per participant.

Expected CSV columns can be named in any of the following ways:
- q1, q2, ..., q10
- sus_1, sus_2, ..., sus_10
- item_1, item_2, ..., item_10
- question_1, question_2, ..., question_10

The script also accepts an optional participant identifier column such as:
participant_id, participant, id, subject_id
"""

from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path


def get_response(row: dict, item_number: int):
    """Return the response for a given numbered item from a CSV row."""
    candidate_names = [
        f"q{item_number}",
        f"sus_{item_number}",
        f"item_{item_number}",
        f"question_{item_number}",
        f"response_{item_number}",
        f"item{item_number}",
    ]

    for name in candidate_names:
        if name in row:
            value = row[name]
            if value is not None and str(value).strip() != "":
                return float(value)

    raise ValueError(f"Missing response for item {item_number} in row: {row}")


def calculate_sus_score(row: dict) -> float:
    """Compute a single participant's SUS score from 10 Likert items."""
    total = 0.0

    for item_number in range(1, 11):
        response = get_response(row, item_number)

        if not 1 <= response <= 5:
            raise ValueError(
                f"Response for item {item_number} must be between 1 and 5; got {response}."
            )

        if item_number % 2 == 1:
            total += response - 1
        else:
            total += 5 - response

    return total * 2.5


def find_participant_id(row: dict, index: int) -> str:
    """Find a participant identifier if available, otherwise create one."""
    id_candidates = [
        "participant_id",
        "participant",
        "id",
        "subject_id",
        "respondent_id",
    ]

    for name in id_candidates:
        if name in row and str(row[name]).strip() != "":
            return str(row[name]).strip()

    return f"Participant {index + 1}"


def load_scores(csv_path: str):
    """Load all participant SUS scores from a CSV file."""
    results = []

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError("CSV file is missing a header row.")

        for index, row in enumerate(reader):
            score = calculate_sus_score(row)
            participant_id = find_participant_id(row, index)
            results.append({"participant_id": participant_id, "score": score})

    if not results:
        raise ValueError("No participant records were found in the CSV file.")

    return results


def summarize_scores(scores):
    """Compute mean, standard deviation, and median across participant scores."""
    values = [entry["score"] for entry in scores]
    mean_score = sum(values) / len(values)
    stdev = statistics.pstdev(values) if len(values) > 1 else 0.0
    median_score = statistics.median(values)
    return mean_score, stdev, median_score


def main():
    parser = argparse.ArgumentParser(
        description="Calculate SUS scores from a CSV file containing 10 Likert responses per participant."
    )
    parser.add_argument("csv_file", help="Path to the CSV file containing SUS item responses.")
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    participant_scores = load_scores(str(csv_path))

    print("SUS score by participant")
    print("-" * 70)
    for entry in participant_scores:
        print(f"{entry['participant_id']}: {entry['score']:.2f}")

    mean_score, stdev, median_score = summarize_scores(participant_scores)

    print("\nAggregate statistics")
    print("-" * 70)
    print(f"Participants: {len(participant_scores)}")
    print(f"Mean SUS score: {mean_score:.2f}")
    print(f"Standard deviation: {stdev:.2f}")
    print(f"Median SUS score: {median_score:.2f}")


if __name__ == "__main__":
    main()
