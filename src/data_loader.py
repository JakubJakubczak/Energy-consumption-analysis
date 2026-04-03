import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = [
    "Date", "Time", "Global_active_power", "Global_reactive_power",
    "Voltage", "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3",
]


def validate_columns(df: pd.DataFrame) -> list[str]:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing


def load_data(file_path: str | Path) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(
        path,
        sep=";",
        low_memory=False,
        na_values=["?", ""],
    )

    missing_cols = validate_columns(df)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Combine Date + Time into a single datetime column
    df["datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S"
    )
    df = df.drop(columns=["Date", "Time"])
    df = df.set_index("datetime").sort_index()

    # Convert numeric columns
    numeric_cols = [c for c in df.columns]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    return df
