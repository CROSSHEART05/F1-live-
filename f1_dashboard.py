import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh
import fastf1


st.set_page_config(page_title="F1 Live Timing", layout="wide")

st.title("🏎 Formula 1 Live Race Analytics")

st_autorefresh(interval=30000, key="f1refresh")

positions_url = "https://api.openf1.org/v1/position?session_key=latest"
laps_url = "https://api.openf1.org/v1/laps?session_key=latest"
drivers_url = "https://api.openf1.org/v1/drivers?session_key=latest"
intervals_url = "https://api.openf1.org/v1/intervals?session_key=latest"

# LOAD LAP DATA

@st.cache_data(ttl=5)
def load_data():

    laps = requests.get(laps_url).json()
    drivers = requests.get(drivers_url).json()

    laps_df = pd.DataFrame(laps)
    drivers_df = pd.DataFrame(drivers)

    df = laps_df.merge(
        drivers_df[['driver_number','full_name','team_name']],
        on='driver_number',
        how='left'
    )

    return df
  
# LOAD POSITION DATA

@st.cache_data(ttl=5)
def load_positions():
  
    positions = requests.get(positions_url).json()
    drivers = requests.get(drivers_url).json()
    
    position_df = pd.DataFrame(positions)
    drivers_df = pd.DataFrame(drivers)

    position_df = position_df.merge(
        drivers_df[['driver_number','full_name','team_name']],
        on='driver_number',
        how='left'
    )

    return position_df
  
# LOAD INTERVAL DATA

@st.cache_data(ttl=5)
def load_intervals():

    try:
        response = requests.get(intervals_url)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            interval_df = pd.DataFrame(data)
        else:
            interval_df = pd.DataFrame()

    except Exception as e:
        st.warning("Interval data not available (race may not be live)")
        interval_df = pd.DataFrame()

    return interval_df
  
# load dataset
df = load_data()
position_df = load_positions()
interval_df = load_intervals()

# ---------------------------------------------
# fastest lap

st.subheader("⚡ Fastest Lap")

fastest = df.loc[df['lap_duration'].idxmin()]

st.metric(
    label="Fastest Driver",
    value=fastest['full_name'],
    delta = f"{fastest['lap_duration']} sec"
)

# ---------------------------------------------
# layout 
# col1, col2 = st.columns(2)

# ---------------------------------------------
# lap leaderboard



st.subheader("🏁 Lap Leaderboard")

leaderboard = df.sort_values("lap_duration")

st.dataframe(
    leaderboard[['full_name','team_name','lap_number','lap_duration']],
    use_container_width=True
)
    
# ---------------------------------------------
# live positions


st.subheader("📊 Live Race Positions")

live_positions = (
position_df.sort_values("position")
.drop_duplicates("driver_number", keep="last")
)

st.dataframe(
    live_positions[['position','full_name','team_name']],
    use_container_width=True
)

# ---------------------------------------------
# gap to leader

st.subheader("⏱ Gap to Leader")
if not interval_df.empty:
    st.dataframe(
        interval_df[['driver_number','gap_to_leader']],
        use_container_width=True
    )

# -------------------------
# Official Race Results (FastF1)


st.subheader("🏆 Official Race Results")

fastf1.Cache.enable_cache("f1_cache")

session = fastf1.get_session(2026, "Australia", "R")
session.load()

results = session.results[['Position', 'Abbreviation', 'TeamName', 'Time']]

results = results.rename(columns={
    "Abbreviation": "Driver",
    "TeamName": "Team"
})

st.dataframe(results, use_container_width=True)