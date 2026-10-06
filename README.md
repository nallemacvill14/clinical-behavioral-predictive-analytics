# Clinical Behavioral Data Pipeline & Predictive Modeling Framework

An end-to-end healthcare analytics and machine learning pipeline designed to process, govern, and model neurobehavioral clinical datasets. Grounded in methodologies from precision behavioral interventions (Macias Villalpando, 2026, *Obesity Reviews*, DOI: 10.1111/obr.70191), this repository demonstrates:

1. **HIPAA/e-PHI Compliance & Governance:** Automated verification of Safe Harbor de-identification standards prior to downstream analytics.
2. **Behavioral Feature Engineering:** Ingestion of cognitive and attentional metrics derived from computerized experimental paradigms (PsychoPy) alongside metabolic baselines.
3. **Predictive Modeling (Scikit-Learn):** Machine learning classification pipeline to predict treatment response and non-adherence risk.
4. **Relational Data Auditing (SQL):** Cohort stratification, dropout tracking, and clinical KPI reporting.
5. **Business Intelligence (Power BI / DAX):** Measure definitions for clinical operations and patient adherence tracking.

---

## Architecture & Workflow

```text
clinical-behavioral-predictive-analytics/
│
├── data/
│   └── synthetic_clinical_cohort.csv      # Synthetic cohort with cognitive & clinical markers
├── scripts/
│   └── pipeline_and_modeling.py            # HIPAA audit, feature engineering, and ML model
├── sql/
│   └── cohort_analysis.sql                 # SQL KPI extraction and clinical cohort stratification
├── powerbi/
│   └── dax_measures.txt                    # DAX measures for executive and clinical monitoring
└── README.md                               # Project documentation and reproduction guide
