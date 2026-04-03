from src.data_loader import load_data
from src.preprocessing import handle_missing_values, filter_by_date_range, add_energy_kwh
from src.analysis import compute_statistics, get_peak_and_offpeak_hours, compare_periods, aggregate_data
from src.anomaly_detection import detect_anomalies, get_anomaly_summary
from src.forecasting import forecast
from src.visualization import plot_aggregated, plot_weekday_comparison, plot_daily_profile, plot_anomalies, plot_forecast

print("Loading data...")
df = load_data("data/household_power_consumption.txt")
print(f"Loaded: {df.shape}, index range: {df.index.min()} to {df.index.max()}")
print(f"NaN count: {df.isna().sum().sum()}")

print("Handling missing values...")
df = handle_missing_values(df, "interpolate")
print(f"After interpolation NaN: {df.isna().sum().sum()}")

df = add_energy_kwh(df)
print(f"energy_kwh column added: {df['energy_kwh'].head(3).tolist()}")

print("Filtering by date range...")
df_filtered = filter_by_date_range(df, "2007-01-01", "2007-01-31")
print(f"Filtered shape: {df_filtered.shape}")

print("Computing statistics...")
stats = compute_statistics(df_filtered)
print(f"Stats: {stats}")

print("Peak hours...")
peak = get_peak_and_offpeak_hours(df_filtered)
print(f"Peak: {peak}")

print("Aggregating daily...")
agg = aggregate_data(df_filtered, "D")
print(f"Daily agg shape: {agg.shape}, head:")
print(agg.head())

print("Period comparison...")
comp = compare_periods(df, "2007-01-01", "2007-01-31", "2007-02-01", "2007-02-28")
print(f"Comparison: {comp}")

print("Anomaly detection...")
df_anom = detect_anomalies(df_filtered, threshold=2.0)
anom_count = df_anom["is_anomaly"].sum()
print(f"Anomalies detected: {anom_count}")

print("Anomaly summary...")
summary = get_anomaly_summary(df_anom)
print(f"Anomaly summary rows: {len(summary)}")

print("Forecasting (linear regression)...")
fc = forecast(df, method="linear_regression", horizon_days=7)
print(f"Forecast:\n{fc}")

print("Forecasting (moving average)...")
fc2 = forecast(df, method="moving_average", horizon_days=7)
print(f"Moving avg forecast:\n{fc2}")

print("Testing visualizations...")
fig1 = plot_aggregated(agg, "Test daily", "Global_active_power_mean")
print(f"plot_aggregated: OK")

fig2 = plot_weekday_comparison(df_filtered, ["Monday", "Saturday"])
print(f"plot_weekday_comparison: OK")

fig3 = plot_daily_profile(df_filtered)
print(f"plot_daily_profile: OK")

fig4 = plot_anomalies(df_anom)
print(f"plot_anomalies: OK")

fig5 = plot_forecast(df, fc)
print(f"plot_forecast: OK")

print("\n=== ALL TESTS PASSED! ===")
