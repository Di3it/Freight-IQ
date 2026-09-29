import streamlit as st
import pandas as pd
from forecast import get_forecast
from matching import match_vessel, estimate_turnaround_time, estimate_voyage_time, get_port_lists
from risk import (get_risk_alerts, get_port_congestion, get_idle_management_suggestion,
                  get_charter_timing_recommendation, get_coal_price_trend)
@st.cache_data
def run_analysis(origin, destination, cargo_tons, days):
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
@st.cache_data
def run_analysis(origin, destination, cargo_tons, days):
    ...
    # (unchanged, keep as is)


def extract_port_name(raw):
    parts = raw.replace("\t", "-").split("-")
    return parts[1].strip() if len(parts) > 2 else parts[0].strip()




st.title("Frieght forecasting & prediction🗺️")
with st.form("cargo_detail"):
  st.header("Cargo Details", divider="red")
  st.radio("choose the required cargo you want to look for🏗️.",
         ["PRIMARY COKING COAL","MEDIUM COKING COAL","WEAK COKING COAL","PCL COAL","THERMAL COAL"],
         key ="cargo_type")
  cargo_qt = st.number_input("Volume of shipment",1000,500000,10000,key = "cargo_qt")
  submitted = st.form_submit_button("Submit",type="primary",disabled=False)
  if submitted:
  
   st.write(f"You have chosen :blue-background[{st.session_state.cargo_type}] of volume :blue-background[{str(st.session_state.cargo_qt)}] Metric tonne.")
with st.form("shipping_details"):
     st.header("Voyage Details", divider="red")
     st.subheader("Choose your preferred ")
     st.subheader("1. Origin Port")
     if st.session_state.cargo_type == "PRIMARY COKING COAL":
      st.selectbox("the following ports provide PRIMARY COKING COAL",
               ("Abbot Point	Australia	Adani Abbot Point Terminal — Berth 1",
                 "Abbot Point	Australia	Adani Abbot Point Terminal — Berth 2",
                  "Mozambique-Beira-Berth 8 — Coal Terminal (TCC8)",
                  "Russia-Taman-Berth No. 1","Russia-Taman-Berth No. 4",
                  "Russia-Vanino-VaninoTransUgol Coal Terminal — Berth 01",
                  "Russia-Vanino-VaninoTransUgol Coal Terminal — Berth 02",
                  "USA-Baltimore-CONSOL Marine Terminal",
                  "USA-Lamberts Point / Norfolk-Pier 6 — Lamberts Point Coal Terminal"
                  
                  ),key = "origin_pt"
               )
     elif st.session_state.cargo_type == "MEDIUM COKING COAL":
            st.selectbox("the following ports provide MEDIUM COKING COAL",
                     ("Abbot Point	Australia	Adani Abbot Point Terminal — Berth 1", 
                      "Abbot Point	Australia	Adani Abbot Point Terminal — Berth 2",
                       "Newcastle	Australia	Kooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                       "Taman	Russia	Berth No. 1",
                       "Taman	Russia	Berth No. 3",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 01",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 02",
                       "Baltimore	USA	CONSOL Marine Terminal",
                       "Lamberts Point / Norfolk	USA	Pier 6 — Lamberts Point Coal Terminal"
                       ),key = "origin_pt"
                     )
     elif st.session_state.cargo_type == "WEAK COKING COAL":
            st.selectbox("the following ports provide WEAK COKING COAL",
                     ("Abbot Point	Australia	Adani Abbot Point Terminal — Berth 1", 
                      "Abbot Point	Australia	Adani Abbot Point Terminal — Berth 2",
                       "Newcastle	Australia	Kooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                       "Taman	Russia	Berth No. 1",
                       "Taman	Russia	Berth No. 3",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 01",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 02",
                       "Baltimore	USA	CONSOL Marine Terminal",
                       "Lamberts Point / Norfolk	USA	Pier 6 — Lamberts Point Coal Terminal"
                       ),key = "origin_pt"
                    )
     elif st.session_state.cargo_type == "PCL COAL":
            st.selectbox("the following ports provide PCL COAL",
                     ("Abbot Point	Australia	Adani Abbot Point Terminal — Berth 1",
                      "Abbot Point	Australia	Adani Abbot Point Terminal — Berth 2",
                      "Newcastle	Australia	Kooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                      "Taboneo	Indonesia	Taboneo Anchorage (ship-to-ship coal loading)",
                      "Tanjung Bara	Indonesia	Tanjung Bara Coal Terminal — Deepwater Berth",
                      "Taman	Russia	Berth No. 1",
                      "Taman	Russia	Berth No. 3",
                      "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 01",
                      "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 02",
                      "Baltimore	USA	CONSOL Marine Terminal",
                      "Lamberts Point / Norfolk	USA	Pier 6 — Lamberts Point Coal Terminal",     
                      ),key = "origin_pt"
                     )
     elif st.session_state.cargo_type == "THERMAL COAL":
            st.selectbox("the following ports provide THERMAL COAL",
                     ("Abbot Point	Australia	Adani Abbot Point Terminal — Berth 1",
                      "Abbot Point	Australia	Adani Abbot Point Terminal — Berth 2",
                            "Newcastle	Australia	Kooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                            "Taboneo	Indonesia	Taboneo Anchorage (ship-to-ship coal loading)",
                            "Tanjung Bara	Indonesia	Tanjung Bara Coal Terminal — Deepwater Berth",
                            "Beira	Mozambique	Berth 8 — Coal Terminal (TCC8)",
                            "Maputo / Matola	Mozambique	Matola Coal Terminal (TCM)",
                            "Taman	Russia	Berth No. 1",
                            "Taman	Russia	Berth No. 3",
                            "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 01",
                            "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 02",
                            "Baltimore	USA	CONSOL Marine Terminal",
                            "Lamberts Point / Norfolk	USA	Pier 6 — Lamberts Point Coal Terminal"
                      ),key = "origin_pt"
                     )
     
     st.subheader("2. Destination Port")
     if st.session_state.cargo_type == "PRIMARY COKING COAL":
      st.selectbox("the following ports can import PRIMARY COKING COAL",
               (
                    "Paradip	India	Berth No. 03 - New Coal Import Berth",
                    "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                    "Vizag	India	WQ-2 / WQ-3",
                    "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                    "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                    "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                    "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
               ),key = "destination_pt"
               )
     elif st.session_state.cargo_type == "MEDIUM COKING COAL":
            st.selectbox("the following ports can import MEDIUM COKING COAL",
                     (
                       "Paradip	India	Berth No. 03 - New Coal Import Berth",
                            "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                            "Vizag	India	WQ-2 / WQ-3",
                            "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                            "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                            "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                            "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
                     ),key = "destination_pt"
                     )
     elif st.session_state.cargo_type == "WEAK COKING COAL":
            st.selectbox("the following ports can import WEAK COKING COAL",
                     (
                            "Paradip	India	Berth No. 03 - New Coal Import Berth",
                            "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                            "Vizag	India	WQ-2 / WQ-3",
                            "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                            "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                            "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                            "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
                     ),key = "destination_pt"
                     )

     elif st.session_state.cargo_type == "PCL COAL":
            st.selectbox("the following ports can import PCL COAL",
                     (
                            "Paradip	India	Berth No. 03 - New Coal Import Berth",
                            "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                            "Vizag	India	WQ-2 / WQ-3",
                            "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                            "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                            "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                            "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
                     ),key = "destination_pt"
                     )
     elif st.session_state.cargo_type == "THERMAL COAL":
            st.selectbox("the following ports can import THERMAL COAL",
                     ("Paradip	India	Berth No. 05  Coal Berth-01",
                      "Gopalpur	India	Berth Nos. 1, 2 & 3 Coastal Coal Handling",
                      "Paradip	India	Berth No. 06 Coal Berth-02",
                      "Vizag	India	VGCB  Vizag General Cargo Berth",
                      "Vizag	India	WQ-2 / WQ-3",
                      "Gangavaram	India	Mechanised Coal Berths 2 berths",
                      "Dhamra	India	BB-1 / BB-2  Mechanised Bulk Import Berths",
                      "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                      "Haldia	India	Berth No. 3  Mechanical Thermal Coal Handling Facility",
                      ),key = "destination_pt"
                     )
     st.subheader("3. Contract Duration")
     st.text("select the contract duration for your shipment")
     st.selectbox("", ("short term", "mid term"),key = "contract_duration")
     submitted1 = st.form_submit_button("Submit",type="primary",disabled=False) 




           
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

