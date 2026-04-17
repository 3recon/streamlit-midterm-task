import csv
from random import Random
from pathlib import Path


def split_answers(answer_text: str) -> list[str]:
    cleaned = answer_text.strip().strip('"').strip("'")
    return [
        answer.strip().strip('"').strip("'")
        for answer in cleaned.split("|")
        if answer.strip().strip('"').strip("'")
    ]


def load_quizzes(csv_path: Path) -> list[dict[str, object]]:
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    return [
        {
            "quiz": row["quiz"].strip(),
            "answers": split_answers(row["answer"]),
            "comment": (row.get("coment") or "").strip(),
        }
        for row in rows
        if row.get("quiz") and row.get("answer")
    ]


def normalize_text(text: str) -> str:
    cleaned = text.strip().strip('"').strip("'").strip(",")
    return " ".join(cleaned.lower().split())


def check_answer(quiz: dict[str, object], user_answer: str) -> bool:
    normalized_input = normalize_text(user_answer)
    answers = [normalize_text(answer) for answer in quiz["answers"]]
    return normalized_input in answers


def get_display_answer(quiz: dict[str, object]) -> str:
    answers = quiz["answers"]
    return answers[0] if answers else ""


def create_result_breakdown(score: int, total: int) -> list[dict[str, object]]:
    wrong_count = max(total - score, 0)
    return [
        {"label": "맞춘 문제", "count": score},
        {"label": "맞추지 못한 문제", "count": wrong_count},
    ]


def select_quizzes(
    quizzes: list[dict[str, object]],
    count: int,
    rng: Random | None = None,
) -> list[dict[str, object]]:
    picker = rng or Random()
    limit = min(count, len(quizzes))
    return picker.sample(quizzes, limit)
