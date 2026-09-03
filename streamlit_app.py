import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PIM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    # -----------------------------------------------------
    # LOGIN PAGE CSS
    # -----------------------------------------------------

    st.markdown(
        """
        <style>

        /* =================================================
           LOGIN BACKGROUND
        ================================================= */

        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #0F172A 0%,
                    #172554 50%,
                    #0F172A 100%
                ) !important;
        }


        /* =================================================
           LOGIN MAIN CONTAINER
        ================================================= */

        .main .block-container {

            /* Use minimum height instead of fixed height */
            min-height: 100vh !important;

            padding-top: 30px !important;
            padding-bottom: 30px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;

            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
        }


        /* =================================================
           PIM TITLE
        ================================================= */

        .pim-title {

            text-align: center;

            color: white;

            font-size: 42px;

            font-weight: 700;

            margin-top: 0 !important;

            margin-bottom: 5px !important;
        }


        /* =================================================
           SUBTITLE
        ================================================= */

        .pim-subtitle {

            text-align: center;

            color: #CBD5E1;

            font-size: 17px;

            margin-top: 0 !important;

            margin-bottom: 20px !important;
        }


        /* =================================================
           LOGIN FORM
        ================================================= */

        [data-testid="stForm"] {

            background:
                rgba(15, 23, 42, 0.95);

            padding: 30px !important;

            border-radius: 18px;

            border:
                1px solid
                rgba(255,255,255,0.18);

            box-shadow:
                0px 10px 40px
                rgba(0,0,0,0.45);
        }


        /* =================================================
           LOGIN LABELS
        ================================================= */

        [data-testid="stForm"] label {

            color: #E5E7EB !important;

            font-weight: 500 !important;
        }


        /* =================================================
           LOGIN INPUTS
        ================================================= */

        [data-testid="stForm"] input {

            background-color:
                rgba(255,255,255,0.08) !important;

            color: white !important;

            border:
                1px solid
                rgba(255,255,255,0.25) !important;

            border-radius: 8px !important;
        }


        [data-testid="stForm"] input::placeholder {

            color: #94A3B8 !important;
        }


        /* =================================================
           LOGIN BUTTON
        ================================================= */

        [data-testid="stFormSubmitButton"] button {

            width: 100% !important;

            background-color: #2563EB !important;

            color: white !important;

            border: none !important;

            border-radius: 8px !important;

            padding: 10px !important;

            font-size: 16px !important;

            font-weight: 600 !important;
        }


        [data-testid="stFormSubmitButton"] button:hover {

            background-color: #1D4ED8 !important;

            color: white !important;
        }


        /* =================================================
           SMALL SCREEN
        ================================================= */

        @media (max-height: 700px) {

            .main .block-container {

                justify-content: flex-start !important;

                padding-top: 25px !important;

                padding-bottom: 25px !important;
            }

            .pim-title {

                font-size: 34px;

                margin-bottom: 3px !important;
            }

            .pim-subtitle {

                font-size: 15px;

                margin-bottom: 15px !important;
            }

            [data-testid="stForm"] {

                padding: 22px !important;
            }
        }


        /* =================================================
           VERY SMALL SCREEN
        ================================================= */

        @media (max-height: 550px) {

            .main .block-container {

                justify-content: flex-start !important;

                padding-top: 15px !important;

                padding-bottom: 15px !important;
            }

            .pim-title {

                font-size: 28px;
            }

            .pim-subtitle {

                font-size: 13px;

                margin-bottom: 10px !important;
            }

            [data-testid="stForm"] {

                padding: 18px !important;
            }
        }


        /* =================================================
           MOBILE WIDTH
        ================================================= */

        @media (max-width: 600px) {

            .main .block-container {

                padding-left: 0.7rem !important;

                padding-right: 0.7rem !important;
            }

            .pim-title {

                font-size: 32px;
            }

            .pim-subtitle {

                font-size: 14px;
            }

            [data-testid="stForm"] {

                padding: 22px !important;

                border-radius: 14px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # LOGIN TITLE
    # -----------------------------------------------------

    st.markdown(
        '<div class="pim-title">📊 PIM Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="pim-subtitle">'
        'Monitor &nbsp;•&nbsp; Analyze &nbsp;•&nbsp; Improve'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # CENTER LOGIN BOX
    # -----------------------------------------------------

    left, center, right = st.columns([1, 1.1, 1])

    with center:

        st.markdown(
            """
            <div style="
                text-align:center;
                color:white;
                font-size:24px;
                font-weight:600;
                margin-bottom:10px;
            ">
                Welcome Back!
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                text-align:center;
                color:#CBD5E1;
                font-size:14px;
                margin-bottom:12px;
            ">
                Sign in to access the PIM Dashboard
            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # LOGIN FORM
        # -------------------------------------------------

        with st.form("login_form"):

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            login_button = st.form_submit_button(
                "🔐 Login"
            )


        # -------------------------------------------------
        # LOGIN VALIDATION
        # -------------------------------------------------

        if login_button:

            if username == "admin" and password == "1234":

                st.session_state.logged_in = True

                st.rerun()

            else:

                st.error(
                    "Incorrect username or password."
                )


# =========================================================
# DASHBOARD
# =========================================================

else:

    # -----------------------------------------------------
    # DASHBOARD CSS
    # -----------------------------------------------------

    st.markdown(
        """
        <style>

        /* =================================================
           DASHBOARD BACKGROUND
        ================================================= */

        .stApp {

            background:
                linear-gradient(
                    135deg,
                    #F8FAFC 0%,
                    #EEF2FF 50%,
                    #F8FAFC 100%
                ) !important;
        }


        /* =================================================
           FULL WIDTH DASHBOARD
        ================================================= */

        .main .block-container {

            max-width: none !important;

            width: 100% !important;

            padding-top: 2rem !important;

            padding-left: 2rem !important;

            padding-right: 2rem !important;

            padding-bottom: 2rem !important;
        }


        /* =================================================
           DASHBOARD TITLE
        ================================================= */

        .dashboard-title {

            color: #0F172A;

            font-size: 32px;

            font-weight: 700;

            margin-bottom: 5px;
        }


        /* =================================================
           DASHBOARD SUBTITLE
        ================================================= */

        .dashboard-subtitle {

            color: #64748B;

            font-size: 16px;

            margin-bottom: 25px;
        }


        /* =================================================
           METRIC CARDS
        ================================================= */

        [data-testid="stMetric"] {

            background: white;

            padding: 20px;

            border-radius: 14px;

            border: 1px solid #E2E8F0;

            box-shadow:
                0px 4px 15px
                rgba(15,23,42,0.08);
        }


        /* =================================================
           SIDEBAR
        ================================================= */

        [data-testid="stSidebar"] {

            background-color: #0F172A;
        }


        [data-testid="stSidebar"] * {

            color: white !important;
        }


        /* =================================================
           DASHBOARD MOBILE
        ================================================= */

        @media (max-width: 600px) {

            .main .block-container {

                padding-left: 1rem !important;

                padding-right: 1rem !important;
            }

            .dashboard-title {

                font-size: 26px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    st.sidebar.title("📊 PIM Dashboard")

    page = st.sidebar.selectbox(
        "Go to",
        [
            "Home",
            "Schools",
            "Teachers",
            "Visits",
            "Reports"
        ]
    )


    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()


    # =====================================================
    # HOME
    # =====================================================

    if page == "Home":

        st.markdown(
            '<div class="dashboard-title">🏠 Home</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'Welcome to the PIM Dashboard'
            '</div>',
            unsafe_allow_html=True
        )


        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Schools",
                25
            )

        with col2:

            st.metric(
                "Total Teachers",
                150
            )

        with col3:

            st.metric(
                "Total Visits",
                500
            )

        with col4:

            st.metric(
                "Standards Met",
                "82%"
            )


    # =====================================================
    # SCHOOLS
    # =====================================================

    elif page == "Schools":

        st.markdown(
            '<div class="dashboard-title">🏫 Schools</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'School-level analysis'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "School-level analysis will appear here."
        )


    # =====================================================
    # TEACHERS
    # =====================================================

    elif page == "Teachers":

        st.markdown(
            '<div class="dashboard-title">👨‍🏫 Teachers</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'Teacher-level analysis'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "Teacher-level analysis will appear here."
        )


    # =====================================================
    # VISITS
    # =====================================================

    elif page == "Visits":

        st.markdown(
            '<div class="dashboard-title">📍 Visits</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'Visit monitoring and analysis'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "Visit analysis will appear here."
        )


    # =====================================================
    # REPORTS
    # =====================================================

    elif page == "Reports":

        st.markdown(
            '<div class="dashboard-title">📈 Reports</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'Reports and summaries'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            "Reports will appear here."
        )
