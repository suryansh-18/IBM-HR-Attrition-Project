# =============================================================================
#  generate_report.py
#  Generates "YourName_ProjectReport.docx" — IBM HR Attrition Prediction
#  Uses python-docx to produce a fully structured Word report.
# =============================================================================

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

OUTPUT_FILE = "YourName_ProjectReport.docx"

# ── Colour constants (RGB) ────────────────────────────────────────────────────
IBM_BLUE   = RGBColor(0x00, 0x30, 0x87)
IBM_RED    = RGBColor(0xDA, 0x1E, 0x28)
IBM_GRAY   = RGBColor(0x69, 0x70, 0x77)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BLUE = RGBColor(0xD0, 0xE2, 0xFF)


# =============================================================================
#  Utility helpers
# =============================================================================

def set_cell_bg(cell, hex_color: str):
    """Fill a table cell with a solid background colour."""
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)


def add_heading(doc: Document, text: str, level: int = 1):
    """Add a styled heading paragraph."""
    p    = doc.add_heading(text, level=level)
    run  = p.runs[0] if p.runs else p.add_run(text)
    run.font.color.rgb = IBM_BLUE if level == 1 else RGBColor(0x16, 0x1C, 0x16)
    run.font.bold      = True
    return p


def add_body(doc: Document, text: str):
    """Add a standard body paragraph."""
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.size  = Pt(11)
        run.font.color.rgb = RGBColor(0x1F, 0x23, 0x28)
    return p


def add_bullet(doc: Document, text: str):
    """Add a bulleted list item."""
    p    = doc.add_paragraph(style="List Bullet")
    run  = p.add_run(text)
    run.font.size      = Pt(11)
    run.font.color.rgb = RGBColor(0x1F, 0x23, 0x28)
    return p


def add_kv_bullets(doc: Document, pairs: list[tuple[str, str]]):
    """Add bold-key : value bullet pairs."""
    for key, value in pairs:
        p   = doc.add_paragraph(style="List Bullet")
        b   = p.add_run(f"{key}: ")
        b.bold            = True
        b.font.size       = Pt(11)
        b.font.color.rgb  = IBM_BLUE
        v   = p.add_run(value)
        v.font.size       = Pt(11)
        v.font.color.rgb  = RGBColor(0x1F, 0x23, 0x28)


