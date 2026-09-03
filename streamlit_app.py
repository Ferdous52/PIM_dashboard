import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PIM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.markdown("""
    <style>

    .stApp {
        background:
            linear-gradient(
                135deg,
                #F8FAFC 0%,
                #EEF2FF 50%,
                #F8FAFC 100%
            );
    }

    .main .block-container {
        min-height: 100vh;
        box-sizing: border-box;
        padding-top: 30px !important;
        padding-bottom: 30px !important;
    }

    .pim-title {
        text-align: center;
        color: #0F172A;
        font-size: 42px;
        font-weight: 700;
        margin-top: 50px;
        margin-bottom: 5px;
    }

    .pim-subtitle {
        text-align: center;
        color: #64748B;
        font-size: 17px;
        margin-bottom: 30px;
    }

    [data-testid="stForm"] {
        background: white;
        padding: 35px;
        border-radius: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0px 10px 40px rgba(15,23,42,0.12);
    }

    [data-testid="stForm"] label {
        color: #334155 !important;
        font-weight: 500;
    }

    [data-testid="stForm"] input {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    [data-testid="stFormSubmitButton"] button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        font-weight: 600;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #1D4ED8;
        color: white;
    }

    /* Small screens */
    @media (max-width: 600px) {

        .pim-title {
            font-size: 30px;
            margin-top: 20px;
        }

        .pim-subtitle {
            font-size: 14px;
            margin-bottom: 20px;
        }

        [data-testid="stForm"] {
            padding: 20px;
        }

    }

    /* Short screens */
    @media (max-height: 700px) {

        .pim-title {
            margin-top: 10px;
        }

        .main .block-container {
            padding-top: 15px !important;
            padding-bottom: 20px !important;
        }

    }

    </style>
    """, unsafe_allow_html=True)


    st.markdown(
        '<div class="pim-title">📊 PIM Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="pim-subtitle">Monitor &nbsp;•&nbsp; Analyze &nbsp;•&nbsp; Improve</div>',
        unsafe_allow_html=True
    )


    left, center, right = st.columns([1, 1.1, 1])

    with center:

        st.markdown(
            """
            <div style="
                text-align:center;
                color:#0F172A;
                font-size:24px;
                font-weight:600;
                margin-bottom:15px;
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
                color:#64748B;
                font-size:14px;
                margin-bottom:15px;
            ">
                Sign in to access the PIM Dashboard
            </div>
            """,
            unsafe_allow_html=True
        )


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

            login_button = st.form_submit_button("🔐 Login")


        if login_button:

            if username == "admin" and password == "1234":

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("Incorrect username or password.")


    st.stop()


# ============================================================
# LOAD EXCEL DATA
# ============================================================

@st.cache_data
def load_data():

    # Put your Excel file in the same folder as app.py
    file_path = "Compile_LP PIM_Classroom Observation Monthly Summary_June 2026.xlsx"

    df = pd.read_excel(
        file_path,
        sheet_name="JFO",
        skiprows=17,
        header=None
    )


    # --------------------------------------------------------
    # CREATE COLUMN NAMES
    # --------------------------------------------------------

    main_header = df.iloc[0].ffill()
    month_header = df.iloc[1]

    columns = []

    for main, month in zip(main_header, month_header):

        if pd.notna(month):

            columns.append(f"{main}_{month}")

        else:

            columns.append(str(main))


    df.columns = columns

    df = df.iloc[2:].reset_index(drop=True)


    # --------------------------------------------------------
    # CHANGE DATE FORMAT
    # --------------------------------------------------------

    def change_date_format(col):

        if "_" in col:

            prefix, date = col.rsplit("_", 1)

            try:

                date = pd.to_datetime(date)

                return f"{prefix}_{date.strftime('%b')}"

            except:

                return col

        return col


    df.columns = [change_date_format(col) for col in df.columns]


    # --------------------------------------------------------
    # REMOVE EMPTY DATA
    # --------------------------------------------------------

    df = df.dropna(axis=1, how="all")

    df = df.dropna(subset=["School Name"])

    if "S/N" in df.columns:

        df = df.drop(columns=["S/N"])


    # --------------------------------------------------------
    # IDENTIFY COLUMNS
    # --------------------------------------------------------

    minimum_standard_cols = [
        col for col in df.columns
        if col.startswith("Meeting Minimum Standards By Grade?")
    ]


    priority_cols = [
        col for col in df.columns
        if col.startswith(
            "Teacher's Priority Area"
        )
    ]


    total_visit_cols = [
        col for col in df.columns
        if col.startswith(
            "Total Number of Visits Per Month"
        )
    ]


    # --------------------------------------------------------
    # CONVERT MINIMUM STANDARD
    # --------------------------------------------------------

    for col in minimum_standard_cols:

        df[col] = df[col].map({
            "No": 0,
            "Yes": 1
        })


    # --------------------------------------------------------
    # CONVERT PRIORITY AREA
    # --------------------------------------------------------

    priority_mapping = {

        "0: No Priority Areas Achieved": 0,

        "1: Mastered Instructional Routine": 1,

        "2: Mastered Basic Skills": 2,

        "3: Mastered Advanced Skills": 3
    }


    for col in priority_cols:

        df[col] = df[col].map(priority_mapping)


    # --------------------------------------------------------
    # CONVERT VISITS TO NUMERIC
    # --------------------------------------------------------

    for col in total_visit_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)


    return (
        df,
        minimum_standard_cols,
        priority_cols,
        total_visit_cols
    )


