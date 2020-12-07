SELECT
    v.position_name AS vacancy_name,
    e.employer_name AS employer_name,
    e.area_id AS area_id
FROM homework.vacancy AS v 
LEFT JOIN homework.employer AS e ON v.employer_id = e.employer_id
WHERE 
    v.compensation_from IS NULL 
    AND v.compensation_to IS NULL
ORDER BY v.created_at DESC LIMIT 10;


WITH pretaxed_values AS (
    SELECT
    CASE 
        WHEN compensation_gross is FALSE
        THEN compensation_from / 0.87
        ELSE compensation_from
        END AS compensation_from,
    CASE 
        WHEN compensation_gross is FALSE
        THEN compensation_to / 0.87
        ELSE compensation_to
        END AS compensation_to
    FROM homework.vacancy AS v
)
SELECT
    avg(compensation_from) as average_min_salary,
    avg(compensation_to) as average_max_salary,
    avg(compensation_to - compensation_from) as average_salary_range
FROM pretaxed_values;


WITH response_count AS (
    SELECT
        v.employer_id,
        v.position_name,
        count(resume_id) AS responses
    FROM homework.vacancy AS v
    LEFT JOIN homework.vacancy_resume AS vr ON vr.vacancy_id = v.vacancy_id
    GROUP BY v.vacancy_id
)
SELECT
    e.employer_name,
    rc.position_name,
    rc.responses
FROM homework.employer AS e 
LEFT JOIN response_count AS rc ON rc.employer_id = e.employer_id
ORDER BY responses DESC, employer_name ASC LIMIT 5;

WITH vac_number AS (
    SELECT
        e.employer_id,
        employer_name,
        count(v.vacancy_id) as vac_count
    FROM homework.employer as e
    LEFT JOIN homework.vacancy AS v ON v.employer_id = e.employer_id
    GROUP BY e.employer_id ORDER BY vac_count
)
SELECT
    percentile_cont(0.5) WITHIN GROUP (ORDER BY vac_count) as median_value
FROM vac_number;

WITH creation_times AS (
    SELECT
        a.area_name,
        v.created_at AS vacancy_creation,
        vr.created_at AS first_response
    FROM homework.vacancy AS v
    LEFT JOIN homework.vacancy_resume as vr ON v.vacancy_id = vr.vacancy_id
    LEFT JOIN homework.employer AS e ON e.employer_id = v.employer_id
    LEFT JOIN homework.area AS a ON e.area_id = a.area_id
)
SELECT
    area_name,
    min(first_response - vacancy_creation) AS min_time,
    max(first_response - vacancy_creation) AS max_time
FROM creation_times
GROUP BY area_name ORDER BY area_name;