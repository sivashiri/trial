"""
Enterprise LMS Dashboard - Synthetic Data Generator
Generates realistic training compliance data for testing and demo
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class DataGenerator:
    """Generate synthetic LMS training data"""
    
    def __init__(self, num_records=500, seed=42):
        self.num_records = num_records
        np.random.seed(seed)
        random.seed(seed)
        
        self.departments = [
            'Engineering', 'Operations', 'Sales', 'HR', 'Finance',
            'Marketing', 'IT', 'Legal', 'Supply Chain', 'Quality Assurance'
        ]
        
        self.designations = [
            'Engineer', 'Manager', 'Senior Manager', 'Director',
            'Executive', 'Coordinator', 'Specialist', 'Analyst',
            'Lead', 'Trainee', 'Associate', 'Officer'
        ]
        
        self.training_categories = [
            'Compliance', 'Technical', 'Leadership', 'Safety',
            'Software', 'Soft Skills', 'HSSE', 'Quality',
            'Customer Service', 'Product Knowledge'
        ]
        
        self.trainings = {
            'Compliance': [
                'Annual Safety Training', 'Data Privacy Compliance',
                'Code of Conduct', 'Anti-Corruption Training',
                'Environmental Compliance', 'Labor Law Compliance'
            ],
            'Technical': [
                'Advanced Python', 'Cloud Architecture',
                'Data Analytics', 'System Design', 'DevOps Essentials',
                'Database Management', 'API Development'
            ],
            'Leadership': [
                'Effective Leadership', 'Team Management',
                'Conflict Resolution', 'Decision Making',
                'Strategic Planning', 'Emotional Intelligence'
            ],
            'Safety': [
                'Workplace Safety', 'Fire Safety', 'Chemical Safety',
                'Ergonomics', 'First Aid', 'Emergency Response'
            ],
            'Software': [
                'Microsoft Office', 'Salesforce', 'SAP Basics',
                'Project Management Tools', 'Communication Tools',
                'CRM Systems', 'ERP Systems'
            ],
            'Soft Skills': [
                'Communication', 'Critical Thinking', 'Problem Solving',
                'Time Management', 'Presentation Skills',
                'Negotiation', 'Customer Focus'
            ],
            'HSSE': [
                'Health & Safety Awareness', 'Environmental Protection',
                'Sustainable Practices', 'Risk Management',
                'Hazard Identification', 'Incident Reporting'
            ],
            'Quality': [
                'Quality Management Systems', 'ISO Certification',
                'Six Sigma Basics', 'Kaizen', 'Root Cause Analysis',
                'Process Improvement'
            ],
            'Customer Service': [
                'Customer Relations', 'Service Excellence',
                'Complaint Handling', 'Customer Retention',
                'Feedback Management', 'Service Recovery'
            ],
            'Product Knowledge': [
                'Product Features', 'Market Trends', 'Competitor Analysis',
                'Product Roadmap', 'Sales Techniques', 'Industry Insights'
            ]
        }
        
        self.locations = [
            'New York', 'Los Angeles', 'Chicago', 'Houston',
            'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego',
            'Dallas', 'San Jose', 'Austin', 'Seattle', 'Denver',
            'Boston', 'Miami', 'Atlanta', 'Remote'
        ]
        
        self.trainers = [
            'John Smith', 'Sarah Johnson', 'Michael Chen', 'Emily Davis',
            'Robert Wilson', 'Jennifer Martinez', 'David Brown', 'Lisa Anderson',
            'James Taylor', 'Maria Garcia', 'William Moore', 'Patricia Jackson'
        ]
        
        self.statuses = ['Completed', 'In Progress', 'Not Started', 'Overdue', 'Failed', 'Expired']
    
    def generate_employee_id(self, index):
        """Generate unique employee ID"""
        return f"EMP{str(index).zfill(6)}"
    
    def generate_employee_name(self):
        """Generate random employee name"""
        first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'Robert', 'Emily',
            'David', 'Lisa', 'James', 'Patricia', 'William', 'Maria',
            'Richard', 'Jennifer', 'Joseph', 'Linda', 'Thomas', 'Barbara',
            'Charles', 'Susan', 'Christopher', 'Nancy', 'Daniel', 'Karen'
        ]
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
            'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez',
            'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore',
            'Jackson', 'Martin', 'Lee', 'White', 'Harris', 'Sanchez'
        ]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def generate_dates(self):
        """Generate planned and completion dates"""
        today = datetime.now()
        
        # Planned date: past 6 months to future 6 months
        planned_offset = random.randint(-180, 180)
        planned_date = today + timedelta(days=planned_offset)
        
        # Completion date based on status
        status = random.choice(self.statuses)
        
        if status in ['Completed', 'Expired']:
            # Completed between planned date and 30 days after
            completion_offset = random.randint(0, 30)
            completion_date = planned_date + timedelta(days=completion_offset)
        elif status == 'Overdue':
            completion_date = None
        elif status == 'In Progress':
            completion_date = None
        elif status == 'Not Started':
            completion_date = None
        elif status == 'Failed':
            # Failed before deadline or shortly after
            completion_offset = random.randint(0, 15)
            completion_date = planned_date + timedelta(days=completion_offset)
        
        return planned_date, completion_date, status
    
    def calculate_validity_and_expiry(self, completion_date, status):
        """Calculate validity period and expiry date"""
        if status not in ['Completed', 'Expired']:
            return None, None
        
        # Validity periods in days based on training type
        validity_options = [30, 90, 180, 365, 730]  # 1 month to 2 years
        validity_days = random.choice(validity_options)
        
        if completion_date:
            expiry_date = completion_date + timedelta(days=validity_days)
        else:
            expiry_date = None
        
        return validity_days, expiry_date
    
    def calculate_days_remaining(self, expiry_date):
        """Calculate days remaining for certificate"""
        if not expiry_date:
            return None
        
        today = datetime.now().date()
        expiry = expiry_date.date() if isinstance(expiry_date, datetime) else expiry_date
        days_remaining = (expiry - today).days
        return max(0, days_remaining)
    
    def generate_alert(self, days_remaining, status):
        """Generate alert based on days remaining"""
        if status == 'Expired' or (days_remaining is not None and days_remaining == 0):
            return 'EXPIRED'
        elif days_remaining is not None:
            if days_remaining <= 7:
                return 'CRITICAL'
            elif days_remaining <= 30:
                return 'WARNING'
            elif days_remaining <= 90:
                return 'INFO'
        
        if status == 'Overdue':
            return 'OVERDUE'
        elif status == 'Not Started':
            return 'PENDING'
        
        return 'NONE'
    
    def generate_compliance_status(self, status, alert):
        """Generate compliance status"""
        if status == 'Completed' and alert != 'EXPIRED':
            return 'COMPLIANT'
        elif status in ['Overdue', 'Not Started'] or alert == 'EXPIRED':
            return 'NON-COMPLIANT'
        elif status == 'In Progress':
            return 'IN PROGRESS'
        else:
            return 'NON-COMPLIANT'
    
    def generate_certificate_status(self, status):
        """Generate certificate status"""
        if status == 'Completed':
            return 'ISSUED'
        elif status == 'In Progress':
            return 'PENDING'
        elif status == 'Failed':
            return 'FAILED'
        else:
            return 'NOT APPLICABLE'
    
    def generate_score(self, status):
        """Generate training score"""
        if status == 'Completed':
            return random.randint(75, 100)
        elif status == 'In Progress':
            return random.randint(30, 70)
        elif status == 'Failed':
            return random.randint(0, 45)
        else:
            return None
    
    def generate_data(self):
        """Generate complete dataset"""
        data = []
        
        for i in range(self.num_records):
            employee_id = self.generate_employee_id(i + 1)
            employee_name = self.generate_employee_name()
            department = random.choice(self.departments)
            designation = random.choice(self.designations)
            
            category = random.choice(list(self.training_categories))
            training = random.choice(self.trainings[category])
            trainer = random.choice(self.trainers)
            location = random.choice(self.locations)
            
            planned_date, completion_date, status = self.generate_dates()
            validity_days, expiry_date = self.calculate_validity_and_expiry(completion_date, status)
            days_remaining = self.calculate_days_remaining(expiry_date)
            alert = self.generate_alert(days_remaining, status)
            compliance = self.generate_compliance_status(status, alert)
            certificate_status = self.generate_certificate_status(status)
            
            score = self.generate_score(status)
            
            # Extract temporal features
            year = planned_date.year
            month = planned_date.month
            quarter = (month - 1) // 3 + 1
            
            data.append({
                'Employee ID': employee_id,
                'Employee Name': employee_name,
                'Department': department,
                'Designation': designation,
                'Training Category': category,
                'Training': training,
                'Trainer': trainer,
                'Location': location,
                'Planned Date': planned_date,
                'Completion Date': completion_date,
                'Status': status,
                'Score': score,
                'Validity (Days)': validity_days,
                'Expiry Date': expiry_date,
                'Days Remaining': days_remaining,
                'Alert': alert,
                'Compliance': compliance,
                'Certificate Status': certificate_status,
                'Year': year,
                'Month': month,
                'Quarter': f'Q{quarter}'
            })
        
        return pd.DataFrame(data)
    
    def save_to_csv(self, filepath='data/lms_training_data.csv'):
        """Generate and save data to CSV"""
        df = self.generate_data()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
        return df


def generate_and_save_data(num_records=500, filepath='data/lms_training_data.csv'):
    """Convenience function to generate and save data"""
    generator = DataGenerator(num_records=num_records)
    return generator.save_to_csv(filepath)


if __name__ == "__main__":
    # Generate 500 records
    print("Generating LMS training data...")
    generator = DataGenerator(num_records=500)
    df = generator.save_to_csv('data/lms_training_data.csv')
    
    print(f"\nGenerated {len(df)} records")
    print("\nData Preview:")
    print(df.head(10))
    
    print("\nData Info:")
    print(df.info())
    
    print("\nStatistics:")
    print(f"Total Employees: {df['Employee ID'].nunique()}")
    print(f"Departments: {df['Department'].nunique()}")
    print(f"Trainings: {df['Training'].nunique()}")
    print(f"Compliance Rate: {(df['Compliance'] == 'COMPLIANT').sum() / len(df) * 100:.1f}%")
    """
