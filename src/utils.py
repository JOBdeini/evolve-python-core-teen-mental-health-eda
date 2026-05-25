import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


def validate_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Valida rangos esperados del dataset y devuelve un resumen."""
    checks = [
        {
            "check": "depression_label_binary",
            "invalid_rows": int(~df["depression_label"].isin([0, 1]).sum())
            if False
            else int((~df["depression_label"].isin([0, 1])).sum()),
            "description": "depression_label debe contener solo 0 o 1",
        },
        {
            "check": "daily_social_media_hours_0_24",
            "invalid_rows": int((~df["daily_social_media_hours"].between(0, 24)).sum()),
            "description": "daily_social_media_hours debe estar entre 0 y 24",
        },
        {
            "check": "sleep_hours_0_24",
            "invalid_rows": int((~df["sleep_hours"].between(0, 24)).sum()),
            "description": "sleep_hours debe estar entre 0 y 24",
        },
        {
            "check": "screen_time_before_sleep_0_24",
            "invalid_rows": int((~df["screen_time_before_sleep"].between(0, 24)).sum()),
            "description": "screen_time_before_sleep debe estar entre 0 y 24",
        },
        {
            "check": "stress_level_1_10",
            "invalid_rows": int((~df["stress_level"].between(1, 10)).sum()),
            "description": "stress_level debe estar entre 1 y 10",
        },
        {
            "check": "anxiety_level_1_10",
            "invalid_rows": int((~df["anxiety_level"].between(1, 10)).sum()),
            "description": "anxiety_level debe estar entre 1 y 10",
        },
        {
            "check": "addiction_level_1_10",
            "invalid_rows": int((~df["addiction_level"].between(1, 10)).sum()),
            "description": "addiction_level debe estar entre 1 y 10",
        },
        {
            "check": "physical_activity_non_negative",
            "invalid_rows": int((df["physical_activity"] < 0).sum()),
            "description": "physical_activity no debe ser negativa",
        },
    ]

    return pd.DataFrame(checks)


def data_quality_summary(raw_df: pd.DataFrame, processed_df: pd.DataFrame) -> pd.DataFrame:
    """Resume calidad y dimensiones antes/despues del pipeline."""
    return pd.DataFrame(
        [
            {
                "metric": "raw_rows",
                "value": len(raw_df),
            },
            {
                "metric": "raw_columns",
                "value": raw_df.shape[1],
            },
            {
                "metric": "processed_rows",
                "value": len(processed_df),
            },
            {
                "metric": "processed_columns",
                "value": processed_df.shape[1],
            },
            {
                "metric": "raw_duplicates",
                "value": int(raw_df.duplicated().sum()),
            },
            {
                "metric": "processed_duplicates",
                "value": int(processed_df.duplicated().sum()),
            },
            {
                "metric": "raw_missing_values",
                "value": int(raw_df.isna().sum().sum()),
            },
            {
                "metric": "processed_missing_values",
                "value": int(processed_df.isna().sum().sum()),
            },
        ]
    )


def cramers_v(confusion_matrix: pd.DataFrame) -> float:
    """Calcula Cramer's V a partir de una tabla de contingencia."""
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    r, k = confusion_matrix.shape

    return np.sqrt(chi2 / (n * (min(r, k) - 1)))


def missing_values_report(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen de nulos por columna."""
    return (
        df.isna()
        .sum()
        .rename("missing_values")
        .to_frame()
        .assign(missing_pct=lambda x: x["missing_values"] / len(df) * 100)
        .sort_values("missing_values", ascending=False)
    )


def chi_square_report(
    df: pd.DataFrame,
    columns: list[str],
    target: str,
) -> pd.DataFrame:
    """Calcula chi-cuadrado y Cramer's V para variables categoricas."""
    rows = []

    for col in columns:
        table = pd.crosstab(df[col], df[target])
        chi2, p_value, dof, _ = chi2_contingency(table)
        rows.append(
            {
                "feature": col,
                "chi2": chi2,
                "p_value": p_value,
                "dof": dof,
                "cramers_v": cramers_v(table),
            }
        )

    return pd.DataFrame(rows).sort_values("cramers_v", ascending=False)


def target_distribution(df: pd.DataFrame, target: str = "depression_label") -> pd.DataFrame:
    """Devuelve recuentos y porcentajes de la variable objetivo."""
    counts = df[target].value_counts().sort_index()
    return pd.DataFrame(
        {
            target: counts.index,
            "count": counts.values,
            "percentage": (counts.values / len(df) * 100).round(2),
        }
    )


def numeric_summary_by_target(
    df: pd.DataFrame,
    target: str = "depression_label",
) -> pd.DataFrame:
    """Compara medias numericas por clase objetivo."""
    numeric_cols = [
        col for col in df.select_dtypes(include="number").columns
        if col != target
    ]
    summary = df.groupby(target)[numeric_cols].mean().T

    if 0 in summary.columns and 1 in summary.columns:
        summary["diff_1_minus_0"] = summary[1] - summary[0]
        summary["pct_diff_vs_0"] = (
            (summary["diff_1_minus_0"] / summary[0]) * 100
        ).round(2)

    return summary.reset_index(names="feature").round(3)


def crosstab_with_rates(
    df: pd.DataFrame,
    feature: str,
    target: str = "depression_label",
) -> pd.DataFrame:
    """Tabla cruzada con recuentos y tasa positiva por categoria."""
    table = pd.crosstab(df[feature], df[target])

    for label in [0, 1]:
        if label not in table.columns:
            table[label] = 0

    table = table[[0, 1]].rename(columns={0: "target_0_count", 1: "target_1_count"})
    table["total"] = table["target_0_count"] + table["target_1_count"]
    table["target_1_rate_pct"] = (
        table["target_1_count"] / table["total"] * 100
    ).round(2)

    return table.reset_index()
