import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import zipfile

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------- LOGIN CHECK ----------------
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")

# ---------------- MAIN ----------------
st.title("📊 AI Data Dashboard")

file = st.file_uploader(
    "Upload File",
    type=["csv", "xlsx", "xls", "zip", "json"]
)

# ---------------- FILE HANDLING ----------------
df = None

if file:
    file_type = file.name.split(".")[-1].lower()

    if file_type == "csv":
        df = pd.read_csv(file)

    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(file)

    elif file_type == "json":
        df = pd.read_json(file)

    elif file_type == "zip":
        with zipfile.ZipFile(file) as z:
            for name in z.namelist():
                if name.endswith(".csv"):
                    df = pd.read_csv(z.open(name))
                    break

# ---------------- PROCESS ----------------
if df is not None:

    st.subheader("📂 Raw Data")
    st.dataframe(df.head())

# ---------------- DATASET UNDERSTANDING ----------------
    st.markdown("### 🧠 Dataset Understanding & Problem Definition")

    # DATASET SOURCE
    file_type = file.name.split(".")[-1].upper()

    source_map = {
        "CSV": "CSV file containing structured tabular data",
        "XLSX": "Excel file with spreadsheet-based structured data",
        "XLS": "Excel file with spreadsheet-based structured data",
        "JSON": "JSON file containing semi-structured hierarchical data",
        "ZIP": "Compressed ZIP file containing dataset files"
    }

    dataset_source = source_map.get(file_type, "User uploaded dataset")

    # COLUMN TYPES
    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include="object").columns

    # OBJECTIVE (DETAILED)
    if len(num_cols) >= 2:
        objective = f"""
The primary objective of this analysis is to explore relationships between key numerical variables such as **{num_cols[0]}** and **{num_cols[1]}**.  
This includes identifying trends, measuring correlations, and understanding how changes in one variable may influence another.

The analysis also aims to support predictive modeling and uncover meaningful patterns that can assist in decision-making.
"""
    elif len(num_cols) == 1:
        objective = f"""
The objective of this analysis is to study the behavior and distribution of the numerical variable **{num_cols[0]}**.  
This includes evaluating central tendencies (mean, median), variability, and identifying any unusual patterns or outliers.

Such analysis helps in understanding performance consistency and variability in the dataset.
"""
    elif len(cat_cols) > 0:
        objective = f"""
The objective is to analyze categorical data, particularly focusing on **{cat_cols[0]}**, to identify dominant categories, frequency distribution, and segmentation patterns.

This helps in understanding classification trends and grouping behavior within the dataset.
"""
    else:
        objective = """
The objective is to perform general exploratory data analysis to understand the structure, composition, and key characteristics of the dataset.
"""

    # BUSINESS PROBLEM (DETAILED)
    if len(cat_cols) > 0 and len(num_cols) > 0:
        business_problem = f"""
The key analytical problem is to understand how categorical factors such as **{cat_cols[0]}** influence numerical outcomes like **{num_cols[0]}**.

This helps in identifying:
- High-performing categories  
- Key drivers affecting performance  
- Opportunities for optimization  

Such insights are valuable for improving strategy, segmentation, and decision-making.
"""
    elif len(num_cols) >= 2:
        business_problem = f"""
The main problem is to analyze how **{num_cols[0]}** impacts **{num_cols[1]}** and whether a strong relationship exists between them.

This is useful for:
- Predictive modeling  
- Performance forecasting  
- Identifying key influencing variables  
"""
    else:
        business_problem = """
The problem focuses on extracting meaningful insights, identifying patterns, and detecting anomalies to support data-driven decision-making.
"""

    # DISPLAY
    st.write(f"""
### 📌 Objective of Analysis
{objective}

### 📂 Dataset Source
{dataset_source}

### 🔑 Key Variables
- Total Columns: {df.shape[1]}  
- Numerical Features: {list(num_cols)}  
- Categorical Features: {list(cat_cols)}  

### 💼 Business / Analytical Problem
{business_problem}
""")

    # ---------------- DATA CLEANING ----------------
    st.subheader("🧹 Data Cleaning & Preprocessing")

    st.write("""
    This step ensures data quality by:
    - Removing duplicate records  
    - Handling missing values  
    - Preparing dataset for analysis  
    """)

    before = len(df)

    df = df.drop_duplicates()
    after_dup = len(df)

    missing = df.isnull().sum().sum()
    df = df.dropna()

    df = df.infer_objects()

    st.success(f"✔ Removed {before - after_dup} duplicate rows")
    st.success(f"✔ Removed {missing} missing values")

    st.markdown("""
    ### 🧠 Cleaning Insight
    - Duplicate removal ensures no repeated data  
    - Missing values removal improves accuracy  
    - Data is now consistent and ready for analysis  
    """)

    st.subheader("✅ Cleaned Data")
    st.dataframe(df.head())

    # ---------------- DOWNLOAD ----------------
    st.markdown("### ⬇️ Download Cleaned Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Cleaned Data",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    # SIMPLIFY LARGE DATA
    if len(df) > 500:
        for col in df.select_dtypes(include="object").columns:
            top_vals = df[col].value_counts().nlargest(7).index
            df = df[df[col].isin(top_vals)]
        st.info("Large data simplified → showing top categories")

  st.markdown("### 📊 KPI Insight (AI Analysis)")

try:
    col = num_cols[0]

    mean_val = df[col].mean()
    median_val = df[col].median()
    max_val = df[col].max()
    min_val = df[col].min()
    std_val = df[col].std()

    st.info(f"""
### 🔍 Detailed KPI Analysis for **{col}**

**1. Central Tendency**
- Mean (Average): {round(mean_val,2)}
- Median: {round(median_val,2)}

👉 Interpretation:
- If mean ≈ median → balanced data  
- Mean > median → right skew  
- Mean < median → left skew  

---

**2. Range & Extremes**
- Maximum: {max_val}  
- Minimum: {min_val}  

👉 Shows spread and peak values  

---

**3. Variability**
- Standard Deviation: {round(std_val,2)}

👉 Low → stable | High → fluctuating  

---

### 💼 Business Insight
Helps understand performance, consistency, and risk in the dataset.
""")

except Exception as e:
    st.warning(f"KPI Insight error: {e}")
    
