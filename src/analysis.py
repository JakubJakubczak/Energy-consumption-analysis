import pandas as pd


def compute_statistics(df: pd.DataFrame, column: str = "Global_active_power") -> dict:
    series = df[column].dropna()
    return {
        "mean": round(series.mean(), 4),
        "median": round(series.median(), 4),
        "min": round(series.min(), 4),
        "max": round(series.max(), 4),
        "std": round(series.std(), 4),
        "sum": round(series.sum(), 4),
        "count": int(series.count()),
    }


def get_peak_and_offpeak_hours(df: pd.DataFrame, column: str = "Global_active_power") -> dict:
    hourly_avg = df.groupby(df.index.hour)[column].mean()
    peak_hours = hourly_avg.nlargest(3).index.tolist()
    offpeak_hours = hourly_avg.nsmallest(3).index.tolist()
    return {"peak_hours": peak_hours, "offpeak_hours": offpeak_hours}


def compare_periods(
    df: pd.DataFrame,
    period1_start: str,
    period1_end: str,
    period2_start: str,
    period2_end: str,
    column: str = "Global_active_power",
) -> dict:
    p1 = df.loc[period1_start:period1_end, column].sum()
    p2 = df.loc[period2_start:period2_end, column].sum()
    if p1 == 0:
        pct_change = float("inf") if p2 != 0 else 0.0
    else:
        pct_change = round(((p2 - p1) / p1) * 100, 2)
    return {
        "period1_sum": round(p1, 4),
        "period2_sum": round(p2, 4),
        "pct_change": pct_change,
    }


def aggregate_data(df: pd.DataFrame, freq: str, column: str = "Global_active_power") -> pd.DataFrame:
    agg = df[[column]].resample(freq).agg(["mean", "sum"])
    agg.columns = [f"{column}_mean", f"{column}_sum"]
    return agg
