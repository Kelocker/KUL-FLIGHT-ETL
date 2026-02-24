import streamlit as st
import pandas as pd
import sqlite3

# 1. Page Setup
st.set_page_config(page_title="FLIGHT INFO / 運行情報", layout="centered")

# 2. Terminal CSS (Custom Amber Accents)
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; }
    html, body, [class*="css"] {
        font-family: 'Courier New', Courier, monospace;
        color: #f0f0f0;
    }
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stMetric"] {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-top: 4px solid #ffaa00;
        padding: 15px;
    }
    [data-testid="stMetricLabel"] {
        color: #ffaa00 !important;
        font-weight: bold;
    }
    /* Styling progress bars to look like amber LED segments */
    div[st-external="true"] > div {
        background-color: #ffaa00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown("<h1 style='color: #ffaa00; font-size: 42px; margin-bottom: 0;'>DEPARTURES / 出発案内</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888; font-size: 16px;'>KUALA LUMPUR INTL (KUL) </p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)

# 4. Data Loading
@st.cache_data
def load_data():
    conn = sqlite3.connect('flight.db')
    df = pd.read_sql("SELECT * FROM flights", conn)
    conn.close()
    return df

df = load_data()

# 5. KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("TOTAL / 総計", f"{len(df)} FLT")
col2.metric("AIRLINE / 航空会社", df['airline_name'].nunique())
col3.metric("DELAY / 遅延", f"{round(df['delay_minutes'].mean(), 1)} MIN")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Flight Schedule (Future-proofed width)
st.markdown("<h3 style='color: #f0f0f0;'>SCHEDULE / 運行スケジュール</h3>", unsafe_allow_html=True)
st.dataframe(df, width='stretch', hide_index=True)

# 7. Volume Section (Brutalist Minimalist Style)
st.markdown("<h3 style='color: #f0f0f0;'>VOLUME BY AIRLINE / 航空会社別運航規模</h3>", unsafe_allow_html=True)

airline_counts = df['airline_name'].value_counts()
max_count = airline_counts.max()

# Create a clean grid for the volume bars
for airline, count in airline_counts.items():
    col_name, col_bar, col_val = st.columns([2, 5, 1])
    
    with col_name:
        st.markdown(f"<p style='color: #ffaa00; font-weight: bold; margin: 0;'>{airline.upper()}</p>", unsafe_allow_html=True)
    
    with col_bar:
        # We scale relative to the max airline to fill the space better
        st.progress(count / max_count)
        
    with col_val:
        st.markdown(f"<p style='color: #888; text-align: right; margin: 0;'>{count}</p>", unsafe_allow_html=True)