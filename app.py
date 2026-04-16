import streamlit as st
import base64
from pathlib import Path

from auth_storage import register_user, validate_login


st.set_page_config(
    page_title="광운대학교 퀴즈",
    page_icon="🎓",
    layout="centered",
)

USERS_CSV = Path("data") / "users.csv"
LOGO_PATH = Path("kw_logo.png").resolve().as_posix()


def init_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "auth_user" not in st.session_state:
        st.session_state.auth_user = ""


def go_to(page: str) -> None:
    st.session_state.page = page


def render_logo(width: int) -> None:
    left, center, right = st.columns([1, 2, 1])
    with center:
        if LOGO_PATH.lower().endswith(".svg"):
            svg_data = Path(LOGO_PATH).read_text(encoding="utf-8")
            svg_base64 = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <img src="data:image/svg+xml;base64,{svg_base64}" width="{width}">
                </div>
                """,
                unsafe_allow_html=True,
            )
            return
        raw_data = Path(LOGO_PATH).read_bytes()
        if raw_data.lstrip().startswith(b"<svg"):
            svg_base64 = base64.b64encode(raw_data).decode("utf-8")
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <img src="data:image/svg+xml;base64,{svg_base64}" width="{width}">
                </div>
                """,
                unsafe_allow_html=True,
            )
            return
        st.image(str(LOGO_PATH), width=width)


