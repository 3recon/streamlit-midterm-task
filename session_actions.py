DEFAULT_QUIZ_COUNT = 1


def build_auth_action(logged_in: bool) -> dict[str, str]:
    if logged_in:
        return {"label": "로그아웃", "type": "secondary"}
    return {"label": "로그인", "type": "primary"}


def clear_quiz_state(session_state: dict[str, object]) -> None:
    session_state["quiz_bank"] = []
    session_state["quiz_count"] = DEFAULT_QUIZ_COUNT
    session_state["quiz_index"] = 0
    session_state["quiz_score"] = 0
    session_state["quiz_feedback"] = None
    session_state["quiz_submitted"] = False
    session_state["survey_submitted"] = False
    session_state["survey_message"] = None


def logout_user(session_state: dict[str, object]) -> None:
    session_state["logged_in"] = False
    session_state["auth_user"] = ""
    session_state["page"] = "home"
    clear_quiz_state(session_state)
