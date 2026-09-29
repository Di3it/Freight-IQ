"""
matching.py
Vessel type optimization: given an origin port, destination port, and cargo
tonnage, recommends which vessel type(s) are physically compliant with both
ports' constraints, and picks the best fit for the cargo size.

Uses:
    data/port_data_india.xlsx   (destination ports)
    data/port_data_origin.xlsx  (origin/loading ports)
"""

import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import re

INDIA_PORTS_PATH = "data/port_data_india.xlsx"
ORIGIN_PORTS_PATH = "data/port_data_origin.xlsx"

# Standard industry reference ranges for each vessel type.
# (Approximate typical dimensions/capacity - used to check compliance against
# port constraints and to pick the right-sized vessel for the cargo tonnage.)
VESSEL_SPECS = {
    "Handysize":  {"typical_loa_m": 190, "typical_beam_m": 32, "typical_draft_m": 10, "dwt_min": 10000,  "dwt_max": 40000},
    "Supramax":   {"typical_loa_m": 200, "typical_beam_m": 32, "typical_draft_m": 12, "dwt_min": 50000,  "dwt_max": 60000},
    "Panamax":    {"typical_loa_m": 225, "typical_beam_m": 32, "typical_draft_m": 14, "dwt_min": 60000,  "dwt_max": 80000},
    "Capesize":   {"typical_loa_m": 300, "typical_beam_m": 45, "typical_draft_m": 17, "dwt_min": 80000,  "dwt_max": 220000},
}
def _read_ports(path):
    """Reads a port Excel file, automatically finding the header row (skips any title rows)."""
    raw = pd.read_excel(path, header=None)
    header_row = raw.index[raw.iloc[:, 0] == "Port_Name"][0]
    return pd.read_excel(path, header=header_row)


def _parse_coordinate(value):
    """Converts text like '86.6743° E' or '19.51° S' into signed decimal degrees."""
    if pd.isna(value):
        raise ValueError("Missing coordinate value for this port.")
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"(-?\d+(?:\.\d+)?)\s*°?\s*([NSEW])?", str(value).strip().upper())
    if not match:
        raise ValueError(f"Could not read coordinate: {value}")
    number = float(match.group(1))
    if match.group(2) in ("S", "W"):
        number = -number
    return number


def _load_port_row(port_name: str, is_origin: bool):
    """Finds a port's row(s) in the relevant port data file (case-insensitive, partial match)."""
    path = ORIGIN_PORTS_PATH if is_origin else INDIA_PORTS_PATH
    df = _read_ports(path)
    matches = df[df["Port_Name"].str.contains(port_name, case=False, na=False)]
    if matches.empty:
        raise ValueError(f"Port '{port_name}' not found in {'origin' if is_origin else 'India'} port data.")
    return matches


def _port_is_compliant(port_row, vessel_type):
    """Checks whether a given vessel type's typical dimensions fit within a specific berth's limits."""
    specs = VESSEL_SPECS[vessel_type]
    reasons = []

    max_loa = port_row.get("Max_LOA_m")
    max_beam = port_row.get("Max_Beam_m")
    max_draft = port_row.get("Max_Draft_m")
    max_dwt = port_row.get("Max_DWT")

    if pd.notna(max_loa) and specs["typical_loa_m"] > max_loa:
        reasons.append(f"LOA {specs['typical_loa_m']}m exceeds berth max {max_loa}m")
    if pd.notna(max_beam) and specs["typical_beam_m"] > max_beam:
        reasons.append(f"Beam {specs['typical_beam_m']}m exceeds berth max {max_beam}m")
    if pd.notna(max_draft) and specs["typical_draft_m"] > max_draft:
        reasons.append(f"Draft {specs['typical_draft_m']}m exceeds berth max {max_draft}m")
    if pd.notna(max_dwt) and specs["dwt_max"] > max_dwt:
        reasons.append(f"Max DWT {specs['dwt_max']} exceeds berth max {max_dwt}")

    return (len(reasons) == 0), reasons


