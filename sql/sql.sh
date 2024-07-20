#!/bin/bash
# Запрос с использованием оконной функции (партиционирование) для вычисления среднего значения столбца "salary" среди каждых 3 последовательных строк в таблице "employees":
SELECT
    employee_id,
    salary,
    AVG(salary) OVER (ORDER BY employee_id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_salary_over_3_rows
FROM
    employees;
# Запрос для вывода информации о сотрудниках, у которых только уникальные должности и для каждой должности вывести количество сотрудников:
SELECT
    job_id,
    COUNT(employee_id) AS num_employees
FROM
    employees
GROUP BY
    job_id
HAVING
    COUNT(DISTINCT job_id) = 1;
