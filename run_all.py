from forecast import get_forecast
from matching import match_vessel, estimate_turnaround_time, estimate_voyage_time
from risk import (get_risk_alerts, get_port_congestion, get_idle_management_suggestion,
                  get_charter_timing_recommendation, get_coal_price_trend)

# ---- change these to test other cases ----
ORIGIN = "Newcastle"
DESTINATION = "Paradip"
CARGO_TONS = 55000
VESSEL_TYPE = "Supramax"
# ------------------------------------------


def section(title):
    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)


def show_turnaround(label, port, is_origin):
    t = estimate_turnaround_time(port, CARGO_TONS, is_origin=is_origin)
    if t["turnaround_hours"] is None:
        print(f"{label} at {port}: no handling-rate data available")
    else:
        print(f"{label} at {port}: {t['turnaround_hours']} hours "
              f"({t['turnaround_days']} days) at {t['handling_rate_mt_hr']} t/hr")


section(f"INPUT: {ORIGIN} -> {DESTINATION} | {CARGO_TONS:,} tons | {VESSEL_TYPE}")

# ---------- forecast.py ----------
section("1. RATE FORECAST (forecast.py)")
fc = get_forecast(VESSEL_TYPE, periods=30)
f = fc["forecast"]
print(f"Last actual index value : {fc['history']['Rate'].iloc[-1]:.0f}")
print(f"Forecast, day 1         : {f['Forecast'].iloc[0]:.0f}")
print(f"Forecast, day 30        : {f['Forecast'].iloc[-1]:.0f} "
      f"(likely range {f['Lower_Bound'].iloc[-1]:.0f} to {f['Upper_Bound'].iloc[-1]:.0f})")
print(f"Forecast ends on        : {f['Date'].iloc[-1].date()}")

# ---------- matching.py ----------
section("2. VESSEL MATCHING (matching.py)")
m = match_vessel(ORIGIN, DESTINATION, CARGO_TONS)
print("Recommended vessel :", m["recommended"] or "None - no vessel type fits")
print("Compliant options  :", m["compliant_options"])
for vessel, info in m["details"].items():
    if not info["overall_compliant"]:
        issues = info["origin_issues"] + info["destination_issues"]
        if not info["fits_cargo"]:
            issues.append("cargo too large for this vessel type")
        print(f"  Rejected {vessel}: " + "; ".join(issues))

v = estimate_voyage_time(ORIGIN, DESTINATION)
print(f"\nDistance    : {v['distance_nm']:,} nm (straight-line estimate)")
print(f"Voyage time : {v['voyage_time_days']} days at {v['assumed_speed_knots']} knots")
show_turnaround("Loading time   ", ORIGIN, True)
show_turnaround("Discharge time ", DESTINATION, False)

# ---------- risk.py ----------
section("3. ADVICE AND RISK (risk.py)")
charter = get_charter_timing_recommendation(VESSEL_TYPE)
print(charter["headline"])
print("What to do :", charter["action"])
print("Caution    :", charter["caution"])

risk = get_risk_alerts(VESSEL_TYPE)
print("\nRisk alert :", risk["message"])

idle = get_idle_management_suggestion(VESSEL_TYPE, DESTINATION)
print("Idle advice:", idle["suggestion"])

cong = get_port_congestion(DESTINATION)
print(f"Congestion at {DESTINATION}: {cong['congestion_level']} (simulated)")

coal = get_coal_price_trend("Australia", cargo_tons=CARGO_TONS)
print(f"\nCoal price ({coal['as_of']}): ${coal['latest_price_usd_per_tonne']}/tonne, "
      f"{coal['direction']} ({coal['change_3m_pct']}% over 3 months, "
      f"{coal['change_12m_pct']}% over 12 months)")
print(f"Estimated cargo value: ${coal['estimated_cargo_value_usd']:,}")

# ---------- all four vessel types ----------
section("4. CHARTER TIMING FOR ALL FOUR VESSEL TYPES")
for vt in ["Handysize", "Supramax", "Panamax", "Capesize"]:
    print(get_charter_timing_recommendation(vt)["headline"])