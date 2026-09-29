import streamlit as st
import pandas as pd
from forecast import get_forecast
from matching import match_vessel, estimate_turnaround_time, estimate_voyage_time
from risk import (get_risk_alerts, get_port_congestion, get_idle_management_suggestion,
                  get_charter_timing_recommendation, get_coal_price_trend)


@st.cache_data
def run_analysis(origin, destination, cargo_tons, days):
    """Runs every backend check for one origin/destination/cargo combination."""
    match = match_vessel(origin, destination, cargo_tons)
    vessel = match["recommended"]
    if vessel is None:
        return {"match": match, "vessel": None}
    return {
        "match": match,
        "vessel": vessel,
        "forecast": get_forecast(vessel, periods=days),
        "charter": get_charter_timing_recommendation(vessel, periods=days),
        "risk": get_risk_alerts(vessel, periods=days),
        "idle": get_idle_management_suggestion(vessel, destination, periods=days),
        "congestion": get_port_congestion(destination),
        "coal": get_coal_price_trend("Australia", cargo_tons=cargo_tons),
        "voyage": estimate_voyage_time(origin, destination),
        "load": estimate_turnaround_time(origin, cargo_tons, is_origin=True),
        "discharge": estimate_turnaround_time(destination, cargo_tons, is_origin=False),
    }


def extract_port_name(raw):
    """Pulls the plain port name out of the dropdown label, which uses two
    different formats ('Country-Port-Berth' and 'Port<TAB>Country<TAB>Berth')."""
    parts = raw.replace("\t", "-").split("-")
    return parts[1].strip() if len(parts) > 2 else parts[0].strip()


st.title("Freight Forecasting & Prediction 🗺️")

with st.form("cargo_detail"):
    st.header("Cargo Details", divider="red")
    st.radio(
        "Choose the required cargo you want to look for 🏗️.",
        ["PRIMARY COKING COAL", "MEDIUM COKING COAL", "WEAK COKING COAL", "PCL COAL", "THERMAL COAL"],
        key="cargo_type",
    )
    cargo_qt = st.number_input("Volume of shipment", 1000, 500000, 10000, key="cargo_qt")
    submitted = st.form_submit_button("Submit", type="primary", disabled=False)
    if submitted:
        st.write(
            f"You have chosen :blue-background[{st.session_state.cargo_type}] "
            f"of volume :blue-background[{str(st.session_state.cargo_qt)}] Metric tonne."
        )

