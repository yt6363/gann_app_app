import streamlit as st
import pandas as pd
import numpy as np
import bisect
import math
import io
import plotly.graph_objects as go

# Helper functions from original Dash App
def generate_cycle_levels(start=1.0, max_price=1e9):
    levels = [start]
    current = start
    while current < max_price:
        current = (np.sqrt(current) + 0.25) ** 2
        levels.append(current)
    return levels

def get_cycle_fraction(price, levels):
    if price <= levels[0]:
        return 0.0
    if price >= levels[-1]:
        return (len(levels)-1)/9.0
    idx = bisect.bisect_right(levels, price)
    low, high = levels[idx-1], levels[idx]
    return (idx-1 + (price - low) / (high - low))/9.0

def get_cycle_label(cf):
    cyc_int = math.floor(cf)
    angle_frac = cf - cyc_int
    angle_deg = angle_frac * 360
    angle_rounded = round(angle_deg, 2)
    if angle_rounded >= 360.0:
        cyc_int += 1
        angle_rounded = 0.0
    return f"{cyc_int} & {angle_rounded}°"

def detect_swings(df, threshold=0.05, mode="HighLow"):
    dates = df["Date"].values
    swings = []

    if mode == "Close":
        prices = df["Close"].values
        i = 0
        extreme_price = prices[i]
        extreme_index = i
        trend = 'looking_for_low'
        for k in range(1, len(dates)):
            price = prices[k]
            if trend == 'looking_for_top':
                if price > extreme_price:
                    extreme_price = price
                    extreme_index = k
                elif price < extreme_price * (1 - threshold):
                    swings.append((dates[extreme_index], extreme_price, "Top"))
                    trend = 'looking_for_low'
                    extreme_price = price
                    extreme_index = k
            else:
                if price < extreme_price:
                    extreme_price = price
                    extreme_index = k
                elif price > extreme_price * (1 + threshold):
                    swings.append((dates[extreme_index], extreme_price, "Low"))
                    trend = 'looking_for_top'
                    extreme_price = price
                    extreme_index = k
    else:
        highs, lows = df["High"].values, df["Low"].values
        i = 0
        extreme_price = lows[i]
        extreme_index = i
        trend = 'looking_for_low'
        for k in range(1, len(dates)):
            high, low = highs[k], lows[k]
            if trend == 'looking_for_top':
                if high > extreme_price:
                    extreme_price = high
                    extreme_index = k
                elif low < extreme_price * (1 - threshold):
                    swings.append((dates[extreme_index], extreme_price, "Top"))
                    trend = 'looking_for_low'
                    extreme_price = low
                    extreme_index = k
            else:
                if low < extreme_price:
                    extreme_price = low
                    extreme_index = k
                elif high > extreme_price * (1 + threshold):
                    swings.append((dates[extreme_index], extreme_price, "Low"))
                    trend = 'looking_for_top'
                    extreme_price = high
                    extreme_index = k

    return pd.DataFrame(swings, columns=["Date", "Price", "Type"])

# Main function to integrate with your Streamlit app
def run_swing_cycle_projections():
    st.title("📈 Financial Market Oracle: Swing & Cycle Projections")

    uploaded_file = st.file_uploader("📂 Upload CSV", type="csv")

    if uploaded_file:
        with st.sidebar:
            st.header("⚙️ Settings")
            threshold = st.number_input("Threshold (%)", value=0.05, step=0.01, format="%.2f")
            timeframe = st.selectbox("Timeframe", ["Daily", "Weekly"])
            swingmode = st.selectbox("Swing Type", ["HighLow", "Close"])

        content = uploaded_file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        df.columns = [c.strip() for c in df.columns]

        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').replace('-', np.nan), errors='coerce')

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date', 'Open', 'High', 'Low', 'Close'])

        if timeframe == 'Weekly':
            df = df.resample('W-MON', on='Date').agg({
                'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'
            }).dropna().reset_index()

        swings_df = detect_swings(df, threshold, swingmode)

        levels = generate_cycle_levels(max_price=50000)
        swings_df['CycleFraction'] = swings_df['Price'].apply(lambda p: get_cycle_fraction(p, levels))
        swings_df['CyclePosition'] = swings_df['CycleFraction'].apply(get_cycle_label)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["High"], mode='lines', name='High', line=dict(color='royalblue')))

        fig.add_trace(go.Scatter(
            x=swings_df["Date"], y=swings_df["Price"], mode='markers+text',
            marker=dict(
                size=14,
                color=['crimson' if t == 'Top' else 'green' for t in swings_df["Type"]],
                symbol=['triangle-up' if t == 'Top' else 'triangle-down' for t in swings_df["Type"]]
            ),
            text=swings_df["CyclePosition"], textposition='top center'
        ))

        fig.update_layout(
            title="Swing & Cycle Projections",
            height=700,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified',
            uirevision='fixed'
        )

        st.plotly_chart(fig, use_container_width=True)
