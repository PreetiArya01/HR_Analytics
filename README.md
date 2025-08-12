HR Analytics — Employee Attrition Prediction

Project Overview
The **HR Analytics Project** demonstrates a complete **ETL + Machine Learning pipeline** for analyzing and predicting employee attrition risk.  
This project simulates a real-world HR scenario where multiple datasets (employee details, salaries, performance, and exits) are stored in **MySQL**, processed with **Python**, and used to train a predictive model.

**Goal:**  
Help HR teams identify **high-risk employees** so they can take preventive action and reduce attrition.

---

Tech Stack
- **Python** — Data processing, modeling, and ETL
- **MySQL** — Data storage and querying
- **Pandas / SQLAlchemy** — Data manipulation and database connection
- **Scikit-learn** — Machine learning
- **Joblib** — Model persistence

---

Project Structure
HR_Analytics/
│
├── Data/
│ └── risk_scores.csv # Output: predicted attrition risk scores
│
├── Notebooks/
│ ├── 1_generate_data.py # Generate synthetic HR dataset
│ ├── 2_load_to_mysql.py # Load dataset into MySQL
│ ├── 3_read_queries_mysql.py # Execute SQL queries for insights
│ └── 4_etl_and_model.py # ETL process + ML model training
│
├── sql/ # SQL schema & queries
│
├── model/
│ ├── hr_attrition_model.joblib # Saved Logistic Regression model
│ └── hr_scaler.joblib # Feature scaler for model
│
└── README.md # Project documentation


---

ETL & Modeling Workflow

1️⃣ Extract
- Connect to MySQL database using **SQLAlchemy**.
- Load tables:  
  - `employees`
  - `salaries`
  - `performance`
  - `exits`

2️⃣ Transform
- Standardize column names (`emp_id`).
- Merge datasets into one DataFrame.
- Create `attrition` flag:  
  - `1` → Employee left  
  - `0` → Employee stayed
- Handle missing values:
  - Numeric → fill with median
  - Categorical → fill with `"Unknown"`
- One-hot encode categorical columns.
- Scale features for modeling.

3️⃣ Load
- Train **Logistic Regression** model.
- Save model and scaler in `/model`.
- Output `risk_scores.csv` with probability of attrition for each employee.

---

Machine Learning Model
- **Algorithm:** Logistic Regression  
- **Target Variable:** `attrition` (binary classification)  
- **Features:** Demographics, salary, performance ratings, etc.  
- **Split:** 80% train / 20% test (stratified)  
- **Output:** Probability (`risk_score`) of each employee leaving

---

Example Output
| emp_id | risk_score |
|--------|-----------|
| 101    | 0.72      |
| 102    | 0.15      |
| 103    | 0.54      |

> Higher `risk_score` means a greater likelihood the employee will leave.

---

How to Run

1️⃣ Install Dependencies

pip install pandas sqlalchemy pymysql scikit-learn joblib
2️⃣ Execute Workflow

Run the scripts in order:

python Notebooks/1_generate_data.py
python Notebooks/2_load_to_mysql.py
python Notebooks/3_read_queries_mysql.py
python Notebooks/4_etl_and_model.py


**Key Learnings**
Database Integration: Connecting Python to MySQL

ETL Pipelines: Extract, Transform, Load processes

Data Preprocessing: Missing values, encoding, scaling

Machine Learning: Logistic Regression for classification

Model Deployment Prep: Saving trained models and scalers

Business Insight: Identifying high attrition risk employees

