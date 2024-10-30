with a as (
      SELECT 
        FORMAT_DATE('%B', date) AS MONTH,
        COUNT(CASE 
            WHEN CAST(JSON_VALUE(scores, '$.satisfaction') AS INT64) > 8 THEN patient_id 
            END) AS promoters,
        COUNT(CASE 
            WHEN CAST(JSON_VALUE(scores, '$.satisfaction') AS INT64) < 7 THEN patient_id 
            END) AS detractors,
        COUNT(patient_id) AS num_patient
    FROM 
        patient_data.sh_data
    GROUP BY 
        FORMAT_DATE('%B', date)
)

SELECT 
    MONTH,
    CAST((COALESCE(promoters, 0) - COALESCE(detractors, 0)) * 100 / COALESCE(num_patient, 1) AS INT64) AS NPS
    FROM a
    ORDER BY  a.MONTH;