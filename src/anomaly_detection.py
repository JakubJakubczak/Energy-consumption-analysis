import pandas as pd


def detect_anomalies(
    df: pd.DataFrame,
    column: str = "Global_active_power",
    window: int = 1440,
    threshold: float = 2.0,
) -> pd.DataFrame:
    df = df.copy()
    rolling_mean = df[column].rolling(window=window, min_periods=1).mean()
    rolling_std = df[column].rolling(window=window, min_periods=1).std()

    df["rolling_mean"] = rolling_mean
    df["rolling_std"] = rolling_std
    df["upper_bound"] = rolling_mean + threshold * rolling_std
    df["lower_bound"] = rolling_mean - threshold * rolling_std
    df["is_anomaly"] = (df[column] > df["upper_bound"]) | (df[column] < df["lower_bound"])

    return df


def get_anomaly_summary(df: pd.DataFrame) -> pd.DataFrame:
    anomalies = df[df["is_anomaly"]].copy()
    return anomalies
