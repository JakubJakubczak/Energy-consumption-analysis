import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_moving_average(
    df: pd.DataFrame,
    column: str = "Global_active_power",
    horizon_days: int = 7,
    window_days: int = 30,
) -> pd.DataFrame:
    daily = df[[column]].resample("D").mean().dropna()
    ma = daily[column].rolling(window=window_days, min_periods=1).mean().iloc[-1]

    last_date = daily.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon_days, freq="D")
    forecast = pd.DataFrame({"forecast": [ma] * horizon_days}, index=future_dates)
    return forecast


def forecast_linear_regression(
    df: pd.DataFrame,
    column: str = "Global_active_power",
    horizon_days: int = 7,
) -> pd.DataFrame:
    daily = df[[column]].resample("D").mean().dropna()
    daily = daily.reset_index()
    daily["day_num"] = (daily["datetime"] - daily["datetime"].min()).dt.days

    X = daily[["day_num"]].values
    y = daily[column].values

    model = LinearRegression()
    model.fit(X, y)

    last_day = int(daily["day_num"].iloc[-1])
    last_date = daily["datetime"].iloc[-1]
    future_days = np.arange(last_day + 1, last_day + 1 + horizon_days).reshape(-1, 1)
    predictions = model.predict(future_days)

    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon_days, freq="D")
    forecast = pd.DataFrame({"forecast": predictions}, index=future_dates)
    return forecast


def forecast(
    df: pd.DataFrame,
    method: str = "linear_regression",
    column: str = "Global_active_power",
    horizon_days: int = 7,
) -> pd.DataFrame:
    if method == "linear_regression":
        return forecast_linear_regression(df, column, horizon_days)
    elif method == "moving_average":
        return forecast_moving_average(df, column, horizon_days)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'linear_regression' or 'moving_average'.")
