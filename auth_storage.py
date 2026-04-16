import csv
from pathlib import Path


FIELDNAMES = ["student_id", "password"]
DEFAULT_ADMIN = {"student_id": "admin", "password": "1234"}


def ensure_storage(csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        with csv_path.open("w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=FIELDNAMES).writeheader()
    ensure_default_admin(csv_path)


def ensure_default_admin(csv_path: Path) -> None:
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        users = list(csv.DictReader(file))
    if any(user["student_id"] == DEFAULT_ADMIN["student_id"] for user in users):
        return
    with csv_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(DEFAULT_ADMIN)


def read_users(csv_path: Path) -> list[dict[str, str]]:
    ensure_storage(csv_path)
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def user_exists(csv_path: Path, student_id: str) -> bool:
    return any(user["student_id"] == student_id for user in read_users(csv_path))


def register_user(csv_path: Path, student_id: str, password: str) -> bool:
    if user_exists(csv_path, student_id):
        return False
    with csv_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({"student_id": student_id, "password": password})
    return True


def validate_login(csv_path: Path, student_id: str, password: str) -> bool:
    users = read_users(csv_path)
    return any(
        user["student_id"] == student_id and user["password"] == password
        for user in users
    )