with st.form("shipping_details"):
    st.header("Voyage Details", divider="red")
    st.subheader("Choose your preferred ")
    st.subheader("1. Origin Port")

    if st.session_state.cargo_type == "PRIMARY COKING COAL":
        st.selectbox(
            "The following ports provide PRIMARY COKING COAL",
            (
                "Australia-Adani Abbot Point Terminal — Berth 1",
                "Australia-Adani Abbot Point Terminal — Berth 2",
                "Mozambique-Beira-Berth 8 — Coal Terminal (TCC8)",
                "Russia-Taman-Berth No. 1", "Russia-Taman-Berth No. 4",
                "Russia-Vanino-VaninoTransUgol Coal Terminal — Berth 01",
                "Russia-Vanino-VaninoTransUgol Coal Terminal — Berth 02",
                "USA-Baltimore-CONSOL Marine Terminal",
                "USA-Lamberts Point / Norfolk-Pier 6 — Lamberts Point Coal Terminal",
            ),
            key="origin_pt",
        )
    elif st.session_state.cargo_type == "MEDIUM COKING COAL":
        st.selectbox(
            "The following ports provide MEDIUM COKING COAL",
            (
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 1",
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 2",
                "Newcastle\tAustralia\tKooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                "Taman\tRussia\tBerth No. 1",
                "Taman\tRussia\tBerth No. 3",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 01",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 02",
                "Baltimore\tUSA\tCONSOL Marine Terminal",
                "Lamberts Point / Norfolk\tUSA\tPier 6 — Lamberts Point Coal Terminal",
            ),
            key="origin_pt",
        )
    elif st.session_state.cargo_type == "WEAK COKING COAL":
        st.selectbox(
            "The following ports provide WEAK COKING COAL",
            (
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 1",
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 2",
                "Newcastle\tAustralia\tKooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                "Taman\tRussia\tBerth No. 1",
                "Taman\tRussia\tBerth No. 3",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 01",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 02",
                "Baltimore\tUSA\tCONSOL Marine Terminal",
                "Lamberts Point / Norfolk\tUSA\tPier 6 — Lamberts Point Coal Terminal",
            ),
            key="origin_pt",
        )
    elif st.session_state.cargo_type == "PCL COAL":
        st.selectbox(
            "The following ports provide PCL COAL",
            (
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 1",
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 2",
                "Newcastle\tAustralia\tKooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                "Taboneo\tIndonesia\tTaboneo Anchorage (ship-to-ship coal loading)",
                "Tanjung Bara\tIndonesia\tTanjung Bara Coal Terminal — Deepwater Berth",
                "Taman\tRussia\tBerth No. 1",
                "Taman\tRussia\tBerth No. 3",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 01",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 02",
                "Baltimore\tUSA\tCONSOL Marine Terminal",
                "Lamberts Point / Norfolk\tUSA\tPier 6 — Lamberts Point Coal Terminal",
            ),
            key="origin_pt",
        )
    elif st.session_state.cargo_type == "THERMAL COAL":
        st.selectbox(
            "The following ports provide THERMAL COAL",
            (
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 1",
                "Abbot Point\tAustralia\tAdani Abbot Point Terminal — Berth 2",
                "Newcastle\tAustralia\tKooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                "Taboneo\tIndonesia\tTaboneo Anchorage (ship-to-ship coal loading)",
                "Tanjung Bara\tIndonesia\tTanjung Bara Coal Terminal — Deepwater Berth",
                "Beira\tMozambique\tBerth 8 — Coal Terminal (TCC8)",
                "Maputo / Matola\tMozambique\tMatola Coal Terminal (TCM)",
                "Taman\tRussia\tBerth No. 1",
                "Taman\tRussia\tBerth No. 3",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 01",
                "Vanino\tRussia\tVaninoTransUgol Coal Terminal — Berth 02",
                "Baltimore\tUSA\tCONSOL Marine Terminal",
                "Lamberts Point / Norfolk\tUSA\tPier 6 — Lamberts Point Coal Terminal",
            ),
            key="origin_pt",
        )

    st.subheader("2. Destination Port")

    if st.session_state.cargo_type == "PRIMARY COKING COAL":
        st.selectbox(
            "The following ports can import PRIMARY COKING COAL",
            (
                "Paradip\tIndia\tBerth No. 03 - New Coal Import Berth",
                "Gopalpur\tIndia\tBerth Nos. 1, 2 & 3 - Coastal Coal Handling",
                "Vizag\tIndia\tWQ-2 / WQ-3",
                "Dhamra\tIndia\tBB-1 / BB-2 - Mechanised Bulk Import Berths",
                "Sagar-Sandheads\tIndia\tSagar Anchorage / Sandheads Lighterage Point",
                "Haldia\tIndia\tBerth No. 1 - Multipurpose Dry Bulk",
                "Haldia\tIndia\tBerth No. 2 - Multipurpose Dry Bulk",
            ),
            key="destination_pt",
        )
    elif st.session_state.cargo_type == "MEDIUM COKING COAL":
        st.selectbox(
            "The following ports can import MEDIUM COKING COAL",
            (
                "Paradip\tIndia\tBerth No. 03 - New Coal Import Berth",
                "Gopalpur\tIndia\tBerth Nos. 1, 2 & 3 - Coastal Coal Handling",
                "Vizag\tIndia\tWQ-2 / WQ-3",
                "Dhamra\tIndia\tBB-1 / BB-2 - Mechanised Bulk Import Berths",
                "Sagar-Sandheads\tIndia\tSagar Anchorage / Sandheads Lighterage Point",
                "Haldia\tIndia\tBerth No. 1 - Multipurpose Dry Bulk",
                "Haldia\tIndia\tBerth No. 2 - Multipurpose Dry Bulk",
            ),
            key="destination_pt",
        )
    elif st.session_state.cargo_type == "WEAK COKING COAL":
        st.selectbox(
            "The following ports can import WEAK COKING COAL",
            (
                "Paradip\tIndia\tBerth No. 03 - New Coal Import Berth",
                "Gopalpur\tIndia\tBerth Nos. 1, 2 & 3 - Coastal Coal Handling",
                "Vizag\tIndia\tWQ-2 / WQ-3",
                "Dhamra\tIndia\tBB-1 / BB-2 - Mechanised Bulk Import Berths",
                "Sagar-Sandheads\tIndia\tSagar Anchorage / Sandheads Lighterage Point",
                "Haldia\tIndia\tBerth No. 1 - Multipurpose Dry Bulk",
                "Haldia\tIndia\tBerth No. 2 - Multipurpose Dry Bulk",
            ),
            key="destination_pt",
        )
    elif st.session_state.cargo_type == "PCL COAL":
        st.selectbox(
            "The following ports can import PCL COAL",
            (
                "Paradip\tIndia\tBerth No. 03 - New Coal Import Berth",
                "Gopalpur\tIndia\tBerth Nos. 1, 2 & 3 - Coastal Coal Handling",
                "Vizag\tIndia\tWQ-2 / WQ-3",
                "Dhamra\tIndia\tBB-1 / BB-2 - Mechanised Bulk Import Berths",
                "Sagar-Sandheads\tIndia\tSagar Anchorage / Sandheads Lighterage Point",
                "Haldia\tIndia\tBerth No. 1 - Multipurpose Dry Bulk",
                "Haldia\tIndia\tBerth No. 2 - Multipurpose Dry Bulk",
            ),
            key="destination_pt",
        )
    elif st.session_state.cargo_type == "THERMAL COAL":
        st.selectbox(
            "The following ports can import THERMAL COAL",
            (
                "Paradip\tIndia\tBerth No. 05  Coal Berth-01",
                "Gopalpur\tIndia\tBerth Nos. 1, 2 & 3 Coastal Coal Handling",
                "Paradip\tIndia\tBerth No. 06 Coal Berth-02",
                "Vizag\tIndia\tVGCB  Vizag General Cargo Berth",
                "Vizag\tIndia\tWQ-2 / WQ-3",
                "Gangavaram\tIndia\tMechanised Coal Berths 2 berths",
                "Dhamra\tIndia\tBB-1 / BB-2  Mechanised Bulk Import Berths",
                "Sagar-Sandheads\tIndia\tSagar Anchorage / Sandheads Lighterage Point",
                "Haldia\tIndia\tBerth No. 3  Mechanical Thermal Coal Handling Facility",
            ),
            key="destination_pt",
        )

    st.subheader("3. Contract Duration")
    st.text("Select the contract duration for your shipment")
    st.selectbox("", ("short term", "mid term"), key="contract_duration")
    submitted1 = st.form_submit_button("Submit", type="primary", disabled=False)

