-- =========================================================================
-- Clinical & Behavioral Cohort Aggregations
-- Target: Assessment of neurobehavioral parameters, adherence & response rates
-- =========================================================================

-- KPI 1: Efficacy & Adherence by Intervention Arm
SELECT 
    intervention_group,
    COUNT(patient_uuid) AS total_patients,
    ROUND(AVG(baseline_bmi), 2) AS mean_baseline_bmi,
    ROUND(AVG(adherence_rate_pct), 2) AS mean_adherence_pct,
    ROUND(AVG(psychopy_mean_rt_ms), 1) AS mean_reaction_time_ms,
    ROUND(SUM(treatment_response) * 100.0 / COUNT(patient_uuid), 2) AS success_rate_pct
FROM clinical_cohort
GROUP BY intervention_group
ORDER BY success_rate_pct DESC;

-- KPI 2: Identification of High-Risk Non-Adherence Patients (Clinical Alerts)
SELECT 
    patient_uuid,
    age,
    baseline_bmi,
    attentional_bias_score,
    adherence_rate_pct,
    intervention_group
FROM clinical_cohort
WHERE adherence_rate_pct < 60.0 
   OR attentional_bias_score > 0.85
ORDER BY adherence_rate_pct ASC;

-- KPI 3: Cognitive Marker Stratification by Treatment Response
SELECT 
    CASE 
        WHEN treatment_response = 1 THEN 'Responder' 
        ELSE 'Non-Responder' 
    END AS clinical_outcome,
    COUNT(patient_uuid) AS patient_count,
    ROUND(AVG(psychopy_mean_rt_ms), 2) AS avg_reaction_time_ms,
    ROUND(AVG(attentional_bias_score), 3) AS avg_attentional_bias,
    ROUND(AVG(baseline_bmi), 2) AS avg_final_bmi
FROM clinical_cohort
GROUP BY treatment_response;
