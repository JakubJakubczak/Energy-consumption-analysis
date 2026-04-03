import pandas as pd


def handle_missing_values(df: pd.DataFrame, method: str = "interpolate") -> pd.DataFrame:
    if method == "drop":
        return df.dropna()
    elif method == "interpolate":
        return df.interpolate(method="time")
    else:
        raise ValueError(f"Unknown method: {method}. Use 'drop' or 'interpolate'.")


def filter_by_date_range(
    df: pd.DataFrame, start_date: str | None = None, end_date: str | None = None
) -> pd.DataFrame:
    if start_date:
        df = df[df.index >= pd.Timestamp(start_date)]
    if end_date:
        df = df[df.index <= pd.Timestamp(end_date)]
    return df


def add_energy_kwh(df: pd.DataFrame) -> pd.DataFrame:
    # Global_active_power is in kW, measured per minute -> kWh = kW * (1/60)
    df = df.copy()
    df["energy_kwh"] = df["Global_active_power"] / 60.0
    return df
