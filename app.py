import streamlit as st
from pathlib import Path

from auth_storage import register_user, validate_login


st.set_page_config(
    page_title="광운대학교 퀴즈",
    page_icon="🎓",
    layout="centered",
)

USERS_CSV = Path("data") / "users.csv"


def init_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "auth_user" not in st.session_state:
        st.session_state.auth_user = ""


def go_to(page: str) -> None:
    st.session_state.page = page


def render_global_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --primary: #8A1601;
            --primary-dark: #5F0F00;
            --surface: #FFF7F5;
            --surface-strong: #F5E4DF;
            --text-main: #2B1B17;
            --text-soft: #6A4A43;
        }

        .stApp {
            background: linear-gradient(180deg, #fffdfc 0%, var(--surface) 100%);
        }

        .hero-card,
        .form-card {
            max-width: 760px;
            margin: 4rem auto 0;
            padding: 2.5rem 2rem;
            background: white;
            border: 1px solid var(--surface-strong);
            border-top: 8px solid var(--primary);
            border-radius: 24px;
            box-shadow: 0 20px 45px rgba(138, 22, 1, 0.08);
        }


        .title {
            color: var(--text-main);
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 0.75rem;
        }

        .subtitle {
            color: var(--text-soft);
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }

        .info-box {
            background: var(--surface);
            border: 1px solid var(--surface-strong);
            border-radius: 18px;
            padding: 1.1rem 1rem;
        }

        .label {
            color: var(--primary-dark);
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .value {
            color: var(--text-main);
            font-size: 1.15rem;
            font-weight: 700;
        }

        .course-box {
            margin-top: 1rem;
            padding: 1rem 1.1rem;
            background: linear-gradient(135deg, #fff7f5 0%, #f8ece8 100%);
            border-radius: 18px;
            border-left: 6px solid var(--primary);
            color: var(--text-main);
            font-weight: 700;
        }

        .form-title {
            color: var(--text-main);
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .form-description {
            color: var(--text-soft);
            margin-bottom: 1.4rem;
        }

        div[data-testid="stButton"] > button {
            height: 2.8rem;
            border-radius: 14px;
            border: 1px solid var(--primary);
            color: var(--primary);
            font-weight: 700;
            min-height: 2.8rem;
            box-sizing: border-box;
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background: var(--primary);
            color: white;
        }

        div[data-testid="stButton"] > button[kind="secondary"] {
            background: white;
            color: var(--primary);
        }

        div[data-testid="stButton"] > button:disabled {
            background: #efe8e5;
            color: #a88d86;
            border-color: #d7c4bf;
            cursor: not-allowed;
            opacity: 1;
        }

        @media (max-width: 640px) {
            .hero-card,
            .form-card {
                margin-top: 2rem;
                padding: 1.75rem 1.1rem;
            }

            .title {
                font-size: 1.9rem;
            }

            .info-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    st.markdown(
        """
        <section class="hero-card">
            <div class="title">광운대학교 퀴즈</div>
            <div class="info-grid">
                <div class="info-box">
                    <div class="label">학번</div>
                    <div class="value">2022204038</div>
                </div>
                <div class="info-box">
                    <div class="label">이름</div>
                    <div class="value">전창현</div>
                </div>
            </div>
            <div class="course-box">오픈소스소프트웨어 중간고사 대체 과제</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.logged_in:
        st.success(f"{st.session_state.auth_user} 로그인 상태입니다.")

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
    st.button(
        "퀴즈 풀기",
        use_container_width=True,
        type="primary" if st.session_state.logged_in else "secondary",
        disabled=not st.session_state.logged_in,
    )


def render_login_page() -> None:
    st.markdown(
        """
        <section class="form-card">
            <div class="form-title">로그인</div>
            <div class="form-description">
                학번과 비밀번호를 입력해주세요.
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

    if st.button("메인으로 돌아가기", use_container_width=True):
        go_to("home")
        st.rerun()


def render_signup_page() -> None:
    st.markdown(
        """
        <section class="form-card">
            <div class="form-title">회원가입</div>
            <div class="form-description">
                퀴즈 참여를 위한 기본 정보를 입력하는 회원가입 페이지입니다.
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
