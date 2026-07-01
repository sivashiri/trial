import os
import random
import pandas as pd
from datetime import timedelta

random.seed(42)

first_names = [
    "Aarav", "Aditya", "Arjun", "Dev", "Rohan",
    "Saanvi", "Ananya", "Isha", "Priya", "Sneha",
    "Kiran", "Neha", "Vikram", "Rahul", "Pooja",
    "Riya", "Snehal", "Aditi", "Nisha", "Sana"
]

last_names = [
    "Sharma", "Kumar", "Gupta", "Rao", "Menon",
    "Singh", "Patel", "Nair", "Iyer", "Joshi",
    "Desai", "Das", "Chakraborty", "Jain", "Kapoor",
    "Ghosh", "Mathur", "Verma", "Bhat", "Shah"
]


def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------

OUTPUT_FOLDER = "data"
OUTPUT_FILE = "training_data.csv"

NUM_EMPLOYEES = 50

# -------------------------------------------------------
# MASTER DATA
# -------------------------------------------------------

departments = [
    "Production",
    "Maintenance",
    "Quality",
    "EHS",
    "Warehouse",
    "Engineering",
]

designations = [
    "Operator",
    "Senior Operator",
    "Technician",
    "Engineer",
    "Executive",
    "Supervisor",
]

locations = [
    "Chennai",
    "Mumbai",
    "Bengaluru",
]

trainers = [
    "Rahul Sharma",
    "Priya Menon",
    "Anil Kumar",
    "Sanjay Gupta",
    "Sneha Rao",
]

training_master = [
    ("Site HSSE Induction","Induction",365),
    ("Site Risks & Prevention","Safety",365),
    ("SLPia","Safety",365),
    ("Management of Change","Process Safety",365),
    ("CoW","Permit",365),
    ("Energy Isolation","Safety",365),
    ("Hot Work","Permit",365),
    ("Working at Height","Safety",365),
    ("LSR Work Authorisation","Safety",365),
    ("Confined Space Entry","Safety",365),
    ("Lifting & Line of Fire","Safety",365),
    ("AGT","Operations",365),
    ("Confined Watch","Safety",365),
    ("Fire Watch","Safety",365),
    ("Working with Contractor","Safety",365),
    ("Fire Fighting","Emergency",365),
    ("Spill Response","Emergency",365),
    ("First Aid","Emergency",365),
    ("Emergency Response Plan","Emergency",365),
    ("Use & Care of PPE","Safety",365),
]

# -------------------------------------------------------
# EMPLOYEE MASTER
# -------------------------------------------------------

employees = []

for i in range(NUM_EMPLOYEES):

    employees.append({
        "Employee ID": f"EMP{i+1:03}",
        "Employee Name": generate_name(),
        "Department": random.choice(departments),
        "Designation": random.choice(designations)
    })

# -------------------------------------------------------
# CREATE TRAINING RECORDS
# -------------------------------------------------------

records = []

months = [6,7]

for emp in employees:

    trainings = random.sample(training_master, random.randint(8,14))

    for training_name, category, validity in trainings:

        month = random.choice(months)

        planned_date = pd.Timestamp(
            year=2025,
            month=month,
            day=random.randint(1,28)
        )

        probability = random.random()

        if probability < 0.65:

            completion_date = planned_date + timedelta(
                days=random.randint(0,5)
            )

            status = "Executed"

        elif probability < 0.90:

            completion_date = pd.NaT

            status = "Planned"

        else:

            completion_date = pd.NaT

            status = "Overdue"

        score = ""

        if status == "Executed":
            score = random.randint(75,100)

        expiry = ""

        certificate = "Pending"

        if status == "Executed":

            expiry = completion_date + timedelta(days=validity)

            certificate = "Issued"

        compliance = "No"

        if status == "Executed":
            compliance = "Yes"

        records.append({

            "Employee ID": emp["Employee ID"],
            "Employee Name": emp["Employee Name"],
            "Department": emp["Department"],
            "Designation": emp["Designation"],

            "Training Category": category,
            "Training": training_name,

            "Trainer": random.choice(trainers),
            "Location": random.choice(locations),

            "Planned Date": planned_date,

            "Completion Date": completion_date,

            "Status": status,

            "Score": score,

            "Validity (Days)": validity,

            "Expiry Date": expiry,

            "Compliance": compliance,

            "Certificate Status": certificate,

            "Year": 2025,

            "Month": planned_date.strftime("%B"),

            "Quarter": "Q2" if month == 6 else "Q3"

        })