Configuration and constants for LMS Dashboard
"""

import os
from datetime import datetime

# ============= APPLICATION SETTINGS =============
APP_NAME = "Enterprise LMS Dashboard"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False") == "True"

# ============= DATA PATHS =============
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "lms_training_data.csv")
CACHE_DIR = os.path.join(DATA_DIR, "cache")

# ============= DISPLAY SETTINGS =============
PAGE_TITLE = "Enterprise LMS Dashboard"
PAGE_ICON = "📚"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ============= COLORS & STYLING =============
COLOR_PALETTE = {
    'primary': '#0066CC',
    'secondary': '#00CCFF',
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'info': '#17A2B8',
    'light': '#F8F9FA',
    'dark': '#343A40'
}

STATUS_COLORS = {
    'Completed': '#28A745',  # Green
    'In Progress': '#17A2B8',  # Blue
    'Not Started': '#6C757D',  # Gray
    'Overdue': '#DC3545',  # Red
    'Failed': '#721C24',  # Dark Red
    'Expired': '#FFC107'  # Yellow
}

ALERT_COLORS = {
    'CRITICAL': '#DC3545',
    'WARNING': '#FFC107',
    'INFO': '#17A2B8',
    'PENDING': '#6C757D',
    'OVERDUE': '#DC3545',
    'EXPIRED': '#FFC107',
    'NONE': '#28A745'
}

COMPLIANCE_COLORS = {
    'COMPLIANT': '#28A745',
    'NON-COMPLIANT': '#DC3545',
    'IN PROGRESS': '#17A2B8'
}

# ============= TRAINING CATEGORIES =============
TRAINING_CATEGORIES = [
    'Compliance', 'Technical', 'Leadership', 'Safety',
    'Software', 'Soft Skills', 'HSSE', 'Quality',
    'Customer Service', 'Product Knowledge'
]

# ============= STATUS OPTIONS =============
STATUS_OPTIONS = [
    'Completed', 'In Progress', 'Not Started', 'Overdue', 'Failed', 'Expired'
]

COMPLIANCE_OPTIONS = ['COMPLIANT', 'NON-COMPLIANT', 'IN PROGRESS']

ALERT_OPTIONS = ['CRITICAL', 'WARNING', 'INFO', 'PENDING', 'OVERDUE', 'EXPIRED', 'NONE']

CERTIFICATE_OPTIONS = ['ISSUED', 'PENDING', 'FAILED', 'NOT APPLICABLE']

# ============= PAGINATION =============
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ============= CACHE SETTINGS =============
CACHE_TTL = 3600  # 1 hour in seconds
CACHE_MAX_ENTRIES = 1000

# ============= REPORT SETTINGS =============
REPORT_FORMATS = ['CSV', 'Excel', 'PDF']
REPORT_DEFAULT_FORMAT = 'CSV'

# ============= CHART SETTINGS =============
CHART_HEIGHT = 400
CHART_WIDTH = 600
CHART_COLOR_PALETTE = [
    '#0066CC', '#00CCFF', '#28A745', '#FFC107',
    '#DC3545', '#17A2B8', '#6C757D', '#007BFF'
]

# ============= ALERT THRESHOLDS =============
ALERT_THRESHOLDS = {
    'days_critical': 7,      # Days remaining for CRITICAL alert
    'days_warning': 30,      # Days remaining for WARNING alert
    'days_info': 90,         # Days remaining for INFO alert
    'compliance_target': 95  # Target compliance percentage
}

# ============= ROLE PERMISSIONS =============
ROLE_PERMISSIONS = {
    'admin': [
        'view_dashboard',
        'view_reports',
        'manage_users',
        'manage_courses',
        'export_data',
        'send_alerts',
        'view_analytics'
    ],
    'manager': [
        'view_dashboard',
        'view_reports',
        'view_team_data',
        'export_data',
        'view_analytics'
    ],
    'employee': [
        'view_dashboard',
        'view_my_courses',
        'download_certificate'
    ],
    'trainer': [
        'view_dashboard',
        'view_reports',
        'manage_courses',
        'grade_assessments'
    ]
}

# ============= METRIC DEFINITIONS =============
METRICS = {
    'total_employees': 'Total Employees',
    'total_trainings': 'Total Trainings Assigned',
    'completion_rate': 'Completion Rate (%)',
    'compliance_rate': 'Compliance Rate (%)',
    'average_score': 'Average Score',
    'overdue_trainings': 'Overdue Trainings',
    'expiring_soon': 'Expiring Soon (30 days)',
    'expired_certificates': 'Expired Certificates'
}

# ============= DATE FORMATS =============
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DISPLAY_DATE_FORMAT = '%B %d, %Y'
DISPLAY_DATETIME_FORMAT = '%B %d, %Y %I:%M %p'

# ============= EMAIL SETTINGS =============
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "False") == "True"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "lms@company.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

# ============= DATABASE SETTINGS (IF USING) =============
USE_DATABASE = os.getenv("USE_DATABASE", "False") == "True"
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "lms_db")

# ============= LOGGING SETTINGS =============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.path.join(DATA_DIR, "lms.log")

# ============= FEATURE FLAGS =============
FEATURES = {
    'enable_reports': True,
    'enable_exports': True,
    'enable_alerts': True,
    'enable_analytics': True,
    'enable_forecasting': False,
    'enable_ml_recommendations': False
}

# ============= DATA QUALITY RULES =============
DATA_QUALITY = {
    'min_score': 0,
    'max_score': 100,
    'min_validity_days': 1,
    'max_validity_days': 1095  # 3 years
}

# ============= PAGE CONFIGURATIONS =============
PAGES = {
    'dashboard': {
        'title': 'Dashboard',
        'icon': '📊',
        'description': 'Overview of training compliance metrics'
    },
    'training_tracker': {
        'title': 'Training Tracker',
        'icon': '📋',
        'description': 'Track individual training progress'
    },
    'analytics': {
        'title': 'Analytics',
        'icon': '📈',
        'description': 'Advanced analytics and insights'
    },
    'reporting': {
        'title': 'Reports',
        'icon': '📄',
        'description': 'Generate and download reports'
    },
    'settings': {
        'title': 'Settings',
        'icon': '⚙️',
        'description': 'Configure dashboard and preferences'
    }
}

# ============= EXPORT COLUMN MAPPING =============
EXPORT_COLUMNS = {
    'Employee ID': 'Employee ID',
    'Employee Name': 'Employee Name',
    'Department': 'Department',
    'Designation': 'Designation',
    'Training Category': 'Training Category',
    'Training': 'Training',
    'Trainer': 'Trainer',
    'Location': 'Location',
    'Planned Date': 'Planned Date',
    'Completion Date': 'Completion Date',
    'Status': 'Status',
    'Score': 'Score',
    'Validity (Days)': 'Validity (Days)',
    'Expiry Date': 'Expiry Date',
    'Days Remaining': 'Days Remaining',
    'Alert': 'Alert Status',
    'Compliance': 'Compliance Status',
    'Certificate Status': 'Certificate Status'
}

# ============= VALIDATION RULES =============
VALIDATION_RULES = {
    'employee_id': r'^EMP\d{6}$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'score': {'min': 0, 'max': 100},
    'days_remaining': {'min': 0}
}
"""
Data Manager - Handles data loading, caching, and processing
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import os
from config import DATA_FILE, DATA_DIR, DATE_FORMAT
import logging

