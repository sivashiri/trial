import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ========================= CONFIG =========================
st.set_page_config(page_title="Enterprise LMS Dashboard", page_icon="📚", layout="wide")

# ========================= DATA GENERATOR =========================
class DataGenerator:
    def __init__(self, num_records=500, seed=42):
        self.num_records = num_records
        np.random.seed(seed)
        random.seed(seed)
        
        self.departments = ['Engineering', 'Operations', 'Sales', 'HR', 'Finance', 'Marketing', 'IT', 'Legal', 'Supply Chain', 'Quality Assurance']
        self.designations = ['Engineer', 'Manager', 'Senior Manager', 'Director', 'Executive', 'Coordinator', 'Specialist', 'Analyst', 'Lead', 'Trainee']
        self.training_categories = ['Compliance', 'Technical', 'Leadership', 'Safety', 'Software', 'Soft Skills', 'HSSE', 'Quality', 'Customer Service', 'Product Knowledge']
        
        self.trainings = {
            'Compliance': ['Annual Safety Training', 'Data Privacy Compliance', 'Code of Conduct', 'Anti-Corruption Training'],
            'Technical': ['Advanced Python', 'Cloud Architecture', 'Data Analytics', 'DevOps Essentials'],
            'Leadership': ['Effective Leadership', 'Team Management', 'Conflict Resolution'],
            'Safety': ['Workplace Safety', 'Fire Safety', 'First Aid'],
            'Software': ['Microsoft Office', 'Salesforce', 'SAP Basics'],
            'Soft Skills': ['Communication', 'Problem Solving', 'Time Management'],
            'HSSE': ['Health & Safety Awareness', 'Risk Management'],
            'Quality': ['Quality Management Systems', 'Six Sigma Basics'],
            'Customer Service': ['Customer Relations', 'Service Excellence'],
            'Product Knowledge': ['Product Features', 'Market Trends']
        }
        self.locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Remote']
        self.trainers = ['John Smith', 'Sarah Johnson', 'Michael Chen', 'Emily Davis']
        self.statuses = ['Completed', 'In Progress', 'Not Started', 'Overdue', 'Failed', 'Expired']

    def generate_data(self):
        data = []
        today = datetime.now()
        for i in range(self.num_records):
            emp_id = f"EMP{str(i+1).zfill(6)}"
            name = f"Employee {random.randint(100,999)}"
            dept = random.choice(self.departments)
            desig = random.choice(self.designations)
            category = random.choice(self.training_categories)
            training = random.choice(self.trainings[category])
            trainer = random.choice(self.trainers)
            location = random.choice(self.locations)
            
            planned = today + timedelta(days=random.randint(-180, 180))
            status = random.choice(self.statuses)
            
            completion = planned + timedelta(days=random.randint(0, 30)) if status in ['Completed', 'Failed', 'Expired'] else None
            
            validity = random.choice([30, 90, 180, 365]) if status in ['Completed', 'Expired'] else None
            expiry = completion + timedelta(days=validity) if completion and validity else None
            days_remaining = (expiry - today).days if expiry else None
            
            data.append({
                'Employee ID': emp_id,
                'Employee Name': name,
                'Department': dept,
                'Designation': desig,
                'Training Category': category,
                'Training': training,
                'Trainer': trainer,
                'Location': location,
                'Planned Date': planned.date(),
                'Completion Date': completion.date() if completion else None,
                'Status': status,
                'Score': random.randint(75, 100) if status == 'Completed' else None,
                'Validity (Days)': validity,
                'Expiry Date': expiry.date() if expiry else None,
                'Days Remaining': max(0, days_remaining) if days_remaining is not None else None,
                'Alert': 'EXPIRED' if days_remaining and days_remaining <= 0 else 'WARNING' if days_remaining and days_remaining <= 30 else 'NONE',
                'Compliance': 'COMPLIANT' if status == 'Completed' else 'NON-COMPLIANT',
                'Certificate Status': 'ISSUED' if status == 'Completed' else 'PENDING'
            })
        return pd.DataFrame(data)

# Load Data
@st.cache_data(ttl=3600)
def get_data():
    if not os.path.exists("data/lms_training_data.csv"):
        os.makedirs("data", exist_ok=True)
        generator = DataGenerator(500)
        df = generator.generate_data()
        df.to_csv("data/lms_training_data.csv", index=False)
        return df
    else:
        df = pd.read_csv("data/lms_training_data.csv")
        date_cols = ['Planned Date', 'Completion Date', 'Expiry Date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df

df = get_data()

# ========================= UI =========================
st.title("📊 Enterprise LMS Dashboard")

# Sidebar
st.sidebar.header("🔍 Filters")
search = st.sidebar.text_input("Search Employee", "")
departments = st.sidebar.multiselect("Department", options=df['Department'].unique())
statuses = st.sidebar.multiselect("Status", options=df['Status'].unique())

# Apply filters
filtered_df = df.copy()
if search:
    filtered_df = filtered_df[filtered_df['Employee Name'].str.contains(search, case=False) | 
                              filtered_df['Employee ID'].str.contains(search)]
if departments:
    filtered_df = filtered_df[filtered_df['Department'].isin(departments)]
if statuses:
    filtered_df = filtered_df[filtered_df['Status'].isin(statuses)]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trainings", len(filtered_df))
col2.metric("Completion Rate", f"{(filtered_df['Status']=='Completed').mean():.1%}")
col3.metric("Compliance Rate", f"{(filtered_df['Compliance']=='COMPLIANT').mean():.1%}")
col4.metric("Overdue", len(filtered_df[filtered_df['Status']=='Overdue']))

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Training Tracker", "Analytics", "Reports"])

with tab1:
    st.subheader("Status Distribution")
    st.bar_chart(filtered_df['Status'].value_counts())
    
    st.subheader("Department Performance")
    dept_perf = filtered_df.groupby('Department')['Status'].value_counts().unstack().fillna(0)
    st.bar_chart(dept_perf)

with tab2:
    st.subheader("Training Records")
    st.dataframe(filtered_df, use_container_width=True, height=600)

with tab3:
    st.subheader("Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.write("By Department")
        st.bar_chart(filtered_df.groupby('Department').size())
    with col2:
        st.write("By Training Category")
        st.bar_chart(filtered_df.groupby('Training Category').size())

with tab4:
    st.subheader("Export Reports")
    csv = filtered_df.to_csv(index=False)
    st.download_button("Download CSV", csv, "lms_report.csv", "text/csv")
    
    if st.button("Generate New Sample Data"):
        generator = DataGenerator(500)
        df = generator.generate_data()
        df.to_csv("data/lms_training_data.csv", index=False)
        st.success("New data generated!")
        st.rerun()

st.caption("Enterprise LMS Dashboard • Full Featured Single File Version")