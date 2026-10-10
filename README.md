# 👥 IBM HR Attrition Prediction

> An interactive **Machine Learning web application** built with **Streamlit** and **Scikit-Learn** that predicts employee attrition risk using the IBM HR Analytics dataset.

---

## 📌 Project Overview

Employee attrition is one of the most costly challenges faced by HR departments. This project uses a **Random Forest Classifier** trained on IBM HR Analytics data to predict whether an employee is likely to leave the organisation. The app provides:

- Real-time attrition risk scoring per employee profile
- Colour-coded risk indicators (Low / Moderate / High)
- Actionable risk-factor breakdowns
- Full model performance metrics (Accuracy, ROC-AUC, Confusion Matrix, Feature Importances)
- An interactive dataset explorer with CSV export

---

## 📂 Dataset

| Detail | Info |
|--------|------|
| **Name** | IBM HR Analytics Employee Attrition & Performance |
| **Source** | [Kaggle — IBM HR Analytics](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) |
| **Records** | 1,470 employees (original) · 1,500 synthetic records used in app |
| **Target** | `Attrition` — Yes / No |

### Features Used

| Feature | Type | Description |
|---------|------|-------------|
| `Age` | Numeric | Employee age (22–60) |
| `Department` | Categorical | Sales · R&D · Human Resources |
| `JobRole` | Categorical | 9 distinct roles |
| `MonthlyIncome` | Numeric | Salary in USD (2,000–20,000) |
| `OverTime` | Categorical | Yes / No |
| `YearsAtCompany` | Numeric | Tenure in years (0–30) |
| `Attrition` | Target | Yes / No |

---

## 🛠️ Tech Stack

| Layer | Library / Tool |
|-------|---------------|
| **Web UI** | [Streamlit](https://streamlit.io) |
| **ML Model** | [Scikit-Learn](https://scikit-learn.org) — Random Forest Classifier |
| **Data** | [Pandas](https://pandas.pydata.org) · [NumPy](https://numpy.org) |
| **Model Persistence** | [Joblib](https://joblib.readthedocs.io) |
| **Report Generation** | [python-docx](https://python-docx.readthedocs.io) |
| **Language** | Python 3.9+ |

---

## 🚀 Setup & Run Instructions

### 1 · Clone / Download the project

```bash
git clone https://github.com/your-username/ibm-hr-attrition.git
cd ibm-hr-attrition
```

### 2 · Create a virtual environment (recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Launch the Streamlit app

```bash
streamlit run YourName_HR_Attrition_Prediction.py
```

The app will open automatically in your browser at **http://localhost:8501**.

### 5 · Generate the Word project report (optional)

```bash
python generate_report.py
```

This produces `YourName_ProjectReport.docx` in the project root.

---

## 📁 Project Structure

```
ibm-hr-attrition/
│
├── YourName_HR_Attrition_Prediction.py   # Main Streamlit ML application
├── generate_report.py                    # Word report generator (python-docx)
├── YourName_ProjectReport.docx           # Generated project report (auto-created)
├── requirements.txt                      # Python dependencies
└── README.md                             # This file
```

---

## 🧠 Model Details

| Parameter | Value |
|-----------|-------|
| Algorithm | Random Forest Classifier |
| Estimators | 300 trees |
| Max Depth | 8 |
| Class Weight | `balanced` (handles imbalance) |
| Train / Test Split | 80% / 20% (stratified) |
| Encoding | Label Encoding for categoricals |

### Typical Performance (on synthetic data)

| Metric | Value |
|--------|-------|
| Accuracy | ~82–86% |
| ROC-AUC | ~0.87–0.91 |
| Precision (Attrition) | ~72–78% |
| Recall (Attrition) | ~74–80% |

---

## 🖥️ App Tabs

| Tab | Description |
|-----|-------------|
| 🎯 **Risk Prediction** | Configure an employee profile in the sidebar and get an instant attrition risk score with colour-coded verdict and risk factor breakdown |
| 📊 **Model Metrics** | KPI cards, Confusion Matrix, Feature Importances, full Classification Report |
| 🗄️ **Dataset Explorer** | Summary statistics, attrition rates by department, raw data table, CSV download |

---

## 📄 License

This project is released for **educational and demonstration purposes**.  
The IBM HR Analytics dataset is publicly available on [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) under the [DbCL v1.0](https://opendatacommons.org/licenses/dbcl/1-0/) licence.

---