logger = logging.getLogger(__name__)


class DataManager:
    """Manage LMS training data"""
    
    def __init__(self):
        self.df = None
        self.df_filtered = None
        self.cache = {}
    
    @st.cache_data(ttl=3600)
    def load_data(_self, filepath=DATA_FILE):
        """Load data from CSV with caching"""
        try:
            if not os.path.exists(filepath):
                logger.error(f"Data file not found: {filepath}")
                return None
            
            df = pd.read_csv(filepath)
            
            # Convert date columns
            date_columns = ['Planned Date', 'Completion Date', 'Expiry Date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Ensure numeric columns
            numeric_columns = ['Score', 'Validity (Days)', 'Days Remaining']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            logger.info(f"Loaded {len(df)} records from {filepath}")
            return df
        
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None
    
    def get_data(self, filepath=DATA_FILE):
        """Get loaded data"""
        if self.df is None:
            self.df = self.load_data(filepath)
        return self.df
    
    def apply_filters(self, df, filters):
        """Apply multiple filters to dataframe"""
        df_filtered = df.copy()
        
        if not filters:
            return df_filtered
        
        # Department filter
        if 'department' in filters and filters['department']:
            df_filtered = df_filtered[df_filtered['Department'].isin(filters['department'])]
        
        # Status filter
        if 'status' in filters and filters['status']:
            df_filtered = df_filtered[df_filtered['Status'].isin(filters['status'])]
        
        # Compliance filter
        if 'compliance' in filters and filters['compliance']:
            df_filtered = df_filtered[df_filtered['Compliance'].isin(filters['compliance'])]
        
        # Alert filter
        if 'alert' in filters and filters['alert']:
            df_filtered = df_filtered[df_filtered['Alert'].isin(filters['alert'])]
        
        # Training category filter
        if 'category' in filters and filters['category']:
            df_filtered = df_filtered[df_filtered['Training Category'].isin(filters['category'])]
        
        # Location filter
        if 'location' in filters and filters['location']:
            df_filtered = df_filtered[df_filtered['Location'].isin(filters['location'])]
        
        # Date range filter
        if 'date_range' in filters and filters['date_range']:
            start_date, end_date = filters['date_range']
            df_filtered = df_filtered[
                (df_filtered['Planned Date'].dt.date >= start_date) &
                (df_filtered['Planned Date'].dt.date <= end_date)
            ]
        
        # Score range filter
        if 'score_range' in filters and filters['score_range']:
            min_score, max_score = filters['score_range']
            df_filtered = df_filtered[
                (df_filtered['Score'].fillna(0) >= min_score) &
                (df_filtered['Score'].fillna(0) <= max_score)
            ]
        
        # Days remaining filter
        if 'days_remaining' in filters and filters['days_remaining']:
            min_days, max_days = filters['days_remaining']
            df_filtered = df_filtered[
                (df_filtered['Days Remaining'].fillna(0) >= min_days) &
                (df_filtered['Days Remaining'].fillna(0) <= max_days)
            ]
        
        # Search/text filter
        if 'search' in filters and filters['search']:
            search_text = filters['search'].lower()
            mask = df_filtered['Employee Name'].str.lower().str.contains(search_text) | \
                   df_filtered['Employee ID'].str.lower().str.contains(search_text) | \
                   df_filtered['Training'].str.lower().str.contains(search_text)
            df_filtered = df_filtered[mask]
        
        return df_filtered
    
    def get_summary_metrics(self, df):
        """Calculate key metrics"""
        if df is None or len(df) == 0:
            return {}
        
        total_records = len(df)
        unique_employees = df['Employee ID'].nunique()
        unique_trainings = df['Training'].nunique()
        
        # Status counts
        status_counts = df['Status'].value_counts()
        completed_count = len(df[df['Status'] == 'Completed'])
        overdue_count = len(df[df['Status'] == 'Overdue'])
        in_progress_count = len(df[df['Status'] == 'In Progress'])
        not_started_count = len(df[df['Status'] == 'Not Started'])
        failed_count = len(df[df['Status'] == 'Failed'])
        
        # Rates
        completion_rate = (completed_count / total_records * 100) if total_records > 0 else 0
        compliance_rate = (len(df[df['Compliance'] == 'COMPLIANT']) / total_records * 100) if total_records > 0 else 0
        
        # Scores
        average_score = df[df['Score'].notna()]['Score'].mean() if 'Score' in df.columns else 0
        max_score = df['Score'].max() if 'Score' in df.columns else 0
        min_score = df[df['Score'] > 0]['Score'].min() if 'Score' in df.columns else 0
        
        # Expiry information
        expired_count = len(df[df['Alert'] == 'EXPIRED'])
        expiring_soon = len(df[(df['Days Remaining'] <= 30) & (df['Days Remaining'] > 0)])
        
        # Time metrics
        total_training_hours = (df['Validity (Days)'] / 30).sum() if 'Validity (Days)' in df.columns else 0
        
        return {
            'total_records': total_records,
            'unique_employees': unique_employees,
            'unique_trainings': unique_trainings,
            'completed': completed_count,
            'overdue': overdue_count,
            'in_progress': in_progress_count,
            'not_started': not_started_count,
            'failed': failed_count,
            'completion_rate': round(completion_rate, 2),
            'compliance_rate': round(compliance_rate, 2),
            'average_score': round(average_score, 2),
            'max_score': max_score,
            'min_score': min_score,
            'expired_count': expired_count,
            'expiring_soon': expiring_soon,
            'total_training_hours': round(total_training_hours, 2)
        }
    
    def get_department_summary(self, df):
        """Get summary by department"""
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        summary = df.groupby('Department').agg({
            'Employee ID': 'count',
            'Status': lambda x: (x == 'Completed').sum(),
            'Compliance': lambda x: (x == 'COMPLIANT').sum(),
            'Score': 'mean'
        }).round(2)
        
        summary.columns = ['Total Trainings', 'Completed', 'Compliant', 'Avg Score']
        summary['Completion Rate %'] = (summary['Completed'] / summary['Total Trainings'] * 100).round(2)
        summary['Compliance Rate %'] = (summary['Compliant'] / summary['Total Trainings'] * 100).round(2)
        
        return summary.sort_values('Completion Rate %', ascending=False)
    
    def get_training_category_summary(self, df):
        """Get summary by training category"""
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        summary = df.groupby('Training Category').agg({
            'Employee ID': 'count',
            'Status': lambda x: (x == 'Completed').sum(),
            'Alert': lambda x: (x == 'CRITICAL').sum(),
            'Score': 'mean'
        }).round(2)
        
        summary.columns = ['Total Trainings', 'Completed', 'Critical Alerts', 'Avg Score']
        summary['Completion Rate %'] = (summary['Completed'] / summary['Total Trainings'] * 100).round(2)
        
        return summary.sort_values('Completion Rate %', ascending=False)
    
    def get_location_summary(self, df):
        """Get summary by location"""
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        summary = df.groupby('Location').agg({
            'Employee ID': 'count',
            'Status': lambda x: (x == 'Completed').sum(),
            'Score': 'mean'
        }).round(2)
        
        summary.columns = ['Total Trainings', 'Completed', 'Avg Score']
        summary['Completion Rate %'] = (summary['Completed'] / summary['Total Trainings'] * 100).round(2)
        
        return summary.sort_values('Completion Rate %', ascending=False)
    
    def get_compliance_detail(self, df, employee_id):
        """Get detailed compliance record for an employee"""
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        employee_df = df[df['Employee ID'] == employee_id].copy()
        return employee_df[[
            'Training', 'Training Category', 'Status', 'Planned Date',
            'Completion Date', 'Score', 'Expiry Date', 'Days Remaining',
            'Alert', 'Compliance', 'Certificate Status'
        ]]
    
    def get_overdue_trainings(self, df):
        """Get overdue trainings"""
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        overdue = df[df['Status'] == 'Overdue'].copy()
        return overdue[[
            'Employee ID', 'Employee Name', 'Department', 'Training',
            'Training Category', 'Planned Date', 'Alert'
        ]].sort_values('Employee Name')
    
    def get_expiring_certifications(self, df, days=30):
        """Get certifications expiring within specified days"""
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        today = pd.Timestamp.now()
        target_date = today + timedelta(days=days)
        
        expiring = df[
            (df['Days Remaining'] <= days) & 
            (df['Days Remaining'] > 0) &
            (df['Certificate Status'] == 'ISSUED')
        ].copy()
        
        return expiring[[
            'Employee ID', 'Employee Name', 'Department', 'Training',
            'Expiry Date', 'Days Remaining'
        ]].sort_values('Days Remaining')
    
    def get_employee_list(self, df):
        """Get unique list of employees"""
        if df is None or len(df) == 0:
            return []
        return sorted(df['Employee ID'].unique().tolist())
    
    def get_departments(self, df):
        """Get unique departments"""
        if df is None or len(df) == 0:
            return []
        return sorted(df['Department'].unique().tolist())
    
    def get_training_categories(self, df):
        """Get unique training categories"""
        if df is None or len(df) == 0:
            return []
        return sorted(df['Training Category'].unique().tolist())
    
    def get_locations(self, df):
        """Get unique locations"""
        if df is None or len(df) == 0:
            return []
        return sorted(df['Location'].unique().tolist())
    
    def get_statuses(self, df):
        """Get unique statuses"""
        if df is None or len(df) == 0:
            return []
        return sorted(df['Status'].unique().tolist())
    
    def get_trainers(self, df):
        """Get unique trainers"""
        if df is None or len(df) == 0:
            return []
        return sorted(df['Trainer'].unique().tolist())
    
    def export_to_csv(self, df, filename='export.csv'):
        """Export dataframe to CSV"""
        try:
            filepath = os.path.join(DATA_DIR, filename)
            df.to_csv(filepath, index=False)
            logger.info(f"Data exported to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return None
    
    def export_to_excel(self, df, filename='export.xlsx'):
        """Export dataframe to Excel"""
        try:
            filepath = os.path.join(DATA_DIR, filename)
            df.to_excel(filepath, index=False, sheet_name='Training Data')
            logger.info(f"Data exported to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return None


# Global instance
@st.cache_resource
def get_data_manager():
    """Get global data manager instance"""
    return DataManager()
"""
Dashboard Components - Reusable UI components for the LMS dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import (
    COLOR_PALETTE, STATUS_COLORS, ALERT_COLORS, COMPLIANCE_COLORS,
    CHART_HEIGHT, CHART_WIDTH, METRICS
)
from datetime import datetime


class DashboardComponents:
    """Reusable dashboard components"""
    
    @staticmethod
    def render_metric_card(label, value, subtext="", col=None):
        """Render a metric card"""
        if col:
            with col:
                st.metric(label=label, value=value, delta=subtext)
        else:
            st.metric(label=label, value=value, delta=subtext)
    
    @staticmethod
    def render_kpi_row(metrics_dict, num_cols=4):
        """Render row of KPI cards"""
        cols = st.columns(num_cols)
        
        items = list(metrics_dict.items())
        for idx, (label, value) in enumerate(items):
            if idx < len(cols):
                with cols[idx]:
                    st.metric(label, value)
    
    @staticmethod
    def render_status_distribution(df):
        """Render status distribution chart"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        status_counts = df['Status'].value_counts()
        colors = [STATUS_COLORS.get(status, '#999999') for status in status_counts.index]
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color=status_counts.index,
            color_discrete_map=STATUS_COLORS,
            title="Training Status Distribution"
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_compliance_distribution(df):
        """Render compliance distribution chart"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        compliance_counts = df['Compliance'].value_counts()
        
        fig = px.pie(
            values=compliance_counts.values,
            names=compliance_counts.index,
            color=compliance_counts.index,
            color_discrete_map=COMPLIANCE_COLORS,
            title="Compliance Status Distribution"
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_department_performance(df):
        """Render department performance chart"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        dept_summary = df.groupby('Department').agg({
            'Status': lambda x: (x == 'Completed').sum(),
            'Employee ID': 'count'
        }).reset_index()
        
        dept_summary.columns = ['Department', 'Completed', 'Total']
        dept_summary['Completion Rate'] = (dept_summary['Completed'] / dept_summary['Total'] * 100).round(2)
        dept_summary = dept_summary.sort_values('Completion Rate', ascending=True)
        
        fig = px.barh(
            dept_summary,
            x='Completion Rate',
            y='Department',
            color='Completion Rate',
            color_continuous_scale='RdYlGn',
            title="Completion Rate by Department",
            text='Completion Rate',
            range_color=[0, 100]
        )
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400, xaxis_title="Completion Rate (%)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_training_category_performance(df):
        """Render training category performance"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        cat_summary = df.groupby('Training Category').agg({
            'Status': lambda x: (x == 'Completed').sum(),
            'Employee ID': 'count'
        }).reset_index()
        
        cat_summary.columns = ['Category', 'Completed', 'Total']
        cat_summary['Completion Rate'] = (cat_summary['Completed'] / cat_summary['Total'] * 100).round(2)
        cat_summary = cat_summary.sort_values('Completion Rate', ascending=False)
        
        fig = px.bar(
            cat_summary,
            x='Category',
            y='Completion Rate',
            color='Completion Rate',
            color_continuous_scale='Blues',
            title="Completion Rate by Training Category",
            text='Completion Rate',
            range_color=[0, 100]
        )
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400, xaxis_title="", yaxis_title="Completion Rate (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_alert_distribution(df):
        """Render alert status distribution"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        alert_counts = df['Alert'].value_counts()
        
        fig = px.bar(
            x=alert_counts.index,
            y=alert_counts.values,
            color=alert_counts.index,
            color_discrete_map=ALERT_COLORS,
            title="Alert Distribution",
            text=alert_counts.values,
            labels={'x': 'Alert Status', 'y': 'Count'}
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_score_distribution(df):
        """Render score distribution histogram"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        scores = df[df['Score'].notna()]['Score']
        
        fig = px.histogram(
            x=scores,
            nbins=20,
            title="Score Distribution",
            labels={'x': 'Score', 'count': 'Number of Records'},
            color_discrete_sequence=[COLOR_PALETTE['primary']]
        )
        
        fig.add_vline(
            x=scores.mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {scores.mean():.1f}",
            annotation_position="top right"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_timeline(df):
        """Render training timeline"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        # Create monthly summary
        df_temp = df.copy()
        df_temp['Year-Month'] = df_temp['Planned Date'].dt.to_period('M')
        monthly = df_temp.groupby('Year-Month').size()
        
        fig = px.line(
            x=monthly.index.astype(str),
            y=monthly.values,
            markers=True,
            title="Training Volume Timeline",
            labels={'x': 'Month', 'y': 'Number of Trainings'}
        )
        
        fig.update_traces(line=dict(color=COLOR_PALETTE['primary'], width=3))
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_location_performance(df):
        """Render location performance chart"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        loc_summary = df.groupby('Location').agg({
            'Status': lambda x: (x == 'Completed').sum(),
            'Employee ID': 'count'
        }).reset_index()
        
        loc_summary.columns = ['Location', 'Completed', 'Total']
        loc_summary['Completion Rate'] = (loc_summary['Completed'] / loc_summary['Total'] * 100).round(2)
        loc_summary = loc_summary.sort_values('Completion Rate', ascending=False).head(10)
        
        fig = px.bar(
            loc_summary,
            x='Completion Rate',
            y='Location',
            orientation='h',
            color='Completion Rate',
            color_continuous_scale='Viridis',
            title="Top 10 Locations by Completion Rate",
            text='Completion Rate',
            range_color=[0, 100]
        )
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_data_table(df, title="Data Table", max_rows=100):
        """Render interactive data table"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        st.subheader(title)
        
        # Display table
        display_df = df.head(max_rows).copy()
        
        # Format dates
        date_cols = display_df.select_dtypes(include=['datetime64']).columns
        for col in date_cols:
            display_df[col] = display_df[col].dt.strftime('%Y-%m-%d')
        
        st.dataframe(display_df, use_container_width=True, height=400)
        
        st.caption(f"Showing {min(len(df), max_rows)} of {len(df)} records")
    
    @staticmethod
    def render_filter_panel():
        """Render filter panel in sidebar"""
        st.sidebar.header("🔍 Filters")
        
        filters = {}
        
        # Search
        filters['search'] = st.sidebar.text_input("Search by name or ID", "")
        
        # Department
        filters['department'] = st.sidebar.multiselect(
            "Department",
            options=['All Departments'],  # Will be populated dynamically
            default=['All Departments']
        )
        
        # Status
        filters['status'] = st.sidebar.multiselect(
            "Status",
            options=['Completed', 'In Progress', 'Not Started', 'Overdue', 'Failed', 'Expired'],
            default=['Completed', 'In Progress']
        )
        
        # Compliance
        filters['compliance'] = st.sidebar.multiselect(
            "Compliance Status",
            options=['COMPLIANT', 'NON-COMPLIANT', 'IN PROGRESS'],
            default=['COMPLIANT']
        )
        
        # Alert
        filters['alert'] = st.sidebar.multiselect(
            "Alert Status",
            options=['CRITICAL', 'WARNING', 'INFO', 'NONE'],
            default=[]
        )
        
        return filters
    
    @staticmethod
    def render_employee_card(employee_data):
        """Render employee information card"""
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.write(f"**ID:** {employee_data.get('Employee ID', 'N/A')}")
            with col2:
                st.write(f"**Name:** {employee_data.get('Employee Name', 'N/A')}")
            with col3:
                st.write(f"**Dept:** {employee_data.get('Department', 'N/A')}")
    
    @staticmethod
    def render_stats_section(metrics_dict):
        """Render statistics section"""
        cols = st.columns(len(metrics_dict))
        
        for idx, (key, value) in enumerate(metrics_dict.items()):
            with cols[idx]:
                st.metric(key, value)
    
    @staticmethod
    def render_alert_badge(alert_status):
        """Render alert status badge"""
        color = ALERT_COLORS.get(alert_status, '#999999')
        
        # Return HTML for badge (for use in tables)
        return f'<span style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{alert_status}</span>'
    
    @staticmethod
    def render_status_badge(status):
        """Render status badge"""
        color = STATUS_COLORS.get(status, '#999999')
        return f'<span style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{status}</span>'
    
    @staticmethod
    def render_compliance_badge(compliance):
        """Render compliance badge"""
        color = COMPLIANCE_COLORS.get(compliance, '#999999')
        return f'<span style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{compliance}</span>'
    
    @staticmethod
    def render_progress_bar(value, max_value=100):
        """Render progress bar"""
        percentage = min(value / max_value * 100, 100) if max_value > 0 else 0
        return st.progress(int(percentage) / 100)
    
    @staticmethod
    def render_info_box(title, content, info_type="info"):
        """Render information box"""
        if info_type == "success":
            st.success(f"✅ {title}: {content}")
        elif info_type == "warning":
            st.warning(f"⚠️ {title}: {content}")
        elif info_type == "error":
            st.error(f"❌ {title}: {content}")
        else:
            st.info(f"ℹ️ {title}: {content}")
    
    @staticmethod
    def render_metric_comparison(df, metric_col, title=""):
        """Render metric comparison across categories"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        comparison = df.groupby('Department')[metric_col].agg(['mean', 'min', 'max']).reset_index()
        comparison = comparison.sort_values('mean', ascending=False)
        
        fig = px.bar(
            comparison,
            x='Department',
            y='mean',
            error_y='mean',
            title=f"{title} by Department",
            labels={'mean': 'Average', 'Department': ''}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_heatmap(df, x_col, y_col, value_col):
        """Render heatmap chart"""
        if df is None or len(df) == 0:
            st.warning("No data available")
            return
        
        pivot_data = df.pivot_table(
            values=value_col,
            index=y_col,
            columns=x_col,
            aggfunc='mean'
        )
        
        fig = px.imshow(
            pivot_data,
            labels=dict(x=x_col, y=y_col, color=value_col),
            color_continuous_scale='RdYlGn',
            title=f"{value_col} by {x_col} and {y_col}"
        )
        
        st.plotly_chart(fig, use_container_width=True)


# Exported functions for easy access
def render_kpi_cards(metrics):
    """Convenience function to render KPI cards"""
    DashboardComponents.render_kpi_row(metrics)


def render_status_chart(df):
    """Convenience function to render status chart"""
    DashboardComponents.render_status_distribution(df)
"""
Enterprise LMS Dashboard - Main Application
Built with Streamlit for interactive training compliance tracking
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from config import (
    APP_NAME, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE,
    DATA_FILE, ALERT_THRESHOLDS, FEATURES
)
from data_manager import get_data_manager
from dashboard_components import DashboardComponents
from generate_data import DataGenerator

# ============= LOGGING SETUP =============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============= PAGE CONFIGURATION =============
st.set_page_config(
    page_title=APP_NAME,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE
)

# ============= CUSTOM STYLING =============
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0066CC;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066CC;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .danger-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# ============= SESSION STATE INITIALIZATION =============
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = get_data_manager()

if 'df' not in st.session_state:
    st.session_state.df = None

if 'df_filtered' not in st.session_state:
    st.session_state.df_filtered = None

if 'filters' not in st.session_state:
    st.session_state.filters = {}

# ============= SIDEBAR NAVIGATION =============
def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown(f"# {APP_NAME}")
        st.divider()
        
        # Navigation
        page = st.radio(
            "Select Page",
            options=['📊 Dashboard', '📋 Training Tracker', '📈 Analytics', '📄 Reports', '⚙️ Settings'],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Data management
        st.subheader("📁 Data Management")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state.df = None
            st.rerun()
        
        if st.button("📥 Generate Sample Data", use_container_width=True):
            with st.spinner("Generating data..."):
                generator = DataGenerator(num_records=500)
                generator.save_to_csv(DATA_FILE)
                st.session_state.df = None
                st.success("Sample data generated successfully!")
                st.rerun()
        
        st.divider()
        
        # Info
        st.caption("**Version:** 1.0.0")
        st.caption("**Last Updated:** " + datetime.now().strftime("%B %d, %Y"))
        
        return page

# ============= MAIN DASHBOARD PAGE =============
def render_dashboard():
    """Render main dashboard page"""
    st.markdown('<h1 class="main-header">📊 Training Compliance Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available. Please generate sample data from the sidebar.")
        return
    
    # Filters
    with st.sidebar:
        st.subheader("🔍 Filters")
        
        search = st.text_input("Search by name or ID", "")
        departments = st.multiselect("Department", options=dm.get_departments(df), default=[])
        statuses = st.multiselect("Status", options=dm.get_statuses(df), default=[])
        
        filters = {
            'search': search,
            'department': departments if departments else None,
            'status': statuses if statuses else None
        }
    
    # Apply filters
    df_filtered = dm.apply_filters(df, filters)
    
    # Metrics
    metrics = dm.get_summary_metrics(df_filtered)
    
    # KPI Section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Total Trainings",
            metrics.get('total_records', 0),
            delta=f"Employees: {metrics.get('unique_employees', 0)}"
        )
    
    with col2:
        st.metric(
            "✅ Completion Rate",
            f"{metrics.get('completion_rate', 0)}%",
            delta=f"Completed: {metrics.get('completed', 0)}"
        )
    
    with col3:
        st.metric(
            "🎯 Compliance Rate",
            f"{metrics.get('compliance_rate', 0)}%",
            delta=f"Compliant: {metrics.get('unique_employees', 0)}"
        )
    
    with col4:
        st.metric(
            "⚠️ Overdue",
            metrics.get('overdue', 0),
            delta=f"Failed: {metrics.get('failed', 0)}"
        )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Training Status Distribution")
        DashboardComponents.render_status_distribution(df_filtered)
    
    with col2:
        st.subheader("Compliance Status Distribution")
        DashboardComponents.render_compliance_distribution(df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Completion Rate by Department")
        DashboardComponents.render_department_performance(df_filtered)
    
    with col2:
        st.subheader("Completion Rate by Category")
        DashboardComponents.render_training_category_performance(df_filtered)
    
    # Additional metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Alert Distribution")
        DashboardComponents.render_alert_distribution(df_filtered)
    
    with col2:
        st.subheader("Score Distribution")
        DashboardComponents.render_score_distribution(df_filtered)

# ============= TRAINING TRACKER PAGE =============
def render_training_tracker():
    """Render training tracker page"""
    st.markdown('<h1 class="main-header">📋 Training Tracker</h1>', unsafe_allow_html=True)
    
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available.")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Overdue Trainings", "Expiring Certifications", "All Trainings"])
    
    with tab1:
        st.subheader("🔴 Overdue Trainings")
        overdue_df = dm.get_overdue_trainings(df)
        
        if len(overdue_df) == 0:
            st.success("No overdue trainings! ✅")
        else:
            st.warning(f"⚠️ {len(overdue_df)} overdue trainings found")
            DashboardComponents.render_data_table(overdue_df, "Overdue Trainings")
    
    with tab2:
        st.subheader("📅 Expiring Certifications (30 days)")
        expiring_df = dm.get_expiring_certifications(df, days=30)
        
        if len(expiring_df) == 0:
            st.success("No certifications expiring soon! ✅")
        else:
            st.warning(f"⚠️ {len(expiring_df)} certifications expiring within 30 days")
            DashboardComponents.render_data_table(expiring_df, "Expiring Certifications")
    
    with tab3:
        st.subheader("📋 All Training Records")
        
        # Filters
        with st.sidebar:
            st.subheader("🔍 Filters")
            
            search = st.text_input("Search", key="tracker_search")
            departments = st.multiselect("Department", options=dm.get_departments(df), key="tracker_dept")
            statuses = st.multiselect("Status", options=dm.get_statuses(df), key="tracker_status")
            
            filters = {
                'search': search,
                'department': departments if departments else None,
                'status': statuses if statuses else None
            }
        
        df_filtered = dm.apply_filters(df, filters)
        DashboardComponents.render_data_table(df_filtered, f"All Trainings ({len(df_filtered)} records)", max_rows=100)

# ============= ANALYTICS PAGE =============
def render_analytics():
    """Render analytics page"""
    st.markdown('<h1 class="main-header">📈 Analytics</h1>', unsafe_allow_html=True)
    
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available.")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Department Analysis", "Location Analysis", "Timeline"])
    
    with tab1:
        st.subheader("🏢 Department Analysis")
        
        dept_summary = dm.get_department_summary(df)
        st.dataframe(dept_summary, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Completion Rate by Department")
            DashboardComponents.render_department_performance(df)
        
        with col2:
            st.subheader("Average Score by Department")
            dept_scores = df.groupby('Department')['Score'].mean().sort_values(ascending=False)
            st.bar_chart(dept_scores)
    
    with tab2:
        st.subheader("📍 Location Analysis")
        
        loc_summary = dm.get_location_summary(df)
        st.dataframe(loc_summary, use_container_width=True)
        
        st.subheader("Performance by Location")
        DashboardComponents.render_location_performance(df)
    
    with tab3:
        st.subheader("📅 Timeline Analysis")
        
        # Monthly statistics
        monthly_stats = df.groupby(df['Planned Date'].dt.to_period('M')).size()
        st.subheader("Training Volume Over Time")
        st.line_chart(monthly_stats)
        
        # Completion trends
        completion_trends = df.groupby(df['Completion Date'].dt.to_period('M')).size()
        st.subheader("Completion Trends")
        st.line_chart(completion_trends)

# ============= REPORTS PAGE =============
def render_reports():
    """Render reports page"""
    st.markdown('<h1 class="main-header">📄 Reports</h1>', unsafe_allow_html=True)
    
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available.")
        return
    
    # Report type selection
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Compliance Summary",
            "Training Status",
            "Department Performance",
            "Employee Compliance",
            "Expiry Calendar"
        ]
    )
    
    if report_type == "Compliance Summary":
        st.subheader("📋 Compliance Summary Report")
        metrics = dm.get_summary_metrics(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", metrics.get('total_records', 0))
        with col2:
            st.metric("Completion Rate %", f"{metrics.get('completion_rate', 0)}")
        with col3:
            st.metric("Compliance Rate %", f"{metrics.get('compliance_rate', 0)}")
        with col4:
            st.metric("Avg Score", f"{metrics.get('average_score', 0)}")
        
        # Export option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv,
            file_name="compliance_summary.csv",
            mime="text/csv"
        )
    
    elif report_type == "Training Status":
        st.subheader("📊 Training Status Report")
        
        status_counts = df['Status'].value_counts()
        st.dataframe(status_counts, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("Status Distribution")
            DashboardComponents.render_status_distribution(df)
        with col2:
            st.write("Status Details")
            status_df = df.groupby('Status').agg({
                'Employee ID': 'count',
                'Score': 'mean'
            }).round(2)
            status_df.columns = ['Count', 'Avg Score']
            st.dataframe(status_df, use_container_width=True)
    
    elif report_type == "Department Performance":
        st.subheader("🏢 Department Performance Report")
        dept_summary = dm.get_department_summary(df)
        st.dataframe(dept_summary, use_container_width=True)
        
        csv = dept_summary.to_csv()
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv,
            file_name="department_performance.csv",
            mime="text/csv"
        )
    
    elif report_type == "Employee Compliance":
        st.subheader("👥 Employee Compliance Report")
        
        employee_id = st.selectbox("Select Employee", options=dm.get_employee_list(df))
        
        if employee_id:
            emp_compliance = dm.get_compliance_detail(df, employee_id)
            st.dataframe(emp_compliance, use_container_width=True)
            
            csv = emp_compliance.to_csv(index=False)
            st.download_button(
                label="📥 Download Employee Report as CSV",
                data=csv,
                file_name=f"employee_{employee_id}_compliance.csv",
                mime="text/csv"
            )
    
    elif report_type == "Expiry Calendar":
        st.subheader("📅 Certificate Expiry Calendar")
        expiring_df = dm.get_expiring_certifications(df, days=90)
        
        if len(expiring_df) > 0:
            st.dataframe(expiring_df, use_container_width=True)
        else:
            st.success("No certifications expiring in the next 90 days!")

