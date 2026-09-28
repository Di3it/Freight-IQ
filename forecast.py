"""
forecast.py
Freight rate forecasting for the Freight Forecasting Model demo.

Uses historical Baltic sub-index data (data/baltic_dry_index.csv) to forecast
future freight rate trends for a given vessel type using ARIMA.

Supported vessel types (mapped to BDI columns):
    "Handysize" -> HSI
    "Supramax"  -> SI
    "Panamax"   -> PI
    "Capesize"  -> CI
"""

import pandas as pd
import warnings
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")  # ARIMA prints noisy convergence warnings; safe to ignore for a demo

# Maps user-friendly vessel type names to the actual BDI column names
VESSEL_COLUMN_MAP = {
    "Handysize": "HSI",
    "Supramax": "SI",
    "Panamax": "PI",
    "Capesize": "CI",
}

DATA_PATH = "data/baltic_dry_index.csv"


def load_bdi_data():
    """Loads and cleans the Baltic Dry Index dataset."""
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def get_forecast(vessel_type: str, periods: int = 30):
    """
    Forecasts freight rate index values for the given vessel type.

    Args:
        vessel_type: one of "Handysize", "Supramax", "Panamax", "Capesize"
        periods: number of future days to forecast

    Returns:
        dict with:
            history: DataFrame of historical Date + rate values
            forecast: DataFrame of forecasted Date + predicted rate + lower/upper confidence bounds
    """
    if vessel_type not in VESSEL_COLUMN_MAP:
        raise ValueError(f"Unknown vessel_type '{vessel_type}'. Choose from {list(VESSEL_COLUMN_MAP.keys())}")

    column = VESSEL_COLUMN_MAP[vessel_type]
    df = load_bdi_data()

    series = df[["Date", column]].dropna().reset_index(drop=True)
    series = series.rename(columns={column: "Rate"})

    # Fit ARIMA model (order chosen as a reasonable general-purpose default for a demo)
    model = ARIMA(series["Rate"], order=(2, 1, 2))
    fitted = model.fit()

    forecast_result = fitted.get_forecast(steps=periods)
    forecast_mean = forecast_result.predicted_mean
    conf_int = forecast_result.conf_int(alpha=0.2)  # 80% confidence interval

    last_date = series["Date"].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq="D")

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast": forecast_mean.values,
        "Lower_Bound": conf_int.iloc[:, 0].values,
        "Upper_Bound": conf_int.iloc[:, 1].values,
    })

    return {
        "vessel_type": vessel_type,
        "history": series,
        "forecast": forecast_df,
    }


if __name__ == "__main__":
    # Quick manual test when running this file directly
    for vessel in ["Handysize", "Supramax"]:
        result = get_forecast(vessel, periods=14)
        print(f"\n=== {vessel} Forecast (next 14 days) ===")
        print(result["forecast"]) 