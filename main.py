from pathlib import Path

from src.cleaning import clean_data
from src.features import build_features
from src.io import load_data, save_data
from src.utils import (
    chi_square_report,
    crosstab_with_rates,
    data_quality_summary,
    numeric_summary_by_target,
    target_distribution,
    validate_dataset,
)
from src.viz import (
    save_correlation_matrix,
    save_cramers_v_by_category,
    save_depression_rate_by_category,
    save_numeric_distributions,
    save_numeric_vs_target,
    save_target_distribution,
)

RAW_DATA_PATH = Path("data/raw/Teen_Mental_Health_Dataset.csv")
PROCESSED_DATA_PATH = Path("data/processed/teen_mental_health_processed.csv")
FIGURES_DIR = Path("reports/figures")
TABLES_DIR = Path("reports/tables")

CATEGORICAL_COLUMNS = [
    "gender",
    "platform_usage",
    "social_interaction_level",
    "sleep_quality",
    "risk_category",
    "heavy_social_media_user",
]


def save_report_tables(raw_df, processed_df) -> None:
    """Exporta tablas clave para revisar el EDA sin ejecutar el notebook."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    data_quality_summary(raw_df, processed_df).to_csv(
        TABLES_DIR / "data_quality_summary.csv",
        index=False,
    )
    validate_dataset(processed_df).to_csv(
        TABLES_DIR / "validation_report.csv",
        index=False,
    )
    target_distribution(processed_df).to_csv(
        TABLES_DIR / "target_distribution.csv",
        index=False,
    )
    numeric_summary_by_target(processed_df).to_csv(
        TABLES_DIR / "numeric_summary_by_target.csv",
        index=False,
    )
    chi_square_report(
        processed_df,
        CATEGORICAL_COLUMNS,
        "depression_label",
    ).to_csv(TABLES_DIR / "chi_square_report.csv", index=False)

    for feature in [
        "heavy_social_media_user",
        "sleep_quality",
        "risk_category",
        "gender",
        "platform_usage",
        "social_interaction_level",
    ]:
        crosstab_with_rates(processed_df, feature).to_csv(
            TABLES_DIR / f"{feature}_by_depression_label.csv",
            index=False,
        )


def save_report_figures(df) -> None:
    """Exporta las visualizaciones principales del EDA."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    numeric_cols = df.select_dtypes(include="number").columns
    chi_report = chi_square_report(df, CATEGORICAL_COLUMNS, "depression_label")

    save_target_distribution(df, FIGURES_DIR / "01_target_distribution.png")
    save_numeric_distributions(df, FIGURES_DIR / "02_numeric_distributions.png", numeric_cols)
    save_correlation_matrix(df, FIGURES_DIR / "03_correlation_matrix.png", numeric_cols)
    save_numeric_vs_target(df, FIGURES_DIR / "04_numeric_vs_depression_label.png")
    save_depression_rate_by_category(
        df,
        FIGURES_DIR / "05_depression_rate_by_category.png",
        ["gender", "platform_usage", "social_interaction_level"],
    )
    save_cramers_v_by_category(chi_report, FIGURES_DIR / "06_cramers_v_by_category.png")


def main() -> None:
    """Ejecuta el pipeline completo de datos, tablas y figuras."""
    raw_df = load_data(RAW_DATA_PATH)
    processed_df = clean_data(raw_df)
    processed_df = build_features(processed_df)

    save_data(processed_df, PROCESSED_DATA_PATH)
    save_report_tables(raw_df, processed_df)
    save_report_figures(processed_df)

    print(f"Dataset procesado guardado en: {PROCESSED_DATA_PATH}")
    print(f"Tablas guardadas en: {TABLES_DIR}")
    print(f"Figuras guardadas en: {FIGURES_DIR}")
    print(f"Filas: {processed_df.shape[0]} | Columnas: {processed_df.shape[1]}")


if __name__ == "__main__":
    main()
