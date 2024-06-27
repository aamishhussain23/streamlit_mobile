import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Function to calculate profit/loss
def calculate_pnl(strike_prices, target_price, expiry_days):
    # Dummy calculation, replace with actual strategy logic
    pnl_expiry = np.maximum(strike_prices - target_price, 0) - np.maximum(target_price - strike_prices, 0)
    pnl_current = pnl_expiry * (expiry_days / 30)
    return pnl_expiry, pnl_current

# Streamlit layout
st.title("Option Strategy Payoff Graph")

# Sliders for target price and expiry days
target_price = st.slider("Target Price", min_value=20000, max_value=25000, value=23721, step=1)
expiry_days = st.slider("Days to Expiry", min_value=0, max_value=30, value=1, step=1)

# Strike prices range
strike_prices = np.arange(20000, 25001, 100)

# Calculate P&L
pnl_expiry, pnl_current = calculate_pnl(strike_prices, target_price, expiry_days)

# Create the figure
fig = go.Figure()

# Add expiry day P&L line
fig.add_trace(go.Scatter(x=strike_prices, y=pnl_expiry, mode='lines', name='Expiry Day P&L', line=dict(color='blue')))

# Add current day P&L line
fig.add_trace(go.Scatter(x=strike_prices, y=pnl_current, mode='lines', name=f'P&L with {expiry_days} days to expiry', line=dict(color='orange')))

# Update layout
fig.update_layout(
    title="Option Strategy Payoff",
    xaxis_title="Strike Price",
    yaxis_title="Profit / Loss",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=0, r=0, t=50, b=100),
    hovermode="x unified"
)

# Display the figure with full width
st.plotly_chart(fig, use_container_width=True)

# Optional: display current settings
st.write(f"Current Price: {target_price}")
st.write(f"Days to Expiry: {expiry_days}")
