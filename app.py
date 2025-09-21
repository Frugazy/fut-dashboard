import streamlit as st
import requests
from datetime import datetime
import threading
import time

# =====================
# CONFIG
# =====================
DATA_URL = "https://fut-backend.onrender.com/data"  # <-- Your Render backend URL
PING_INTERVAL = 300  # 5 minutes for keep-alive ping
REFRESH_INTERVAL = 600  # 10 minutes auto-refresh (optional)

# =====================
# KEEP-ALIVE THREAD
# =====================
def keep_alive():
    while True:
        try:
            requests.get(DATA_URL, timeout=5)
        except:
            pass
        time.sleep(PING_INTERVAL)

threading.Thread(target=keep_alive, daemon=True).start()

# =====================
# FETCH DATA
# =====================
def fetch_data():
    try:
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        return response.json().get("players", [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# =====================
# DASHBOARD LAYOUT
# =====================
st.set_page_config(page_title="FUT Trading Dashboard", layout="wide")
st.title("⚽ FUT Trading Dashboard")

players = fetch_data()

if players:
    tabs = st.tabs(["Overview", "Certified Buys", "High Risk", "Monitor"])
    
    # Overview Tab
    with tabs[0]:
        st.subheader("All Players Overview")
        for p in players:
            st.image(p.get("image",""), width=80)
            st.markdown(
                f"**{p['name']} ({p['rating']})** - {p.get('cardType','N/A')}\n"
                f"💰 Current BIN: {p['currentBIN']:,}\n"
                f"📉 6h Low: {p['historical']['6h']['low']:,} | "
                f"12h Low: {p['historical']['12h']['low']:,} | "
                f"24h Low: {p['historical']['24h']['low']:,}\n"
                f"🎯 Target Buy: {p['targetBuy']:,} | 🏷️ Target Sell: {p['targetSell']:,}\n"
                f"📊 Profit Margin: {p['profitMargin']}% | 🛡️ Risk: {p['classification']} | 💡 Confidence: {p['confidence']}"
            )
    # Certified Buys Tab
    with tabs[1]:
        st.subheader("Certified Buys")
        for p in [pl for pl in players if pl["classification"] == "Certified Buy"]:
            st.markdown(f"**{p['name']} ({p['rating']})** | 💰 {p['currentBIN']:,} | 🎯 {p['targetBuy']:,}")
    # High Risk Tab
    with tabs[2]:
        st.subheader("High Risk")
        for p in [pl for pl in players if pl["classification"] == "High Risk"]:
            st.markdown(f"**{p['name']} ({p['rating']})** | 💰 {p['currentBIN']:,} | Risk: {p['classification']}")
    # Monitor Tab
    with tabs[3]:
        st.subheader("Monitor")
        for p in [pl for pl in players if pl["classification"] == "Monitor"]:
            st.markdown(f"**{p['name']} ({p['rating']})** | 💰 {p['currentBIN']:,} | Conf: {p['confidence']}")
else:
    st.warning("No player data available.")

st.markdown(f"Data last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

# =====================
# OPTIONAL AUTO-REFRESH
# =====================
if REFRESH_INTERVAL:
    time.sleep(REFRESH_INTERVAL)
    st.experimental_rerun()
