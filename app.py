import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.preprocessing import handle_missing_values, filter_by_date_range, add_energy_kwh
from src.analysis import compute_statistics, get_peak_and_offpeak_hours, compare_periods, aggregate_data
from src.anomaly_detection import detect_anomalies, get_anomaly_summary
from src.forecasting import forecast
from src.visualization import (
    plot_aggregated,
    plot_weekday_comparison,
    plot_daily_profile,
    plot_anomalies,
    plot_forecast,
)

DATA_PATH = "data/household_power_consumption.txt"

st.set_page_config(page_title="Energy Consumption Analysis", layout="wide")
st.title("Energy Consumption Analysis")

# ── Load & cache data ──────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data…")
def get_data():
    df = load_data(DATA_PATH)
    df = handle_missing_values(df, method="interpolate")
    df = add_energy_kwh(df)
    return df

try:
    df_full = get_data()
except (FileNotFoundError, ValueError) as e:
    st.error(f"Data loading error: {e}")
    st.stop()

# ── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.header("Settings")

min_date = df_full.index.min().date()
max_date = df_full.index.max().date()

start_date = st.sidebar.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")
    st.stop()

df = filter_by_date_range(df_full, str(start_date), str(end_date))

if df.empty:
    st.warning("No data in the selected date range.")
    st.stop()

missing_method = st.sidebar.selectbox("Missing values handling", ["interpolate", "drop"])
aggregation = st.sidebar.selectbox("Aggregation", ["Daily", "Weekly", "Monthly"])
agg_map = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}
freq = agg_map[aggregation]

# ── Data preview ───────────────────────────────────────────────────────────
st.header("Data Preview")
page_size = 50
total_rows = len(df)
total_pages = max(1, (total_rows + page_size - 1) // page_size)
page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
start_idx = (page - 1) * page_size
st.dataframe(df.iloc[start_idx : start_idx + page_size], use_container_width=True)
st.caption(f"Showing rows {start_idx + 1}–{min(start_idx + page_size, total_rows)} of {total_rows}")

# ── Aggregated charts ─────────────────────────────────────────────────────
st.header(f"{aggregation} Consumption")
df_agg = aggregate_data(df, freq)
col_mean = "Global_active_power_mean"
col_sum = "Global_active_power_sum"

tab_mean, tab_sum = st.tabs(["Average", "Sum"])
with tab_mean:
    st.plotly_chart(plot_aggregated(df_agg, f"{aggregation} Average Consumption", col_mean), use_container_width=True)
with tab_sum:
    st.plotly_chart(plot_aggregated(df_agg, f"{aggregation} Total Consumption", col_sum), use_container_width=True)

# ── Weekday comparison ─────────────────────────────────────────────────────
st.header("Weekday Comparison")
all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
selected_days = st.multiselect("Select days to compare", all_days, default=["Monday", "Saturday"])
if selected_days:
    st.plotly_chart(plot_weekday_comparison(df, selected_days), use_container_width=True)

# ── Daily profile ─────────────────────────────────────────────────────────
st.header("Daily Profile (Workday vs Weekend)")
st.plotly_chart(plot_daily_profile(df), use_container_width=True)

# ── Statistics ─────────────────────────────────────────────────────────────
st.header("Statistics")
stats = compute_statistics(df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mean (kW)", stats["mean"])
col2.metric("Median (kW)", stats["median"])
col3.metric("Std Dev (kW)", stats["std"])
col4.metric("Sum (kW·min)", stats["sum"])

col5, col6, col7 = st.columns(3)
col5.metric("Min (kW)", stats["min"])
col6.metric("Max (kW)", stats["max"])
col7.metric("Count", stats["count"])

# Peak / off-peak hours
peak_info = get_peak_and_offpeak_hours(df)
st.subheader("Peak & Off-Peak Hours")
pcol1, pcol2 = st.columns(2)
pcol1.write(f"**Peak hours:** {', '.join(f'{h}:00' for h in peak_info['peak_hours'])}")
pcol2.write(f"**Off-peak hours:** {', '.join(f'{h}:00' for h in peak_info['offpeak_hours'])}")

# ── Period comparison ──────────────────────────────────────────────────────
st.header("Period Comparison")
comp_col1, comp_col2 = st.columns(2)
with comp_col1:
    st.subheader("Period 1")
    p1_start = st.date_input("P1 start", value=min_date, min_value=min_date, max_value=max_date, key="p1s")
    p1_end = st.date_input("P1 end", value=min_date + pd.Timedelta(days=30), min_value=min_date, max_value=max_date, key="p1e")
with comp_col2:
    st.subheader("Period 2")
    p2_start = st.date_input("P2 start", value=min_date + pd.Timedelta(days=31), min_value=min_date, max_value=max_date, key="p2s")
    p2_end = st.date_input("P2 end", value=min_date + pd.Timedelta(days=61), min_value=min_date, max_value=max_date, key="p2e")

if st.button("Compare Periods"):
    comp = compare_periods(df_full, str(p1_start), str(p1_end), str(p2_start), str(p2_end))
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Period 1 Sum (kW·min)", comp["period1_sum"])
    cc2.metric("Period 2 Sum (kW·min)", comp["period2_sum"])
    cc3.metric("Change (%)", f"{comp['pct_change']}%")

# ── Anomaly detection ─────────────────────────────────────────────────────
st.header("Anomaly Detection")
threshold = st.sidebar.slider("Anomaly threshold (σ)", min_value=1.5, max_value=3.0, value=2.0, step=0.1)
df_anomaly = detect_anomalies(df, threshold=threshold)
anomaly_count = df_anomaly["is_anomaly"].sum()
st.write(f"Detected **{anomaly_count}** anomalous data points (threshold = {threshold}σ)")
st.plotly_chart(plot_anomalies(df_anomaly), use_container_width=True)

# ── Forecast ───────────────────────────────────────────────────────────────
st.header("Forecast")
forecast_method = st.sidebar.selectbox("Forecast method", ["gradient_boosting", "moving_average"])
horizon = st.sidebar.selectbox("Forecast horizon (days)", [7, 14, 30])

forecast_df = forecast(df, method=forecast_method, horizon_days=horizon)
st.plotly_chart(plot_forecast(df, forecast_df), use_container_width=True)

# ── Export ─────────────────────────────────────────────────────────────────
st.header("Export Results")
export_col1, export_col2 = st.columns(2)
with export_col1:
    stats_df = pd.DataFrame([stats])
    st.download_button(
        "Download Statistics (CSV)",
        stats_df.to_csv(index=False),
        file_name="statistics.csv",
        mime="text/csv",
    )
with export_col2:
    anomalies_export = get_anomaly_summary(df_anomaly)
    st.download_button(
        "Download Anomalies (CSV)",
        anomalies_export.to_csv(),
        file_name="anomalies.csv",
        mime="text/csv",
    )
