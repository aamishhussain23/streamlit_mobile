from fastapi import FastAPI
from fastapi.responses import JSONResponse
import plotly.graph_objects as go
import numpy as np

app = FastAPI()

# Function to calculate profit/loss
def calculate_pnl(strike_prices, target_price, expiry_days):
    pnl_expiry = np.maximum(strike_prices - target_price, 0) - np.maximum(target_price - strike_prices, 0)
    pnl_current = pnl_expiry * (expiry_days / 30)
    return pnl_expiry, pnl_current

@app.get("/get_graph_data/")
def get_graph_data(initial_target_price: int, expiry_days: int):
    strike_prices = np.arange(20000, 25001, 100)
    pnl_expiry, pnl_current = calculate_pnl(strike_prices, initial_target_price, expiry_days)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strike_prices, y=pnl_expiry, mode='lines', name='Expiry Day P&L', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=strike_prices, y=pnl_current, mode='lines', name=f'P&L with {expiry_days} days to expiry', line=dict(color='orange')))
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
    
    return JSONResponse(content=fig.to_json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
