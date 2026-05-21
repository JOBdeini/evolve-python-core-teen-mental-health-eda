from pathlib import Path

import pandas as pd


def load_data(path: str | Path) -> pd.DataFrame:
    """Carga un CSV y devuelve un DataFrame."""
    return pd.read_csv(path)


def save_data(df: pd.DataFrame, path: str | Path) -> None:
    """Guarda un DataFrame en CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
