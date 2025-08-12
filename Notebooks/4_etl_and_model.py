

import os
os.makedirs("model", exist_ok=True)


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from joblib import dump

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="RISHI@garv1222",  
    host="localhost",
    port=3306,
    database="hr_analytics",
    query={"charset": "utf8mb4"}
)

engine = create_engine(connection_url)

# Load all tables from MySQL
employees = pd.read_sql("SELECT * FROM employees", engine)
salaries = pd.read_sql("SELECT * FROM salaries", engine)
performance = pd.read_sql("SELECT * FROM performance", engine)
exits = pd.read_sql("SELECT * FROM exits", engine)

# ---------- STEP 2: Fix column names ----------
# Make sure all tables have the same employee ID column name
for df in [employees, salaries, performance, exits]:
    if "emp_id" not in df.columns:
        # Try to find a column containing 'id' in its name
        id_col = [c for c in df.columns if 'id' in c.lower()][0]
        df.rename(columns={id_col: "emp_id"}, inplace=True)

# ---------- STEP 3: Merge datasets ----------
df = employees \
    .merge(salaries, on="emp_id", how="left") \
    .merge(performance, on="emp_id", how="left") \
    .merge(exits, on="emp_id", how="left")

# ---------- STEP 4: Feature engineering ----------
# Create attrition flag (1 = left, 0 = stayed)
df["attrition"] = df["exit_date"].notnull().astype(int)

# Drop columns that won't be used in modeling
drop_cols = ["emp_id", "exit_date", "hire_date"]
df.drop(columns=drop_cols, inplace=True, errors="ignore")

# Fill missing numeric values with median
num_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# Fill missing categorical values with 'Unknown'
cat_cols = df.select_dtypes(include=['object']).columns
df[cat_cols] = df[cat_cols].fillna("Unknown")

# One-hot encode categorical columns
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# ---------- STEP 5: Train model ----------
X = df.drop("attrition", axis=1)
y = df["attrition"]

# Scale features for logistic regression
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ---------- STEP 6: Save model & scaler ----------
dump(model, "model/hr_attrition_model.joblib")
dump(scaler, "model/hr_scaler.joblib")

# Save dataset for Power BI
risk_scores = pd.DataFrame({
    "emp_id": employees["emp_id"],
    "risk_score": model.predict_proba(X_scaled)[:, 1]
})
risk_scores.to_csv("Data/risk_scores.csv", index=False)

print("✅ Model training complete. risk_scores.csv saved.")