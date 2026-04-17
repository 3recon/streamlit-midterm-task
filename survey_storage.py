import csv
from pathlib import Path


QUESTION_KEYS = [
    "communication",
    "difficulty",
    "clarity",
    "fun",
    "retry",
]

FIELDNAMES = ["student_id", "score", "total", *QUESTION_KEYS]


def ensure_survey_storage(csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if csv_path.exists():
        return
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=FIELDNAMES).writeheader()


def save_survey_response(
    csv_path: Path,
    student_id: str,
    score: int,
    total: int,
    responses: dict[str, str],
) -> None:
    ensure_survey_storage(csv_path)
    row = {"student_id": student_id, "score": score, "total": total}
    row.update({key: responses[key] for key in QUESTION_KEYS})
    with csv_path.open("a", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=FIELDNAMES).writerow(row)
