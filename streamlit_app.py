import streamlit as st
import pandas as pd

st.title("Frieght forecasting & prediction🗺️")
st.write("Hello, *World!* :sunglasses:")
with st.form("cargo_detail"):
  st.header("Cargo details:", divider=True)
  cargo_type = st.radio("choose the required cargo you want to look for🏗️.",
         ["coal1","coal2","coal3","coal4","coal5",],
         captions=[
             "PRIMARY COKING COAL",
             "MEDIUM COKING COAL",
             "WEAK COKING COAL",
             "PCL COAL",
             "THERMAL COAL",

         ])
  cargo_qt = st.slider("Volume of shipment",1000,500000,10000)
  submitted = st.form_submit_button("Submit")

if submitted:
   st.write("Wanted ",cargo_type,"of volume",cargo_qt,"Metric tonne.")
with st.form("shipping_details"):
     st.header("Voyage detail")
     st.write("Choose your preferred origin port for",cargo_type)
     if cargo_type == "coal1":
      st.selectbox("the following ports provide coal1",
               ("Australia-Adani Abbot Point Terminal — Berth 1", "Australia-Adani Abbot Point Terminal — Berth 2", "Mozambique-Beira-Berth 8 — Coal Terminal (TCC8)","Russia-Taman-Berth No. 1","Russia-Taman-Berth No. 4","Russia-Vanino-VaninoTransUgol Coal Terminal — Berth 01","Russia-Vanino-VaninoTransUgol Coal Terminal — Berth 02","USA-Baltimore-CONSOL Marine Terminal","USA-Lamberts Point / Norfolk-Pier 6 — Lamberts Point Coal Terminal")
               )
     elif cargo_type == "coal2":
            st.selectbox("the following ports provide coal2",
                     ("Abbot Point	Australia	Adani Abbot Point Terminal — Berth 1", 
                      "Abbot Point	Australia	Adani Abbot Point Terminal — Berth 2",
                       "Newcastle	Australia	Kooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                       "Taman	Russia	Berth No. 1",
                       "Taman	Russia	Berth No. 3",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 01",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 02",
                       "Baltimore	USA	CONSOL Marine Terminal",
                       "Lamberts Point / Norfolk	USA	Pier 6 — Lamberts Point Coal Terminal"
                       )
                     )
     elif cargo_type == "coal3":
            st.selectbox("the following ports provide coal3",
                     ("Abbot Point	Australia	Adani Abbot Point Terminal — Berth 1", 
                      "Abbot Point	Australia	Adani Abbot Point Terminal — Berth 2",
                       "Newcastle	Australia	Kooragang 8, 9 & 10 (NCIG Coal Export Terminal)",
                       "Taman	Russia	Berth No. 1",
                       "Taman	Russia	Berth No. 3",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 01",
                       "Vanino	Russia	VaninoTransUgol Coal Terminal — Berth 02",
                       "Baltimore	USA	CONSOL Marine Terminal",
                       "Lamberts Point / Norfolk	USA	Pier 6 — Lamberts Point Coal Terminal"
                       )
                    )
     elif cargo_type == "coal4":
            st.selectbox("the following ports provide coal4",
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
                      )
                     )
     elif cargo_type == "coal5":
            st.selectbox("the following ports provide coal5",
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
                      )
                     )
     
     st.write("Choose your preferred destination port for",cargo_type)
     if cargo_type == "coal1":
      st.selectbox("the following ports can import coal1",
               (
                    "Paradip	India	Berth No. 03 - New Coal Import Berth",
                    "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                    "Vizag	India	WQ-2 / WQ-3",
                    "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                    "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                    "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                    "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
               )
               )
     elif cargo_type == "coal2":
            st.selectbox("the following ports can import coal2",
                     (
                       "Paradip	India	Berth No. 03 - New Coal Import Berth",
                            "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                            "Vizag	India	WQ-2 / WQ-3",
                            "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                            "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                            "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                            "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
                     )
                     )
     elif cargo_type == "coal3":
            st.selectbox("the following ports can import coal3",
                     (
                            "Paradip	India	Berth No. 03 - New Coal Import Berth",
                            "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                            "Vizag	India	WQ-2 / WQ-3",
                            "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                            "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                            "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                            "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
                     )
                     )

     elif cargo_type == "coal4":
            st.selectbox("the following ports can import coal4",
                     (
                            "Paradip	India	Berth No. 03 - New Coal Import Berth",
                            "Gopalpur	India	Berth Nos. 1, 2 & 3 - Coastal Coal Handling",
                            "Vizag	India	WQ-2 / WQ-3",
                            "Dhamra	India	BB-1 / BB-2 - Mechanised Bulk Import Berths",
                            "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                            "Haldia	India	Berth No. 1 - Multipurpose Dry Bulk",
                            "Haldia	India	Berth No. 2 - Multipurpose Dry Bulk",
                     )
                     )
     elif cargo_type == "coal5":
            st.selectbox("the following ports can import coal5",
                     ("Paradip	India	Berth No. 05  Coal Berth-01",
                      "Gopalpur	India	Berth Nos. 1, 2 & 3 Coastal Coal Handling",
                      "Paradip	India	Berth No. 06 Coal Berth-02",
                      "Vizag	India	VGCB  Vizag General Cargo Berth",
                      "Vizag	India	WQ-2 / WQ-3",
                      "Gangavaram	India	Mechanised Coal Berths 2 berths",
                      "Dhamra	India	BB-1 / BB-2  Mechanised Bulk Import Berths",
                      "Sagar-Sandheads	India	Sagar Anchorage / Sandheads Lighterage Point",
                      "Haldia	India	Berth No. 3  Mechanical Thermal Coal Handling Facility",
                      )
                     )
     st.write("Choose your desired contract duration for",cargo_type)
     st.selectbox("Contract duration", ("short term", "mid term"))
     submitted1 = st.form_submit_button("Submit") 

if submitted1:
    st.write("You have chosen",cargo_type,"of volume",cargo_qt,"Metric tonne.")
    st.write("Your preferred origin port is",st.session_state["the following ports provide coal1"])
    st.write("Your preferred destination port is",st.session_state["the following ports provide coal1"])
    st.write("Your desired contract duration is",st.session_state["Contract duration"])