from flask import Flask
import dash
from dash import dcc, html
import requests
import pandas as pd
import plotly.express as px
# create flask server
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=server)

# Fetch data from Flask API
summary_data = requests.get("http://127.0.0.1:5000/summary").json()
fraud_trends = pd.DataFrame(requests.get("http://127.0.0.1:5000/fraud_trends").json())
fraud_by_device = pd.DataFrame(requests.get("http://127.0.0.1:5000/fraud_by_device").json())

# Create figures
fig_trends = px.line(fraud_trends, x="signup_week", y="class", title="Fraud Cases Over Time")
fig_device = px.bar(fraud_by_device, x="device_id", y="class", title="Fraud Cases by Device")

# Layout
app.layout = html.Div(children=[
    html.H1("Fraud Detection Dashboard", style={"text-align": "center"}),

    html.Div([
        html.Div(f"Total Transactions: {summary_data['total_transactions']}", style={"fontSize": 20}),
        html.Div(f"Fraud Cases: {summary_data['fraud_cases']}", style={"fontSize": 20}),
        html.Div(f"Fraud Percentage: {summary_data['fraud_percentage']}%", style={"fontSize": 20}),
    ], style={"display": "flex", "justify-content": "space-around"}),

    dcc.Graph(figure=fig_trends),
    dcc.Graph(figure=fig_device)
])

if __name__ == "__main__":
    app.run_server(debug=True)