if submitted1:
    origin_name = extract_port_name(st.session_state.origin_pt)
    dest_name = extract_port_name(st.session_state.destination_pt)
    days = 30 if st.session_state.contract_duration == "short term" else 90

    st.write(
        f"You have chosen :blue-background[{st.session_state.cargo_type}] "
        f"of volume :blue-background[{str(st.session_state.cargo_qt)}] Metric tonne, "
        f"from :blue-background[{origin_name}] to :blue-background[{dest_name}] "
        f"for a :blue-background[{st.session_state.contract_duration}] contract duration."
    )

    try:
        st.session_state["result"] = run_analysis(
            origin_name, dest_name, st.session_state.cargo_qt, days
        )
    except ValueError as e:
        st.error(str(e))
        st.session_state["result"] = None

result = st.session_state.get("result")
if result:
    if result["vessel"] is None:
        st.warning("No single vessel type fits this cargo and port pair.")
    else:
        st.subheader(f"Recommended vessel: {result['vessel']}")
        st.write("Other compliant options:", result["match"]["compliant_options"])

        st.subheader("Charter Timing")
        st.write(result["charter"]["headline"])
        st.write(result["charter"]["action"])
        st.caption(result["charter"]["caution"])

        st.subheader("Voyage")
        st.write(
            f"Distance: {result['voyage']['distance_nm']:,} nm "
            f"({result['voyage']['voyage_time_days']} days at "
            f"{result['voyage']['assumed_speed_knots']} knots)"
        )
        st.caption("Straight-line distance estimate, not the actual sailed route.")

        load_hrs = result["load"]["turnaround_hours"]
        discharge_hrs = result["discharge"]["turnaround_hours"]
        st.write(f"Loading time at origin: {load_hrs if load_hrs is not None else 'data not available'} hours")
        st.write(f"Discharge time at destination: {discharge_hrs if discharge_hrs is not None else 'data not available'} hours")

        st.subheader("Risk & Idle Management")
        st.write(result["risk"]["message"])
        st.write("Idle management:", result["idle"]["suggestion"])
        st.write(f"Port congestion at {dest_name}: {result['congestion']['congestion_level']}")
        st.caption("Congestion is simulated for this demo.")

        st.subheader("Coal Price Context")
        st.write(
            f"${result['coal']['latest_price_usd_per_tonne']}/tonne as of "
            f"{result['coal']['as_of']} ({result['coal']['direction']}, "
            f"{result['coal']['change_3m_pct']}% over 3 months)"
        )
        st.write(f"Estimated cargo value: ${result['coal']['estimated_cargo_value_usd']:,}")

        st.subheader("Rate Forecast")
        chart_data = result["forecast"]["forecast"].set_index("Date")[
            ["Forecast", "Lower_Bound", "Upper_Bound"]
        ]
        st.line_chart(chart_data)
        st.caption("Market data ends July 2019. Forecast dates shown continue from there.")