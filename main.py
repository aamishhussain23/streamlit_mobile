import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Custom CSS for mobile responsiveness
st.markdown(
    """
    <style>
    @media (max-width: 768px) {
        .block-container {
            padding: 0rem 0.5rem;
        }
        .stSlider, .stDateInput {
            width: 100% !important;
        }
        .stPlotlyChart {
            width: 100% !important;
            height: auto !important;
        }
        .stMarkdown {
            font-size: 14px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sample data
strike_prices = np.arange(22000, 25000, 100)
profit_loss = np.random.randint(-1500, 1000, len(strike_prices))
open_interest_call = [0]*len(strike_prices)
open_interest_put = [0]*len(strike_prices)

# Set specific values for the strike price of 23300
index_23300 = np.where(strike_prices == 23300)[0][0]
open_interest_call[index_23300] = 1140000  # 11.4L
open_interest_put[index_23300] = 6043000   # 60.43L

expiry_profit_loss = np.random.randint(-1500, 1000, len(strike_prices))  # Sample data for expiry day P&L

# Create a DataFrame
df = pd.DataFrame({
    'strike_price': strike_prices,
    'profit_loss': profit_loss,
    'expiry_profit_loss': expiry_profit_loss,
    'open_interest_call': open_interest_call,
    'open_interest_put': open_interest_put
})

# Streamlit app
st.title('Option Profit/Loss Visualization')

# User inputs
target_price = st.slider('NIFTY Target', min_value=22000, max_value=25000, value=23722)
expiry_date = st.date_input('Expiry date', pd.to_datetime('2024-06-26'))

# Find the closest strike price
closest_strike_price = df.iloc[(df['strike_price'] - target_price).abs().argsort()[:1]]['strike_price'].values[0]
projected_loss = df.loc[df['strike_price'] == closest_strike_price, 'profit_loss'].values[0]
expiry_projected_loss = df.loc[df['strike_price'] == closest_strike_price, 'expiry_profit_loss'].values[0]

# Creating the plot
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add current profit/loss trace (blue line)
fig.add_trace(
    go.Scatter(x=df['strike_price'], y=df['profit_loss'], name="Current P&L", mode='lines+markers', line=dict(color='blue')),
    secondary_y=False,
)

# Add expiry profit/loss trace (orange line)
fig.add_trace(
    go.Scatter(x=df['strike_price'], y=df['expiry_profit_loss'], name="Expiry Day P&L", mode='lines+markers', line=dict(color='orange')),
    secondary_y=False,
)

# Add open interest traces
fig.add_trace(
    go.Bar(x=df['strike_price'], y=df['open_interest_call'], name="Call OI", marker_color='red', opacity=0.6),
    secondary_y=True,
)
fig.add_trace(
    go.Bar(x=df['strike_price'], y=df['open_interest_put'], name="Put OI", marker_color='green', opacity=0.6),
    secondary_y=True,
)

# Customize axes
fig.update_xaxes(title_text="Strike Price")
fig.update_yaxes(title_text="Profit/Loss", secondary_y=False)
fig.update_yaxes(title_text="Open Interest", secondary_y=True)

# Add a vertical line for the target price
fig.add_shape(
    go.layout.Shape(
        type="line",
        x0=closest_strike_price, x1=closest_strike_price,
        y0=min(df['profit_loss']), y1=max(df['profit_loss']),
        line=dict(color="RoyalBlue", width=2)
    )
)

# Add text annotations for the projected loss
fig.add_annotation(
    go.layout.Annotation(
        x=closest_strike_price,
        y=projected_loss,
        text=f"Projected loss: {projected_loss}",
        showarrow=True,
        arrowhead=1,
        font=dict(size=12),
        arrowcolor='blue'
    )
)

fig.add_annotation(
    go.layout.Annotation(
        x=closest_strike_price,
        y=expiry_projected_loss,
        text=f"Expiry P&L: {expiry_projected_loss}",
        showarrow=True,
        arrowhead=1,
        font=dict(size=12),
        arrowcolor='orange'
    )
)

# Update layout to improve readability on mobile devices
fig.update_layout(
    margin=dict(l=10, r=10, t=30, b=10),
    height=450,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    # title={
    #     'text': "Option Profit/Loss Visualization",
    #     'y':0.95,
    #     'x':0.5,
    #     'xanchor': 'center',
    #     'yanchor': 'top'
    # }
)

# Show plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Display additional information
st.markdown(f"**Current Price:** {target_price}")
st.markdown(f"**Expected P&L on {expiry_date}:** {projected_loss}")
st.markdown(f"**Projected P&L on Expiry Day:** {expiry_projected_loss}")