# ============= SETTINGS PAGE =============
def render_settings():
    """Render settings page"""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["General", "Data", "About"])
    
    with tab1:
        st.subheader("General Settings")
        
        st.write("**Application Settings**")
        auto_refresh = st.checkbox("Enable Auto-Refresh", value=False)
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval (seconds)", 30, 300, 60)
        
        theme = st.selectbox("Theme", options=["Light", "Dark"])
    
    with tab2:
        st.subheader("Data Management")
        
        st.write("**Data Settings**")
        dm = st.session_state.data_manager
        df = dm.load_data(DATA_FILE)
        
        if df is not None:
            st.metric("Total Records", len(df))
            st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            st.divider()
            
            if st.button("Clear Cache"):
                st.cache_data.clear()
                st.success("Cache cleared!")
            
            if st.button("Reset Data"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                    st.success("Data reset!")
                    st.rerun()
    
    with tab3:
        st.subheader("About")
        
        st.markdown("""
        ### Enterprise LMS Dashboard
        
        **Version:** 1.0.0  
        **Built with:** Streamlit  
        **Purpose:** Training Compliance Tracking
        
        #### Features
        - 📊 Real-time compliance dashboards
        - 📋 Training progress tracking
        - 📈 Advanced analytics
        - 📄 Comprehensive reporting
        - ⚙️ Customizable settings
        
        #### Key Metrics Tracked
        - Training completion rates
        - Compliance status
        - Certificate expiry
        - Employee performance
        - Department analytics
        """)

# ============= MAIN EXECUTION =============
def main():
    """Main application"""
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Route to selected page
    if "Dashboard" in page:
        render_dashboard()
    elif "Training Tracker" in page:
        render_training_tracker()
    elif "Analytics" in page:
        render_analytics()
    elif "Reports" in page:
        render_reports()
    elif "Settings" in page:
        render_settings()

if __name__ == "__main__":
    main()
