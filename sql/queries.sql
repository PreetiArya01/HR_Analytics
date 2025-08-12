#Attrition by Department

SELECT e.department,
       COUNT(*) AS headcount,
       SUM(CASE WHEN x.exit_date IS NOT NULL THEN 1 ELSE 0 END) AS exited,
       ROUND(100.0 * SUM(CASE WHEN x.exit_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*),2) AS attrition_pct
FROM employees e
LEFT JOIN exits x ON e.employee_id = x.employee_id
GROUP BY e.department
ORDER BY attrition_pct DESC;

#Monthly Attrition Trend

SELECT date_format(exit_date, '%Y-%m') as ym, count(*) as exits
from exits
where exit_date is not null
group by ym
order by ym;

#Performance vs attrition(use last year)

SELECT p.performance_rating,
       COUNT(DISTINCT p.employee_id) AS count_emp,
       SUM(CASE WHEN x.exit_date IS NOT NULL THEN 1 ELSE 0 END) AS exited
FROM performance p
LEFT JOIN exits x ON p.employee_id = x.employee_id
WHERE p.year = 2023
GROUP BY p.performance_rating
ORDER BY p.performance_rating;

#Average salary by department

SELECT e.department, ROUND(AVG(s.monthly_salary)*12,0) AS avg_annual_salary
FROM employees e
JOIN salaries s ON e.employee_id = s.employee_id
GROUP BY e.department
ORDER BY avg_annual_salary DESC;

#Employee count by department
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
ORDER BY employee_count DESC;

#gender distribution
SELECT gender, COUNT(*) AS count
FROM employees
GROUP BY gender;

#Average age of employees
SELECT ROUND(AVG(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())), 2) AS avg_age
FROM employees;

#Hiring trend per year
SELECT YEAR(hire_date) AS hire_year, COUNT(*) AS hires
FROM employees
GROUP BY hire_year
ORDER BY hire_year;

