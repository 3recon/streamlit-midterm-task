import streamlit as st


st.set_page_config(
    page_title="광운대학교 퀴즈",
    page_icon="🎓",
    layout="centered",
)


def init_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "home"


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

        .eyebrow {
            color: var(--primary);
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
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
            border-radius: 14px;
            border: 1px solid var(--primary);
            color: var(--primary);
            font-weight: 700;
            min-height: 2.8rem;
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background: var(--primary);
            color: white;
        }

        div[data-testid="stButton"] > button.signup-button {
            background: white;
            color: var(--primary);
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
            <div class="subtitle">
                광운대학교에 대한 재미있는 TMI를 퀴즈로 풀어보는 웹 애플리케이션입니다.
            </div>
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

    st.write("")
    left, right = st.columns(2)

    with left:
        if st.button("로그인", use_container_width=True, type="primary"):
            go_to("login")
            st.rerun()

    with right:
        st.markdown(
            """
            <style>
            div[data-testid="stButton"] > button[kind="secondary"] {
                background: white;
                color: #8A1601;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        if st.button("회원가입", use_container_width=True):
            go_to("signup")
            st.rerun()


def render_login_page() -> None:
    st.markdown(
        """
        <section class="form-card">
            <div class="eyebrow">Login</div>
            <div class="form-title">로그인</div>
            <div class="form-description">
                학번과 이름을 입력해 광운대학교 TMI 퀴즈에 접속하세요.
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        student_id = st.text_input("학번", placeholder="예: admin")
        name = st.text_input("이름", placeholder="1234")
        submitted = st.form_submit_button("로그인", type="primary", use_container_width=True)

    if submitted:
        st.success(f"{name or '사용자'} 로그인 화면이 연결되었습니다.")

    if st.button("메인으로 돌아가기", use_container_width=True):
        go_to("home")
        st.rerun()


def render_signup_page() -> None:
    st.markdown(
        """
        <section class="form-card">
            <div class="eyebrow">Sign Up</div>
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
        name = st.text_input("이름", placeholder="예: 1234")
        submitted = st.form_submit_button("회원가입", type="primary", use_container_width=True)

    if submitted:
        st.success(f"{name or '사용자'} 회원가입 화면이 연결되었습니다.")

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