def match_vessel(origin_port: str, destination_port: str, cargo_tons: float):
    """
    Recommends compliant vessel type(s) for a given origin, destination, and cargo size.

    Returns:
        dict with:
            compliant_options: list of vessel types that fit both ports' constraints
                                AND can carry the cargo tonnage
            recommended: the best single recommendation (largest compliant vessel
                         that doesn't exceed the cargo size, for efficiency)
            details: per-vessel-type compliance breakdown (for transparency/debugging)
    """
    origin_rows = _load_port_row(origin_port, is_origin=True)
    dest_rows = _load_port_row(destination_port, is_origin=False)

    details = {}
    compliant_options = []

    for vessel_type, specs in VESSEL_SPECS.items():
        # Cargo tonnage check: vessel must be able to carry this cargo size
        # (allowing some flexibility - vessel dwt_max should be >= cargo size,
        # and dwt_min shouldn't be wildly oversized for very small cargoes)
        fits_cargo = cargo_tons <= specs["dwt_max"]

        # Check compliance against every relevant berth at both origin and destination;
        # a vessel type is compliant only if AT LEAST ONE berth at each port can take it
        origin_ok = False
        origin_reasons = []
        for _, row in origin_rows.iterrows():
            ok, reasons = _port_is_compliant(row, vessel_type)
            if ok:
                origin_ok = True
                break
            origin_reasons.extend(reasons)

        dest_ok = False
        dest_reasons = []
        for _, row in dest_rows.iterrows():
            ok, reasons = _port_is_compliant(row, vessel_type)
            if ok:
                dest_ok = True
                break
            dest_reasons.extend(reasons)

        is_compliant = fits_cargo and origin_ok and dest_ok

        details[vessel_type] = {
            "fits_cargo": fits_cargo,
            "origin_compliant": origin_ok,
            "destination_compliant": dest_ok,
            "origin_issues": list(set(origin_reasons)),
            "destination_issues": list(set(dest_reasons)),
            "overall_compliant": is_compliant,
        }

        if is_compliant:
            compliant_options.append(vessel_type)

    # Pick the largest compliant vessel (maximizes cargo efficiency / fewest voyages)
    recommended = None
    if compliant_options:
        recommended = min(compliant_options, key=lambda v: VESSEL_SPECS[v]["dwt_max"])

    return {
        "origin_port": origin_port,
        "destination_port": destination_port,
        "cargo_tons": cargo_tons,
        "compliant_options": compliant_options,
        "recommended": recommended,
        "details": details,
    }
def estimate_turnaround_time(port_name: str, cargo_tons: float, is_origin: bool):
    """
    Estimates loading/discharge turnaround time at a port, based on its
    cargo handling rate. Uses the fastest (most capable) matching berth
    if a port has multiple rows.
    """
    rows = _load_port_row(port_name, is_origin=is_origin)
    rates = rows["Cargo_Handling_Rate_MT_hr"].dropna()

    if rates.empty:
        return {
            "port": port_name,
            "turnaround_hours": None,
            "note": "No cargo handling rate data available for this port.",
        }

    best_rate = rates.max()  # fastest available berth
    hours = cargo_tons / best_rate

    return {
        "port": port_name,
        "cargo_tons": cargo_tons,
        "handling_rate_mt_hr": best_rate,
        "turnaround_hours": round(hours, 1),
        "turnaround_days": round(hours / 24, 2),
    }
AVERAGE_VESSEL_SPEED_KNOTS = 12  # typical laden bulk carrier speed for voyage estimation

def calculate_distance_nm(origin_port: str, destination_port: str):
    """
    Calculates great-circle distance (in nautical miles) between an origin
    and destination port using their lat/long coordinates.
    """
    origin_rows = _load_port_row(origin_port, is_origin=True)
    dest_rows = _load_port_row(destination_port, is_origin=False)
    lat1 = _parse_coordinate(origin_rows.iloc[0]["LATITUDE"])
    lon1 = _parse_coordinate(origin_rows.iloc[0]["LONGITUDE"])
    lat2 = _parse_coordinate(dest_rows.iloc[0]["LATITUDE"])
    lon2 = _parse_coordinate(dest_rows.iloc[0]["LONGITUDE"])

    R_km = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance_km = R_km * c
    distance_nm = distance_km * 0.539957  # km to nautical miles

    return round(distance_nm, 1)
def get_port_lists():
    origin = _read_ports(ORIGIN_PORTS_PATH)["Port_Name"].dropna().unique().tolist()
    india = _read_ports(INDIA_PORTS_PATH)["Port_Name"].dropna().unique().tolist()
    return origin, india

def estimate_voyage_time(origin_port: str, destination_port: str):
    """
    Estimates voyage duration in days, based on great-circle distance and an
    assumed average vessel speed. Note: this is straight-line distance, not
    actual sailed route distance (which would be longer due to coastlines,
    traffic separation schemes, etc.) - a simplification appropriate for demo.
    """
    distance_nm = calculate_distance_nm(origin_port, destination_port)
    hours = distance_nm / AVERAGE_VESSEL_SPEED_KNOTS
    days = hours / 24

    return {
        "origin_port": origin_port,
        "destination_port": destination_port,
        "distance_nm": distance_nm,
        "assumed_speed_knots": AVERAGE_VESSEL_SPEED_KNOTS,
        "voyage_time_days": round(days, 1),
        "note": "Straight-line distance estimate, not actual sailed route.",
    }

if __name__ == "__main__":
    # Quick manual test
    print(match_vessel("Baltimore", "Gopalpur", cargo_tons=40000))
    result = match_vessel("Newcastle", "Paradip", cargo_tons=55000)
    print(f"\nOrigin: {result['origin_port']} -> Destination: {result['destination_port']}")
    print(f"Cargo: {result['cargo_tons']} tons")
    print(f"Compliant options: {result['compliant_options']}")
    print(f"Recommended vessel: {result['recommended']}")
    print("\nFull breakdown:")
    for vessel, info in result["details"].items():
        print(f"  {vessel}: {info}")

    print("\n=== Turnaround Time Estimates ===")
    print(estimate_turnaround_time("Paradip", cargo_tons=55000, is_origin=False))
    print(estimate_voyage_time("Taman", "Vizag"))