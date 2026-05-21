from pathlib import Path

from src.cleaning import clean_data
from src.features import build_features
from src.io import load_data, save_data

RAW_DATA_PATH = Path("data/raw/Teen_Mental_Health_Dataset.csv")
PROCESSED_DATA_PATH = Path("data/processed/teen_mental_health_processed.csv")


def main() -> None:
    """Ejecuta el pipeline de limpieza y feature engineering."""
    df = load_data(RAW_DATA_PATH)
    df = clean_data(df)
    df = build_features(df)
    save_data(df, PROCESSED_DATA_PATH)

    print(f"Dataset procesado guardado en: {PROCESSED_DATA_PATH}")
    print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")


if __name__ == "__main__":
    main()