# ============================================================
# LOAD DATA
# ============================================================

try:

    (
        df,
        minimum_standard_cols,
        priority_cols,
        total_visit_cols
    ) = load_data()

except Exception as e:

    st.error(
        "Unable to load the Excel file."
    )

    st.code(str(e))

    st.info(
        "Make sure the Excel file is in the same folder as app.py."
    )

    st.stop()


# ============================================================
# CALCULATIONS
# ============================================================


# ------------------------------------------------------------
# SCHOOL AND TEACHER SUMMARY
# ------------------------------------------------------------

table_1 = pd.pivot_table(

    df,

    index="RtR Staff Name",

    values=[
        "School Name",
        "Teacher Name"
    ],

    aggfunc={
        "School Name": "nunique",
        "Teacher Name": "count"
    },

    margins=True,

    margins_name="Total"
)


school_teacher_summary = table_1.reset_index()


# ------------------------------------------------------------
# TARGET VISIT
# ------------------------------------------------------------

df2 = table_1.copy()


Target_Visit = (
    df2["School Name"]
    * 2
    * 2
    * len(total_visit_cols)
)


Target_Visit = pd.DataFrame(
    Target_Visit,
    columns=["Target_Visit"]
)


# ------------------------------------------------------------
# TOTAL VISITED
# ------------------------------------------------------------

visited = pd.pivot_table(

    df,

    index="RtR Staff Name",

    values=total_visit_cols,

    aggfunc="sum",

    margins=True,

    margins_name="Total"
)


visited = visited.sum(axis=1).to_frame(
    "Total_visited"
)


# ------------------------------------------------------------
# GRADE 1 VISITS
# ------------------------------------------------------------

g1 = df[df["Grade"] == 1]


g1 = pd.pivot_table(

    g1,

    index="RtR Staff Name",

    values=total_visit_cols,

    aggfunc="sum",

    margins=True,

    margins_name="Total"
)


g1 = g1.sum(axis=1).reset_index()


g1.columns = [
    "RtR Staff Name",
    "Visit Grade_1"
]


Grade1 = g1


# ------------------------------------------------------------
# GRADE 2 VISITS
# ------------------------------------------------------------

g2 = df[df["Grade"] == 2]


g2 = pd.pivot_table(

    g2,

    index="RtR Staff Name",

    values=total_visit_cols,

    aggfunc="sum",

    margins=True,

    margins_name="Total"
)


g2 = g2.sum(axis=1).reset_index()


g2.columns = [
    "RtR Staff Name",
    "Visit Grade_2"
]


Grade2 = g2


# ------------------------------------------------------------
# MERGE GRADE VISITS
# ------------------------------------------------------------

visit_grade = Grade1.merge(

    Grade2,

    on="RtR Staff Name",

    how="outer"
)


# ------------------------------------------------------------
# VISIT GAP
# ------------------------------------------------------------

diff = Target_Visit.merge(

    visited,

    on="RtR Staff Name",

    how="left"
)


diff["Gap of Visit"] = (
    diff["Target_Visit"]
    - diff["Total_visited"]
)


# ------------------------------------------------------------
# FINAL STAFF VISIT TABLE
# ------------------------------------------------------------

Final_Total_Visited = diff.merge(

    visit_grade,

    on="RtR Staff Name",

    how="left"
)


# ------------------------------------------------------------
# MONTHLY VISITS
# ------------------------------------------------------------