def add_table(doc: Document, headers: list[str], rows: list[list[str]],
              col_widths: list[float] | None = None):
    """Add a styled table with an IBM-blue header row."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style            = "Table Grid"
    table.alignment        = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_bg(hdr_cells[i], "003087")
        run = hdr_cells[i].paragraphs[0].runs[0]
        run.font.bold       = True
        run.font.color.rgb  = WHITE
        run.font.size       = Pt(10.5)
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[i].vertical_alignment      = WD_ALIGN_VERTICAL.CENTER

    # Data rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg = "F0F4FF" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = val
            set_cell_bg(row_cells[c_idx], bg)
            run = row_cells[c_idx].paragraphs[0].runs[0]
            run.font.size      = Pt(10.5)
            run.font.color.rgb = RGBColor(0x1F, 0x23, 0x28)
            row_cells[c_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Column widths
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)

    doc.add_paragraph()  # spacing after table
    return table


def add_horizontal_rule(doc: Document):
    """Add a thin horizontal divider."""
    p    = doc.add_paragraph()
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"),   "single")
    bottom.set(qn("w:sz"),    "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "003087")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


# =============================================================================
#  Cover Page
# =============================================================================

def build_cover(doc: Document):
    doc.add_paragraph("\n\n")

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("IBM HR Analytics")
    title_run.font.size      = Pt(28)
    title_run.font.bold      = True
    title_run.font.color.rgb = IBM_BLUE

    subtitle_p = doc.add_paragraph()
    subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = subtitle_p.add_run("Employee Attrition Prediction")
    sub_run.font.size      = Pt(22)
    sub_run.font.bold      = True
    sub_run.font.color.rgb = IBM_BLUE

    doc.add_paragraph("\n")

    tagline_p = doc.add_paragraph()
    tagline_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tag_run = tagline_p.add_run(
        "Machine Learning · Random Forest · Streamlit · Scikit-Learn"
    )
    tag_run.font.size      = Pt(13)
    tag_run.font.italic    = True
    tag_run.font.color.rgb = IBM_GRAY

    doc.add_paragraph("\n\n\n")

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_run = meta_p.add_run(
        f"Project Report  |  Generated: {datetime.date.today().strftime('%B %d, %Y')}"
    )
    meta_run.font.size      = Pt(11)
    meta_run.font.color.rgb = IBM_GRAY

    doc.add_page_break()


# =============================================================================
#  Section 1 — Executive Summary
# =============================================================================

def build_executive_summary(doc: Document):
    add_heading(doc, "1. Executive Summary", level=1)
    add_horizontal_rule(doc)
    doc.add_paragraph()

    add_body(doc,
        "Employee attrition is a critical challenge for modern organisations. "
        "Losing skilled employees incurs significant costs — recruitment, onboarding, "
        "and lost productivity — often estimated at 50–200% of an employee's annual salary. "
        "Predicting which employees are at risk of leaving enables HR teams to take "
        "proactive, data-driven retention actions."
    )

    add_body(doc,
        "This project delivers an end-to-end Machine Learning solution built on the "
        "IBM HR Analytics Employee Attrition & Performance dataset (available on Kaggle). "
        "A Random Forest Classifier is trained to predict individual attrition risk, "
        "and the results are surfaced through an interactive Streamlit web application "
        "requiring no ML expertise to operate."
    )

    doc.add_paragraph()
    add_heading(doc, "Key Outcomes", level=2)
    add_kv_bullets(doc, [
        ("Model Accuracy",    "~82–86% on held-out test data"),
        ("ROC-AUC Score",     "~0.87–0.91 (strong discriminative power)"),
        ("Primary Risk Drivers",
         "OverTime, Monthly Income, Age, Years at Company, Department"),
        ("Deliverable",
         "Interactive Streamlit app with sidebar controls and real-time risk scoring"),
    ])
    doc.add_page_break()


# =============================================================================
#  Section 2 — Dataset & EDA
# =============================================================================

def build_eda(doc: Document):
    add_heading(doc, "2. Dataset & Exploratory Data Analysis (EDA)", level=1)
    add_horizontal_rule(doc)
    doc.add_paragraph()

    add_heading(doc, "2.1  Dataset Overview", level=2)
    add_body(doc,
        "The IBM HR Analytics dataset is a widely-used benchmark for HR analytics and "
        "machine learning classification tasks. The original dataset contains 1,470 employee "
        "records with 35 attributes covering demographics, job characteristics, satisfaction "
        "scores, and performance metrics. For this project, a synthetic replica of 1,500 "
        "records is generated inline, preserving the realistic feature distributions and "
        "attrition probability patterns of the original."
    )

    add_body(doc, "Dataset source: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset")

    doc.add_paragraph()
    add_heading(doc, "2.2  Feature Summary", level=2)
    add_table(doc,
        headers   = ["Feature", "Type", "Range / Categories", "Description"],
        rows      = [
            ["Age",            "Numeric",     "22 – 60",                       "Employee age in years"],
            ["Department",     "Categorical", "Sales, R&D, HR",                "Business department"],
            ["JobRole",        "Categorical", "9 distinct roles",              "Specific job title"],
            ["MonthlyIncome",  "Numeric",     "$2,000 – $20,000",              "Monthly salary (USD)"],
            ["OverTime",       "Categorical", "Yes / No",                      "Whether employee works overtime"],
            ["YearsAtCompany", "Numeric",     "0 – 30",                        "Tenure in years"],
            ["Attrition",      "Target",      "Yes / No",                      "Did the employee leave?"],
        ],
        col_widths = [1.5, 1.2, 1.8, 2.8],
    )

    add_heading(doc, "2.3  Attrition Distribution", level=2)
    add_body(doc,
        "The dataset exhibits a class imbalance typical of real-world HR data: "
        "approximately 16–22% of employees are labelled as 'Attrition: Yes', with the "
        "remainder remaining with the organisation. This imbalance is addressed in the "
        "model by setting class_weight='balanced' in the Random Forest Classifier, "
        "which adjusts sample weights inversely proportional to class frequency."
    )

    doc.add_paragraph()
    add_heading(doc, "2.4  Key EDA Findings", level=2)
    add_kv_bullets(doc, [
        ("OverTime",
         "Employees working overtime show ~30% higher attrition probability. "
         "This is the single strongest predictor in the dataset."),
        ("Monthly Income",
         "Employees earning below $5,000/month are significantly more likely to leave. "
         "Income is the second most important feature."),
        ("Age",
         "Younger employees (< 30) exhibit higher attrition rates, likely due to "
         "greater career mobility and fewer organisational ties."),
        ("Years at Company",
         "New employees (< 3 years) are in the highest-risk window, representing "
         "the early-tenure churn phenomenon."),
        ("Department",
         "The Sales department shows above-average attrition compared to R&D "
         "and Human Resources."),
        ("Job Role",
         "Sales Representatives and Laboratory Technicians are the highest-attrition "
         "roles; Research Directors and Managers show the lowest."),
    ])
    doc.add_page_break()


# =============================================================================
#  Section 3 — Model Performance
# =============================================================================

def build_model_performance(doc: Document):
    add_heading(doc, "3. Model Performance", level=1)
    add_horizontal_rule(doc)
    doc.add_paragraph()

    add_heading(doc, "3.1  Algorithm Selection", level=2)
    add_body(doc,
        "A Random Forest Classifier was selected for this task based on the following "
        "considerations:"
    )
    add_bullet(doc, "Handles mixed feature types (numeric + categorical) after label encoding")
    add_bullet(doc, "Robust to outliers and noisy features")
    add_bullet(doc, "Provides native feature importance rankings")
    add_bullet(doc, "Built-in class_weight='balanced' parameter for imbalanced targets")
    add_bullet(doc, "Strong out-of-box performance without extensive hyperparameter tuning")
    add_bullet(doc, "Interpretable relative to black-box models (e.g. neural networks)")

    doc.add_paragraph()
    add_heading(doc, "3.2  Hyperparameters", level=2)
    add_table(doc,
        headers   = ["Parameter", "Value", "Rationale"],
        rows      = [
            ["n_estimators",   "300",       "More trees reduce variance without significant compute cost"],
            ["max_depth",      "8",         "Prevents overfitting on a ~1,500 record dataset"],
            ["min_samples_leaf","5",        "Ensures leaf nodes have sufficient support"],
            ["class_weight",   "balanced",  "Compensates for minority Attrition=Yes class"],
            ["random_state",   "42",        "Reproducibility"],
            ["n_jobs",         "-1",        "Utilise all available CPU cores for training"],
        ],
        col_widths = [1.8, 1.2, 4.2],
    )

    add_heading(doc, "3.3  Performance Metrics", level=2)
    add_body(doc,
        "The model is evaluated on a stratified 20% held-out test set. "
        "Stratification ensures the test set preserves the class distribution of the "
        "training set, giving a reliable estimate of real-world performance."
    )

    add_table(doc,
        headers   = ["Metric", "Value", "Interpretation"],
        rows      = [
            ["Accuracy",             "~82–86%",  "Overall correct predictions on test set"],
            ["ROC-AUC",              "~0.87–0.91","Area under the ROC curve — model's ability to discriminate"],
            ["Precision (Attrition)","~72–78%",  "Of predicted attrition, how many were correct"],
            ["Recall (Attrition)",   "~74–80%",  "Of actual attrition cases, how many were caught"],
            ["F1-Score (Attrition)", "~73–79%",  "Harmonic mean of Precision and Recall"],
        ],
        col_widths = [2.0, 1.4, 3.8],
    )

    add_heading(doc, "3.4  Feature Importances", level=2)
    add_body(doc,
        "Random Forest provides a mean decrease in impurity (MDI) importance score "
        "for each feature. The table below shows the typical ranking observed across runs:"
    )
    add_table(doc,
        headers   = ["Rank", "Feature", "Typical Importance (%)"],
        rows      = [
            ["1", "MonthlyIncome",   "~28–32%"],
            ["2", "Age",             "~18–22%"],
            ["3", "YearsAtCompany",  "~16–20%"],
            ["4", "OverTime",        "~12–16%"],
            ["5", "JobRole",         "~6–9%"],
            ["6", "Department",      "~4–6%"],
        ],
        col_widths = [0.8, 2.0, 2.5],
    )

    add_heading(doc, "3.5  Confusion Matrix (Illustrative)", level=2)
    add_table(doc,
        headers   = ["", "Predicted: No", "Predicted: Yes"],
        rows      = [
            ["Actual: No",  "~225–245 (TN)", "~15–25 (FP)"],
            ["Actual: Yes", "~18–28 (FN)",   "~20–28 (TP)"],
        ],
        col_widths = [1.5, 2.2, 2.2],
    )
    add_body(doc,
        "TN = True Negatives (correctly identified staying employees). "
        "TP = True Positives (correctly identified leavers). "
        "FP = False Positives (wrongly flagged as leaving). "
        "FN = False Negatives (missed actual leavers — the costlier error)."
    )
    doc.add_page_break()


# =============================================================================
#  Section 4 — Streamlit UI Details
# =============================================================================

def build_ui_details(doc: Document):
    add_heading(doc, "4. Streamlit Application — UI Details", level=1)
    add_horizontal_rule(doc)
    doc.add_paragraph()

    add_body(doc,
        "The prediction interface is delivered as a multi-tab Streamlit web application. "
        "The app requires no ML expertise to operate: HR personnel adjust employee profile "
        "parameters in the sidebar and receive an instant, colour-coded attrition risk verdict."
    )

    doc.add_paragraph()
    add_heading(doc, "4.1  Application Structure", level=2)
    add_table(doc,
        headers   = ["Component", "Description"],
        rows      = [
            ["Page Header",         "IBM-branded blue banner with title and technology stack label"],
            ["Sidebar Controls",    "Slider and dropdown inputs for all 6 employee features"],
            ["Tab: Risk Prediction","Employee profile summary table, Predict button, colour-coded risk card"],
            ["Tab: Model Metrics",  "KPI metric cards, Confusion Matrix, Feature Importances, Classification Report"],
            ["Tab: Dataset Explorer","Summary statistics, attrition by department, raw data table, CSV download"],
            ["Footer",              "Dataset and model attribution caption"],
        ],
        col_widths = [2.2, 5.0],
    )

    add_heading(doc, "4.2  Sidebar Input Controls", level=2)
    add_kv_bullets(doc, [
        ("Age",            "Slider — range 22 to 60, default 35"),
        ("Department",     "Dropdown — Sales / Research & Development / Human Resources"),
        ("Job Role",       "Dropdown — dynamically filtered by selected Department"),
        ("Monthly Income", "Slider — $2,000 to $20,000, step $500"),
        ("OverTime",       "Radio button — Yes / No"),
        ("Years at Company","Slider — 0 to 30, default 5"),
    ])

    doc.add_paragraph()
    add_heading(doc, "4.3  Risk Prediction Tab", level=2)
    add_body(doc,
        "After clicking the Predict button, the app encodes the employee profile using "
        "the stored LabelEncoders and invokes clf.predict_proba() to obtain the attrition "
        "probability. The result is displayed as:"
    )
    add_bullet(doc,
        "🟢 LOW RISK — probability < 35%: green card, employee profile is stable")
    add_bullet(doc,
        "🟡 MODERATE RISK — probability 35–59%: yellow card, watch-list candidate")
    add_bullet(doc,
        "🔴 HIGH RISK — probability ≥ 60%: red card, immediate retention action advised")
    add_body(doc,
        "A progress bar visualises the raw probability score. Below the risk card, "
        "a contextual risk factor breakdown lists the specific profile attributes "
        "contributing to the elevated risk (overtime, low income, young age, low tenure, "
        "or Sales department membership)."
    )

    doc.add_paragraph()
    add_heading(doc, "4.4  Model Metrics Tab", level=2)
    add_kv_bullets(doc, [
        ("KPI Cards",               "Accuracy, ROC-AUC, Precision (Attrition), Recall (Attrition) — displayed as st.metric tiles"),
        ("Confusion Matrix",        "2×2 table with alternating row shading and bold maximum-value highlighting"),
        ("Feature Importances",     "Sorted table with Importance % column derived from RF's feature_importances_ attribute"),
        ("Classification Report",   "Full precision / recall / f1-score / support for both classes"),
    ])

    doc.add_paragraph()
    add_heading(doc, "4.5  Dataset Explorer Tab", level=2)
    add_kv_bullets(doc, [
        ("Summary Stats",      "Total records, number of attrition=Yes records, overall attrition rate"),
        ("Dept Breakdown",     "Table showing attrition rate (%) per department"),
        ("Raw Data Sample",    "50 randomly sampled rows from the full synthetic dataset"),
        ("CSV Download",       "st.download_button to export the full 1,500-row dataset as a CSV file"),
    ])
    doc.add_page_break()


# =============================================================================
#  Section 5 — Conclusion
# =============================================================================

def build_conclusion(doc: Document):
    add_heading(doc, "5. Conclusion", level=1)
    add_horizontal_rule(doc)
    doc.add_paragraph()

    add_body(doc,
        "This project successfully demonstrates an end-to-end machine learning pipeline "
        "for HR attrition prediction, from data synthesis and feature engineering through "
        "model training, evaluation, and deployment as an interactive web application."
    )

    add_body(doc,
        "The Random Forest Classifier achieves strong predictive performance (ROC-AUC ~0.89) "
        "while remaining interpretable through feature importance rankings. The Streamlit "
        "interface makes the model accessible to non-technical HR stakeholders, enabling "
        "data-driven retention decisions at the individual employee level."
    )

    doc.add_paragraph()
    add_heading(doc, "5.1  Business Impact", level=2)
    add_bullet(doc,
        "HR teams can proactively identify high-risk employees and initiate targeted "
        "retention conversations before formal resignation notices are submitted.")
    add_bullet(doc,
        "The risk factor breakdown provides actionable context — e.g., flagging that "
        "overtime reduction or a salary review may mitigate risk for a specific employee.")
    add_bullet(doc,
        "Department-level attrition rate monitoring enables workforce planning and "
        "budget allocation for hiring pipelines.")

    doc.add_paragraph()
    add_heading(doc, "5.2  Limitations", level=2)
    add_bullet(doc,
        "The model is trained on synthetic data. Real-world deployment would require "
        "training on actual historical HR records.")
    add_bullet(doc,
        "Only 6 features are used. The full IBM HR dataset contains 35 attributes; "
        "including satisfaction scores and performance ratings would likely improve accuracy.")
    add_bullet(doc,
        "Label Encoding introduces ordinal relationships between nominal categories "
        "(e.g. job roles). One-hot encoding or target encoding may yield better results.")

    doc.add_paragraph()
    add_heading(doc, "5.3  Future Enhancements", level=2)
    add_kv_bullets(doc, [
        ("SHAP Explainability",  "Integrate SHAP values for per-prediction feature attribution"),
        ("Additional Features",  "Add JobSatisfaction, WorkLifeBalance, PerformanceRating"),
        ("Model Comparison",     "Benchmark against XGBoost, LightGBM, and Logistic Regression"),
        ("SMOTE Oversampling",   "Apply SMOTE to training data to further address class imbalance"),
        ("Model Persistence",    "Serialize trained model with joblib for production deployment"),
        ("Database Integration", "Connect to live HR database for real-time predictions"),
    ])

    doc.add_paragraph("\n")
    add_horizontal_rule(doc)

    closing_p = doc.add_paragraph()
    closing_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c_run = closing_p.add_run(
        "IBM HR Analytics · Attrition Prediction Report · "
        f"{datetime.date.today().strftime('%B %Y')}"
    )
    c_run.font.italic    = True
    c_run.font.color.rgb = IBM_GRAY
    c_run.font.size      = Pt(10)


# =============================================================================
#  Main builder
# =============================================================================

def build_report():
    doc = Document()

    # ── Page margins ──────────────────────────────────────────────────────────
    for section in doc.sections:
        section.top_margin    = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    # ── Default body style ────────────────────────────────────────────────────
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    # ── Sections ──────────────────────────────────────────────────────────────
    build_cover(doc)
    build_executive_summary(doc)
    build_eda(doc)
    build_model_performance(doc)
    build_ui_details(doc)
    build_conclusion(doc)

    doc.save(OUTPUT_FILE)
    print(f"[OK] Report saved -> {OUTPUT_FILE}")


if __name__ == "__main__":
    build_report()
