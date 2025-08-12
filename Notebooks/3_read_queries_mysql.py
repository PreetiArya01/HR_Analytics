import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

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

# Queries

# 1. Attrition By Department

query ="""SELECT e.department,
       COUNT(*) AS headcount,
       SUM(CASE WHEN x.exit_date IS NOT NULL THEN 1 ELSE 0 END) AS exited,
       ROUND(100.0 * SUM(CASE WHEN x.exit_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*),2) AS attrition_pct
FROM employees e
LEFT JOIN exits x ON e.employee_id = x.employee_id
GROUP BY e.department
ORDER BY attrition_pct DESC;"""

attrition_by_dept = pd.read_sql(query,engine)

print(attrition_by_dept)

#2. Monthly Attrition Trend

query ="""SELECT date_format(exit_date, '%%Y-%%m') as ym, count(*) as exits
from exits
where exit_date is not null
group by ym
order by ym;"""

monthly_attriton_trend = pd.read_sql(query,engine)
print(monthly_attriton_trend)

#3. Performance vs attrition(use last year)

query = """SELECT p.performance_rating,
       COUNT(DISTINCT p.employee_id) AS count_emp,
       SUM(CASE WHEN x.exit_date IS NOT NULL THEN 1 ELSE 0 END) AS exited
FROM performance p
LEFT JOIN exits x ON p.employee_id = x.employee_id
WHERE p.year = 2023
GROUP BY p.performance_rating
ORDER BY p.performance_rating;"""

performance_vs_attrition = pd.read_sql(query,engine)
print(performance_vs_attrition)

#4. Average salary by department

query = """SELECT e.department, ROUND(AVG(s.monthly_salary)*12,0) AS avg_annual_salary
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id
GROUP BY e.department
ORDER BY avg_annual_salary DESC;"""

avg_salary_by_deprt = pd.read_sql(query,engine)
print(avg_salary_by_deprt)

#5. Employee count by department

query = """SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
ORDER BY employee_count DESC;"""

emp_count_by_dept = pd.read_sql(query, engine)
print(emp_count_by_dept)

#6. Gender Distribution

query ="""SELECT gender, COUNT(*) AS count
FROM employees
GROUP BY gender;"""

gender_distribution = pd.read_sql(query,engine)
print(gender_distribution)

#7. Average age of employees

query ="""SELECT ROUND(AVG(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())), 2) AS avg_age
FROM employees;"""

avg_age_of_emp = pd.read_sql(query,engine)
print(avg_age_of_emp)

#8. Hiring trend per year

query = """SELECT YEAR(hire_date) AS hire_year, COUNT(*) AS hires
FROM employees
GROUP BY hire_year
ORDER BY hire_year;"""

hiring_trend_per_year = pd.read_sql(query,engine)
print(hiring_trend_per_year)