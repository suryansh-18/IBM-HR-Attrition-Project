# =============================================================================
#  IBM HR Analytics — Employee Attrition Prediction
#  Streamlit + Scikit-Learn  |  Random Forest Classifier
# =============================================================================

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score,
)
import joblib
import io

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HR Attrition Predictor",
    page_icon="👥",
    layout="wide",
)

# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY   = "#003087"   # IBM Blue
DANGER    = "#da1e28"   # IBM Red
SUCCESS   = "#198038"   # IBM Green
WARNING   = "#f1c21b"   # IBM Yellow
NEUTRAL   = "#697077"   # IBM Gray 50

# =============================================================================
#  1. Synthetic IBM HR Dataset
# =============================================================================

@st.cache_data
def generate_dataset(n: int = 1_500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    departments = ["Sales", "Research & Development", "Human Resources"]
    job_roles   = {
        "Sales":                   ["Sales Executive", "Sales Representative", "Manager"],
        "Research & Development":  ["Research Scientist", "Laboratory Technician",
                                    "Healthcare Representative", "Manufacturing Director",
                                    "Research Director", "Manager"],
        "Human Resources":         ["Human Resources", "Manager"],
    }
    overtime_choices = ["Yes", "No"]

    rows = []
    for _ in range(n):
        dept    = rng.choice(departments)
        role    = rng.choice(job_roles[dept])
        age     = int(rng.integers(22, 61))
        income  = int(rng.integers(2_000, 20_001))
        ot      = rng.choice(overtime_choices, p=[0.30, 0.70])
        yac     = int(rng.integers(0, 31))

        # Attrition probability driven by realistic factors
        p_attr  = 0.12
        if ot == "Yes":          p_attr += 0.18
        if age < 30:             p_attr += 0.08
        if income < 5_000:       p_attr += 0.10
        if yac < 3:              p_attr += 0.07
        if dept == "Sales":      p_attr += 0.05
        p_attr = min(p_attr, 0.85)

        attrition = "Yes" if rng.random() < p_attr else "No"
        rows.append([age, dept, role, income, ot, yac, attrition])

    return pd.DataFrame(rows, columns=[
        "Age", "Department", "JobRole", "MonthlyIncome",
        "OverTime", "YearsAtCompany", "Attrition",
    ])


# =============================================================================
#  2. Pre-processing & Model Training
# =============================================================================

@st.cache_resource
def train_model(df: pd.DataFrame):
    df_enc = df.copy()
    encoders = {}

    for col in ["Department", "JobRole", "OverTime", "Attrition"]:
        le = LabelEncoder()
        df_enc[col] = le.fit_transform(df_enc[col])
        encoders[col] = le

    X = df_enc.drop(columns=["Attrition"])
    y = df_enc["Attrition"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=300, max_depth=8, min_samples_leaf=5,
        class_weight="balanced", random_state=42, n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    y_pred     = clf.predict(X_test)
    y_prob     = clf.predict_proba(X_test)[:, 1]
    accuracy   = accuracy_score(y_test, y_pred)
    roc_auc    = roc_auc_score(y_test, y_prob)
    report     = classification_report(y_test, y_pred,
                                       target_names=["No Attrition", "Attrition"],
                                       output_dict=True)
    cm         = confusion_matrix(y_test, y_pred)
    feat_imp   = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)

    return clf, encoders, X.columns.tolist(), accuracy, roc_auc, report, cm, feat_imp


# =============================================================================
#  3. Helper — encode a single employee record
# =============================================================================

def encode_employee(raw: dict, encoders: dict, feature_cols: list) -> pd.DataFrame:
    row = raw.copy()
    for col in ["Department", "JobRole", "OverTime"]:
        row[col] = encoders[col].transform([row[col]])[0]
    return pd.DataFrame([row])[feature_cols]


# =============================================================================
#  4. Main Streamlit App
# =============================================================================

def main():
    df    = generate_dataset()
    clf, encoders, feature_cols, accuracy, roc_auc, report, cm, feat_imp = train_model(df)

    dept_roles = {
        dept: df[df["Department"] == dept]["JobRole"].unique().tolist()
        for dept in df["Department"].unique()
    }

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style='background:{PRIMARY};padding:28px 36px;border-radius:8px;margin-bottom:24px'>
          <h1 style='color:white;margin:0;font-size:2rem'>👥 IBM HR Attrition Predictor</h1>
          <p style='color:#a8c4e0;margin:6px 0 0'>
            Random Forest · Scikit-Learn · Streamlit
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar ───────────────────────────────────────────────────────────────
    st.sidebar.header("🔧 Employee Profile")

    age = st.sidebar.slider("Age", 22, 60, 35)

    dept = st.sidebar.selectbox("Department", sorted(df["Department"].unique()))

    role = st.sidebar.selectbox("Job Role", sorted(dept_roles[dept]))

    monthly_income = st.sidebar.slider(
        "Monthly Income ($)", 2_000, 20_000, 6_000, step=500,
        format="$%d",
    )

    overtime = st.sidebar.radio("Works OverTime?", ["Yes", "No"], horizontal=True)

    years_at = st.sidebar.slider("Years at Company", 0, 30, 5)

    st.sidebar.markdown("---")
    st.sidebar.caption("Adjust the controls above, then click **Predict** in the main panel.")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_pred, tab_metrics, tab_data = st.tabs(
        ["🎯 Risk Prediction", "📊 Model Metrics", "🗄️ Dataset Explorer"]
    )

    # ── Tab 1 · Risk Prediction ───────────────────────────────────────────────
    with tab_pred:
        st.subheader("Employee Attrition Risk Evaluation")

        col_form, col_result = st.columns([1, 1], gap="large")

        with col_form:
            st.markdown("##### Selected Profile")
            profile_md = f"""
| Field | Value |
|-------|-------|
| **Age** | {age} |
| **Department** | {dept} |
| **Job Role** | {role} |
| **Monthly Income** | ${monthly_income:,} |
| **OverTime** | {overtime} |
| **Years at Company** | {years_at} |
"""
            st.markdown(profile_md)
            predict_btn = st.button("🔍 Predict Attrition Risk", use_container_width=True, type="primary")

        with col_result:
            if predict_btn:
                raw = {
                    "Age": age,
                    "Department": dept,
                    "JobRole": role,
                    "MonthlyIncome": monthly_income,
                    "OverTime": overtime,
                    "YearsAtCompany": years_at,
                }
                X_input = encode_employee(raw, encoders, feature_cols)
                prob_attrition = clf.predict_proba(X_input)[0][1]
                label          = clf.predict(X_input)[0]
                prediction     = encoders["Attrition"].inverse_transform([label])[0]

                pct = prob_attrition * 100

                if pct >= 60:
                    colour, icon, verdict = DANGER,  "🔴", "HIGH RISK"
                elif pct >= 35:
                    colour, icon, verdict = WARNING, "🟡", "MODERATE RISK"
                else:
                    colour, icon, verdict = SUCCESS, "🟢", "LOW RISK"

                st.markdown(
                    f"""
                    <div style='background:{colour}18;border:2px solid {colour};
                                border-radius:10px;padding:24px;text-align:center'>
                      <div style='font-size:2.4rem'>{icon}</div>
                      <div style='color:{colour};font-size:1.6rem;font-weight:700'>{verdict}</div>
                      <div style='font-size:2.8rem;font-weight:800;color:{colour}'>{pct:.1f}%</div>
                      <div style='color:{NEUTRAL};margin-top:6px'>Attrition Probability</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.progress(prob_attrition)

                st.markdown("##### Risk Factors")
                factors = []
                if overtime == "Yes":      factors.append("⚠️ Working overtime increases risk significantly")
                if age < 30:               factors.append("⚠️ Younger employees tend to leave more often")
                if monthly_income < 5_000: factors.append("⚠️ Below-average income is a retention risk")
                if years_at < 3:           factors.append("⚠️ Low tenure — still in the high-churn window")
                if dept == "Sales":        factors.append("⚠️ Sales roles show above-average attrition")

                if factors:
                    for f in factors:
                        st.markdown(f)
                else:
                    st.success("✅ No major risk factors detected for this profile.")
            else:
                st.info("👈 Configure the employee profile in the sidebar, then click **Predict**.")

    # ── Tab 2 · Model Metrics ─────────────────────────────────────────────────
    with tab_metrics:
        st.subheader("Model Performance")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Accuracy",   f"{accuracy*100:.1f}%")
        m2.metric("ROC-AUC",    f"{roc_auc:.3f}")
        m3.metric("Precision",  f"{report['Attrition']['precision']*100:.1f}%")
        m4.metric("Recall",     f"{report['Attrition']['recall']*100:.1f}%")

        col_cm, col_fi = st.columns(2)

        with col_cm:
            st.markdown("##### Confusion Matrix")
            tn, fp, fn, tp = cm.ravel()
            cm_df = pd.DataFrame(
                [[tn, fp], [fn, tp]],
                index   =["Actual: No", "Actual: Yes"],
                columns =["Pred: No",   "Pred: Yes"],
            )
            st.dataframe(cm_df.style.highlight_max(axis=None, color="#003087", props="color:white;font-weight:bold"), use_container_width=True)

        with col_fi:
            st.markdown("##### Feature Importances")
            fi_df = feat_imp.reset_index()
            fi_df.columns = ["Feature", "Importance"]
            fi_df["Importance %"] = (fi_df["Importance"] * 100).round(2)
            st.dataframe(fi_df[["Feature", "Importance %"]]
                         .sort_values("Importance %", ascending=False)
                         .reset_index(drop=True),
                         use_container_width=True)

        st.markdown("##### Full Classification Report")
        report_df = pd.DataFrame(report).T.drop(index="accuracy", errors="ignore")
        report_df = report_df[["precision", "recall", "f1-score", "support"]].round(3)
        st.dataframe(report_df, use_container_width=True)

    # ── Tab 3 · Dataset Explorer ──────────────────────────────────────────────
    with tab_data:
        st.subheader("Synthetic HR Dataset")

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Records",      f"{len(df):,}")
        c2.metric("Attrition (Yes)",    f"{(df['Attrition']=='Yes').sum():,}")
        attrition_rate = (df["Attrition"] == "Yes").mean() * 100
        c3.metric("Attrition Rate",     f"{attrition_rate:.1f}%")

        st.markdown("##### Attrition by Department")
        dept_summary = (
            df.groupby("Department")["Attrition"]
            .apply(lambda x: (x == "Yes").mean() * 100)
            .round(1)
            .reset_index()
        )
        dept_summary.columns = ["Department", "Attrition Rate (%)"]
        st.dataframe(dept_summary, use_container_width=True)

        st.markdown("##### Raw Data Sample")
        st.dataframe(df.sample(50, random_state=1).reset_index(drop=True),
                     use_container_width=True)

        # Download button
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            label="⬇️ Download Full Dataset (CSV)",
            data=csv_buf.getvalue(),
            file_name="IBM_HR_Attrition_Synthetic.csv",
            mime="text/csv",
        )

    # ── Footer ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.caption(
        "IBM HR Analytics · Attrition Prediction · Random Forest Classifier "
        "· Synthetic dataset generated for demonstration purposes only."
    )


if __name__ == "__main__":
    main()
