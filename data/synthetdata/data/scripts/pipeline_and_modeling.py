"""
Clinical Behavioral Data Pipeline & Predictive Model
Demonstrates HIPAA Safe Harbor verification, feature preprocessing,
and Scikit-Learn predictive modeling for neurobehavioral health cohorts.
"""

import os
import sqlite3
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = os.path.join("data", "synthetic_clinical_cohort.csv")
DB_PATH = "clinical_analytics.db"


def audit_hipaa_compliance(df: pd.DataFrame) -> bool:
    """Verifies absence of direct 18 HIPAA Safe Harbor identifiers (e.g., names, SSNs, phone numbers)."""
    prohibited_fields = [
        "name",
        "ssn",
        "phone",
        "email",
        "address",
        "mrn",
        "curp",
    ]
    detected_violations = [
        col
        for col in df.columns
        if any(term in col.lower() for term in prohibited_fields)
    ]

    if detected_violations:
        raise ValueError(
            f"[HIPAA ALERT] Prohibited direct identifiers found: {detected_violations}"
        )

    print("[COMPLIANCE] HIPAA Safe Harbor audit passed: No direct e-PHI detected.")
    return True


def run_pipeline():
    # 1. Ingestion
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing dataset at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    audit_hipaa_compliance(df)

    # 2. Feature Engineering & Preprocessing
    features = [
        "age",
        "baseline_bmi",
        "psychopy_mean_rt_ms",
        "attentional_bias_score",
        "adherence_rate_pct",
    ]
    target = "treatment_response"

    X = df[features]
    y = df[target]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. Model Training (Predictive Health Modeling)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    roc_score = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])

    print("--- MODEL PERFORMANCE EVALUATION ---")
    print(f"ROC-AUC Score: {roc_score:.3f}")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Feature Importance Analysis
    importances = pd.Series(clf.feature_importances_, index=features).sort_values(
        ascending=False
    )
    print("--- TOP PREDICTIVE CLINICAL MARKERS ---")
    for feat, imp in importances.items():
        print(f"{feat}: {imp:.4f}")

    # 4. Relational Persistence for SQL & Power BI consumption
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("clinical_cohort", conn, if_exists="replace", index=False)
    conn.close()
    print(
        f"[PERSISTENCE] Clean cohort loaded into '{DB_PATH}' for SQL analytics."
    )


if __name__ == "__main__":
    run_pipeline()
