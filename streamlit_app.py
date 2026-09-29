import streamlit as st
import pandas as pd

"st.session_state object:", st.session_state


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
               ("Australia-Adani Abbot Point Terminal — Berth 1",
                 "Australia-Adani Abbot Point Terminal — Berth 2",
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
    st.write(f"You have chosen :blue-background[{st.session_state.cargo_type}] of volume :blue-background[{str(st.session_state.cargo_qt)}] Metric tonne.")
    st.write(f"and your shipment will be from :blue-background[{st.session_state.origin_pt}] to :blue-background[{st.session_state.destination_pt}] for a :blue-background[{st.session_state.contract_duration}] contract duration.")
    


           

