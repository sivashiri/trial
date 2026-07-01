import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import os

st.set_page_config(page_title="Enterprise LMS Dashboard", layout="wide", page_icon="📅")

# Load or generate data
@st.cache_data
def load_data():
    if os.path.exists("data/lms_data.csv"):
        df = pd.read_csv("data/lms_data.csv")
        df['Planned Date'] = pd.to_datetime(df['Planned Date'])
        df['Completion Date'] = pd.to_datetime(df['Completion Date'])
        return df
    else:
        # Generate sample data
        np.random.seed(42)
        dates = pd.date_range(start='2025-06-01', periods=100)
        data = {
            'Training': np.random.choice(['Safety Induction', 'Leadership Skills', 'Python for Data Science', 'Process Safety', 'Fire Safety Training', 'Confined Space Entry', 'First Aid Training'], 100),
            'Category': np.random.choice(['Safety', 'Technical', 'Leadership', 'Soft Skills'], 100),
            'Planned Date': np.random.choice(dates, 100),
            'Department': np.random.choice(['Engineering', 'Operations', 'HSE', 'Maintenance'], 100),
            'Status': np.random.choice(['Planned', 'In Progress', 'Completed', 'Cancelled'], 100, p=[0.4, 0.25, 0.3, 0.05]),
            'Score': np.random.randint(70, 100, 100)
        }
        df = pd.DataFrame(data)
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/lms_data.csv', index=False)
        return df

df = load_data()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=LMS", use_column_width=True)
    st.title("LMS DASHBOARD")
    page = st.radio("Menu", ["Overview", "Calendar", "Training Plans", "Training Execution", "Reports"])

st.title("Enterprise LMS Dashboard – Calendar View & Training Tracker")
st.markdown("**Track Training Plans & Execution Effortlessly**")

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Trainings", "82", "📊")
col2.metric("Planned", "47", "📅")
col3.metric("In Progress", "21", "🔄")
col4.metric("Completed", "14", "✅")
col5.metric("Cancelled", "5", "❌")

if page == "Calendar":
    st.subheader("Calendar View - June 2025")
    
    # Simple Calendar Simulation
    calendar_cols = st.columns(7)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        with calendar_cols[i]:
            st.markdown(f"**{day}**")
    
    # Sample Calendar Grid (you can enhance with streamlit-calendar later)
    st.info("Interactive Calendar View - Click on dates to see scheduled trainings")
    st.dataframe(df[['Training', 'Planned Date', 'Status']].head(15), use_container_width=True)

elif page == "Training Plans":
    st.subheader("Training Plans")
    st.dataframe(df, use_container_width=True)

elif page == "Training Execution":
    st.subheader("Training Execution Tracker")
    execution = df.groupby('Status').size().reset_index(name='Count')
    fig = px.pie(execution, names='Status', values='Count', title="Training Status Breakdown")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Reports":
    st.subheader("Training Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Completion Rate", "68.3%")
        st.metric("Compliance Rate", "76.4%")
    with col2:
        st.metric("Avg Score", "86.4%")
        st.metric("Expired Trainings", "3")

# Footer
st.caption("Enterprise LMS Dashboard | Built with Streamlit")
