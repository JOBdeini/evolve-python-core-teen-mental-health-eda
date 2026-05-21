import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza los nombres de columnas a snake_case."""
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def convert_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte a category las variables cualitativas conocidas."""
    df = df.copy()
    categorical_cols = [
        "gender",
        "platform_usage",
        "social_interaction_level",
        "sleep_quality",
        "risk_category",
    ]

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas."""
    return df.drop_duplicates()


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa nulos simples manteniendo el dataset utilizable para el EDA."""
    df = df.copy()
    numeric_cols = df.select_dtypes(include=["number"]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode(dropna=True).iloc[0])

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica las transformaciones de limpieza principales."""
    df = clean_column_names(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = convert_categories(df)

    return df


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Devuelve las filas atipicas de una columna usando el criterio IQR."""
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return df[(df[column] < lower) | (df[column] > upper)]
