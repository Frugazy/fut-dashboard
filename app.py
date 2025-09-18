import streamlit as st
from supabase import create_client

url = "https://dhxidllmvgitxtjmsuaw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRoeGlkbGxtdmdpdHh0am1zdWF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxMjc3NDIsImV4cCI6MjA3MzcwMzc0Mn0.iDMzwN6pUe8FHi3StPvQMCdiGhHcKlmPh7pPT5UYaOU"

supabase = create_client(url, key)

st.set_page_config(page_title="FUT Trading Dashboard", layout="wide")
st.title("⚽ FUT Trading System")

search_query = st.text_input("Search for a player:")

if search_query:
    response = supabase.table("fut_cards").select("*").ilike("player_name", f"%{search_query}%").execute()
else:
    response = supabase.table("fut_cards").select("*").limit(10).execute()

cards = response.data

if cards:
    for card in cards:
        st.subheader(f"{card['player_name']} - {card['card_version']}")
        st.write(f"Overall Rating: {card.get('overall_rating')}")
        st.write(f"Current BIN: {card.get('current_bin')}")
        st.write(f"Lowest BIN: {card.get('lowest_bin')}")
        st.write(f"Target Buy Zone: {card.get('target_buy_zone')}")
        st.write(f"Target Sell Zone: {card.get('target_sell_zone')}")
        st.write(f"Profit After Tax: {card.get('profit_after_tax')}")
        st.markdown("---")
else:
    st.info("No players found.")
