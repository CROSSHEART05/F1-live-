import streamlit as st
import pandas as pd
import requests
import fastf1
import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="F1 Live Analytics", layout="wide")

st.title("🏎 Formula 1 Live Analytics Dashboard")
st_autorefresh(interval=30000, key="f1refresh") 

fastf1.Cache.enable_cache("f1_cache")

current_year = datetime.datetime.now().year

# ---------------------------------------------------
# GRAND PRIX SELECTOR
# ---------------------------------------------------

schedule = fastf1.get_event_schedule(current_year)

gp_list = schedule['EventName'].tolist()

selected_gp = st.selectbox(
    "Select Grand Prix",
    gp_list
)

event_row = schedule[schedule['EventName'] == selected_gp].iloc[0]

event_name = event_row['EventName']
country = event_row['Country']

st.subheader(f"🏁 {event_name}")

# ---------------------------------------------------
# SESSION SELECTOR
# ---------------------------------------------------

session_options = {
    "Practice 1": "Practice 1",
    "Practice 2": "Practice 2",
    "Practice 3": "Practice 3",
    "Sprint Shootout": "Sprint Shootout",
    "Sprint": "Sprint",
    "Qualifying": "Qualifying",
    "Race": "Race"
}

selected_session = st.selectbox(
    "Select Session",
    list(session_options.keys())
)

session_name = session_options[selected_session]

# ---------------------------------------------------
# FASTF1 SESSION CODES
# ---------------------------------------------------

fastf1_sessions = {
    "Practice 1": "FP1",
    "Practice 2": "FP2",
    "Practice 3": "FP3",
    "Sprint Shootout": "SQ",
    "Sprint": "S",
    "Qualifying": "Q",
    "Race": "R"
}

session_code = fastf1_sessions[selected_session]

# ---------------------------------------------------
# LOAD FASTF1 SESSION
# ---------------------------------------------------

try:

    session = fastf1.get_session(current_year, event_name, session_code)

    session.load()

except:

    st.warning("Session timing data not available yet.")

# ---------------------------------------------------
# GET SESSION KEY FROM OPENF1
# ---------------------------------------------------

session_api = f"https://api.openf1.org/v1/sessions?year={current_year}&country_name={country}"

session_data = requests.get(session_api).json()

session_key = None

for s in session_data:

    if s["session_name"] == session_name:

        session_key = s["session_key"]

if session_key is None:

    st.warning("Session not available yet.")
    st.stop()

# ---------------------------------------------------
# LOAD OPENF1 DATA
# ---------------------------------------------------

laps_url = f"https://api.openf1.org/v1/laps?session_key={session_key}"
positions_url = f"https://api.openf1.org/v1/position?session_key={session_key}"
drivers_url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"

laps = requests.get(laps_url).json()
positions = requests.get(positions_url).json()
drivers = requests.get(drivers_url).json()

# safe dataframe creation

def safe_dataframe(data):

    if isinstance(data, list):

        return pd.DataFrame(data)

    else:

        return pd.DataFrame()

laps_df = safe_dataframe(laps)
pos_df = safe_dataframe(positions)
drivers_df = safe_dataframe(drivers)

# ---------------------------------------------------
# MERGE DRIVER INFO
# ---------------------------------------------------

if not laps_df.empty:

    laps_df = laps_df.merge(
        drivers_df[['driver_number','full_name','team_name']],
        on="driver_number",
        how="left"
    )

if not pos_df.empty:

    pos_df = pos_df.merge(
        drivers_df[['driver_number','full_name','team_name']],
        on="driver_number",
        how="left"
    )

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

col1, col2 = st.columns(2)

# ---------------------------------------------------
# LAP LEADERBOARD
# ---------------------------------------------------

with col1:

    st.subheader("🏁 Lap Leaderboard")

    if not laps_df.empty:

        leaderboard = laps_df.sort_values("lap_duration")

        st.dataframe(
            leaderboard[['full_name','team_name','lap_number','lap_duration']],
            width="stretch"
        )

# ---------------------------------------------------
# LIVE POSITIONS
# ---------------------------------------------------

with col2:

    st.subheader("🏎 Live Positions")

    if not pos_df.empty:

        live_positions = (
            pos_df.sort_values("position")
            .drop_duplicates("driver_number", keep="last")
        )

        st.dataframe(
            live_positions[['position','full_name','team_name']],
            width="stretch"
        )

# ---------------------------------------------------
# FASTEST LAP
# ---------------------------------------------------

if not laps_df.empty and 'lap_duration' in laps_df.columns:
    
    valid_laps = laps_df.dropna(subset=['lap_duration'])

    if not valid_laps.empty:

        fastest = valid_laps.loc[valid_laps['lap_duration'].idxmin()]

        st.metric(
            label="⚡ Fastest Lap",
            value=fastest['full_name'],
            delta=f"{fastest['lap_duration']} sec"
        )

    else:
        st.info("No valid lap times available yet.")

# ---------------------------------------------------
# FINAL SESSION RESULTS (FASTF1)
# ---------------------------------------------------

st.subheader("🏆 Final Session Results")

try:

    results = session.results[
        ['Position','Abbreviation','TeamName','Time','Status']
    ]

    results = results.rename(columns={
        "Abbreviation": "Driver",
        "TeamName": "Team"
    })

    st.dataframe(results, width="stretch")

except:

    st.info("Final results not available yet.")