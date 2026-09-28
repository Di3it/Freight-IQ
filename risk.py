"""
risk.py
Covers PS Requirements C (Idle Scenario Management) and D (Risk Mitigation).

This is intentionally rule-based rather than a full simulation/ML model - for a
demo, transparent rules on top of the forecast are more defensible than an
unvalidated "black box" prediction. In production, the congestion and
repositioning logic here would be replaced with live AIS/port-authority data
and a proper optimization-simulation model.

Uses:
    forecast.py -> get_forecast()
"""

from forecast import get_forecast
import pandas as pd
COAL_PRICE_PATH = "data/coal_price.csv" 
CHARTER_STRONG_THRESHOLD = 10   # % change over the forecast window -> clear Wait / Charter Now
CHARTER_LEAN_THRESHOLD = 2      # % change below this -> no clear signal
# Simple reference list of alternative regions a vessel could reposition toward,
# per vessel type - stand-in for real market/broker visibility (see caveat in
# the PS discussion: full "alternative employment" suggestions need live broker
# data this demo does not have access to).
REPOSITIONING_HUBS = {
    "Handysize": ["Southeast Asia", "West Coast India"],
    "Supramax": ["Southeast Asia", "West Coast India", "Persian Gulf"],
    "Panamax": ["China", "Persian Gulf"],
    "Capesize": ["China", "Brazil"],
}

# Thresholds for flagging volatility (percentage change over the forecast horizon)
VOLATILITY_WARNING_THRESHOLD = 0.10   # 10% swing -> "Watch"
VOLATILITY_HIGH_THRESHOLD = 0.20      # 20% swing -> "High risk"

# Simulated port congestion levels (stand-in for a live AIS/port-authority feed).
# In production this dict would be replaced by a real-time data source.
SIMULATED_CONGESTION = {
    "Paradip": "Low",
    "Vizag": "Moderate",
    "Gangavaram": "Low",
    "Gopalpur": "Low",
    "Dhamra": "Moderate",
    "Sagar-Sandheads": "High",
    "Haldia": "Moderate",
}


def get_risk_alerts(vessel_type: str, periods: int = 30):
    """
    Requirement D: Risk Mitigation / Early Warnings.

    Flags potential rate volatility by comparing the start and end of the
    forecast window, and returns a directional risk level.
    """
    result = get_forecast(vessel_type, periods=periods)
    forecast_df = result["forecast"]

    start_val = forecast_df["Forecast"].iloc[0]
    end_val = forecast_df["Forecast"].iloc[-1]
    pct_change = (end_val - start_val) / start_val

    if abs(pct_change) >= VOLATILITY_HIGH_THRESHOLD:
        level = "High"
    elif abs(pct_change) >= VOLATILITY_WARNING_THRESHOLD:
        level = "Watch"
    else:
        level = "Stable"

    direction = "rising" if pct_change > 0 else "falling"

    return {
        "vessel_type": vessel_type,
        "pct_change": round(pct_change * 100, 2),
        "direction": direction,
        "risk_level": level,
        "message": f"{vessel_type} rates projected {direction} by {abs(pct_change) * 100:.1f}% "
                   f"over the next {periods} days. Risk level: {level}.",
    }


def get_port_congestion(port_name: str):
    """
    Requirement D (supporting): port congestion flag.
    Uses simulated data for the demo - swap for a live feed in production.
    """
    level = SIMULATED_CONGESTION.get(port_name, "Unknown")
    return {
        "port": port_name,
        "congestion_level": level,
        "note": "Simulated for demo - production would use live AIS/port-authority data.",
    }


def get_idle_management_suggestion(vessel_type: str, destination_port: str, periods: int = 30):
    """
    Requirement C: Idle Scenario Management.

    If the forecast shows a falling trend (softening demand), suggests
    repositioning toward alternative regions for this vessel type, and flags
    the destination port's congestion as a factor affecting turnaround/idle time.
    """
    risk = get_risk_alerts(vessel_type, periods=periods)
    congestion = get_port_congestion(destination_port)

    suggestion = None
    if risk["direction"] == "falling" and risk["risk_level"] in ("Watch", "High"):
        hubs = REPOSITIONING_HUBS.get(vessel_type, [])
        suggestion = (
            f"Demand for {vessel_type} is softening. Consider positioning toward: "
            f"{', '.join(hubs)} to reduce idle/deadheading risk."
        )
    else:
        suggestion = f"No repositioning action indicated - the forecast change for {vessel_type} is too small to justify moving the vessel."

    return {
        "vessel_type": vessel_type,
        "destination_port": destination_port,
        "forecast_direction": risk["direction"],
        "risk_level": risk["risk_level"],
        "destination_congestion": congestion["congestion_level"],
        "suggestion": suggestion,
    }