# -------------------------------------------------------
# SAVE
# -------------------------------------------------------

df = pd.DataFrame(records)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df.to_csv(
    os.path.join(OUTPUT_FOLDER, OUTPUT_FILE),
    index=False
)

print("="*60)
print("Dataset Created Successfully")
print("="*60)
print(df.head())
print()
print("Total Records :", len(df))
print("Employees     :", df["Employee ID"].nunique())
print("Trainings     :", df["Training"].nunique())
print("Saved To      :", os.path.join(OUTPUT_FOLDER, OUTPUT_FILE))
import sys
import streamlit as st
import pandas as pd
from pathlib import Path

# ensure local imports work when running from the app directory
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------

st.set_page_config(
    page_title="Enterprise LMS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------
# LOAD CSS
# --------------------------------------------------------

css_file = Path("assets/style.css")

if css_file.exists():
    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# --------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/training_data.csv")

    df["Planned Date"] = pd.to_datetime(df["Planned Date"])

    df["Completion Date"] = pd.to_datetime(
        df["Completion Date"],
        errors="coerce"
    )

    return df


df = load_data()

# --------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------

st.sidebar.title("🎓 Enterprise LMS")

page = st.sidebar.radio(
    "Navigation",
    [
        "Training Calendar",
        "Employee Training"
    ]
)

st.sidebar.divider()

months = sorted(df["Month"].unique())

selected_month = st.sidebar.selectbox(
    "Month",
    months
)

status_filter = st.sidebar.multiselect(
    "Training Status",
    ["Planned","Executed","Overdue"],
    default=["Planned","Executed","Overdue"]
)

department = st.sidebar.multiselect(
    "Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

# --------------------------------------------------------
# FILTER DATA
# --------------------------------------------------------

filtered = df[
    (df["Month"] == selected_month)
    &
    (df["Status"].isin(status_filter))
    &
    (df["Department"].isin(department))
]

# --------------------------------------------------------
# KPI CARDS
# --------------------------------------------------------

def metric_card(title, value, color):

    st.markdown(
        f"""
        <div style="
        background:white;
        padding:18px;
        border-radius:14px;
        border-left:6px solid {color};
        box-shadow:0 2px 8px rgba(0,0,0,.08);
        ">
            <div style="font-size:14px;color:gray;">
                {title}
            </div>

            <div style="
            font-size:34px;
            font-weight:bold;
            color:{color};
            ">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------------
# HEADER
# --------------------------------------------------------

st.title("Enterprise Learning Management System")

st.caption(
    "Training Planning & Execution Dashboard"
)

c1,c2,c3,c4 = st.columns(4)

with c1:
    metric_card(
        "Total Trainings",
        len(filtered),
        "#2563eb"
    )

with c2:
    metric_card(
        "Planned",
        len(filtered[filtered.Status=="Planned"]),
        "#3b82f6"
    )

with c3:
    metric_card(
        "Executed",
        len(filtered[filtered.Status=="Executed"]),
        "#22c55e"
    )

with c4:
    metric_card(
        "Overdue",
        len(filtered[filtered.Status=="Overdue"]),
        "#f97316"
    )

st.divider()

# --------------------------------------------------------
# PAGE VIEWS
# --------------------------------------------------------

def show_calendar(filtered):

    st.subheader("Training Calendar")

    if filtered.empty:
        st.info("No training records match the selected filters.")
        return

    st.write(
        filtered.sort_values("Planned Date").reset_index(drop=True)
    )


def show_employee(filtered):

    st.subheader("Employee Training")

    employees = sorted(filtered["Employee Name"].unique())

    if not employees:
        st.info("No training records match the selected filters.")
        return

    selected_employee = st.selectbox("Select Employee", employees)

    emp_df = filtered[filtered["Employee Name"] == selected_employee]

    st.write(
        emp_df.sort_values("Planned Date").reset_index(drop=True)
    )

# --------------------------------------------------------
# ROUTING
# --------------------------------------------------------

if page == "Training Calendar":

    show_calendar(filtered)

elif page == "Employee Training":

    show_employee(filtered)
import calendar
from datetime import datetime
import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

STATUS_COLORS = {
    "Planned": "#2563EB",      # Blue
    "Executed": "#16A34A",     # Green
    "Overdue": "#EA580C"       # Orange
}


# ---------------------------------------------------------
# EVENT CARD
# ---------------------------------------------------------

def event_card(row):

    color = STATUS_COLORS.get(row["Status"], "#94A3B8")

    return f"""
    <div style="
        background:{color};
        color:white;
        border-radius:7px;
        padding:4px 6px;
        margin-top:4px;
        font-size:11px;
        overflow:hidden;
        white-space:nowrap;
        text-overflow:ellipsis;
        line-height:1.2;
    ">
        {row["Training"]}
    </div>
    """


# ---------------------------------------------------------
# BUILD MONTHLY CALENDAR
# ---------------------------------------------------------

def monthly_calendar(df, year, month):

    cal = calendar.Calendar(firstweekday=6)

    month_days = cal.monthdayscalendar(year, month)

    today = datetime.today()

    html = """

    <style>

    .calendar{

        display:grid;
        grid-template-columns:repeat(7,1fr);
        gap:10px;

    }

    .header{

        background:#F8FAFC;

        text-align:center;

        padding:10px;

        font-weight:700;

        border-radius:8px;

        border:1px solid #E2E8F0;

    }

    .day{

        min-height:140px;

        background:white;

        border-radius:10px;

        border:1px solid #E5E7EB;

        padding:8px;

        transition:0.2s;

        box-shadow:0 1px 4px rgba(0,0,0,.05);

    }

    .day:hover{

        transform:translateY(-2px);

        box-shadow:0 6px 18px rgba(0,0,0,.10);

    }

    .today{

        border:2px solid #2563EB;

    }

    .date{

        font-weight:700;

        color:#374151;

        margin-bottom:6px;

        font-size:14px;

    }

    .empty{

        visibility:hidden;

        min-height:140px;

    }

    </style>

    """

    html += '<div class="calendar">'

    for day in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:

        html += f'<div class="header">{day}</div>'

    for week in month_days:

        for day in week:

            if day == 0:

                html += '<div class="empty"></div>'

                continue

            current_date = pd.Timestamp(year, month, day)

            events = df[df["Planned Date"] == current_date]

            classes = "day"

            if (
                today.year == year
                and today.month == month
                and today.day == day
            ):

                classes += " today"

            html += f'<div class="{classes}">'

            html += f'<div class="date">{day}</div>'

            if len(events):

                for _, row in events.iterrows():

                    html += event_card(row)

            html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# RIGHT PANEL
# ---------------------------------------------------------

def upcoming_trainings(df):

    st.markdown("### Upcoming Trainings")

    planned = df[df["Status"] == "Planned"].sort_values("Planned Date")

    if planned.empty:

        st.success("No planned trainings.")

        return

    for _, row in planned.head(10).iterrows():

        st.markdown(
            f"""
            <div style="
                background:white;
                border-radius:10px;
                padding:12px;
                margin-bottom:10px;
                border-left:5px solid #2563EB;
                box-shadow:0 1px 4px rgba(0,0,0,.05);
            ">

            <b>{row["Training"]}</b><br>

            👤 {row["Employee Name"]}<br>

            📅 {row["Planned Date"].strftime("%d %b %Y")}<br>

            🏢 {row["Department"]}

            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# LEGEND
# ---------------------------------------------------------

def legend():

    st.markdown(
        """
        <div style="display:flex;gap:20px;margin-bottom:15px;">

        <div>
        <span style="
        background:#2563EB;
        width:14px;
        height:14px;
        display:inline-block;
        border-radius:4px;"></span>

        Planned

        </div>

        <div>
        <span style="
        background:#16A34A;
        width:14px;
        height:14px;
        display:inline-block;
        border-radius:4px;"></span>

        Executed

        </div>

        <div>
        <span style="
        background:#EA580C;
        width:14px;
        height:14px;
        display:inline-block;
        border-radius:4px;"></span>

        Overdue

        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# MAIN CALENDAR VIEW
# ---------------------------------------------------------

def show_month(df, year, month):

    left, right = st.columns([3.6, 1.2])

    with left:

        legend()

        monthly_calendar(df, year, month)

    with right:

        upcoming_trainings(df)
# pages/training_calendar.py

import streamlit as st


# ---------------------------------------------------------
# TRAINING CALENDAR PAGE
# ---------------------------------------------------------

def show_calendar(df):

    st.markdown(
        """
        <h2 style="margin-bottom:5px;">
            📅 Training Calendar
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "View planned, executed and overdue trainings."
    )

    st.write("")

    # -----------------------------------------------------
    # MONTH SELECTION
    # -----------------------------------------------------

    month_lookup = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }

    months = list(month_lookup.keys())

    available_months = sorted(
        df["Month"].dropna().unique(),
        key=lambda x: month_lookup[x]
    )

    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:

        selected_month = st.selectbox(
            "Month",
            available_months
        )

    with col3:

        year = st.selectbox(
            "Year",
            sorted(df["Year"].unique())
        )

    month_number = month_lookup[selected_month]

    filtered = df[
        (df["Month"] == selected_month)
        &
        (df["Year"] == year)
    ]

    st.write("")

    # -----------------------------------------------------
    # SUMMARY BAR
    # -----------------------------------------------------

    total = len(filtered)

    planned = len(
        filtered[
            filtered["Status"] == "Planned"
        ]
    )

    executed = len(
        filtered[
            filtered["Status"] == "Executed"
        ]
    )

    overdue = len(
        filtered[
            filtered["Status"] == "Overdue"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Trainings",
        total
    )

    c2.metric(
        "Planned",
        planned
    )

    c3.metric(
        "Executed",
        executed
    )

    c4.metric(
        "Overdue",
        overdue
    )

    st.write("")

    # -----------------------------------------------------
    # CALENDAR
    # -----------------------------------------------------

    show_month(
        filtered,
        year,
        month_number
    )

    st.write("")

    # -----------------------------------------------------
    # TRAINING LIST
    # -----------------------------------------------------

    with st.expander(
        "📋 Training Schedule",
        expanded=False
    ):

        table = filtered[
            [
                "Planned Date",
                "Training",
                "Employee Name",
                "Department",
                "Trainer",
                "Status",
            ]
        ].sort_values("Planned Date")

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

    # -----------------------------------------------------
    # STATUS DISTRIBUTION
    # -----------------------------------------------------

    st.write("")

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Daily Training Count")

        daily = (
            filtered.groupby(
                filtered["Planned Date"].dt.date
            )
            .size()
            .reset_index(name="Trainings")
        )

        st.bar_chart(
            daily.set_index("Planned Date")
        )

    with right:

        st.subheader("Status Summary")

        status = (
            filtered["Status"]
            .value_counts()
        )

        st.dataframe(
            status,
            use_container_width=True
        )
# pages/employee_training.py

import streamlit as st
import pandas as pd


# ---------------------------------------------------------
# STATUS COLORS
# ---------------------------------------------------------

STATUS_COLOR = {
    "Executed": "#16A34A",
    "Planned": "#2563EB",
    "Overdue": "#EA580C"
}


# ---------------------------------------------------------
# EMPLOYEE PAGE
# ---------------------------------------------------------

def show_employee(df):

    st.title("👨‍💼 Employee Training")

    st.caption("Track employee learning progress and compliance")

    st.write("")

    # ---------------------------------------------------------
    # FILTERS
    # ---------------------------------------------------------

    left, right = st.columns([2, 1])

    with left:

        employee = st.selectbox(
            "Employee",
            sorted(df["Employee Name"].unique())
        )

    with right:

        department = st.selectbox(
            "Department",
            ["All"] + sorted(df["Department"].unique())
        )

    emp_df = df[df["Employee Name"] == employee]

    if department != "All":
        emp_df = emp_df[emp_df["Department"] == department]

    if emp_df.empty:
        st.warning("No records found.")
        return

    # ---------------------------------------------------------
    # EMPLOYEE INFORMATION
    # ---------------------------------------------------------

    info = emp_df.iloc[0]

    total = len(emp_df)

    completed = len(emp_df[emp_df["Status"] == "Executed"])

    planned = len(emp_df[emp_df["Status"] == "Planned"])

    overdue = len(emp_df[emp_df["Status"] == "Overdue"])

    progress = round((completed / total) * 100)

    st.write("")

    col1, col2 = st.columns([1.3, 2])

    # ---------------------------------------------------------
    # PROFILE CARD
    # ---------------------------------------------------------

    with col1:

        st.markdown(
            f"""
            <div style="
            background:white;
            padding:20px;
            border-radius:15px;
            box-shadow:0 2px 10px rgba(0,0,0,.08);
            ">

            <h3>{info['Employee Name']}</h3>

            <hr>

            <b>Employee ID</b><br>
            {info['Employee ID']}<br><br>

            <b>Department</b><br>
            {info['Department']}<br><br>

            <b>Designation</b><br>
            {info['Designation']}<br><br>

            </div>

            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.subheader("Completion")

        st.progress(progress / 100)

        st.markdown(f"### {progress}%")

    # ---------------------------------------------------------
    # KPI
    # ---------------------------------------------------------

    with col2:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total", total)

        c2.metric("Executed", completed)

        c3.metric("Planned", planned)

        c4.metric("Overdue", overdue)

        st.write("")

        # ---------------------------------------------------------
        # TRAINING HISTORY
        # ---------------------------------------------------------

        st.subheader("Training History")

        history = emp_df.sort_values("Planned Date")

        for _, row in history.iterrows():

            color = STATUS_COLOR[row["Status"]]

            if row["Status"] == "Executed":
                icon = "✅"

            elif row["Status"] == "Planned":
                icon = "📘"

            else:
                icon = "⚠️"

            completion = "-"

            if pd.notna(row["Completion Date"]):
                completion = row["Completion Date"].strftime("%d %b %Y")

            score = "-"

            if pd.notna(row["Score"]):
                score = row["Score"]

            st.markdown(
                f"""
                <div style="
                background:white;
                border-left:6px solid {color};
                padding:14px;
                border-radius:12px;
                margin-bottom:10px;
                box-shadow:0 1px 6px rgba(0,0,0,.05);
                ">

                <b>{icon} {row['Training']}</b>

                <br>

                Category :
                {row['Training Category']}

                <br>

                Planned :
                {row['Planned Date'].strftime('%d %b %Y')}

                <br>

                Completed :
                {completion}

                <br>

                Trainer :
                {row['Trainer']}

                <br>

                Status :
                <span style="color:{color};font-weight:bold;">
                {row['Status']}
                </span>

                <br>

                Score :
                {score}

                </div>

                """,
                unsafe_allow_html=True,
            )

    # ---------------------------------------------------------
    # CERTIFICATES
    # ---------------------------------------------------------

    st.write("")

    left, right = st.columns(2)

    with left:

        st.subheader("Certificate Status")

        cert = emp_df[
            [
                "Training",
                "Certificate Status",
                "Expiry Date",
            ]
        ]

        st.dataframe(
            cert,
            hide_index=True,
            use_container_width=True,
        )

    # ---------------------------------------------------------
    # UPCOMING
    # ---------------------------------------------------------

    with right:

        st.subheader("Upcoming Trainings")

        upcoming = emp_df[
            emp_df["Status"] == "Planned"
        ].sort_values("Planned Date")

        if upcoming.empty:

            st.success("No upcoming trainings.")

        else:

            for _, row in upcoming.iterrows():

                st.info(
                    f"""
**{row['Training']}**

📅 {row['Planned Date'].strftime('%d %b %Y')}

👨‍🏫 {row['Trainer']}

📍 {row['Location']}
"""
                )

    # ---------------------------------------------------------
    # FULL TABLE
    # ---------------------------------------------------------

    st.write("")

    with st.expander("View Complete Training Records"):

        st.dataframe(
            emp_df.sort_values("Planned Date"),
            use_container_width=True,
            hide_index=True,
        )
