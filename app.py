import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Enterprise LMS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    df=pd.read_csv("data/training_data.csv")

    df["Planned Date"]=pd.to_datetime(df["Planned Date"])

    df["Completion Date"]=pd.to_datetime(
        df["Completion Date"],
        errors="coerce"
    )

    df["Expiry Date"]=pd.to_datetime(
        df["Expiry Date"],
        errors="coerce"
    )

    return df


df=load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("🎓 Enterprise LMS")

page=st.sidebar.radio(

    "Navigation",

    [

        "Training Calendar",

        "Employee Training"

    ]

)

st.sidebar.divider()

month=st.sidebar.selectbox(

    "Month",

    sorted(df["Month"].unique())

)

status=st.sidebar.multiselect(

    "Status",

    [

        "Planned",

        "Executed",

        "Overdue"

    ],

    default=[

        "Planned",

        "Executed",

        "Overdue"

    ]

)

department=st.sidebar.multiselect(

    "Department",

    sorted(df["Department"].unique()),

    default=sorted(df["Department"].unique())

)

filtered=df[
    (df["Month"]==month)
    &
    (df["Status"].isin(status))
    &
    (df["Department"].isin(department))
]

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🎓 Enterprise Learning Management System")

st.caption("Training Planning & Execution Dashboard")

st.divider()

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

c1,c2,c3,c4=st.columns(4)

c1.metric("Total Trainings",len(filtered))

c2.metric(

    "Planned",

    len(filtered[filtered["Status"]=="Planned"])

)

c3.metric(

    "Executed",

    len(filtered[filtered["Status"]=="Executed"])

)

c4.metric(

    "Overdue",

    len(filtered[filtered["Status"]=="Overdue"])

)

st.divider()

# -------------------------------------------------
# ROUTING
# -------------------------------------------------

if page=="Training Calendar":

    from pages.training_calendar import show_calendar

    show_calendar(filtered)

else:

    from pages.employee_training import show_employee

    show_employee(filtered)
