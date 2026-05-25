import pandas as pd


def create_heavy_usage(df: pd.DataFrame, threshold: float = 5) -> pd.DataFrame:
    """Marca adolescentes con uso diario intensivo de redes sociales."""
    df = df.copy()
    df["heavy_social_media_user"] = (
        df["daily_social_media_hours"] >= threshold
    ).astype(int)

    return df


def create_sleep_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Clasifica las horas de sueno en niveles interpretables."""
    df = df.copy()
    df["sleep_quality"] = pd.cut(
        df["sleep_hours"],
        bins=[0, 5, 7, float("inf")],
        labels=["poor", "normal", "good"],
        include_lowest=True,
    )

    return df


def create_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """Crea un indice heuristico de riesgo exploratorio.

    No es una metrica clinica. Resume senales observadas en el EDA:
    uso de redes, sueno, estres, ansiedad y rendimiento academico.
    """
    df = df.copy()
    df["risk_score"] = (
        df["daily_social_media_hours"] * 0.30
        + (10 - df["sleep_hours"]) * 0.25
        + df["stress_level"] * 0.20
        + df["anxiety_level"] * 0.20
        - df["academic_performance"] * 0.15
    )

    return df


def create_risk_category(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa el risk_score en terciles bajo, medio y alto."""
    df = df.copy()
    df["risk_category"] = pd.qcut(
        df["risk_score"],
        q=3,
        labels=["low", "medium", "high"],
        duplicates="drop",
    )

    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ejecuta todo el pipeline de feature engineering."""
    df = create_heavy_usage(df)
    df = create_sleep_quality(df)
    df = create_risk_score(df)
    df = create_risk_category(df)

    return df
