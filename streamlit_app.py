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
    if not raw:
        return ""
    parts = raw.replace("\t", "-").split("-")
    return parts[0].strip()


# Set wide page layout to give maximum side-by-side space
st.set_page_config(page_title="Freight Forecasting", layout="wide")

st.title("Freight Forecasting & Prediction 🗺️")

# ---------------------------------------------------------
# 1. PROCESS TAB SWITCHES BEFORE WIDGET INSTANTIATION
# ---------------------------------------------------------
if "target_tab" in st.session_state:
    st.session_state["active_tab"] = st.session_state.pop("target_tab")

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "📋 Input"

# ---------------------------------------------------------
# 2. RENDER TOP NAVIGATION WIDGET
# ---------------------------------------------------------
active_tab = st.radio(
    "Navigation",
    options=["📋 Input", "📊 Results"],
    horizontal=True,
    key="active_tab",
    label_visibility="collapsed"
)

# =========================================================
# TAB 1: INPUT FORM
# =========================================================
if active_tab == "📋 Input":
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
                ("Abbot Point-Australia-Adani Abbot Point Terminal — Berth 1",
                 "Abbot Point-Australia-Adani Abbot Point Terminal — Berth 2",
                 "Beira-Mozambique-Berth 8 — Coal Terminal (TCC8)",
                 "Taman-Russia-Berth No. 1", "Taman-Russia-Berth No. 4",
                 "Vanino-Russia-VaninoTransUgol Coal Terminal — Berth 01",
                 "Vanino-Russia-VaninoTransUgol Coal Terminal — Berth 02",
                 "Baltimore-USA-CONSOL Marine Terminal",
                 "Lamberts Point / Norfolk-USA-Pier 6 — Lamberts Point Coal Terminal",
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
        st.selectbox("Choose contract duration", ["short term", "mid term"], key="contract_duration")
        submitted1 = st.form_submit_button("Submit", type="primary", disabled=False)

    if submitted1:
        origin_name = extract_port_name(st.session_state.origin_pt)
        dest_name = extract_port_name(st.session_state.destination_pt)
        days = 30 if st.session_state.contract_duration == "short term" else 90

        try:
            st.session_state["result"] = run_analysis(
                origin_name, dest_name, st.session_state.cargo_qt, days
            )
        except ValueError as e:
            st.error(str(e))
            st.session_state["result"] = None

        # Store target tab for next run and trigger rerun
        st.session_state["target_tab"] = "📊 Results"
        st.rerun()

# =========================================================
# TAB 2: RESULTS VIEW (COMPACT SIDE-BY-SIDE DASHBOARD)
# =========================================================
if active_tab == "📊 Results":
    result = st.session_state.get("result")
    if result:
        dest_name = extract_port_name(st.session_state.get("destination_pt", ""))
        origin_name = extract_port_name(st.session_state.get("origin_pt", ""))

        # Top summary bar
        st.info(
            f"**Cargo:** {st.session_state.cargo_type} | "
            f"**Volume:** {st.session_state.cargo_qt:,} MT | "
            f"**Route:** {origin_name} ➔ {dest_name} | "
            f"**Duration:** {st.session_state.contract_duration}"
        )

        if result["vessel"] is None:
            st.warning("No single vessel type fits this cargo and port pair.")
        else:
            # Side-by-side Layout
            col1, col2 = st.columns([1, 1], gap="medium")

            with col1:
                st.subheader("🚢 Vessel & Voyage")
                
                # Metric Cards
                m1, m2, m3 = st.columns(3)
                m1.metric("Recommended Vessel", result['vessel'])
                m2.metric("Distance", f"{result['voyage']['distance_nm']:,} nm")
                m3.metric("Voyage Time", f"{result['voyage']['voyage_time_days']} days")

                st.caption(f"**Other options:** {', '.join(result['match']['compliant_options'])}")
                
                load_hrs = result["load"]["turnaround_hours"]
                discharge_hrs = result["discharge"]["turnaround_hours"]
                st.write(
                    f"**Turnaround:** Load ({origin_name}): **{load_hrs or 'N/A'} hrs** | "
                    f"Discharge ({dest_name}): **{discharge_hrs or 'N/A'} hrs**"
                )

                st.divider()

                st.subheader("📈 Rate Forecast")
                chart_data = result["forecast"]["forecast"].set_index("Date")[
                    ["Forecast", "Lower_Bound", "Upper_Bound"]
                ]
                st.line_chart(chart_data, height=220)

            with col2:
                st.subheader("⏱️ Charter & Market Context")
                
                st.success(f"**Action:** {result['charter']['headline']} - {result['charter']['action']}")
                
                m4, m5 = st.columns(2)
                m4.metric(
                    label="Coal Price",
                    value=f"${result['coal']['latest_price_usd_per_tonne']}/MT",
                    delta=f"{result['coal']['change_3m_pct']}% (3m)"
                )
                m5.metric("Est. Cargo Value", f"${result['coal']['estimated_cargo_value_usd']:,}")

                st.divider()

                st.subheader("⚠️ Risk & Port Congestion")
                st.write(f"• **Risk Alert:** {result['risk']['message']}")
                st.write(f"• **Idle Strategy:** {result['idle']['suggestion']}")
                st.write(f"• **Port Congestion at {dest_name}:** `{result['congestion']['congestion_level']}`")

    else:
        st.info("Fill in the Input tab and submit to see your results here.")