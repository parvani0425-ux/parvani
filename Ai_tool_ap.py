import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------- CLEAN DATA ----------------
def clean_data(df):
    df = df.copy()

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    df.columns = df.columns.str.strip()

    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()

    return df


# ---------------- REGRESSION MODEL ----------------
def run_regression(df):
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.shape[1] < 2:
        return None, None, None, None

    X = numeric_df.iloc[:, :-1]
    y = numeric_df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    score = r2_score(y_test, predictions)

    return score, numeric_df, predictions, y_test
