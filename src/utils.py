import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


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
