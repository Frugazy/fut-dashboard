import streamlit as st
import requests
from datetime import datetime

# =====================
# CONFIG
# =====================
DATA_URL = "https://fut-backend-x7qo.onrender.com/data"  # Render backend URL

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
            trading = p.get("trading", {})
            historical = p.get("historical", {})
            st.markdown(
                f"**{p['name']} ({p['rating']})** - {p.get('cardType','N/A')}\n"
                f"💰 Current BIN: {p.get('currentBIN',0):,}\n"
                f"📉 6h Low: {historical.get('6h',{{}}).get('low',0):,} | "
                f"12h Low: {historical.get('12h',{{}}).get('low',0):,} | "
                f"24h Low: {historical.get('24h',{{}}).get('low',0):,}\n"
                f"🎯 Target Buy: {trading.get('targetBuy',0):,} | 🏷️ Target Sell: {trading.get('targetSell',0):,}\n"
                f"📊 Profit Margin: {trading.get('profitMargin',0)}% | 🛡️ Risk: {trading.get('classification','N/A')}"
            )

    # Certified Buys Tab
    with tabs[1]:
        st.subheader("Certified Buys")
        for p in [pl for pl in players if pl.get("trading",{}).get("classification")=="Certified Buy"]:
            st.image(p.get("image",""), width=80)
            trading = p.get("trading",{})
            st.markdown(
                f"**{p['name']} ({p['rating']})** | 💰 {p.get('currentBIN',0):,} | 🎯 {trading.get('targetBuy',0):,} | 🏷️ {trading.get('targetSell',0):,}"
            )

    # High Risk Tab
    with tabs[2]:
        st.subheader("High Risk")
        for p in [pl for pl in players if pl.get("trading",{}).get("classification")=="High Risk"]:
            st.image(p.get("image",""), width=80)
            trading = p.get("trading",{})
            st.markdown(
                f"**{p['name']} ({p['rating']})** | 💰 {p.get('currentBIN',0):,} | Risk: {trading.get('classification','N/A')}"
            )

    # Monitor Tab
    with tabs[3]:
        st.subheader("Monitor")
        for p in [pl for pl in players if pl.get("trading",{}).get("classification")=="Monitor"]:
            st.image(p.get("image",""), width=80)
            trading = p.get("trading",{})
            st.markdown(
                f"**{p['name']} ({p['rating']})** | 💰 {p.get('currentBIN',0):,} | Conf: {trading.get('confidence','N/A')}"
            )
else:
    st.warning("No player data available.")

st.markdown(f"Data last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
