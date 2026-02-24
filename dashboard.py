import streamlit as st
import pandas as pd
import sqlite3
import datetime

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
    /* Styling the Warning Box */
    .demo-warning {
        background-color: #331a00;
        color: #ffaa00;
        padding: 10px;
        border: 1px solid #ffaa00;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Demo Disclaimer (The "Safety First" part)
st.markdown("""
    <div class="demo-warning">
        ⚠️ DEMO USE ONLY / 本サービスはデモ専用です<br>
        DATA MAY BE DELAYED OR INACCURATE. DO NOT USE FOR ACTUAL TRAVEL.
    </div>
    """, unsafe_allow_html=True)

# 4. Header Section
st.markdown("<h1 style='color: #ffaa00; font-size: 42px; margin-bottom: 0;'>DEPARTURES / 出発案内</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888; font-size: 16px;'>KUALA LUMPUR INTL (KUL) </p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)

# 5. Data Loading (Simplified for your new main.py)
@st.cache_data
def load_data():
    conn = sqlite3.connect('flight.db')
    df = pd.read_sql("SELECT * FROM flights", conn)
    conn.close()
    # Shuffle for the "Mechanical Board" feel
    return df.sample(frac=1).reset_index(drop=True)

try:
    df = load_data()

    # 6. KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("TOTAL / 総計", f"{len(df)} FLT")
    col2.metric("AIRLINE / 航空会社", df['AIRLINE'].nunique())
    # We use 'N/A' for delays if the data is simplified, or calculate if column exists
    col3.metric("STATUS / 状態", "ACTIVE")

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. The Flight Board Table
    st.markdown("<h3 style='color: #f0f0f0;'>SCHEDULE / 運行スケジュール</h3>", unsafe_allow_html=True)
    st.dataframe(df, width='stretch', hide_index=True)

    # 8. Footer with Timestamp and Repository Link
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.markdown("<br><hr style='border-color: #333;'>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"<p style='color: #444; font-size: 12px;'>LAST UPDATED: {current_time} MYT</p>", unsafe_allow_html=True)

    with col_right:
        # Replace '#' with your actual GitHub URL
        st.markdown(f"<p style='color: #444; font-size: 12px; text-align: right;'><element style='color: #888;'>SOURCE:</element> <a href='https://github.com/Kelocker/KUL-FLIGHT-ETL' style='color: #ffaa00; text-decoration: none;'>GITHUB REPOSITORY / リポジトリ</a></p>", unsafe_allow_html=True)

except Exception as e:
    st.error("Waiting for initial data sync...")
    st.info("Run your main.py script to populate the database.")