g import streamlit as st
import requests
from datetime import datetime

# =========================
# CONFIGURATION
# =========================
DATA_URL = "https://e39c98a1-56a9-4cfb-8388-8d0b9968e590-00-1qolyv41k2k.riker.replit.dev/data"

# =========================
# FETCH DATA
# =========================
try:
    response = requests.get(DATA_URL)
    response.raise_for_status()
    data_json = response.json()
    players = data_json.get("players", [])
except Exception as e:
    st.error(f"Error fetching data: {e}")
    players = []

# =========================
# DASHBOARD LAYOUT
# =========================

st.set_page_config(page_title="FUT Trading Dashboard", layout="wide")
st.title("FUT Trading Dashboard")
st.write(f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

# Tabs for 6h, 12h, 24h lows (can expand with Replit DB if needed)
tabs = st.tabs(["Certified Buys", "Hold Until 6PM", "High Risk", "Monitor"])

# Helper to filter players by classification
def filter_players(classification):
    return [p for p in players if p.get("trading", {}).get("classification") == classification]

# =========================
# POPULATE TABS
# =========================
for idx, tab_name in enumerate(["Certified Buy", "Hold Until 6PM", "High Risk", "Monitor"]):
    with tabs[idx]:
        filtered_players = filter_players(tab_name)
        if not filtered_players:
            st.info("No players in this category at the moment.")
        else:
            for p in filtered_players:
                tr = p["trading"]
                mk = p["market"]
                pl = p["player"]
                st.markdown(f"### 🛒 {pl['name']} ({pl['rating']}) - {pl['cardType']}")
                st.markdown(
                    f"💰 **Current BIN:** {mk['currentBIN']:,} coins  \n"
                    f"📉 **24h Low:** {mk['historical']['24h']['low']:,} coins  \n"
                    f"📈 **7d High:** {mk['historical']['7d']['high']:,} coins  \n"
                    f"🎯 **Target Buy:** {tr['targetBuy']:,} coins  \n"
                    f"🏷️ **Target Sell:** {tr['targetSell']:,} coins  \n"
                    f"📊 **Profit:** {tr['estimatedProfit']:,} coins ({tr['profitMargin']}%)  \n"
                    f"🛡️ **Risk:** {tr['classification']}  \n"
                    f"💡 **Reasoning:** {tr['reasoning']}  \n"
                    f"**Position:** {pl['position']} | **Club:** {pl['club']} | **League:** {pl['league']}  \n"
                    f"**Confidence:** {tr['confidence']} | **Data Points:** {mk['dataPoints']}"
                )
                st.markdown("---")