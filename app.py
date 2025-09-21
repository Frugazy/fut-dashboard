import streamlit as st
import requests
from datetime import datetime

# =====================
# CONFIG
# =====================
DATA_URL = "https://fut-backend-x7qo.onrender.com/data"  # <-- Your Render backend URL

def fetch_data():
    try:
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        return response.json().get("players", [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# =====================
# STREAMLIT UI
# =====================
st.set_page_config(page_title="⚽ FUT Trading Dashboard", layout="wide")
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
            st.image(p.get("image",""), width=80)
            st.markdown(
                f"**{p['name']} ({p['rating']})** | 💰 {p['currentBIN']:,} | 🎯 {p['targetBuy']:,} | 🏷️ {p['targetSell']:,}"
            )

    # High Risk Tab
    with tabs[2]:
        st.subheader("High Risk")
        for p in [pl for pl in players if pl["classification"] == "High Risk"]:
            st.image(p.get("image",""), width=80)
            st.markdown(
                f"**{p['name']} ({p['rating']})** | 💰 {p['currentBIN']:,} | Risk: {p['classification']}"
            )

    # Monitor Tab
    with tabs[3]:
        st.subheader("Monitor")
        for p in [pl for pl in players if pl["classification"] == "Monitor"]:
            st.image(p.get("image",""), width=80)
            st.markdown(
                f"**{p['name']} ({p['rating']})** | 💰 {p['currentBIN']:,} | Conf: {p['confidence']}"
            )
else:
    st.warning("No player data available.")

st.markdown(f"Data last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
