import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor


def _build_features(daily: pd.DataFrame, column: str) -> pd.DataFrame:
    df = daily[[column]].copy()
    df["day_of_week"] = df.index.dayofweek
    df["month"] = df.index.month
    df["day_of_year"] = df.index.dayofyear
    df["lag_7"] = df[column].shift(7)
    df["lag_14"] = df[column].shift(14)
    df["lag_30"] = df[column].shift(30)
    df["rolling_7"] = df[column].shift(1).rolling(7, min_periods=1).mean()
    df["rolling_30"] = df[column].shift(1).rolling(30, min_periods=1).mean()
    return df


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


def forecast_gradient_boosting(
    df: pd.DataFrame,
    column: str = "Global_active_power",
    horizon_days: int = 7,
) -> pd.DataFrame:
    daily = df[[column]].resample("D").mean().dropna()
    featured = _build_features(daily, column)
    featured = featured.dropna()

    feature_cols = ["day_of_week", "month", "day_of_year", "lag_7", "lag_14", "lag_30", "rolling_7", "rolling_30"]
    X = featured[feature_cols].values
    y = featured[column].values

    model = GradientBoostingRegressor(n_estimators=200, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X, y)

    # Iteratively predict future days
    last_date = daily.index[-1]
    history = daily[column].tolist()
    predictions = []

    for i in range(horizon_days):
        future_date = last_date + pd.Timedelta(days=i + 1)
        day_of_week = future_date.dayofweek
        month = future_date.month
        day_of_year = future_date.timetuple().tm_yday
        lag_7 = history[-7] if len(history) >= 7 else history[-1]
        lag_14 = history[-14] if len(history) >= 14 else history[-1]
        lag_30 = history[-30] if len(history) >= 30 else history[-1]
        rolling_7 = np.mean(history[-7:])
        rolling_30 = np.mean(history[-30:])

        X_pred = np.array([[day_of_week, month, day_of_year, lag_7, lag_14, lag_30, rolling_7, rolling_30]])
        pred = model.predict(X_pred)[0]
        predictions.append(pred)
        history.append(pred)

    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon_days, freq="D")
    return pd.DataFrame({"forecast": predictions}, index=future_dates)


def forecast(
    df: pd.DataFrame,
    method: str = "gradient_boosting",
    column: str = "Global_active_power",
    horizon_days: int = 7,
) -> pd.DataFrame:
    if method == "gradient_boosting":
        return forecast_gradient_boosting(df, column, horizon_days)
    elif method == "moving_average":
        return forecast_moving_average(df, column, horizon_days)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'gradient_boosting' or 'moving_average'.")
