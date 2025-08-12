
import random
from faker import Faker
import pandas as pd
from datetime import timedelta, date

fake = Faker()
random.seed(42)

N = 1000
departments = ["Engineering", "Sales", "HR", "Finance", "Product", "Support", "Marketing"]
roles_by_dept = {
    "Engineering": ["Software Engineer", "Senior Engineer", "Tech Lead", "DevOps"],
    "Sales": ["Sales Executive", "Sales Manager", "Account Manager"],
    "HR": ["HR Executive", "HR Manager"],
    "Finance": ["Accountant", "Finance Manager"],
    "Product": ["Product Manager", "Business Analyst"],
    "Support": ["Support Engineer", "Support Lead"],
    "Marketing": ["Marketing Executive", "SEO Specialist"]
}

# FIX: Use datetime.date objects instead of strings
def random_date(start_year=2015, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return fake.date_between(start_date=start, end_date=end)

employees = []
salaries = []
performance = []
exits = []
trainings = []

for i in range(1, N + 1):
    dept = random.choice(departments)
    role = random.choice(roles_by_dept[dept])
    gender = random.choice(["Male", "Female", "Non-binary"])
    first = fake.first_name()
    last = fake.last_name()
    birth = fake.date_of_birth(tzinfo=None, minimum_age=22, maximum_age=60)
    hire = random_date(2015, 2024)
    location = random.choice(["Bangalore", "Pune", "Hyderabad", "Noida", "Chennai", "Mumbai"])
    employees.append({
        "employee_id": i,
        "first_name": first,
        "last_name": last,
        "gender": gender,
        "department": dept,
        "role": role,
        "location": location,
        "birth_date": birth,
        "hire_date": hire
    })

    # Salary: simple base by role seniority
    base = 30000
    if "Senior" in role or "Manager" in role or "Lead" in role:
        base = 90000
    elif "Engineer" in role and dept == "Engineering":
        base = 70000
    elif dept == "Sales":
        base = 40000
    monthly = base + random.randint(-5000, 50000)
    bonus = round(random.uniform(0, 20), 2)
    salaries.append({"employee_id": i, "monthly_salary": monthly, "bonus_percent": bonus})

    # Training hours
    trainings.append({"employee_id": i, "training_hours": round(random.uniform(0, 80), 1)})

    # Performance ratings for years 2021-2024
    for yr in [2021, 2022, 2023, 2024]:
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 40, 30, 10])[0]
        performance.append({"employee_id": i, "year": yr, "performance_rating": rating})

    # Exit: ~18% attrition (random)
    if random.random() < 0.18:
        leave_days = random.randint(30, 3000)
        exit_date = hire + timedelta(days=leave_days)
        if exit_date > date.today():
            exit_date = date.today()
        exits.append({
            "employee_id": i,
            "exit_date": exit_date,
            "reason_for_leaving": random.choice(["Resignation", "Termination", "Retirement", "Better Offer", "Relocation"])
        })

# Save CSVs
pd.DataFrame(employees).to_csv("data/employees.csv", index=False)
pd.DataFrame(salaries).to_csv("data/salaries.csv", index=False)
pd.DataFrame(performance).to_csv("data/performance.csv", index=False)
pd.DataFrame(exits).to_csv("data/exits.csv", index=False)
pd.DataFrame(trainings).to_csv("data/trainings.csv", index=False)

print("CSV files created in ./data")
