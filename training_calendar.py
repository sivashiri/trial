import streamlit as st
import pandas as pd

from components.calendar import (
    render_calendar,
    upcoming_trainings
)

# ---------------------------------------------------------
# TRAINING CALENDAR PAGE
# ---------------------------------------------------------

def show_calendar(df):

    st.markdown(
        """
        <h2 style="margin-bottom:0px;">
        📅 Training Calendar
        </h2>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "View all planned and completed trainings."
    )

    st.write("")

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    left, right = st.columns([1, 1])

    with left:

        employee = st.selectbox(
            "Employee",
            ["All"] + sorted(df["Employee Name"].unique())
        )

    with right:

        category = st.selectbox(
            "Training Category",
            ["All"] + sorted(df["Training Category"].unique())
        )

    filtered = df.copy()

    if employee != "All":
        filtered = filtered[
            filtered["Employee Name"] == employee
        ]

    if category != "All":
        filtered = filtered[
            filtered["Training Category"] == category
        ]

    st.write("")

    # -----------------------------------------------------
    # KPI ROW
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total",
        len(filtered)
    )

    c2.metric(
        "Planned",
        len(filtered[
            filtered["Status"] == "Planned"
        ])
    )

    c3.metric(
        "Executed",
        len(filtered[
            filtered["Status"] == "Executed"
        ])
    )

    c4.metric(
        "Overdue",
        len(filtered[
            filtered["Status"] == "Overdue"
        ])
    )

    st.write("")

    # -----------------------------------------------------
    # CALENDAR + UPCOMING
    # -----------------------------------------------------

    left, right = st.columns([4, 1.3])

    with left:

        render_calendar(filtered)

    with right:

        upcoming_trainings(filtered)

    st.write("")

    # -----------------------------------------------------
    # LEGEND
    # -----------------------------------------------------

    st.markdown("### Status Legend")

    l1, l2, l3 = st.columns(3)

    l1.success("🟢 Executed")

    l2.info("🔵 Planned")

    l3.warning("🟠 Overdue")

    st.divider()

    # -----------------------------------------------------
    # TRAINING LIST
    # -----------------------------------------------------

    st.subheader("Training Schedule")

    display = filtered[
        [
            "Planned Date",
            "Employee Name",
            "Training",
            "Department",
            "Trainer",
            "Status",
            "Score",
        ]
    ].sort_values("Planned Date")

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------------------------
    # MONTHLY SUMMARY
    # -----------------------------------------------------

    st.write("")

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Training Trend")

        trend = (
            filtered.groupby(
                filtered["Planned Date"].dt.date
            )
            .size()
            .reset_index(name="Trainings")
        )

        if len(trend):

            st.line_chart(
                trend.set_index("Planned Date")
            )

    with right:

        st.subheader("Status Distribution")

        status = (
            filtered["Status"]
            .value_counts()
        )

        st.bar_chart(status)
