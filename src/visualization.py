import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_aggregated(df_agg: pd.DataFrame, title: str, y_col: str) -> go.Figure:
    fig = px.line(df_agg, y=y_col, title=title)
    fig.update_layout(xaxis_title="Date", yaxis_title="Global Active Power (kW)")
    return fig


def plot_weekday_comparison(df: pd.DataFrame, days: list[str], column: str = "Global_active_power") -> go.Figure:
    day_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
        "Friday": 4, "Saturday": 5, "Sunday": 6,
    }
    fig = go.Figure()
    for day_name in days:
        day_num = day_map.get(day_name)
        if day_num is None:
            continue
        subset = df[df.index.dayofweek == day_num]
        hourly = subset.groupby(subset.index.hour)[column].mean()
        fig.add_trace(go.Scatter(x=hourly.index, y=hourly.values, mode="lines", name=day_name))
    fig.update_layout(
        title="Weekday Comparison — Average Hourly Consumption",
        xaxis_title="Hour of Day",
        yaxis_title="Global Active Power (kW)",
    )
    return fig


def plot_daily_profile(df: pd.DataFrame, column: str = "Global_active_power") -> go.Figure:
    df = df.copy()
    df["hour"] = df.index.hour
    df["is_weekend"] = df.index.dayofweek >= 5

    workday = df[~df["is_weekend"]].groupby("hour")[column].mean()
    weekend = df[df["is_weekend"]].groupby("hour")[column].mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=workday.index, y=workday.values, mode="lines", name="Workday"))
    fig.add_trace(go.Scatter(x=weekend.index, y=weekend.values, mode="lines", name="Weekend"))
    fig.update_layout(
        title="Daily Profile — Average Consumption by Hour",
        xaxis_title="Hour of Day",
        yaxis_title="Global Active Power (kW)",
    )
    return fig


def plot_anomalies(df: pd.DataFrame, column: str = "Global_active_power") -> go.Figure:
    # Resample to hourly for readability
    hourly = df[[column, "rolling_mean", "upper_bound", "lower_bound", "is_anomaly"]].resample("h").agg(
        {column: "mean", "rolling_mean": "mean", "upper_bound": "mean", "lower_bound": "mean", "is_anomaly": "any"}
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hourly.index, y=hourly[column], mode="lines", name="Actual", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=hourly.index, y=hourly["rolling_mean"], mode="lines", name="Rolling Mean", line=dict(color="green", dash="dash")))
    fig.add_trace(go.Scatter(x=hourly.index, y=hourly["upper_bound"], mode="lines", name="Upper Bound", line=dict(color="gray", dash="dot")))
    fig.add_trace(go.Scatter(x=hourly.index, y=hourly["lower_bound"], mode="lines", name="Lower Bound", line=dict(color="gray", dash="dot")))

    anomalies = hourly[hourly["is_anomaly"]]
    fig.add_trace(go.Scatter(
        x=anomalies.index, y=anomalies[column],
        mode="markers", name="Anomaly",
        marker=dict(color="red", size=6),
    ))
    fig.update_layout(title="Anomaly Detection", xaxis_title="Date", yaxis_title="Global Active Power (kW)")
    return fig


def plot_forecast(df: pd.DataFrame, forecast_df: pd.DataFrame, column: str = "Global_active_power") -> go.Figure:
    daily_hist = df[[column]].resample("D").mean().dropna()
    # Show last 90 days of history
    daily_hist = daily_hist.iloc[-90:]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_hist.index, y=daily_hist[column], mode="lines", name="Historical"))
    fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df["forecast"], mode="lines+markers", name="Forecast", line=dict(dash="dash", color="orange")))
    fig.update_layout(title="Energy Consumption Forecast", xaxis_title="Date", yaxis_title="Global Active Power (kW)")
    return fig
