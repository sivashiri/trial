import pandas as pd
import random
import os
from faker import Faker
from datetime import timedelta

fake = Faker("en_IN")

random.seed(42)

os.makedirs("data", exist_ok=True)

departments = [
    "Production",
    "Maintenance",
    "Quality",
    "Warehouse",
    "Engineering",
    "EHS"
]

designations = [
    "Operator",
    "Senior Operator",
    "Executive",
    "Technician",
    "Engineer",
    "Supervisor"
]

locations = [
    "Plant 1",
    "Plant 2",
    "Corporate"
]

trainers = [
    "Rahul Sharma",
    "Priya Menon",
    "Anil Kumar",
    "Sneha Rao",
    "Sanjay Gupta"
]

training_list = [

    ("Fire Safety","Safety"),
    ("LOTO","Safety"),
    ("Working at Height","Safety"),
    ("Hot Work","Safety"),
    ("Confined Space Entry","Safety"),
    ("First Aid","Emergency"),
    ("PPE Awareness","Safety"),
    ("Emergency Response","Emergency"),
    ("Permit to Work","Operations"),
    ("5S","Operations")
]

records=[]

for emp in range(1,51):

    emp_id=f"EMP{emp:03}"

    employee=fake.name()

    dept=random.choice(departments)

    desg=random.choice(designations)

    trainings=random.sample(training_list,6)

    for training,category in trainings:

        month=random.choice([6,7])

        planned=pd.Timestamp(
            year=2025,
            month=month,
            day=random.randint(1,28)
        )

        chance=random.random()

        if chance<0.65:

            status="Executed"

            completion=planned+timedelta(days=random.randint(0,5))

            score=random.randint(75,100)

            expiry=completion+timedelta(days=365)

            compliance="Yes"

            certificate="Issued"

        elif chance<0.90:

            status="Planned"

            completion=None

            score=None

            expiry=None

            compliance="No"

            certificate="Pending"

        else:

            status="Overdue"

            completion=None

            score=None

            expiry=None

            compliance="No"

            certificate="Pending"

        records.append({

            "Employee ID":emp_id,

            "Employee Name":employee,

            "Department":dept,

            "Designation":desg,

            "Training Category":category,

            "Training":training,

            "Trainer":random.choice(trainers),

            "Location":random.choice(locations),

            "Planned Date":planned,

            "Completion Date":completion,

            "Status":status,

            "Score":score,

            "Validity (Days)":365,

            "Expiry Date":expiry,

            "Compliance":compliance,

            "Certificate Status":certificate,

            "Year":2025,

            "Month":planned.strftime("%B"),

            "Quarter":"Q2" if month==6 else "Q3"

        })

df=pd.DataFrame(records)

df.to_csv("data/training_data.csv",index=False)

print(df.head())

print(f"\nDataset created successfully.")

print(f"Total Records : {len(df)}")