result = st.session_state.get("result")
if result:
    if result["vessel"] is None:
        st.warning("No single vessel type fits this cargo and port pair.")
    else:
        st.subheader(f"Recommended vessel: {result['vessel']}")
        st.write("Other compliant options:", result["match"]["compliant_options"])

        st.subheader("Charter timing")
        st.write(result["charter"]["headline"])
        st.write(result["charter"]["action"])
        st.caption(result["charter"]["caution"])

        st.subheader("Voyage")
        st.write(f"Distance: {result['voyage']['distance_nm']:,} nm "
                 f"({result['voyage']['voyage_time_days']} days at "
                 f"{result['voyage']['assumed_speed_knots']} knots)")
        st.caption("Straight-line distance estimate, not the actual sailed route.")
        st.write(f"Loading time: {result['load']['turnaround_hours']} hours")
        st.write(f"Discharge time: {result['discharge']['turnaround_hours']} hours")

        st.subheader("Risk")
        st.write(result["risk"]["message"])
        st.write("Idle management:", result["idle"]["suggestion"])
        st.write(f"Port congestion: {result['congestion']['congestion_level']}")
        st.caption("Congestion is simulated for this demo.")

        st.subheader("Coal price")
        st.write(f"${result['coal']['latest_price_usd_per_tonne']}/tonne as of "
                  f"{result['coal']['as_of']} ({result['coal']['direction']})")
        st.write(f"Estimated cargo value: ${result['coal']['estimated_cargo_value_usd']:,}")

        st.subheader("Rate forecast")
        chart_data = result["forecast"]["forecast"].set_index("Date")[["Forecast", "Lower_Bound", "Upper_Bound"]]
        st.line_chart(chart_data)
        st.caption("Market data ends July 2019. Forecast dates shown continue from there.")