def get_charter_timing_recommendation(vessel_type: str, periods: int = 30):
    """
    Requirement A: Optimal Market Entry Timing.
    Turns the forecast into a plain-language "charter now or wait" answer.
    """
    risk = get_risk_alerts(vessel_type, periods=periods)
    change = float(risk["pct_change"])
    size = abs(change)

    if size < CHARTER_LEAN_THRESHOLD:
        decision = "No clear signal"
        action = "Charter when your cargo is ready. Waiting is unlikely to change the price much."
        headline = (f"{vessel_type}: {decision}. Rates are expected to stay roughly flat "
                    f"({change:+.1f}%) over the next {periods} days.")
    else:
        if change < 0 and size < CHARTER_STRONG_THRESHOLD:
            decision = "Lean towards waiting"
            action = "Rates may ease a little. If your cargo date is flexible, waiting could save some cost."
        elif change < 0:
            decision = "Wait"
            action = "Rates are expected to fall noticeably. Delaying the charter, if possible, may get a lower rate."
        elif size < CHARTER_STRONG_THRESHOLD:
            decision = "Lean towards chartering now"
            action = "Rates may rise a little. If you are ready, chartering now avoids a small increase."
        else:
            decision = "Charter now"
            action = "Rates are expected to rise noticeably. Delaying may cost more."

        trend_word = "fall" if change < 0 else "rise"
        headline = (f"{vessel_type}: {decision}. Rates are expected to {trend_word} "
                    f"by about {size:.1f}% over the next {periods} days.")

    return {
        "vessel_type": vessel_type,
        "decision": decision,
        "headline": headline,
        "action": action,
        "direction": risk["direction"],
        "risk_level": risk["risk_level"],
        "pct_change": change,
        "reason": action,
        "caution": "This is a forecast based on past data, not a guarantee. It gets less certain the further ahead it looks.",
    }
def get_coal_price_trend(source: str = "Australia", cargo_tons: float = None):
    """
    Commodity price context: latest coal price, 3-month and 12-month change,
    and direction. Optionally estimates the cargo's value at the latest price.
    Monthly World Bank data (demo); production would use a live price feed.
    """
    columns = {
        "Australia": "Australia_USD_per_tonne",
        "South Africa": "SouthAfrica_USD_per_tonne",
    }
    if source not in columns:
        raise ValueError(f"Unknown source '{source}'. Choose from {list(columns.keys())}")
    column = columns[source]

    df = pd.read_csv(COAL_PRICE_PATH, parse_dates=["Date"]).sort_values("Date")
    series = df[["Date", column]].dropna().reset_index(drop=True)

    latest_price = series.iloc[-1][column]

    def pct_change(months):
        if len(series) <= months:
            return None
        past = series.iloc[-1 - months][column]
        return round((latest_price - past) / past * 100, 1)

    change_3m = pct_change(3)
    change_12m = pct_change(12)

    if change_3m is None:
        direction = "unknown"
    elif change_3m > 5:
        direction = "rising"
    elif change_3m < -5:
        direction = "falling"
    else:
        direction = "flat"

    result = {
        "source": source,
        "as_of": series.iloc[-1]["Date"].strftime("%Y-%m"),
        "latest_price_usd_per_tonne": round(latest_price, 2),
        "change_3m_pct": change_3m,
        "change_12m_pct": change_12m,
        "direction": direction,
        "note": "Monthly World Bank data for the demo - production would use a live price feed.",
    }
    if cargo_tons is not None:
        result["estimated_cargo_value_usd"] = round(cargo_tons * latest_price)
    return result


if __name__ == "__main__":
    print("=== Risk Alert ===")
    print(get_risk_alerts("Supramax", periods=30))

    print("\n=== Port Congestion ===")
    print(get_port_congestion("Paradip"))

    print("\n=== Idle Management Suggestion ===")
    print(get_idle_management_suggestion("Supramax", "Paradip", periods=30))

    print("\n=== Charter Timing Recommendation ===")
    print(get_charter_timing_recommendation("Supramax", periods=30))