import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -------------------------
# SETTINGS
# -------------------------
PD_ENDPOINT = "https://h82xwhbwrrvrcozunacphm.streamlit.app"  # Your Pipedream JSON endpoint
st.set_page_config(page_title="FUT Trading Dashboard", layout="wide")

# -------------------------
# FETCH DATA FROM PIPEDREAM
# -------------------------
@st.cache_data(ttl=900)  # Cache for 15 min
def fetch_data():
    try:
        response = requests.get(PD_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        return data.get("player_data", [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

players_raw = fetch_data()

# Convert JSON strings to dict
players = [eval(player) if isinstance(player, str) else player for player in players_raw]

# -------------------------
# UI LAYOUT
# -------------------------
st.title("🔥 FUT Trading Dashboard")
st.markdown("Live FUT market data powered by Pipedream 1 workflow.")

# Tabs: Summary / All Players / Charts
tabs = st.tabs(["Summary", "All Players", "Charts"])

# -------------------------
# SUMMARY TAB
# -------------------------
with tabs[0]:
    certified = [p for p in players if p["trading"]["classification"] == "Certified Buy"]
    hold = [p for p in players if p["trading"]["classification"] == "Hold Until 6PM"]
    high_risk = [p for p in players if p["trading"]["classification"] == "High Risk"]
    monitor = [p for p in players if p["trading"]["classification"] == "Monitor"]

    st.subheader("Market Summary")
    st.write(f"Total Players: {len(players)}")
    st.write(f"✅ Certified Buys: {len(certified)}")
    st.write(f"⏳ Hold Until 6PM: {len(hold)}")
    st.write(f"⚠️ High Risk: {len(high_risk)}")
    st.write(f"👀 Monitor: {len(monitor)}")

# -------------------------
# ALL PLAYERS TAB
# -------------------------
with tabs[1]:
    if players:
        # Flatten data for DataFrame
        table_data = []
        for p in players:
            table_data.append({
                "Name": p["player"]["name"],
                "Rating": p["player"]["rating"],
                "Position": p["player"]["position"],
                "Club": p["player"]["club"],
                "League": p["player"]["league"],
                "Card Type": p["player"]["cardType"],
                "Current BIN": p["market"]["currentBIN"],
                "24h Low": p["market"]["historical"]["24h"]["low"],
                "12h Low": p["market"]["historical"].get("12h", {}).get("low", "N/A"),
                "6h Low": p["market"]["historical"].get("6h", {}).get("low", "N/A"),
                "7d High": p["market"]["historical"]["7d"]["high"],
                "Target Buy": p["trading"]["targetBuy"],
                "Target Sell": p["trading"]["targetSell"],
                "Profit": p["trading"]["estimatedProfit"],
                "Profit %": p["trading"]["profitMargin"],
                "Risk": p["trading"]["classification"],
                "Confidence": p["trading"]["confidence"],
                "Reasoning": p["trading"]["reasoning"]
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No player data available.")

# -------------------------
# CHARTS TAB (OPTIONAL)
# -------------------------
with tabs[2]:
    st.subheader("Profit Distribution")
    if players:
        profit_df = pd.DataFrame([{
            "Name": p["player"]["name"],
            "Profit %": p["trading"]["profitMargin"]
        } for p in players])
        st.bar_chart(profit_df.set_index("Name"))