monthly_visit = (
    df[total_visit_cols]
    .sum()
    .reset_index()
)


monthly_visit.columns = [
    "Month",
    "Total_Visit"
]


monthly_visit["Month"] = (
    monthly_visit["Month"]
    .str.extract(r"_([A-Za-z]+)$")[0]
)


# ------------------------------------------------------------
# MINIMUM STANDARD - GRADE 1
# ------------------------------------------------------------

min_std_G1 = (

    df[df["Grade"] == 1]

    .groupby("RtR Staff Name")[minimum_standard_cols]

    .sum()

    .sum(axis=1)

    .reset_index(
        name="Total Standard Meet_Grade-1"
    )
)


# ------------------------------------------------------------
# MINIMUM STANDARD - GRADE 2
# ------------------------------------------------------------

min_std_G2 = (

    df[df["Grade"] == 2]

    .groupby("RtR Staff Name")[minimum_standard_cols]

    .sum()

    .sum(axis=1)

    .reset_index(
        name="Total Standard Meet_Grade-2"
    )
)


# ------------------------------------------------------------
# MERGE MINIMUM STANDARD
# ------------------------------------------------------------

min_std = min_std_G1.merge(

    min_std_G2,

    on="RtR Staff Name",

    how="outer"
).fillna(0)


min_std["Total Standard Meet"] = (

    min_std["Total Standard Meet_Grade-1"]

    + min_std["Total Standard Meet_Grade-2"]
)


# ============================================================
# DASHBOARD CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        linear-gradient(
            135deg,
            #F8FAFC 0%,
            #EEF2FF 50%,
            #F8FAFC 100%
        );
}

.main .block-container {

    max-width: none !important;

    width: 100% !important;

    padding-top: 2rem !important;

    padding-left: 2rem !important;

    padding-right: 2rem !important;

    padding-bottom: 2rem !important;
}


.dashboard-title {

    color: #0F172A;

    font-size: 32px;

    font-weight: 700;

    margin-bottom: 5px;
}


.dashboard-subtitle {

    color: #64748B;

    font-size: 16px;

    margin-bottom: 25px;
}


[data-testid="stMetric"] {

    background: white;

    padding: 20px;

    border-radius: 14px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0px 4px 15px rgba(15,23,42,0.08);
}


[data-testid="stSidebar"] {

    background-color: #0F172A;
}


[data-testid="stSidebar"] * {

    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 📊 PIM Dashboard"
    )

    st.markdown("---")


    page = st.radio(

        "Navigation",

        [
            "Home",
            "Schools",
            "Teachers",
            "Visits",
            "Standards",
            "Reports"
        ]
    )


    st.markdown("---")


    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.rerun()


# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        '<div class="dashboard-title">Dashboard Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Monitor classroom observation performance and visits.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_schools = df["School Name"].nunique()

    total_teachers = df["Teacher Name"].nunique()

    total_visits = int(
        df[total_visit_cols].sum().sum()
    )


    total_standard = int(
        df[minimum_standard_cols].sum().sum()
    )


    total_possible_standard = (

        df[minimum_standard_cols]
        .notna()
        .sum()
        .sum()
    )


    if total_possible_standard > 0:

        standard_percentage = (
            total_standard
            / total_possible_standard
            * 100
        )

    else:

        standard_percentage = 0


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Schools",
            f"{total_schools:,}"
        )


    with col2:

        st.metric(
            "Total Teachers",
            f"{total_teachers:,}"
        )


    with col3:

        st.metric(
            "Total Visits",
            f"{total_visits:,}"
        )


    with col4:

        st.metric(
            "Standards Met",
            f"{standard_percentage:.1f}%"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # MONTHLY VISITS CHART
    # --------------------------------------------------------

    st.subheader("Monthly Total Visits")


    fig, ax = plt.subplots(
        figsize=(10, 4)
    )


    ax.plot(

        monthly_visit["Month"],

        monthly_visit["Total_Visit"],

        marker="o"
    )


    for i, value in enumerate(
        monthly_visit["Total_Visit"]
    ):

        ax.text(

            i,

            value,

            str(int(value)),

            ha="center",

            va="bottom"
        )


    ax.set_xlabel("Month")

    ax.set_ylabel("Number of Visits")

    ax.set_title(
        "Monthly Total Visits"
    )


    st.pyplot(
        fig,
        use_container_width=True
    )


# ============================================================
# SCHOOLS
# ============================================================

elif page == "Schools":

    st.markdown(
        '<div class="dashboard-title">School Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'School distribution by RtR staff.'
        '</div>',
        unsafe_allow_html=True
    )


    school_table = (

        df.groupby("RtR Staff Name")

        .agg(
            Schools=(
                "School Name",
                "nunique"
            ),

            Teachers=(
                "Teacher Name",
                "nunique"
            )
        )

        .reset_index()
    )


    st.dataframe(

        school_table,

        use_container_width=True,

        hide_index=True
    )


    st.subheader("School and Teacher Summary")


    st.dataframe(

        school_teacher_summary,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# TEACHERS
# ============================================================

elif page == "Teachers":

    st.markdown(
        '<div class="dashboard-title">Teacher Summary</div>',
        unsafe_allow_html=True
    )


    teacher_table = (

        df.groupby(
            [
                "RtR Staff Name",
                "School Name"
            ]
        )

        .agg(
            Teachers=(
                "Teacher Name",
                "nunique"
            )
        )

        .reset_index()
    )


    st.dataframe(

        teacher_table,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# VISITS
# ============================================================

elif page == "Visits":

    st.markdown(
        '<div class="dashboard-title">Visit Monitoring</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Target visits, actual visits and visit gaps.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    total_target = int(
        Final_Total_Visited["Target_Visit"]
        .sum()
    )


    total_actual = int(
        Final_Total_Visited["Total_visited"]
        .sum()
    )


    total_gap = (
        total_target
        - total_actual
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Target Visits",
            f"{total_target:,}"
        )


    with c2:

        st.metric(
            "Actual Visits",
            f"{total_actual:,}"
        )


    with c3:

        st.metric(
            "Visit Gap",
            f"{total_gap:,}"
        )


    st.markdown("---")


    st.subheader(
        "Staff-wise Visit Performance"
    )


    display_visits = Final_Total_Visited.copy()


    display_visits = display_visits.round(0)


    st.dataframe(

        display_visits,

        use_container_width=True,

        hide_index=True
    )


    # --------------------------------------------------------
    # GRADE-WISE VISITS
    # --------------------------------------------------------

    st.subheader(
        "Grade-wise Visits"
    )


    grade_visit_display = Final_Total_Visited[
        [
            "RtR Staff Name",
            "Visit Grade_1",
            "Visit Grade_2"
        ]
    ].copy()


    st.dataframe(

        grade_visit_display,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# STANDARDS
# ============================================================

elif page == "Standards":

    st.markdown(
        '<div class="dashboard-title">Minimum Standards</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Minimum standards achieved by grade and staff.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TOTALS
    # --------------------------------------------------------

    total_g1 = int(
        min_std[
            "Total Standard Meet_Grade-1"
        ].sum()
    )


    total_g2 = int(
        min_std[
            "Total Standard Meet_Grade-2"
        ].sum()
    )


    total_standard_met = (
        total_g1 + total_g2
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Grade 1 Standards",
            f"{total_g1:,}"
        )


    with c2:

        st.metric(
            "Grade 2 Standards",
            f"{total_g2:,}"
        )


    with c3:

        st.metric(
            "Total Standards Met",
            f"{total_standard_met:,}"
        )


    st.markdown("---")


    st.subheader(
        "Staff-wise Minimum Standards"
    )


    st.dataframe(

        min_std,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.markdown(
        '<div class="dashboard-title">Reports</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Detailed PIM data and analysis.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        staff_options = [
            "All"
        ] + sorted(
            df["RtR Staff Name"]
            .dropna()
            .unique()
            .tolist()
        )


        selected_staff = st.selectbox(
            "RtR Staff",
            staff_options
        )


    with col2:

        grade_options = [
            "All"
        ] + sorted(
            df["Grade"]
            .dropna()
            .unique()
            .tolist()
        )


        selected_grade = st.selectbox(
            "Grade",
            grade_options
        )


    filtered_df = df.copy()


    if selected_staff != "All":

        filtered_df = filtered_df[
            filtered_df["RtR Staff Name"]
            == selected_staff
        ]


    if selected_grade != "All":

        filtered_df = filtered_df[
            filtered_df["Grade"]
            == selected_grade
        ]


    st.write(
        f"Showing {len(filtered_df):,} records"
    )


    st.dataframe(

        filtered_df,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94A3B8;
        padding:30px 0 10px 0;
        font-size:13px;
    ">
        PIM Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