def render_global_style() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

        :root {
            --bg-main: #f8ece8;
            --bg-deep: #d9c0b8;
            --panel: #40140b;
            --panel-soft: #6b2315;
            --line: #d7b2a8;
            --text-main: #fff8f5;
            --text-soft: #f3d6cd;
            --text-muted: #8f4c3f;
            --cta: #8A1601;
            --cta-shadow: #4e0d00;
            --accent: #b22308;
            --disabled-bg: #d7c3bc;
            --disabled-text: #7f635b;
        }

        .stApp {
            background: var(--bg-main);
            font-family: 'Noto Sans KR', sans-serif;
            color: var(--text-main);
        }

        .block-container {
            max-width: 1200px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }

        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }

        .hero-shell,
        .form-shell {
            width: min(100%, 1020px);
            margin: 0 auto;
        }

        .title {
            font-family: 'Black Han Sans', sans-serif;
            color: var(--text-main);
            font-size: 3.2rem;
            line-height: 1.05;
            letter-spacing: -0.03em;
            margin: 0 0 0.4rem;
            text-align: center;
        }

        .subtitle {
            color: var(--text-soft);
            font-size: 1.2rem;
            margin: 0;
            text-align: center;
            font-weight: 500;
        }

        .hero-band,
        .form-band {
            background: var(--panel);
            padding: 2rem 2.5rem;
            margin: 0 auto 1.6rem;
            box-shadow: 0 8px 0 rgba(78, 13, 0, 0.28);
        }

        .hero-meta {
            margin: 1.5rem auto 2rem;
            display: flex;
            justify-content: center;
            gap: 2.5rem;
            color: #000000;
            font-weight: 700;
        }

        .hero-meta strong {
            color: #000000;
            margin-left: 0.4rem;
            font-size: 1.1rem;
        }

        .course-box {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.95rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-top: 1rem;
        }

        .form-title {
            color: var(--text-main);
            font-family: 'Black Han Sans', sans-serif;
            font-size: 2.6rem;
            letter-spacing: -0.02em;
            margin: 0 0 0.75rem;
            text-align: center;
        }

        .form-description {
            color: var(--text-soft);
            margin: 0;
            text-align: center;
            font-size: 1.08rem;
        }

        .status-strip {
            width: min(100%, 520px);
            margin: 1.2rem auto 1.4rem;
            padding: 0.8rem 1rem;
            border-top: 3px solid var(--accent);
            background: rgba(64, 20, 11, 0.14);
            color: #5a1d11;
            text-align: center;
            font-weight: 700;
        }

        .quiz-lock-row {
            width: min(100%, 540px);
            margin: 0.4rem auto 1rem;
        }

        .quiz-guide {
            width: min(100%, 540px);
            margin: 0 auto 1.3rem;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            align-items: start;
        }

        .guide-line {
            position: relative;
            width: min(100%, 540px);
            height: 16px;
            margin: 0 auto 0.8rem;
        }

        .guide-line::before {
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            top: 7px;
            border-top: 4px solid rgba(138,22,1,0.42);
        }

        .guide-dot {
            position: absolute;
            top: 0;
            width: 16px;
            height: 16px;
            border-radius: 999px;
            background: #eadbd5;
            border: 3px solid #fff9f7;
            box-sizing: border-box;
        }

        .guide-dot.start {
            width: 20px;
            height: 20px;
            top: -2px;
            background: var(--accent);
        }

        .guide-label {
            text-align: center;
            padding: 0.7rem 0;
            background: #ead8d2;
            color: #8c665c;
            font-weight: 700;
            font-size: 0.95rem;
        }

        .guide-label.active {
            background: linear-gradient(180deg, #b22308 0%, #8A1601 100%);
            color: white;
        }

        div[data-testid="stButton"] > button {
            height: 4.1rem;
            border-radius: 0;
            border: none;
            color: white;
            font-weight: 900;
            font-size: 1.6rem;
            min-height: 4.1rem;
            box-sizing: border-box;
            font-family: 'Black Han Sans', sans-serif;
            letter-spacing: -0.02em;
            box-shadow: 0 8px 0 rgba(78, 13, 0, 0.3);
            transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
        }

        div[data-testid="stButton"] > button:hover:not(:disabled) {
            transform: translateY(2px);
            box-shadow: 0 6px 0 rgba(78, 13, 0, 0.3);
            filter: brightness(1.03);
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(90deg, #8A1601 0%, #b22308 100%);
            color: white;
        }

        div[data-testid="stButton"] > button[kind="secondary"] {
            background: linear-gradient(90deg, #f9f0ed 0%, #fffaf8 100%);
            color: #8A1601;
            border: 2px solid rgba(138,22,1,0.85);
            box-shadow: 0 8px 0 rgba(138, 22, 1, 0.12);
        }

        div[data-testid="stButton"] > button:disabled {
            background:
                repeating-linear-gradient(
                    -45deg,
                    #d8c7c1 0,
                    #d8c7c1 16px,
                    #cfbbb4 16px,
                    #cfbbb4 32px
                );
            color: #6d564f;
            cursor: not-allowed;
            opacity: 1;
            box-shadow: 0 8px 0 rgba(116, 88, 80, 0.1);
            border: 2px dashed rgba(109, 86, 79, 0.5);
            filter: grayscale(0.15);
        }

        .quiz-disabled-note {
            text-align: center;
            color: #9a746a;
            font-size: 0.92rem;
            font-weight: 700;
            margin-top: 0.7rem;
            letter-spacing: 0.01em;
        }

        div[data-testid="stTextInput"] label p {
            font-family: 'Black Han Sans', sans-serif;
            color: white;
            font-size: 1.05rem;
            letter-spacing: -0.01em;
        }

        div[data-testid="stTextInput"] input {
            border-radius: 0;
            border: 3px solid rgba(255,248,245,0.88);
            background: rgba(255,250,248,0.98);
            color: #2a130e;
            min-height: 3.4rem;
            font-size: 1rem;
            font-weight: 700;
        }

        div[data-testid="stForm"] {
            width: min(100%, 620px);
            margin: 0 auto;
            padding: 1.4rem 1.8rem 1.8rem;
            background: rgba(138, 22, 1, 0.08);
            border-top: 4px solid rgba(138,22,1,0.5);
        }

        div[data-testid="stAlert"] {
            border-radius: 0;
            width: min(100%, 620px);
            margin: 0.8rem auto;
            border: none;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-top: 1.2rem;
            }

            .title {
                font-size: 2.4rem;
            }

            .hero-band,
            .form-band {
                padding: 1.4rem 1rem;
            }

            .hero-meta {
                flex-direction: column;
                gap: 0.6rem;
                text-align: center;
            }

            .quiz-guide {
                gap: 0.55rem;
            }

            .guide-label {
                font-size: 0.72rem;
            }

            div[data-testid="stButton"] > button {
                font-size: 1.2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    render_logo(360)
    st.markdown(
        """
        <section class="hero-shell">
            <div class="hero-band">
                <div class="title">광운대학교 퀴즈</div>
                <div class="subtitle">나는 과연 광운대를 얼마나 알고 있을까?</div>
            </div>
            <div class="hero-meta">
                <div>학번<strong>2022204038</strong></div>
                <div>이름<strong>전창현</strong></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.logged_in:
        st.markdown(
            f'<div class="status-strip">{st.session_state.auth_user} 로그인 상태입니다.</div>',
            unsafe_allow_html=True,
        )

    st.write("")
    left, right = st.columns(2)

    with left:
        if st.button("로그인", use_container_width=True, type="primary"):
            go_to("login")
            st.rerun()

    with right:
        if st.button("회원가입", use_container_width=True):
            go_to("signup")
            st.rerun()

    st.write("")
    quiz_col = st.columns([0.15, 0.7, 0.15])[1]
    with quiz_col:
        st.button(
            "퀴즈 풀기",
            use_container_width=True,
            type="primary" if st.session_state.logged_in else "secondary",
            disabled=not st.session_state.logged_in,
        )
        if not st.session_state.logged_in:
            st.markdown(
                '<div class="quiz-disabled-note">로그인 후 퀴즈를 시작할 수 있습니다.</div>',
                unsafe_allow_html=True,
            )


def render_login_page() -> None:
    render_logo(220)
    st.markdown(
        """
        <section class="form-shell">
            <div class="form-band">
                <div class="form-title">로그인</div>
                <div class="form-description">
                    저장된 학번과 비밀번호를 입력해 퀴즈를 시작하세요.
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        student_id = st.text_input("학번", placeholder="예: 2022204038")
        password = st.text_input("비밀번호", placeholder="비밀번호를 입력하세요", type="password")
        submitted = st.form_submit_button("로그인", type="primary", use_container_width=True)

    if submitted:
        if not student_id or not password:
            st.error("학번과 비밀번호를 모두 입력해주세요.")
        elif validate_login(USERS_CSV, student_id, password):
            st.session_state.logged_in = True
            st.session_state.auth_user = student_id
            go_to("home")
            st.rerun()
        else:
            st.error("학번 또는 비밀번호가 올바르지 않습니다.")

    back_col = st.columns([1.5, 1, 1.5])[1]
    with back_col:
        if st.button("메인으로 돌아가기", use_container_width=True):
            go_to("home")
            st.rerun()


def render_signup_page() -> None:
    render_logo(220)
    st.markdown(
        """
        <section class="form-shell">
            <div class="form-band">
                <div class="form-title">회원가입</div>
                <div class="form-description">
                    사용할 학번과 비밀번호를 등록한 뒤 로그인하세요.
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.form("signup_form"):
        student_id = st.text_input("학번", placeholder="예: 2022204038")
        password = st.text_input("비밀번호", placeholder="비밀번호를 입력하세요", type="password")
        submitted = st.form_submit_button("회원가입", type="primary", use_container_width=True)

    if submitted:
        if not student_id or not password:
            st.error("학번과 비밀번호를 모두 입력해주세요.")
        elif register_user(USERS_CSV, student_id, password):
            st.success("회원가입이 완료되었습니다. 이제 로그인할 수 있습니다.")
        else:
            st.error("이미 가입된 학번입니다.")

    back_col = st.columns([1.5, 1, 1.5])[1]
    with back_col:
        if st.button("메인으로 돌아가기", use_container_width=True):
            go_to("home")
            st.rerun()


init_state()
render_global_style()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "login":
    render_login_page()
elif st.session_state.page == "signup":
    render_signup_page()
